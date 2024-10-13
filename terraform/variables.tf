variable "region" {
  default = "eu-west-2"
  description = "AWS region for deploying resources"
}

variable "guardian_api_key" {
  default = "your-guardian-api-key"
  description = "API key for The Guardian API"
  type        = string
}
