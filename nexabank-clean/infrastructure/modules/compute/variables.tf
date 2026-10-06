variable "name" {
  description = "Base name for resources (pass local.name from the root)."
  type        = string
}

variable "tags" {
  description = "Common tags (pass local.common_tags from the root)."
  type        = map(string)
  default     = {}
}

variable "subnet_id" {
  description = "Subnet to launch the instance in (e.g. the AZ-1 private subnet)."
  type        = string
}

variable "security_group_ids" {
  description = "Security group IDs to attach. Root wires in module.security outputs (e.g. the keycloak SG)."
  type        = list(string)
}

variable "backup_bucket_arn" {
  description = "ARN of the S3 backup/logs bucket the instance may read/write."
  type        = string
}

variable "ebs_kms_key_arn" {
  description = "KMS key ARN used to encrypt the root EBS volume. Empty uses the AWS-managed aws/ebs key."
  type        = string
  default     = ""
}

variable "s3_kms_key_arn" {
  description = "KMS key ARN protecting the backup/logs bucket, so the instance role can decrypt/generate data keys when reading/writing objects."
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type."
  type        = string
  default     = "t3.micro"
}

variable "ami_id" {
  description = "AMI ID. Leave empty to use the latest Amazon Linux 2023 AMI."
  type        = string
  default     = ""
}

variable "key_name" {
  description = "Existing EC2 key pair name. Leave empty for keyless SSM access."
  type        = string
  default     = ""
}
