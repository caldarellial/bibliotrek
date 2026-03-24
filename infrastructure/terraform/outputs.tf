output "user_media_bucket_id" {
  description = "Name (id) of the user media S3 bucket"
  value       = aws_s3_bucket.user_media.id
}

output "user_media_bucket_arn" {
  description = "ARN of the user media S3 bucket"
  value       = aws_s3_bucket.user_media.arn
}

output "user_media_bucket_region" {
  description = "AWS region of the user media bucket"
  value       = aws_s3_bucket.user_media.region
}

# PostgreSQL — wire these to the API (POSTGRES_HOST, POSTGRES_PORT, etc.) or build DATABASE_URL

output "rds_address" {
  description = "RDS hostname (without port)"
  value       = try(aws_db_instance.main[0].address, null)
}

output "rds_port" {
  description = "PostgreSQL port"
  value       = try(aws_db_instance.main[0].port, null)
}

output "rds_database_name" {
  description = "Database name to use in connection strings"
  value       = try(aws_db_instance.main[0].db_name, null)
}

output "rds_master_username" {
  description = "Master username for PostgreSQL"
  value       = try(aws_db_instance.main[0].username, null)
}

output "rds_master_password" {
  description = "Master password (sensitive)"
  value       = try(random_password.db_master[0].result, null)
  sensitive   = true
}

output "rds_connection_hint" {
  description = "Example POSTGRES_* env vars for the FastAPI app (password omitted; use rds_master_password)"
  value = try(join("\n", [
    "POSTGRES_HOST=${aws_db_instance.main[0].address}",
    "POSTGRES_PORT=${aws_db_instance.main[0].port}",
    "POSTGRES_USER=${aws_db_instance.main[0].username}",
    "POSTGRES_DB=${aws_db_instance.main[0].db_name}",
    "POSTGRES_PASSWORD=<terraform output -raw rds_master_password>",
  ]), null)
}
