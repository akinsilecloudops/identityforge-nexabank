output "vpc_id" {
  description = "ID of the VPC."
  value       = aws_vpc.nexabank.id
}

output "public_subnet_ids" {
  description = "IDs of the public subnets (AZ-1, AZ-2)."
  value       = [aws_subnet.public_primary.id, aws_subnet.public_secondary.id]
}

output "private_subnet_ids" {
  description = "IDs of the private subnets (AZ-1, AZ-2)."
  value       = [aws_subnet.private_primary.id, aws_subnet.private_secondary.id]
}

output "ec2_instance_id" {
  description = "ID of the EC2 instance."
  value       = module.compute.instance_id
}

output "ec2_private_ip" {
  description = "Private IP address of the EC2 instance."
  value       = module.compute.private_ip
}
