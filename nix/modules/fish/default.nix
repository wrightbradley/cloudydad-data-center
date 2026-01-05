{ config, pkgs, lib, ... }:

{
  programs.fish = {
    enable = true;
    interactiveShellInit = ''
      set -g fish_greeting
      set -gx EDITOR nvim
      set -gx GIT_EDITOR "$EDITOR"
      set -gx VISUAL "$EDITOR"
      set -gx KUBECONFIG "$HOME/.kube/config"
      set -gx LANG en_US.UTF-8
      set -gx PATH "$HOME/.local/share/nvim/mason/bin:$PATH"
    '';

    plugins = [
      { name = "jorgebucaran/fisher"; }
      { name = "patrickf1/fzf.fish"; }
    ];

    functions = {
      whoip = {
        body = "curl ip-api.com/$argv";
      };

      urldecode = {
        body = "echo $argv | python3 -c 'from urllib.parse import unquote; print(unquote(sys.stdin.read()))'";
      };

      grsub = {
        body = ''
          if test -z "$argv"
            echo "Please provide a submodule path/name"
          else
            git submodule deinit -f -- $argv
            rm -rf .git/modules/$argv
            git rm -f $argv
          end
        '';
      };

      bak = {
        body = ''
          set LOGDATE (date +%Y%m%dT%H%M%S)
          cp -r "$argv" "$argv.bak.$LOGDATE"
        '';
      };

      fshow = {
        body = "git log --graph --color=always --format='%C(auto)%h%d %s %C(black)%C(bold)%cr' $argv | fzf --ansi --multi --no-sort --reverse | less -R";
      };

      ghpr = {
        body = "command uv run $HOME/bin/open-gh-pr.py $argv";
      };

      ghcw = {
        body = "command uv run $HOME/bin/create-worktree.py $argv";
      };

      kpnr = {
        body = "kubectl get pods -A --field-selector=status.phase!=Running | grep -v Complete";
      };

      knmem = {
        body = "kubectl get no -o json | jq -r '.items | sort_by(.status.capacity.memory)[] | [.metadata.name,.status.capacity.memory] | @tsv'";
      };

      knpc = {
        body = "kubectl get po -o json --all-namespaces | jq '.items | group_by(.spec.nodeName) | map({\"nodeName\": .[0].spec.nodeName, \"count\": length}) | sort_by(.count)'";
      };

      kptc = {
        body = "kubectl top pods -A | sort --reverse --key 3 --numeric";
      };

      kptm = {
        body = "kubectl top pods -A | sort --reverse --key 4 --numeric";
      };

      tf = {
        body = ''
          if test -f terragrunt.hcl
            terragrunt $argv
          else
            terraform $argv
          end
        '';
      };

      tffmt = {
        body = "terraform fmt -recursive && tf_vars_sort **/{outputs,variables}.tf(N) && terragrunt hclfmt";
      };

      awswhoami = {
        body = "aws sts get-caller-identity $argv && aws iam list-account-aliases $argv";
      };

      awsprof = {
        body = "set AWS_PROFILE (perl -nle '/\\[profile (.+)\\]/ < $HOME/.aws/config 2>/dev/null | fzf)";
      };
    };

    shellAliases = {
      l = "ll -a";
      lr = "ll -T";
      lx = "ll -sextension";
      ls = "eza --group-directories-first";

      ".." = "cd ..";
      "..." = "cd ../..";

      vi = "nvim";
      vim = "nvim";
      cat = "bat";
      less = "bat";

      g = "git";
      gs = "git status";
      gd = "git diff";
      ga = "git add";

      kgp = "kubectl get pods -o wide";
      kgd = "kubectl get deployment -o wide";
      kgs = "kubectl get svc -o wide";
      kdp = "kubectl describe pod";
      kdd = "kubectl describe deployment";
      kds = "kubectl describe service";

      tf = "terraform";
    };

    shellInit = ''
      if command -q fzf
        fzf --fish | source
      end

      if command -q starship
        starship init fish | source
      end
    '';
  };
}
