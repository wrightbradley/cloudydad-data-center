variable "github_token" {
  description = "GitHub token"
  sensitive   = true
  type        = string
  default     = ""
}

variable "github_org" {
  description = "GitHub organization"
  type        = string
  default     = ""
}

variable "github_repository" {
  description = "GitHub repository"
  type        = string
  default     = ""
}

variable "kubernetes_context" {
  description = "Kube Context"
  type        = string
  default     = ""
}

variable "cluster_name" {
  description = "Kubernetes Cluster Name"
  type        = string
  default     = ""
}
