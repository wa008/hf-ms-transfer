# Hugging Face to ModelScope Transfer

[简体中文](README_CN.md)

A tool to transfer models/datasets from the Hugging Face Hub to the ModelScope platform.

By default, when transferring a repository from Hugging Face (e.g., `user/package`), it will be created on ModelScope as `package`. If a repository with the same name already exists, a timestamp will be appended to the name (e.g., `package_20250708160640`). You can also specify a custom name using the `--ms-repo-name` argument. **Note: You cannot provide a custom ModelScope repository name when transferring multiple Hugging Face repositories.**

By default, the `dataset_infos.json` file is not uploaded to ModelScope for datasets, as it can sometimes cause issues on the platform. You can choose to keep this file by using the `--keep-dataset-infos` flag.

## Installation

```bash
pip install hf-ms-transfer
```

## Usage

Create a `.env` file in the directory where you will run the command and add your ModelScope [token](https://www.modelscope.cn/my/myaccesstoken) and username:
```
ms_token="your_modelscope_token"
ms_name="your_modelscope_username"
# Optional: Specify a Hugging Face Hub endpoint
# HF_ENDPOINT="https://huggingface.co"
```

Alternatively, you can provide these directly via command-line arguments.
```bash
hf-ms-transfer <hf_repo_ids> [--private] [--ms-token <token>] [--ms-name <username>] [--ms-repo-name <name>] [--keep-dataset-infos]
```

All parameters:
*   `<hf_repo_ids>`: The Hugging Face model or dataset IDs, separated by commas (e.g., `'bert-base-uncased,stanfordnlp/imdb'`).
*   `--private`: (Optional) Make the ModelScope repository private (default is public).
*   `--ms-token <token>`: (Optional) Your ModelScope access token. Overrides the value in `.env`. If not provided, a `ValueError` will be raised.
*   `--ms-name <username>`: (Optional) Your ModelScope username. Overrides the value in `.env`. If not provided, a `ValueError` will be raised.
*   `--ms-repo-name <name>`: (Optional) The desired repository name on ModelScope. If not provided, the Hugging Face repository name (without the username) will be used.
*   `--keep-dataset-infos`: (Optional) Keep the `dataset_infos.json` file for datasets.
