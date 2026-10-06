output "instance_id" {
  description = "ID of the EC2 instance."
  value       = aws_instance.app.id
}

output "private_ip" {
  description = "Private IP of the EC2 instance."
  value       = aws_instance.app.private_ip
}

output "iam_role_name" {
  description = "Name of the instance IAM role."
  value       = aws_iam_role.ec2.name
}
