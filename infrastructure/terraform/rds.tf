locals {
  # LocalStack: default reachable from the host (localhost). AWS: default private unless overridden.
  effective_rds_public = coalesce(var.rds_publicly_accessible, var.use_localstack)
}

resource "random_password" "db_master" {
  count = var.enable_rds ? 1 : 0

  length  = 24
  special = false
}

data "aws_vpc" "default" {
  count   = var.enable_rds ? 1 : 0
  default = true
}

data "aws_subnets" "default" {
  count = var.enable_rds ? 1 : 0

  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default[0].id]
  }
}

resource "aws_security_group" "postgres" {
  count = var.enable_rds ? 1 : 0

  name_prefix = "${var.db_identifier}-pg-"
  description = "Bibliotrek PostgreSQL ingress"
  vpc_id      = data.aws_vpc.default[0].id

  ingress {
    description = "PostgreSQL"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = var.rds_allowed_cidr_blocks
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Project = "bibliotrek"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_db_subnet_group" "main" {
  count = var.enable_rds ? 1 : 0

  name       = "${var.db_identifier}-subnet"
  subnet_ids = data.aws_subnets.default[0].ids

  tags = {
    Project = "bibliotrek"
  }
}

resource "aws_db_instance" "main" {
  count = var.enable_rds ? 1 : 0

  identifier                 = var.db_identifier
  engine                     = "postgres"
  engine_version             = var.postgres_engine_version
  instance_class             = var.db_instance_class
  allocated_storage          = var.db_allocated_storage
  storage_type               = "gp2"
  db_name                    = var.postgres_db_name
  username                   = var.postgres_master_username
  password                   = random_password.db_master[0].result
  db_subnet_group_name       = aws_db_subnet_group.main[0].name
  vpc_security_group_ids     = [aws_security_group.postgres[0].id]
  publicly_accessible        = local.effective_rds_public
  skip_final_snapshot        = true
  apply_immediately          = true
  auto_minor_version_upgrade = true

  tags = {
    Project = "bibliotrek"
  }
}
