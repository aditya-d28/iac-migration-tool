# Resource Mapping Approach

## Overview
This document outlines the methodology used in the **iac-migration-tool** to map resources from a source cloud service (e.g., Azure) to a target cloud service (e.g., GCP). The approach leverages Terraform community modules and a preprocessing phase utilizing Large Language Models (LLMs) to generate module descriptions and facilitate accurate resource mapping during migration.

## Detailed Approach

### 1. Preprocessing Phase

#### a. Fetching Community Modules
In the preprocessing phase, Terraform community modules and examples are downloaded and stored locally. These modules and examples serve as a reference database to identify resource mappings during migration.

#### b. Generating Descriptions Using LLM
For each downloaded community module, an LLM is utilized to analyze the module's code and generate a detailed description. This description includes:
- The module's purpose and primary functionalities.
- Key resources and attributes it provisions.
- Typical use cases and constraints.

These descriptions are stored in a structured format, enabling quick reference and comparison during the migration process.

### 2. Handling Migration Requests
When a migration request for a repository is received, the tool performs the following steps:

#### a. Identifying Provisioned Resources
The tool analyzes the Terraform files in the repository to identify:
- Resources provisioned by the Infrastructure as Code (IaC).
- Modules referenced within the repository.

This step provides a clear inventory of resources and modules to be mapped.

#### b. Analyzing Repository Modules
Each module referenced in the repository is examined, and relevant community modules are identified using the following steps:
- The LLM analyses the module's code.
- And shortlist of relevant community modules is created based on the source module analysis.

### 3. Resource Mapping
In the final step of the migration process, the tool performs detailed resource mapping:

#### a. Code Analysis
The tool analyzes the code of each incoming module and compares it with the descriptions of the shortlisted community modules. This comparison involves:
- Attribute matching: Ensuring the key attributes align between the incoming and community modules.
- Functional equivalence: Verifying that the modules provide similar functionality in the target cloud service.

#### b. Closest Module Selection
The community module with the highest similarity is selected as the closest match for each incoming module. The mapping tries to ensure:
- Functional parity between the source and target configurations.
- Consistency with Terraform best practices as outlined in community modules.

### 4. Report Generation
After completing the mapping process, a comprehensive report is generated and saved in the `output` folder. The report includes:
- A list of identified resources and modules from the source repository.
- The shortlisted community modules and the selected closest matches.
- Any unmapped resources or modules that require manual intervention.

## Future Improvements
- Enhance LLM models to improve description generation and matching accuracy.
- Generate target modules directly based on input configurations.
- Expand the repository of locally available community modules.
- Support the complete migration of Infrastructure as Code (IaC) configurations, including resource creation, dependency resolution, and advanced feature handling.
- Develop a feedback loop to refine mappings based on user input and real-world usage.


