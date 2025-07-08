# Hugging Face to ModelScope Transfer

[简体中文](README_CN.md)

A simple command-line tool to transfer models and datasets from the Hugging Face Hub to the ModelScope Hub.

## Features

- Supports both models and datasets.
- Transfer multiple repositories in a single command.
- Option to specify a custom repository name on ModelScope.
- Automatic repository naming with collision handling (appends a timestamp if the name exists).
- Configure credentials using a `.env` file or command-line arguments.
- Transfer into public or private repositories.

## Installation

```bash
pip install hf-ms-transfer
```

## Usage

### 1. Configuration

Create a `.env` file in your project directory and add your ModelScope token and username. You can get your token from the [ModelScope user center](https://www.modelscope.cn/my/myaccesstoken).

```env
# .env
ms_token="your_modelscope_token"
ms_name="your_modelscope_username"
```

Alternatively, you can provide the token and username directly as command-line arguments.

### 2. Run the Command

```bash
hf-ms-transfer <hf_repo_ids> [options]
```

### Arguments

-   `<hf_repo_ids>`: **(Required)** One or more Hugging Face repository IDs, separated by commas (e.g., `bert-base-uncased,stanfordnlp/imdb`).
-   `--ms-token <token>`: (Optional) Your ModelScope access token. Overrides the value in the `.env` file.
-   `--ms-name <username>`: (Optional) Your ModelScope username. Overrides the value in the `.env` file.
-   `--ms-repo-name <name>`: (Optional) A custom name for the repository on ModelScope.
    > **Note:** This option cannot be used when transferring multiple repositories.
-   `--private`: (Optional) Create the ModelScope repository as private. Defaults to public.
-   `--keep-dataset-infos`: (Optional) For datasets, upload the `dataset_infos.json` file. By default, this file is excluded as it can cause issues when using `load_datastes` function.
