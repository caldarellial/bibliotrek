terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

provider "aws" {
  region = var.aws_region

  # Route S3, EC2, and RDS to LocalStack when use_localstack is true (Postgres via RDS locally and in AWS).
  dynamic "endpoints" {
    for_each = var.use_localstack ? [1] : []
    content {
      s3  = var.localstack_endpoint
      ec2 = var.localstack_endpoint
      rds = var.localstack_endpoint
    }
  }

  access_key                  = var.use_localstack ? "test" : null
  secret_key                  = var.use_localstack ? "test" : null
  skip_credentials_validation = var.use_localstack
  skip_metadata_api_check     = var.use_localstack
  skip_requesting_account_id  = var.use_localstack
  s3_use_path_style           = var.use_localstack
}

resource "aws_s3_bucket" "user_media" {
  bucket = var.user_media_bucket_name

  tags = {
    Environment = var.use_localstack ? "local" : "aws"
    ManagedBy   = "terraform"
    Project     = "bibliotrek"
    Purpose     = "user-uploaded-media"
  }
}

resource "aws_s3_bucket_public_access_block" "user_media" {
  bucket = aws_s3_bucket.user_media.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "user_media" {
  bucket = aws_s3_bucket.user_media.id

  versioning_configuration {
    status = "Enabled"
  }
}
