# Hugging Face to ModelScope Transfer (Hugging Face 模型迁移至 ModelScope)

一个用于将 Hugging Face Hub 上的模型或数据集迁移到 ModelScope 平台的工具。

默认情况下，当从 Hugging Face 迁移一个仓库时 (例如, `user/package`), 它将在 ModelScope 上被创建为 `package`。如果同名仓库已存在，则会在名称后附加时间戳 (例如, `package_20250708160640`)。您也可以使用 `--ms-repo-name` 参数指定自定义名称。**注意：当迁移多个 Hugging Face 仓库时，不能提供自定义的 ModelScope 仓库名称。**

默认情况下，对于数据集，`dataset_infos.json` 文件不会被上传到 ModelScope，因为它有时会在平台上引起问题。您可以选择使用 `--keep-dataset-infos` 标志来保留此文件。

## 安装

```bash
pip install hf-ms-transfer
```

## 使用方法

在您将要运行命令的目录中创建一个 `.env` 文件，并添加您的 ModelScope [令牌](https://www.modelscope.cn/my/myaccesstoken) 和用户名：
```
ms_token="your_modelscope_token"
ms_name="your_modelscope_username"
# 可选：指定 Hugging Face Hub 的端点
# HF_ENDPOINT="https://huggingface.co"
```

或者，您也可以通过命令行参数直接提供这些信息。
```bash
hf-ms-transfer <hf_repo_ids> [--private] [--ms-token <token>] [--ms-name <username>] [--ms-repo-name <name>] [--keep-dataset-infos]
```

所有参数：
*   `<hf_repo_ids>`: 要迁移的 Hugging Face 模型或数据集 ID，多个 ID 之间用逗号分隔 (例如, `'bert-base-uncased,stanfordnlp/imdb'`)。
*   `--private`: (可选) 将 ModelScope 仓库设为私有 (默认为公开)。
*   `--ms-token <token>`: (可选) 您的 ModelScope 访问令牌。会覆盖 `.env` 文件中的值。如果未提供，将引发 `ValueError`。
*   `--ms-name <username>`: (可选) 您的 ModelScope 用户名。会覆盖 `.env` 文件中的值。如果未提供，将引发 `ValueError`。
*   `--ms-repo-name <name>`: (可选) ModelScope 上所需的仓库名称。如果未提供，将使用 Hugging Face 仓库名称 (不包含用户名)。
*   `--keep-dataset-infos`: (可选) 保留数据集的 `dataset_infos.json` 文件。
