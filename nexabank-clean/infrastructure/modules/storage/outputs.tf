output "bucket_id" {
  description = "Name/ID of the backup-and-logs S3 bucket."
  value       = aws_s3_bucket.backup_logs.id
}

output "bucket_arn" {
  description = "ARN of the backup-and-logs S3 bucket (use for IAM policies / bucket policies)."
  value       = aws_s3_bucket.backup_logs.arn
}

output "bucket_domain_name" {
  description = "Regional domain name of the bucket."
  value       = aws_s3_bucket.backup_logs.bucket_regional_domain_name
}
