# Set variables for deployment
export TF_VAR_guardian_api_key := $(guardian_api_key)

# Command to create a virtual environment for Python
create-venv:
	python3 -m venv venv

# Command to activate virtual environment and install dependencies for testing
install-dependencies: create-venv
	. venv/bin/activate && pip install -r requirements-test.txt

# Command to zip the Lambda function and its dependencies
zip-lambda:
	pip install -r requirements-lambda.txt -t ./src
	cd src && zip -r ../lambda_package.zip *

# Command to run tests
run-tests:
	PYTHONPATH=src pytest --maxfail=1 --disable-warnings -v tests/

# Command to deploy using Terraform
deploy-lambda: zip-lambda
	cd terraform && terraform init
	cd terraform && terraform apply -var "guardian_api_key=$(guardian_api_key)" -auto-approve

# Command to destroy resources
destroy-lambda:
	cd terraform && terraform destroy -auto-approve
