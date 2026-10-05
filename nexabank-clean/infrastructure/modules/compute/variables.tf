variable "instance_type" {
  description = "EC2 instance type."
  type        = string
  default     = "t3.micro"
}

variable "ami_id" {
  description = "AMI ID for the EC2 instance. 
  type        = string
  default     = ""
}

variable "ssh_cidr_blocks" {
  description = "CIDR blocks allowed to reach the EC2 instance over SSH (restrict to your bastion/admin range)."
  type        = list(string)
  default     = ["10.0.0.0/16"]
}

variable "key_name" {
  description = "Name of EC2 key pair for SSH access. 
  type        = string
  default     = ""
}
