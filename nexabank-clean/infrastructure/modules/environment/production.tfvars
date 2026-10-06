project_name = "nexabank"
environment  = "prod"

vpc_cidr                   = "10.0.0.0/16"
enable_s3_gateway_endpoint = true

# Admin access to the bastion 
admin_cidr_blocks = ["203.0.113.0/28"] # We need to replace with admin Ip

# ALB
certificate_arn            = "arn:aws:acm:af-south-1:<account-id>:certificate/<id>" #replace with real cert ARN
enable_deletion_protection = true
health_check_path          = "/healthz" 

tags = {
  Owner = "identity-forge"
}
