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

# APPLICATION LOAD BALANCER

module "alb" {
  source = "./modules/alb"

  project_name = var.project_name
  environment  = var.environment

  vpc_id     = module.networking.vpc_id
  subnet_ids = module.networking.alb_subnet_ids

  security_group_id = module.security.alb_sg_id

  gateway_port         = var.gateway_port
  health_check_path    = var.health_check_path
  health_check_matcher = var.health_check_matcher

  certificate_arn = var.certificate_arn
  ssl_policy      = var.ssl_policy

  enable_http_listener = var.enable_http_listener

  enable_deletion_protection = var.enable_deletion_protection
  idle_timeout               = var.idle_timeout

  access_logs_bucket = var.access_logs_bucket

  tags = var.tags
}


# KMS CMK

module "kms" {
  source = "./modules/kms"

  project_name            = var.project_name
  environment             = var.environment
  deletion_window_in_days = var.deletion_window_in_days

  tags = var.tags
}

