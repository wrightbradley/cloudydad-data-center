#!/usr/bin/env python3
"""
GitHub Stars Archiver for Gitea - Optimized Version
Creates pull mirrors in Gitea for GitHub starred repos
Creates date-based archive branches when changes are detected
"""

import asyncio
import json
import os
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Optional

import aiohttp
import requests

# Configuration
GITEA_URL = os.environ.get(
    "GITEA_URL", "http://gitea-http.gitea.svc.cluster.local:3000"
)
GITEA_TOKEN = os.environ.get("GITEA_TOKEN", "")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
ORGANIZATION = os.environ.get("GITEA_ORG", "GitHub")
DRY_RUN = os.environ.get("DRY_RUN", "false").lower() == "true"
MAX_CONCURRENT = int(os.environ.get("MAX_CONCURRENT", "20"))
BATCH_SIZE = int(os.environ.get("BATCH_SIZE", "100"))
MAX_REPO_PROCESSING_TIME = int(
    os.environ.get("MAX_REPO_PROCESSING_TIME", "600")
)  # 10 minutes

# API endpoints
GITEA_API = f"{GITEA_URL}/api/v1"
GITHUB_API = "https://api.github.com"

# Persistence configuration
DATA_DIR = "/data"
PROGRESS_FILE = os.path.join(DATA_DIR, "progress.json")


def retry_git_operation(operation, operation_name, max_attempts=3, initial_delay=1.0):
    """Retry git operations with exponential backoff."""
    last_exception = None
    for attempt in range(max_attempts):
        try:
            return operation()
        except Exception as e:
            last_exception = e
            if attempt < max_attempts - 1:
                sleep_time = initial_delay * (2**attempt)
                log_warning(
                    f"{operation_name} failed (attempt {attempt + 1}/{max_attempts}), "
                    f"retrying in {sleep_time:.1f}s",
                    error=str(e),
                )
                time.sleep(sleep_time)
    # If we get here, all attempts failed
    assert last_exception is not None, (
        "last_exception should be set after all attempts failed"
    )
    raise last_exception


def categorize_error(error_message: str) -> str:
    """Categorize git error for stats tracking."""
    if "shallow update not allowed" in error_message:
        return "shallow"
    elif "Could not read from remote repository" in error_message:
        return "clone"
    elif "Connection timed out" in error_message or "timeout" in error_message.lower():
        return "timeout"
    elif "Repository not found" in error_message:
        return "clone"
    else:
        return "other"


def log_json(level, message, **extra):
    """Output structured JSON log entry"""
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "message": message,
    }
    entry.update(extra)
    print(json.dumps(entry), flush=True)


def log_info(message, **extra):
    """Log info level message"""
    log_json("INFO", message, **extra)


def log_error(message, **extra):
    """Log error level message"""
    log_json("ERROR", message, **extra)


def log_warning(message, **extra):
    """Log warning level message"""
    log_json("WARNING", message, **extra)


def log_success(message, **extra):
    """Log success level message"""
    log_json("SUCCESS", message, **extra)


def get_run_id():
    """Generate a unique run ID based on today's date"""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def load_progress():
    """Load progress from persistence file"""
    try:
        if os.path.exists(PROGRESS_FILE):
            with open(PROGRESS_FILE, "r") as f:
                data = json.load(f)
                # Only return progress if it's from today
                if data.get("run_id") == get_run_id():
                    return data
                else:
                    log_info(
                        "Previous progress is from different day, starting fresh",
                        previous_run=data.get("run_id"),
                        current_run=get_run_id(),
                    )
    except Exception as e:
        log_warning("Could not load progress file", error=str(e))
    return {"run_id": get_run_id(), "completed": [], "failed": [], "in_progress": None}


def save_progress(progress):
    """Save progress to persistence file"""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(PROGRESS_FILE, "w") as f:
            json.dump(progress, f, indent=2)
    except Exception as e:
        log_warning("Could not save progress file", error=str(e))


def is_repo_completed(owner, repo, progress):
    """Check if a repo has already been processed in this run"""
    repo_key = f"{owner}/{repo}"
    return repo_key in progress.get("completed", [])


def mark_repo_completed(owner, repo, progress):
    """Mark a repo as completed"""
    repo_key = f"{owner}/{repo}"
    if repo_key not in progress["completed"]:
        progress["completed"].append(repo_key)
        save_progress(progress)


def mark_repo_failed(owner, repo, progress):
    """Mark a repo as failed"""
    repo_key = f"{owner}/{repo}"
    if repo_key not in progress["failed"]:
        progress["failed"].append(repo_key)
        save_progress(progress)


def set_in_progress(owner, repo, progress):
    """Set current repo as in-progress"""
    progress["in_progress"] = f"{owner}/{repo}"
    save_progress(progress)


def load_repo_list():
    """Load repos from GitHub API starred list"""
    if not GITHUB_TOKEN:
        log_error("GITHUB_TOKEN environment variable is required")
        sys.exit(1)

    repos = fetch_github_starred_repos()
    if not repos:
        log_error("Failed to fetch starred repos from GitHub API")
        sys.exit(1)

    log_info(f"Fetched {len(repos)} starred repos from GitHub API", count=len(repos))
    return repos


def fetch_github_starred_repos():
    """Fetch all starred repos from GitHub API"""
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

    repos = []
    page = 1
    per_page = 100

    while True:
        url = f"{GITHUB_API}/user/starred?page={page}&per_page={per_page}"

        try:
            resp = requests.get(url, headers=headers, timeout=30)

            if resp.status_code != 200:
                log_error(
                    f"GitHub API returned {resp.status_code}", status=resp.status_code
                )
                return None

            page_repos = resp.json()
            if not page_repos:
                break

            for repo in page_repos:
                repos.append(repo["full_name"])

            log_info(
                f"Fetched page {page}: {len(page_repos)} repos",
                page=page,
                count=len(page_repos),
                total=len(repos),
            )

            # Check if we've reached the end
            if len(page_repos) < per_page:
                break

            page += 1

        except Exception as e:
            log_error("Failed to fetch starred repos", error=str(e))
            return None

    return repos


async def get_github_repo_info_async(
    session: aiohttp.ClientSession, owner: str, repo: str
):
    """Get current GitHub repo HEAD commit SHA (async version)"""
    if not GITHUB_TOKEN:
        return None, "No GitHub token"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    url = f"{GITHUB_API}/repos/{owner}/{repo}"

    try:
        async with session.get(
            url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)
        ) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("default_branch"), None
            elif resp.status == 404:
                return None, "Repo not found (may be private or deleted)"
            else:
                return None, f"GitHub API error: {resp.status}"
    except Exception as e:
        return None, f"Request failed: {e}"


async def get_github_branch_sha_async(
    session: aiohttp.ClientSession, owner: str, repo: str, branch: str
):
    """Get SHA of a specific branch on GitHub (async version)"""
    if not GITHUB_TOKEN:
        return None

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    url = f"{GITHUB_API}/repos/{owner}/{repo}/commits/{branch}"

    try:
        async with session.get(
            url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)
        ) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("sha")
    except Exception:
        pass
    return None


async def get_gitea_mirror_async(session: aiohttp.ClientSession, owner: str, repo: str):
    """Get Gitea mirror repo info (async version)"""
    mirror_name = f"{owner}-{repo}"
    headers = {"Authorization": f"token {GITEA_TOKEN}"}
    url = f"{GITEA_API}/repos/{ORGANIZATION}/{mirror_name}"

    try:
        async with session.get(
            url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)
        ) as resp:
            if resp.status == 200:
                return await resp.json()
    except Exception:
        pass
    return None


async def get_archive_repo_async(session: aiohttp.ClientSession, owner: str, repo: str):
    """Get archive repo info (async version)"""
    archive_name = f"{owner}-{repo}-archive"
    headers = {"Authorization": f"token {GITEA_TOKEN}"}
    url = f"{GITEA_API}/repos/{ORGANIZATION}/{archive_name}"

    try:
        async with session.get(
            url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)
        ) as resp:
            if resp.status == 200:
                return await resp.json()
    except Exception:
        pass
    return None


async def create_archive_repo_async(
    session: aiohttp.ClientSession, owner: str, repo: str
):
    """Create a regular (non-mirror) repo for storing archive branches (async version)"""
    headers = {"Authorization": f"token {GITEA_TOKEN}"}
    archive_name = f"{owner}-{repo}-archive"

    # Check if already exists
    check_url = f"{GITEA_API}/repos/{ORGANIZATION}/{archive_name}"
    async with session.get(
        check_url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)
    ) as resp:
        if resp.status == 200:
            return True

    log_info(
        f"Creating archive repo: {ORGANIZATION}/{archive_name}",
        organization=ORGANIZATION,
        repository=archive_name,
    )
    create_url = f"{GITEA_API}/orgs/{ORGANIZATION}/repos"
    payload = {
        "name": archive_name,
        "description": f"Archive branches for {owner}/{repo} (mirror companion)",
        "private": False,
        "auto_init": False,
    }

    async with session.post(
        create_url,
        headers=headers,
        json=payload,
        timeout=aiohttp.ClientTimeout(total=300),
    ) as resp:
        if resp.status in [200, 201]:
            log_success(
                f"Created archive repo: {ORGANIZATION}/{archive_name}",
                organization=ORGANIZATION,
                repository=archive_name,
            )
            return True
        else:
            log_error(
                "Failed to create archive repo",
                organization=ORGANIZATION,
                repository=archive_name,
                status=resp.status,
            )
            return False


async def get_or_create_org_async(session: aiohttp.ClientSession):
    """Ensure the organization exists, create if not (async version)"""
    headers = {"Authorization": f"token {GITEA_TOKEN}"}

    org_url = f"{GITEA_API}/orgs/{ORGANIZATION}"
    async with session.get(
        org_url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)
    ) as resp:
        if resp.status == 200:
            log_info(f"Organization '{ORGANIZATION}' exists", organization=ORGANIZATION)
            return True

    log_info(f"Creating organization '{ORGANIZATION}'...", organization=ORGANIZATION)
    create_url = f"{GITEA_API}/orgs"
    payload = {
        "username": ORGANIZATION,
        "visibility": "public",
        "repo_admin_change_team_access": True,
    }

    async with session.post(
        create_url,
        headers=headers,
        json=payload,
        timeout=aiohttp.ClientTimeout(total=30),
    ) as resp:
        if resp.status in [200, 201]:
            log_success(
                f"Created organization '{ORGANIZATION}'", organization=ORGANIZATION
            )
            return True
        else:
            log_error(
                "Failed to create organization",
                organization=ORGANIZATION,
                status=resp.status,
            )
            return False


async def create_pull_mirror_async(
    session: aiohttp.ClientSession, owner: str, repo: str
):
    """Create a pull mirror repository in Gitea (async version)"""
    headers = {"Authorization": f"token {GITEA_TOKEN}"}
    mirror_name = f"{owner}-{repo}"

    # Check if already exists
    check_url = f"{GITEA_API}/repos/{ORGANIZATION}/{mirror_name}"
    async with session.get(
        check_url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)
    ) as resp:
        if resp.status == 200:
            return True

    log_info(
        f"Creating mirror: {ORGANIZATION}/{mirror_name}",
        organization=ORGANIZATION,
        repository=mirror_name,
    )
    create_url = f"{GITEA_API}/repos/migrate"
    payload = {
        "repo_name": mirror_name,
        "repo_owner": ORGANIZATION,
        "clone_addr": f"https://github.com/{owner}/{repo}.git",
        "mirror": True,
        "wiki": True,
        "private": False,
        "pull_requests": True,
        "releases": True,
        "topics": True,
        "migrations_only": False,
    }

    async with session.post(
        create_url,
        headers=headers,
        json=payload,
        timeout=aiohttp.ClientTimeout(total=300),
    ) as resp:
        if resp.status in [200, 201]:
            log_success(
                f"Created mirror: {ORGANIZATION}/{mirror_name}",
                organization=ORGANIZATION,
                repository=mirror_name,
            )
            return True
        else:
            log_error(
                "Failed to create mirror",
                organization=ORGANIZATION,
                repository=mirror_name,
                status=resp.status,
            )
            return False


async def get_archive_branches_async(
    session: aiohttp.ClientSession, owner: str, repo: str
):
    """Get list of existing archive branches from archive repo (async version)"""
    headers = {"Authorization": f"token {GITEA_TOKEN}"}
    archive_name = f"{owner}-{repo}-archive"
    url = f"{GITEA_API}/repos/{ORGANIZATION}/{archive_name}/branches"

    try:
        async with session.get(
            url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)
        ) as resp:
            if resp.status == 200:
                branches = await resp.json()
                archive_branches = [
                    b["name"] for b in branches if b["name"].startswith("archive-")
                ]
                return sorted(archive_branches), None
            elif resp.status == 404:
                return [], None
    except Exception as e:
        return [], str(e)
    return [], None


def create_archive_branch(
    owner: str, repo: str, branch_name: str, sha: Optional[str]
) -> bool:
    """Create an archive branch by pushing from mirror to archive repo via git (synchronous - git ops are CPU/IO bound)"""
    start_time = time.time()
    log_info(
        "Starting archive branch creation",
        owner=owner,
        repo=repo,
        branch=branch_name,
        sha=sha[:8] if sha else None,
    )

    if DRY_RUN:
        log_info(
            "[DRY RUN] Would create archive branch",
            branch=branch_name,
            sha=sha[:8] if sha else None,
        )
        return True

    mirror_name = f"{owner}-{repo}"
    archive_name = f"{owner}-{repo}-archive"

    # URLs for git operations
    mirror_url = f"{GITEA_URL}/{ORGANIZATION}/{mirror_name}.git"
    archive_url = f"{GITEA_URL}/{ORGANIZATION}/{archive_name}.git"

    # Use token in URL for authentication
    auth_mirror_url = mirror_url.replace("://", f"://token:{GITEA_TOKEN}@")
    auth_archive_url = archive_url.replace("://", f"://token:{GITEA_TOKEN}@")

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            # Clone with --depth 1 for shallow clone (much faster) with retries
            clone_start = time.time()

            def clone_op():
                return subprocess.run(
                    ["git", "clone", "--depth", "1", auth_mirror_url, tmpdir],
                    capture_output=True,
                    text=True,
                    timeout=300,
                )

            clone_result = retry_git_operation(
                clone_op, "Clone mirror", max_attempts=3, initial_delay=1.0
            )
            clone_duration = time.time() - clone_start

            if clone_result.returncode != 0:
                log_error(
                    "Failed to clone mirror",
                    owner=owner,
                    repo=repo,
                    error=clone_result.stderr,
                    duration_seconds=clone_duration,
                )
                return False
            log_info(
                "Clone completed",
                duration_seconds=clone_duration,
                returncode=clone_result.returncode,
            )

            # Add archive repo as remote with retries
            remote_start = time.time()

            def add_remote_op():
                return subprocess.run(
                    ["git", "-C", tmpdir, "remote", "add", "archive", auth_archive_url],
                    capture_output=True,
                    text=True,
                )

            remote_result = retry_git_operation(
                add_remote_op, "Add remote", max_attempts=2, initial_delay=1.0
            )
            remote_duration = time.time() - remote_start

            if remote_result.returncode != 0:
                log_error(
                    "Failed to add archive remote",
                    owner=owner,
                    repo=repo,
                    error=remote_result.stderr,
                    duration_seconds=remote_duration,
                )
                return False
            log_info(
                "Add remote completed",
                duration_seconds=remote_duration,
                returncode=remote_result.returncode,
            )

            # Check per-repo timeout
            elapsed = time.time() - start_time
            if elapsed > MAX_REPO_PROCESSING_TIME:
                log_error(
                    "Repo processing timeout before push",
                    owner=owner,
                    repo=repo,
                    elapsed_seconds=elapsed,
                    max_seconds=MAX_REPO_PROCESSING_TIME,
                )
                return False

            # Push to archive repo with the archive branch name with retries and --force
            push_start = time.time()

            def push_op():
                return subprocess.run(
                    [
                        "git",
                        "-C",
                        tmpdir,
                        "push",
                        "--force",
                        "archive",
                        f"HEAD:refs/heads/{branch_name}",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=60,
                )

            push_result = retry_git_operation(
                push_op, "Push archive branch", max_attempts=3, initial_delay=2.0
            )
            push_duration = time.time() - push_start

            if push_result.returncode == 0:
                total_duration = time.time() - start_time
                log_success(
                    "Created archive branch",
                    branch=branch_name,
                    sha=sha[:8] if sha else None,
                    archive=archive_name,
                    duration_seconds=total_duration,
                )
                return True
            else:
                log_error(
                    "Failed to push archive branch",
                    branch=branch_name,
                    error=push_result.stderr,
                    duration_seconds=push_duration,
                )
                return False

    except subprocess.TimeoutExpired:
        log_error(
            "Timeout creating archive branch",
            branch=branch_name,
            owner=owner,
            repo=repo,
            elapsed_seconds=time.time() - start_time,
        )
        return False
    except Exception as e:
        log_error(
            "Error creating archive branch",
            branch=branch_name,
            owner=owner,
            repo=repo,
            error=str(e),
            elapsed_seconds=time.time() - start_time,
        )
        return False


async def sync_mirror_async(session: aiohttp.ClientSession, owner: str, repo: str):
    """Trigger sync for a mirror repository (async version)"""
    headers = {"Authorization": f"token {GITEA_TOKEN}"}
    mirror_name = f"{owner}-{repo}"
    url = f"{GITEA_API}/repos/{ORGANIZATION}/{mirror_name}/mirror-sync"

    try:
        async with session.post(
            url, headers=headers, timeout=aiohttp.ClientTimeout(total=60)
        ) as resp:
            if resp.status in [200, 202]:
                log_info("Triggered mirror sync", repository=mirror_name)
                return True
    except Exception:
        pass
    return False


async def process_repo_async(
    session: aiohttp.ClientSession,
    owner: str,
    repo: str,
    progress: dict,
    executor: ThreadPoolExecutor,
) -> tuple[bool, str]:
    """Process a single repo - ensure mirror exists and create archive if needed (async version)"""
    today = datetime.now().strftime("%Y-%m-%d")
    archive_branch = f"archive-{today}"

    log_info("Processing repository", owner=owner, repo=repo)

    # Step 1: Ensure mirror exists
    gitea_mirror = await get_gitea_mirror_async(session, owner, repo)
    if not gitea_mirror:
        if not await create_pull_mirror_async(session, owner, repo):
            return False, "Failed to create mirror"
        # Quick wait for mirror to be available
        await asyncio.sleep(0.5)
        gitea_mirror = await get_gitea_mirror_async(session, owner, repo)
        if not gitea_mirror:
            return False, "Mirror creation failed"

    # Step 2: Ensure archive repo exists
    archive_repo = await get_archive_repo_async(session, owner, repo)
    if not archive_repo:
        if not await create_archive_repo_async(session, owner, repo):
            return False, "Failed to create archive repo"
        await asyncio.sleep(0.5)

    # Step 3: Get GitHub current state
    default_branch, error = await get_github_repo_info_async(session, owner, repo)
    if error or not default_branch:
        log_warning(error or "No default branch found", owner=owner, repo=repo)
        return True, error or "No default branch"

    github_sha = await get_github_branch_sha_async(session, owner, repo, default_branch)
    if not github_sha:
        log_warning("Could not get GitHub branch SHA", owner=owner, repo=repo)
        return True, "Could not read GitHub SHA"

    # Step 4: Check existing archive branches
    archive_branches, error = await get_archive_branches_async(session, owner, repo)
    if error:
        log_warning(
            "Error reading archive branches", owner=owner, repo=repo, error=error
        )

    # Step 5: Decide if we need to create archive
    if not archive_branches:
        # No archives yet - create initial archive
        log_info(
            "No archive branches found, creating initial archive",
            owner=owner,
            repo=repo,
        )
        await sync_mirror_async(session, owner, repo)
        # Use thread executor for git operations
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            executor, create_archive_branch, owner, repo, archive_branch, github_sha
        )
        if result:
            return True, f"Created initial archive {archive_branch}"
        else:
            return False, "Failed to create initial archive"

    # Check if we already have an archive for today
    if archive_branch in archive_branches:
        log_info(
            "Archive for today already exists",
            owner=owner,
            repo=repo,
            branch=archive_branch,
        )
        return True, "Archive already exists"

    # Check latest archive vs current state
    latest_archive = archive_branches[-1]
    log_info("Checking latest archive", owner=owner, repo=repo, branch=latest_archive)

    # Get SHA of latest archive branch from archive repo
    archive_name = f"{owner}-{repo}-archive"
    headers = {"Authorization": f"token {GITEA_TOKEN}"}
    branch_url = (
        f"{GITEA_API}/repos/{ORGANIZATION}/{archive_name}/branches/{latest_archive}"
    )
    try:
        async with session.get(
            branch_url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)
        ) as resp:
            if resp.status == 200:
                data = await resp.json()
                archive_sha = data.get("commit", {}).get("sha")
                if archive_sha == github_sha:
                    log_info(
                        "No changes since last archive",
                        owner=owner,
                        repo=repo,
                        branch=latest_archive,
                    )
                    return True, "No changes detected"
                else:
                    log_info(
                        "Changes detected",
                        owner=owner,
                        repo=repo,
                        previous_sha=archive_sha[:8] if archive_sha else None,
                        current_sha=github_sha[:8] if github_sha else None,
                    )
    except Exception:
        log_warning(
            "Could not compare with latest archive, assuming changes",
            owner=owner,
            repo=repo,
        )

    # Create new archive
    await sync_mirror_async(session, owner, repo)
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        executor, create_archive_branch, owner, repo, archive_branch, github_sha
    )
    if result:
        return True, f"Created archive {archive_branch}"
    else:
        return False, "Failed to create archive"


async def process_batch(
    session: aiohttp.ClientSession,
    repos: list[str],
    progress: dict,
    executor: ThreadPoolExecutor,
    stats: dict,
):
    """Process a batch of repos concurrently"""
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)

    async def process_with_limit(repo_full_name: str):
        async with semaphore:
            try:
                owner, repo = repo_full_name.split("/", 1)

                # Skip if already completed
                if is_repo_completed(owner, repo, progress):
                    log_info(
                        "Skipping already processed repository",
                        owner=owner,
                        repo=repo,
                    )
                    stats["skipped"] += 1
                    return

                # Mark as in-progress
                set_in_progress(owner, repo, progress)

                success, message = await process_repo_async(
                    session, owner, repo, progress, executor
                )

                if success:
                    stats["processed"] += 1
                    mark_repo_completed(owner, repo, progress)
                    if (
                        "Created initial archive" in message
                        or "Created archive" in message
                    ):
                        stats["archived"] += 1
                    elif "Mirror" in message:
                        stats["created"] += 1
                    else:
                        stats["skipped"] += 1
                else:
                    stats["failed"] += 1
                    mark_repo_failed(owner, repo, progress)
                    # Categorize error
                    error_type = categorize_error(message)
                    if error_type == "shallow":
                        stats["shallow_failures"] += 1
                    elif error_type == "clone":
                        stats["clone_failures"] += 1
                    elif error_type == "timeout":
                        stats["timeout_failures"] += 1
                    else:
                        stats["other_failures"] += 1
                    log_error(
                        "Failed to process repository",
                        owner=owner,
                        repo=repo,
                        error=message,
                        error_type=error_type,
                    )

            except ValueError:
                log_error("Invalid repo format", repo=repo_full_name)
                stats["failed"] += 1
            except Exception as e:
                log_error(
                    "Error processing repository", repo=repo_full_name, error=str(e)
                )
                stats["failed"] += 1

    # Process all repos in batch concurrently
    await asyncio.gather(*[process_with_limit(repo) for repo in repos])


async def main_async():
    job_start_time = time.time()
    log_info(
        "Starting GitHub Stars Archiver (Optimized)",
        gitea_url=GITEA_URL,
        organization=ORGANIZATION,
        dry_run=DRY_RUN,
        max_concurrent=MAX_CONCURRENT,
        batch_size=BATCH_SIZE,
    )

    if not GITEA_TOKEN:
        log_error("GITEA_TOKEN environment variable is required")
        sys.exit(1)

    if not GITHUB_TOKEN:
        log_error("GITHUB_TOKEN environment variable is required")
        sys.exit(1)

    # Load repo list from GitHub API
    repos = load_repo_list()
    if not repos:
        log_error("No repos to process")
        sys.exit(1)

    log_info("Loaded repositories to process", count=len(repos))

    # Load progress from persistence
    progress = load_progress()
    already_completed = len(progress.get("completed", []))
    if already_completed > 0:
        log_info(
            f"Resuming from previous run: {already_completed} repos already processed",
            completed=already_completed,
            remaining=len(repos) - already_completed,
        )

    # Create aiohttp session with connection pooling
    timeout = aiohttp.ClientTimeout(total=300, connect=30)
    connector = aiohttp.TCPConnector(
        limit=MAX_CONCURRENT * 2,
        limit_per_host=MAX_CONCURRENT,
        enable_cleanup_closed=True,
        force_close=False,
    )

    # Create thread pool for git operations
    executor = ThreadPoolExecutor(max_workers=min(MAX_CONCURRENT, 10))

    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
        # Ensure organization exists
        if not await get_or_create_org_async(session):
            log_error("Failed to ensure organization exists")
            sys.exit(1)

        # Stats tracking
        stats = {
            "processed": 0,
            "created": 0,
            "archived": 0,
            "skipped": 0,
            "failed": 0,
            "shallow_failures": 0,
            "clone_failures": 0,
            "timeout_failures": 0,
            "other_failures": 0,
            "clone_retries": 0,
            "push_retries": 0,
            "successful_retries": 0,
        }

        # Process repos in batches
        total_repos = len(repos)
        for i in range(0, total_repos, BATCH_SIZE):
            batch = repos[i : i + BATCH_SIZE]
            batch_num = i // BATCH_SIZE + 1
            total_batches = (total_repos + BATCH_SIZE - 1) // BATCH_SIZE

            log_info(
                f"Processing batch {batch_num}/{total_batches}",
                batch_size=len(batch),
                remaining=total_repos - min(i + BATCH_SIZE, total_repos),
            )

            await process_batch(session, batch, progress, executor, stats)

    # Shutdown executor
    executor.shutdown(wait=True)

    # Calculate success rate
    total_processed = stats["processed"] + stats["skipped"]
    success_rate = stats["archived"] / max(1, total_processed) * 100
    duration = time.time() - job_start_time
    repos_per_minute = stats["processed"] / max(1, duration / 60)

    log_info(
        "Job complete",
        summary={
            "processed": stats["processed"],
            "mirrors_created": stats["created"],
            "archives_created": stats["archived"],
            "skipped": stats["skipped"],
            "failed": stats["failed"],
            "total_completed": len(progress.get("completed", [])),
            "success_rate_percent": round(success_rate, 2),
            "duration_seconds": round(duration, 1),
            "repos_per_minute": round(repos_per_minute, 2),
            "failure_breakdown": {
                "shallow_push": stats.get("shallow_failures", 0),
                "clone_failures": stats.get("clone_failures", 0),
                "timeout_failures": stats.get("timeout_failures", 0),
                "other_failures": stats.get("other_failures", 0),
            },
            "retry_stats": {
                "clone_retries": stats.get("clone_retries", 0),
                "push_retries": stats.get("push_retries", 0),
                "successful_retries": stats.get("successful_retries", 0),
            },
        },
    )

    if stats["failed"] > 0:
        sys.exit(1)


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
