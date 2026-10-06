output "ec2_instance_id" {
  description = "ID of the EC2 instance."
  value       = module.compute.instance_id
}

output "ec2_private_ip" {
  description = "Private IP address of the EC2 instance."
  value       = module.compute.private_ip
}

output "ec2_iam_role_name" {
  description = "IAM role name attached to the EC2 instance."
  value       = module.compute.iam_role_name
}

# --- Security groups (passthrough from the security module) -----------------
output "alb_sg_id" {
  description = "ALB security group."
  value       = module.security.alb_sg_id
}

output "bastion_sg_id" {
  description = "Bastion security group."
  value       = module.security.bastion_sg_id
}

output "gateway_sg_id" {
  description = "ECS API gateway security group."
  value       = module.security.gateway_sg_id
}

output "keycloak_sg_id" {
  description = "Keycloak security group (attached to the EC2 instance)."
  value       = module.security.keycloak_sg_id
}

output "ca_sg_id" {
  description = "CA (Smallstep/EJBCA) security group."
  value       = module.security.ca_sg_id
}

output "rds_sg_id" {
  description = "RDS security group (attach to primary and replica)."
  value       = module.security.rds_sg_id
}

# --- KMS keys (from the kms module) -----------------------------------------
output "kms_key_arns" {
  description = "Map of KMS key ARNs by purpose (rds / s3 / ebs)."
  value       = module.kms.key_arns
}
