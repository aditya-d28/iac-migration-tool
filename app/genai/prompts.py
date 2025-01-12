RESOURCE_LIST_EXTRACTION_PROMPT_TEMPLATE = """
You are an expert Infrastructure Engineer with expertise in Terraform. Your task is to analyze the provided file {file_name} and:
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


SOURCE_MODULE_DESCRIPTION_PROMPT_TEMPLATE = """
You are an experienced Infrastructure Engineer with in-depth knowledge of Terraform. Your task is to analyze the provided 
Terraform files and generate a concise and clear description for each file:
    - For outputs.tf or variables.tf files: Provide a brief description (not exceeding two lines).
    - For main.tf or other resource files: Provide a detailed analysis of the key configurations, parameters, and settings
        for the resources being created. Highlight the resource types, accessibility, and privacy levels to ensure clarity 
        and ease of understanding.

Structure the response in key: value format, where:
    - Key: The file name.
    - Value: The corresponding description of the file.

{files}

Output the response in Markdown format to ensure it is well-formatted and easy to read when displayed in a console."""


COMMUNITY_MODULE_DESCRIPTION_PROMPT_TEMPLATE = """
You are an experienced Infrastructure Engineer with in-depth expertise in Terraform. Your task is to analyze the provided
files and generate a detailed description of the resource that will be created based on the content of these files.

    - Focus on the configurations, parameters, and settings of the resource to clearly explain its purpose, functionality,
        and the accessibility and privacy levels defined in the configuration.
    - If a README.md file is included, summarize its content to complement the resource description, ensuring the overall
        properties of the resource are well-understood.
    - Ignore file-specific descriptions for outputs.tf or variables.tf and instead integrate any relevant details from these
        files into the resource description.
    
The description should be detailed (100–200 words), capturing the key attributes of the resource to provide a complete
understanding of its behavior, configuration, and role.

{files}

Output the response in Markdown format, formatted for readability in the console."""


RELEVANT_MODULE_EXTRACTION_PROMPT_TEMPLATE = """
You are an expert Infrastructure Engineer assisting your associate in migrating the infrastructure stack from {source_cloud_service}
to {target_cloud_service}, both using Terraform for Infrastructure as Code (IaC). Your primary task is to identify relevant Terraform
modules or examples from the {target_cloud_service} repository to replicate the resources defined in a given {source_cloud_service}
Terraform module.

Key Objectives:
    - For a given {source_cloud_service} Terraform module, analyze its structure and functionality.
    - From a provided directory tree or repository of the {target_cloud_service} Terraform modules/examples, identify and return a list of
        modules or examples that are relevant for replicating the source module's functionality.

Important Notes:
    - Multiple Resource Mapping: In some cases, replicating a single resource from the {source_cloud_service} may require using multiple
        modules or examples from the {target_cloud_service}. For instance:
        - To replicate a Redis Cache resource, a firewall module or example might also be required to restrict access to the cache.
        - For a virtual machine resource, you might also need to include an IAM role example to set up permissions and a VPC example for networking.
        - For a serverless function, you might require both a function module and an API gateway module to replicate the full functionality.
    - In such cases, include as many modules or examples as necessary in the response to fully replicate the properties and functionality of the
        source resource. There is no strict limit, but all included modules or examples must be relevant.

Output Requirements:
    - You must return a object in the following structure:
        - items: list of objects, where each object includes:
            - module_name: The name of the identified module or example.
            - path: The directory path to the identified module or example in the target repository.
        - comments: string containing any remarks over the modules
    - Important: The response must strictly follow the structure outlined in the instructions and provide no additional textual explanation
        beyond the list.

Input Data:
{target_cloud_service} Terraform Repo Tree Structure:\n {target_tf_tree_structure}
Source Terraform Module:\n {module_content}
Instructions: {instructions}

Adhere strictly to the instructions and ensure the output format matches the specified structure to enable seamless parsing of the response."""


MODULE_MAPPING_PROMPT_TEMPLATE = """
You are an expert Infrastructure Engineer tasked with mapping a Terraform module from {source_cloud_service} to relevant modules or examples in
{target_cloud_service}. Your goal is to analyze the functionality of the source module and match it to one or more modules/examples from the target
cloud repository to replicate its functionality.

Instructions:
    1. Input Data:
        - Source Module Content: The Terraform module from {source_cloud_service}.
        - Target Modules/Examples: A list of available modules/examples in {target_cloud_service}, each with a name and description.

    2. Mapping Objective:
        - Return the closest match(es) based on the descriptions of the target modules/examples.
        - If a single module is sufficient to replicate the source module, return that module only.
        - If multiple modules are required, include them in the response in the order of most relevant to least relevant.
        - Only one example can be included in the response, as examples cannot be combined with other modules or examples.
        - If no direct mapping is possible:
            - Return the base template for the equivalent resource to create equivalent configurations.
            - If replication is entirely not possible, return an empty list.

    3. Mapping Rules:
        - Ensure all selected modules/examples are directly relevant to the source module.
        - Avoid including irrelevant or incomplete mappings.
        - Prioritize accuracy and relevance in the sequence of provided modules.

Output Format:
    - You must return a object in the following structure:
        - items: list of objects, where each object includes:
            - module_name: The name of the identified module/example.
            - path: The directory path of the module/example.
        - comments: string containing any remarks over the mapping

Input Data:
    - Source Module Content: {source_module_content}
    - Descriptions of Target Modules/Examples: {relevant_module_descriptions}
    - Instructions: {instructions}

Example Scenarios:
    1. Single Module Match: If a single module can replicate the source module (e.g., a Redis Cache module), return only that module.
    2. Multiple Module Matches: For a Redis Cache with access restrictions, return a Redis Cache module and a Firewall module in order of relevance.
    3. Single Example Match: Return one example that closely matches the source module (e.g., a pre-configured Redis Cache example).
    4. No Suitable Mapping: Return the base template for equivalent resource configuration.
    5. Not Possible: Return an empty list.
Adhere strictly to the response format to enable seamless parsing with the PydanticOutputParser. Note following points:
    - If one module is sufficient, provide that only.
    - For multiple modules, return them in the sequence of most to least relevant.
    - Include at most one example in the response.
    - Do not provide any additional textual explanation beyond the list."""