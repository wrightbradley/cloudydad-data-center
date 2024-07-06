terraform {
  required_version = ">= 1.5.7"

  required_providers {
    flux = {
      source  = "fluxcd/flux"
      version = ">= 1.2"
    }
    github = {
      source  = "integrations/github"
      version = ">= 6.1"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.31.0"
    }
  }
}

resource "flux_bootstrap_git" "this" {
  # embedded_manifests = true
  path                 = "clusters/${var.cluster_name}"
  delete_git_manifests = false
  network_policy       = false
}
