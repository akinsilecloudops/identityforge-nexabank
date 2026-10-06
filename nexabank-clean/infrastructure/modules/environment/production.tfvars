# General

project_name = "nexabank"
environment  = "prod"

tags = {
  Owner = "identity-forge"
}

# Networking

vpc_cidr                   = "10.0.0.0/16"
enable_s3_gateway_endpoint = true

# Security

# Admin access to the bastion 
admin_cidr_blocks = ["203.0.113.0/28"] # We need to replace with admin Ip

# Public application traffic
alb_ingress_cidrs = ["0.0.0.0/0"]

# Port 80 allows the ALB to redirect HTTP to HTTPS when a certificate exists.
enable_http_listener = true

# Service ports
gateway_port  = 8000 # Kong proxy; use 9080 for APISIX
keycloak_port = 8443
ca_port       = 9000 # Smallstep CA; use 8443 for EJBCA
db_port       = 5432
ssh_port      = 22

#  ALB
certificate_arn            = "arn:aws:acm:af-south-1:<account-id>:certificate/<id>" #replace with real cert ARN

ssl_policy = "ELBSecurityPolicy-TLS13-1-2-2021-06"

enable_deletion_protection = true
idle_timeout               = 60
health_check_path    = "/healthz"
health_check_matcher = "200-399"

access_logs_bucket = null # Set to the S3 bucket name once bucket is available.

# KMS
deletion_window_in_days = 30
