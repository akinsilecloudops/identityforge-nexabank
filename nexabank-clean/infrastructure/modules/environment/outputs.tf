output "vpc_id" {
  description = "NexaBank VPC ID"
  value       = module.networking.vpc_id
}

output "vpc_cidr" {
  description = "NexaBank VPC CIDR"
  value       = module.networking.vpc_cidr
}

output "availability_zones" {
  description = "Availability Zones used by the network"
  value       = module.networking.availability_zones
}

output "public_subnet_ids" {
  description = "Public subnet IDs for the ALB"
  value       = module.networking.public_subnet_ids
}

output "private_subnet_ids" {
  description = "Private subnet IDs for application and database workloads"
  value       = module.networking.private_subnet_ids
}

output "private_subnet_id_primary" {
  description = "Primary private subnet ID"
  value       = module.networking.private_subnet_id_primary
}

output "private_subnet_id_secondary" {
  description = "Secondary private subnet ID"
  value       = module.networking.private_subnet_id_secondary
}

output "db_subnet_group_name" {
  description = "RDS DB subnet group name"
  value       = module.networking.db_subnet_group_name
}

output "nat_gateway_ids" {
  description = "NAT Gateway IDs"
  value       = module.networking.nat_gateway_ids
}

output "nat_public_ips" {
  description = "NAT Gateway public IP addresses"
  value       = module.networking.nat_public_ips
}

output "internet_gateway_id" {
  description = "Internet Gateway ID"
  value       = module.networking.internet_gateway_id
}
