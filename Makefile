zip-lambda:
    zip -r lambda_package.zip src/*

deploy-lambda: zip-lambda
    terraform apply -auto-approve
