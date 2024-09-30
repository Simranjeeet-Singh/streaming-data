# Command to zip the Lambda function
zip-lambda:
	cd src && zip -r ../lambda_package.zip *

# Command to deploy using Terraform in a subdirectory
deploy-lambda: zip-lambda
	cd terraform && terraform apply -auto-approve