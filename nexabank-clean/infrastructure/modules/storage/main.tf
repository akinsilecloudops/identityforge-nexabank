resource "random_id" "bucket_suffix" {
  byte_length = 4
}

locals {
  name        = var.name
  common_tags = var.common_tags
  bucket_name = var.s3_bucket_name != "" ? var.s3_bucket_name : "${local.name}-backup-logs-${random_id.bucket_suffix.hex}"
}

resource "aws_s3_bucket" "backup_logs" {
  bucket = local.bucket_name

  tags = merge(local.common_tags, {
    Name    = "${local.name}-backup-logs"
    Purpose = "backup-and-logs"
  })
}

resource "aws_s3_bucket_versioning" "backup_logs" {
  bucket = aws_s3_bucket.backup_logs.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "backup_logs" {
  bucket = aws_s3_bucket.backup_logs.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = var.s3_kms_key_arn
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "backup_logs" {
  bucket                  = aws_s3_bucket.backup_logs.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "backup_logs" {
  bucket = aws_s3_bucket.backup_logs.id

  rule {
    id     = "expire-old-logs"
    status = "Enabled"

    filter {
      prefix = "logs/"
    }

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }
  }
}
