# Set variables for deployment
export TF_VAR_guardian_api_key := $(guardian_api_key)

# Command to zip the Lambda function and its dependencies
zip-lambda:
	pip install -r requirements.txt -t ./src
	cd src && zip -r ../lambda_package.zip *

# Command to run tests
run-tests:
	pytest --maxfail=1 --disable-warnings -v tests/

# Command to deploy using Terraform
deploy-lambda: zip-lambda
	cd terraform && terraform init
	cd terraform && terraform apply -auto-approve

# Command to destroy resources
destroy-lambda:
	cd terraform && terraform destroy -auto-approve
