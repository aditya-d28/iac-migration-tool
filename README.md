# iac-migration-tool

## Overview

The **iac-migration-tool** is a utility designed to assist with the migration of Infrastructure as Code (IaC) files between cloud platforms, focusing on converting Terraform configurations. It provides analysis and code translation. *This project is a work in progress.* The tool currently just simplifies cloud migrations by mapping resources from the source cloud service to the target cloud service, ensuring compatibility and consistency.

## Prerequisites

To use this tool, you need:

- **Terraform:** Installed and configured.
- **Supported Cloud Platforms:** Azure, GCP (others may be added in the future).
- **Python Environment:** Python 3.8+ installed.
- **Poetry:** For package management.
- **Terraform Community Modules:** This project also requires the examples and modules of the target cloud service cloned locally

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/aditya-d28/iac-migration-tool.git
   ```
2. Navigate to the project directory:
   ```bash
   cd iac-migration-tool
   ```
3. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

## Environment Configuration

Add the following configurations to the `.env` file to customize the tool's behavior:

- `PROJECT_NAME`: The name of the project (e.g., `IAC-Migration-Tool`).
- `CONSOLE_LOG_LEVEL`: The logging level for console output (e.g., `INFO`).
- `FILE_LOG_LEVEL`: The logging level for file output (e.g., `DEBUG`).
- `DEV_MODE`: Enable or disable developer mode (`Y` for enable, `N` for disable).
- `LLM_PROVIDER`: The Large Language Model provider (e.g., `ANTHROPIC`).
- `LLM_MODEL_NAME`: The specific model name to use (e.g., `claude-3-5-sonnet-20241022`).
- `LLM_TEMPERATURE`: The temperature setting for LLM responses (e.g., `0.5`).
- `LLM_MAX_RETRIES`: Maximum number of retries for LLM requests (e.g., `1`).
- `ALLOWED_ORIGINS`: Origins allowed for CORS (e.g., `http://localhost:8080`).
- `TF_COMMUNITY_MODULES_PATH`: Path to locally clones community Terraform modules.
- `OUTPUT_DIR`: Directory to store output files.

## Usage

1. Place your Terraform files in the `input` directory.

2. Run the tool to analyze or convert files:

   ```bash
   poetry run uvicorn app.main --reload --port 8080
   ```

   Available actions:

   - `migrate`: Map resources from the source cloud service to the target cloud service.
   - `preProcess`: Generates a description of terraform community modules. 

3. Retrieve results from the `output` directory.

