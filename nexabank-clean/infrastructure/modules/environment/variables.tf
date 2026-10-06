# GENERAL

variable "project_name" {
  description = "Project name used as a prefix for resource names"
  type        = string
}

variable "environment" {
  description = "Deployment environment"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "tags" {
  description = "Additional tags applied to all resources"
  type        = map(string)
  default     = {}
}

# NETWORKING

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"

  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "vpc_cidr must be a valid CIDR block."
  }
}

variable "enable_s3_gateway_endpoint" {
  description = "Create an S3 gateway VPC endpoint"
  type        = bool
  default     = true
}

# SECURITY

variable "admin_cidr_blocks" {
  description = "CIDRs allowed to SSH to the bastion"
  type        = list(string)

  validation {
    condition = (
      length(var.admin_cidr_blocks) > 0 &&
      alltrue([
        for c in var.admin_cidr_blocks : can(cidrhost(c, 0))
      ])
    )
    error_message = "admin_cidr_blocks must contain at least one valid CIDR."
  }

  validation {
    condition     = !contains(var.admin_cidr_blocks, "0.0.0.0/0")
    error_message = "admin_cidr_blocks must not contain 0.0.0.0/0."
  }
}

variable "alb_ingress_cidrs" {
  description = "CIDRs allowed to reach the public ALB"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "enable_http_listener" {
  description = "Allow HTTP port 80 (redirects to HTTPS when a certificate is set)"
  type        = bool
  default     = true
}

variable "gateway_port" {
  description = "API gateway listening port (Kong 8000, APISIX 9080)"
  type        = number
  default     = 8000
}

variable "keycloak_port" {
  description = "Keycloak listening port"
  type        = number
  default     = 8443
}

variable "ca_port" {
  description = "Certificate Authority listening port (Smallstep 9000, EJBCA 8443)"
  type        = number
  default     = 9000
}

variable "db_port" {
  description = "PostgreSQL database port"
  type        = number
  default     = 5432
}

variable "ssh_port" {
  description = "SSH port"
  type        = number
  default     = 22
}

# ALB

variable "health_check_path" {
  description = "Path the ALB probes on the gateway (must return a healthy status)"
  type        = string
  default     = "/"
}

variable "health_check_matcher" {
  description = "HTTP status codes that count as healthy"
  type        = string
  default     = "200-399"
}

variable "certificate_arn" {
  description = "ACM certificate ARN in af-south-1 (null = HTTP-only, dev only)"
  type        = string
  default     = null
}

variable "ssl_policy" {
  description = "TLS policy for the HTTPS listener"
  type        = string
  default     = "ELBSecurityPolicy-TLS13-1-2-2021-06"
}

variable "enable_deletion_protection" {
  description = "Protect the ALB from accidental deletion (true for prod)"
  type        = bool
  default     = false
}

variable "idle_timeout" {
  description = "ALB idle connection timeout in seconds"
  type        = number
  default     = 60
}

variable "access_logs_bucket" {
  description = "S3 bucket for ALB access logs (null = disabled)"
  type        = string
  default     = null
}

#  KMS

variable "deletion_window_in_days" {
  description = "Waiting period before scheduled KMS key deletion"
  type        = number
  default     = 30

  validation {
    condition     = var.deletion_window_in_days >= 7 && var.deletion_window_in_days <= 30
    error_message = "deletion_window_in_days must be between 7 and 30."
  }
}
