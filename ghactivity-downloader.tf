locals {
    function_name = "ghactivity-downloader"
}

data "aws_s3_bucket_object" "scripts_bucket" {
    bucket = "jenkins-deploy-dataengg-tut"
    key = "scripts/${local.function_name}.zip"
}

resource "aws_lambda_function" "ghactivity_downloader_lambda" {
    function_name = "${local.function_name}-function"
    role = "arn:aws:iam::256772913192:role/ghactivity-downloader-role"
    handler = "ghactivity-downloader.lambda_handler"
    s3_bucket = data.aws_s3_bucket_object.scripts_bucket
    s3_key = data.aws_s3_bucket_object.scripts_bucket.key
    runtime = ""
    timeout = "1000"
}