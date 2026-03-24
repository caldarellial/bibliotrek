# Bibliotrek infrastructure (Terraform)

Terraform provisions **S3** (user media) and **RDS PostgreSQL** for both **LocalStack** (local) and **deployed AWS**, controlled by `use_localstack`.

| Environment | Database | Object storage |
|-------------|----------|----------------|
| **Local** (`use_localstack = true`) | **RDS PostgreSQL** on LocalStack | S3 on LocalStack |
| **Deployed** (`use_localstack = false`) | **RDS PostgreSQL** on AWS | S3 on AWS |

The FastAPI app uses **`POSTGRES_*` / `DATABASE_URL`** from Terraform outputs in both cases (see `server/app/config.py`). SQLite remains an optional fallback when no Postgres settings are provided.

## Prerequisites

- Terraform >= 1.0
- **LocalStack** with **S3**, **EC2** (VPC / subnets / security groups), and **RDS** — for example:

  ```bash
  docker run -d -p 4566:4566 \
    -e SERVICES=s3,ec2,rds \
    localstack/localstack
  ```

  RDS on LocalStack requires a [plan that includes RDS](https://docs.localstack.cloud/aws/services/rds/) (licensing resolved on your side).

- **AWS:** valid credentials and `use_localstack = false`.

## LocalStack (default)

```bash
cd infrastructure/terraform
terraform init
terraform apply
```

Defaults: `use_localstack = true`, `enable_rds = true`, `localstack_endpoint = "http://localhost:4566"`.

## Deployed AWS

`terraform.tfvars` or CLI:

```hcl
use_localstack = false
# enable_rds defaults to true
```

```bash
terraform init
terraform apply
```

Tune `aws_region`, RDS size, `rds_allowed_cidr_blocks`, and `rds_publicly_accessible` for your environment.

## Connect the FastAPI server

Configuration priority in `server/app/config.py`:

| Priority | Use |
|----------|-----|
| 1 | `DATABASE_URL` |
| 2 | `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` |
| 3 | SQLite via `SQLITE_PATH` (default `database.db`) if Postgres is not configured |

After `terraform apply`:

```bash
terraform output rds_connection_hint
terraform output -raw rds_master_password
```

For production, prefer **AWS Secrets Manager** (or similar) instead of plain environment variables.

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `aws_region` | `us-east-1` | AWS region |
| `use_localstack` | `true` | LocalStack vs real AWS |
| `localstack_endpoint` | `http://localhost:4566` | LocalStack base URL |
| `user_media_bucket_name` | `bibliotrek-user-media-local` | S3 bucket name |
| `enable_rds` | `true` | Create RDS PostgreSQL |
| `db_identifier` | `bibliotrek-pg` | RDS instance identifier |
| `postgres_engine_version` | `16.4` | Postgres engine (must exist in region / LocalStack) |
| `postgres_db_name` | `bibliotrek` | Initial database name |
| `postgres_master_username` | `bibliotrek` | Master username (not `postgres` on AWS RDS) |
| `db_instance_class` | `db.t3.micro` | RDS instance class |
| `db_allocated_storage` | `20` | Storage (GB) |
| `rds_publicly_accessible` | `null` | Defaults to **true** on LocalStack, **false** on AWS |
| `rds_allowed_cidr_blocks` | `["0.0.0.0/0"]` | Postgres ingress — **tighten for production** |

## Outputs

- **S3:** `user_media_bucket_id`, `user_media_bucket_arn`, `user_media_bucket_region`
- **RDS:** `rds_address`, `rds_port`, `rds_database_name`, `rds_master_username`, `rds_master_password` (sensitive), `rds_connection_hint`

## Notes

- **Provider endpoints:** With `use_localstack = true`, Terraform must send **S3, EC2, and RDS** to LocalStack. If EC2/RDS are omitted, refresh/destroy of those resources can hit real AWS and fail with `AuthFailure` (401).
- **S3 path style:** `s3_use_path_style = true` so path-style URLs work against LocalStack (`http://localhost:4566/...`).
- **Production:** Prefer private RDS, restricted security groups, backups, and proper final snapshots instead of the dev-oriented `skip_final_snapshot` in this template.
- **Engine version:** If apply fails, adjust `postgres_engine_version` for your region or LocalStack.
