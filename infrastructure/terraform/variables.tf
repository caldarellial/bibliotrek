variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "use_localstack" {
  description = "When true, the AWS provider targets LocalStack (test credentials and service endpoints). When false, use real AWS credentials from the environment or IAM."
  type        = bool
  default     = true
}

variable "localstack_endpoint" {
  description = "LocalStack base URL for S3, EC2, and RDS APIs"
  type        = string
  default     = "http://localhost:4566"
}

variable "user_media_bucket_name" {
  description = "Name of the S3 bucket for user-uploaded media"
  type        = string
  default     = "bibliotrek-user-media-local"
}

# --- RDS (PostgreSQL) ---

variable "enable_rds" {
  description = "Provision RDS PostgreSQL (LocalStack or real AWS, depending on use_localstack)."
  type        = bool
  default     = true
}

variable "db_identifier" {
  description = "Unique RDS instance identifier (lowercase, no underscores in some AWS contexts; hyphenated is fine)"
  type        = string
  default     = "bibliotrek-pg"
}

variable "postgres_engine_version" {
  description = "PostgreSQL major.minor for aws_db_instance (must be available in the region)"
  type        = string
  default     = "16.4"
}

variable "postgres_db_name" {
  description = "Initial database name (dbname for connection strings)"
  type        = string
  default     = "bibliotrek"
}

variable "postgres_master_username" {
  description = "RDS master username (not the reserved name 'postgres' on RDS)"
  type        = string
  default     = "bibliotrek"
}

variable "db_instance_class" {
  description = "RDS instance class (e.g. db.t3.micro for LocalStack dev and small production)"
  type        = string
  default     = "db.t3.micro"
}

variable "db_allocated_storage" {
  description = "Allocated storage in GB"
  type        = number
  default     = 20
}

variable "rds_publicly_accessible" {
  description = "If null: true when use_localstack (reachable from host), false on real AWS (private). Override when your network layout differs."
  type        = bool
  default     = null
}

variable "rds_allowed_cidr_blocks" {
  description = "CIDR blocks allowed to connect to PostgreSQL on port 5432. Tighten for production."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}
