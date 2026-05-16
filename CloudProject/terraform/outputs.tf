output "alb_dns_name" {
  description = "Public DNS of the Application Load Balancer"
  value       = module.alb.alb_dns_name
}

output "frontend_url" {
  description = "URL to access the Streamlit frontend"
  value       = "http://${module.alb.alb_dns_name}:8501"
}

output "api_url" {
  description = "URL to access the FastAPI backend"
  value       = "http://${module.alb.alb_dns_name}:8000"
}

output "api_docs_url" {
  description = "FastAPI auto-generated docs"
  value       = "http://${module.alb.alb_dns_name}:8000/docs"
}

output "rds_endpoint" {
  description = "RDS PostgreSQL endpoint (private)"
  value       = module.rds.db_endpoint
  sensitive   = true
}

output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}
