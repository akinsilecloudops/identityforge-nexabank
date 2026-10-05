# NETWORKING

module "networking" {
  source = "./modules/networking"

  project_name = var.project_name
  environment  = var.environment
  vpc_cidr     = var.vpc_cidr

  enable_s3_gateway_endpoint = var.enable_s3_gateway_endpoint

  tags = var.tags
}
