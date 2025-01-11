RESOURCE_LIST_EXTRACTION_PROMPT = """You are an expert Infrastructure Engineer with expertise in Terraform. Your task is to analyze the provided file {file_name} and:
                                        1. Extract all the resources provisioned in the file.
                                        2. Identify the module sources used for provisioning these resources.
                                        3. Determine whether each module is a custom module (created by the developer of the IaC code) or a community module.
                                    Instructions:
                                        - Provide the output strictly as a list of objects.
                                        - Do not provide any explanation along with the list, ONLY LIST is enough.
                                        - Follow the format specified in the instructions provided.
                                        
                                    File Content: {file_content}
                                    
                                    Instructions: {instructions}
                                    
                                    Examples:
                                    
                                    Example Input (HCL Format)
                                        File Name: main.tf
                                        File Content:
                                        ```
                                            provider "aws" {{
                                                region = "us-west-2"
                                            }}

                                            module "s3_bucket" {{
                                                source      = "./modules/s3"
                                                bucket_name = "example-bucket"
                                                acl         = "private"
                                            }}

                                            module "ec2_instance" {{
                                                source = "terraform-aws-modules/ec2-instance/aws"
                                                count  = 1
                                                ami    = "ami-0c55b159cbfafe1f0"
                                                instance_type = "t2.micro"
                                            }}

                                            resource "aws_dynamodb_table" "example" {{
                                                name         = "example-table"
                                                billing_mode = "PAY_PER_REQUEST"
                                                hash_key     = "id"

                                                attribute {{
                                                    name = "id"
                                                    type = "S"
                                                }}
                                            }}
                                        ```
                                        Expected Output: {{"items": [{{"resource": "aws_s3_bucket","module": "./modules/s3","type": "custom"}},{{"resource": "aws_instance","module": "terraform-aws-modules/ec2-instance/aws","type": "community"}},{{"resource": "aws_dynamodb_table","module": null,"type": null}}]}}
                                        
                                    Example Input (JSON Format)
                                        File Name: main.tf.json
                                        File Content:
                                        ```
                                        {{
                                            "provider": {{
                                                "aws": {{
                                                "region": "us-west-2"
                                                }}
                                            }},
                                            "module": {{
                                                "s3_bucket": {{
                                                    "source": "./modules/s3",
                                                    "bucket_name": "example-bucket",
                                                    "acl": "private"
                                                }},
                                                "ec2_instance": {{
                                                    "source": "terraform-aws-modules/ec2-instance/aws",
                                                    "count": 1,
                                                    "ami": "ami-0c55b159cbfafe1f0",
                                                    "instance_type": "t2.micro"
                                                }}
                                            }},
                                            "resource": {{
                                                "aws_dynamodb_table": {{
                                                    "example": {{
                                                        "name": "example-table",
                                                        "billing_mode": "PAY_PER_REQUEST",
                                                        "hash_key": "id",
                                                        "attribute": [
                                                        {{
                                                            "name": "id",
                                                            "type": "S"
                                                        }}
                                                        ]
                                                    }}
                                                }}
                                            }}
                                        }}
                                        ```
                                        Expected Output: {{"items": [{{"resource": "aws_s3_bucket","module": "./modules/s3","type": "custom"}},{{"resource": "aws_instance","module": "terraform-aws-modules/ec2-instance/aws","type": "community"}},{{"resource": "aws_dynamodb_table","module": null,"type": null}}]}}
                                    """
