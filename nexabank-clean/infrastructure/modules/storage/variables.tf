variable "name" {
  description = "Base name prefix for storage resources (pass the root local.name, e.g. nexabank-prod)."
  type        = string
}

variable "common_tags" {
  description = "Common tags applied to all storage resources (pass the root local.common_tags)."
  type        = map(string)
  default     = {}
}

variable "s3_bucket_name" {
  description = "Explicit bucket name. Leave empty to auto-generate as <name>-backup-logs-<random hex>."
  type        = string
  default     = ""
}

variable "s3_kms_key_arn" {
  description = "ARN of the KMS key used for S3 server-side encryption. Wire this from the kms module at the root."
  type        = string
}
