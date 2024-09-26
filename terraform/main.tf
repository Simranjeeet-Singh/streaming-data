resource "aws_api_gateway_rest_api" "guardian_api" {
  name = "guardian-api"
}

resource "aws_api_gateway_resource" "articles" {
  rest_api_id = aws_api_gateway_rest_api.guardian_api.id
  parent_id   = aws_api_gateway_rest_api.guardian_api.root_resource_id
  path_part   = "articles"
}

resource "aws_api_gateway_method" "get_articles" {
  rest_api_id   = aws_api_gateway_rest_api.guardian_api.id
  resource_id   = aws_api_gateway_resource.articles.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id = aws_api_gateway_rest_api.guardian_api.id
  resource_id = aws_api_gateway_resource.articles.id
  http_method = aws_api_gateway_method.get_articles.http_method
  type        = "AWS_PROXY"
  integration_http_method = "POST"
  uri         = aws_lambda_function.guardian_lambda.invoke_arn
}

resource "aws_lambda_permission" "api_gateway_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.guardian_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.guardian_api.execution_arn}/*/*"
}
