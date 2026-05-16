variable "aws_region" {
  description = "AWS region to deploy resources into"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Deployment environment (dev | staging | prod)"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Project name prefix for all resources"
  type        = string
  default     = "cloud-janitor"
}

# ─── Networking ──────────────────────────────────────────────────────────────
variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets (one per AZ)"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets (one per AZ)"
  type        = list(string)
  default     = ["10.0.11.0/24", "10.0.12.0/24"]
}

# ─── RDS ─────────────────────────────────────────────────────────────────────
variable "db_name" {
  description = "PostgreSQL database name"
  type        = string
  default     = "cloudjanitor"
}

variable "db_username" {
  description = "PostgreSQL master username"
  type        = string
  default     = "janitor"
}

variable "db_password" {
  description = "PostgreSQL master password (store in tfvars, never commit)"
  type        = string
  sensitive   = true
}

variable "db_instance_class" {
  description = "RDS instance type"
  type        = string
  default     = "db.t3.micro"
}

# ─── ECS ─────────────────────────────────────────────────────────────────────
variable "backend_image" {
  description = "ECR image URI for the FastAPI backend"
  type        = string
}

variable "frontend_image" {
  description = "ECR image URI for the Streamlit frontend"
  type        = string
}

variable "backend_cpu" {
  description = "Fargate CPU units for backend task"
  type        = number
  default     = 512
}

variable "backend_memory" {
  description = "Fargate memory (MB) for backend task"
  type        = number
  default     = 1024
}

variable "frontend_cpu" {
  description = "Fargate CPU units for frontend task"
  type        = number
  default     = 256
}

variable "frontend_memory" {
  description = "Fargate memory (MB) for frontend task"
  type        = number
  default     = 512
}
