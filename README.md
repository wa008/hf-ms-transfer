# Hugging Face to ModelScope Transfer

A tool to transfer models from the Hugging Face Hub to the ModelScope platform.

## Installation

```bash
pip install .
```

## Setup

1.  Create a `.env` file in the directory where you will run the command and add your ModelScope token and username:
    ```
    ms_token="your_modelscope_token"
    ms_name="your_modelscope_username"
    ```
    Alternatively, you can provide these directly via command-line arguments.

## Usage

```bash
hf-ms-transfer <huggingface_model_id> [--private] [--ms-token <token>] [--ms-name <username>]
```

*   `<huggingface_model_id>`: The ID of the Hugging Face model to transfer (e.g., `bert-base-uncased`).
*   `--private`: (Optional) Make the ModelScope repository private (default is public).
*   `--ms-token <token>`: (Optional) Your ModelScope access token. Overrides the value in `.env`.
*   `--ms-name <username>`: (Optional) Your ModelScope username. Overrides the value in `.env`.