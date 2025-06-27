# Hugging Face to ModelScope Transfer

[简体中文](README_CN.md)

A tool to transfer models from the Hugging Face Hub to the ModelScope platform.

## Installation

```bash
pip install hf-ms-transfer
```

## Usage

Create a `.env` file in the directory where you will run the command and add your ModelScope [token](https://www.modelscope.cn/my/myaccesstoken) and username:
```
ms_token="your_modelscope_token"
ms_name="your_modelscope_username"
```

Alternatively, you can provide these directly via command-line arguments.
```bash
hf-ms-transfer <huggingface_model_id> [--private] [--ms-token <token>] [--ms-name <username>]
```

All parameters:
*   `<huggingface_model_id>`: The ID of the Hugging Face model to transfer (e.g., `bert-base-uncased`).
*   `--private`: (Optional) Make the ModelScope repository private (default is public).
*   `--ms-token <token>`: (Optional) Your ModelScope access token. Overrides the value in `.env`.
*   `--ms-name <username>`: (Optional) Your ModelScope username. Overrides the value in `.env`.
