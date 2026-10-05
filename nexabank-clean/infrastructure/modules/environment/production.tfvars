project_name = "nexabank"
environment  = "prod"

vpc_cidr = "10.0.0.0/16"

enable_s3_gateway_endpoint = true

tags = {
  Project     = "NexaBank"
  Environment = "prod"
  ManagedBy   = "terraform"
}
