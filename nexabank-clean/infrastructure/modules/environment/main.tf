# NETWORKING

module "networking" {
  source = "./modules/networking"

  project_name = var.project_name
  environment  = var.environment
  vpc_cidr     = var.vpc_cidr

  enable_s3_gateway_endpoint = var.enable_s3_gateway_endpoint

  tags = var.tags
}

# SECURITY

module "security" {
  source = "./modules/security"

  project_name = var.project_name
  environment  = var.environment

  # Networking dependency
  vpc_id = module.networking.vpc_id

  # Admin access
  admin_cidr_blocks = var.admin_cidr_blocks

  # Public ALB access
  alb_ingress_cidrs = var.alb_ingress_cidrs

  # ALB HTTP → HTTPS redirect
  enable_http_listener = var.enable_http_listener

  # Service ports
  gateway_port  = var.gateway_port
  keycloak_port = var.keycloak_port
  ca_port       = var.ca_port
  db_port       = var.db_port
  ssh_port      = var.ssh_port

  tags = var.tags
}


