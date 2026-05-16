# Development environment overrides
aws_region   = "us-east-1"
environment  = "dev"
project_name = "cloud-janitor"

db_instance_class = "db.t3.micro"
backend_cpu       = 256
backend_memory    = 512
frontend_cpu      = 256
frontend_memory   = 512

# Set these to your ECR image URIs after pushing
backend_image  = "123456789.dkr.ecr.us-east-1.amazonaws.com/cloud-janitor-backend:latest"
frontend_image = "123456789.dkr.ecr.us-east-1.amazonaws.com/cloud-janitor-frontend:latest"

# db_password = "set-in-tfvars-or-env-var"
