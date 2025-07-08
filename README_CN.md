# Hugging Face to ModelScope Transfer (模型迁移工具)

[English](README.md)

一个用于将 Hugging Face Hub 上的模型和数据集迁移到 ModelScope Hub 的命令行工具。

## 功能特性

-   同时支持模型和数据集。
-   支持在单个命令中迁移多个仓库。
-   可自定义在 ModelScope 上的仓库名称。
-   自动处理命名冲突 (如果仓库名已存在，则追加时间戳)。
-   可通过 `.env` 文件或命令行参数进行配置。
-   支持迁移到公共或私有仓库。

## 安装

```bash
pip install hf-ms-transfer
```

## 使用方法

### 1. 配置

在您的项目目录中创建一个 `.env` 文件，并添加您的 ModelScope 令牌 (Token) 和用户名。您可以从 [ModelScope 个人中心](https://www.modelscope.cn/my/myaccesstoken) 获取令牌。

```env
# .env
ms_token="your_modelscope_token"
ms_name="your_modelscope_username"
```

您也可以通过命令行参数直接提供令牌和用户名。

### 2. 运行命令

```bash
hf-ms-transfer <hf_repo_ids> [options]
```

### 参数说明

-   `<hf_repo_ids>`: **(必需)** 一个或多个 Hugging Face 仓库 ID，用逗号分隔 (例如: `bert-base-uncased,stanfordnlp/imdb`)。
-   `--ms-token <token>`: (可选) 您的 ModelScope 访问令牌。此参数会覆盖 `.env` 文件中的配置。
-   `--ms-name <username>`: (可选) 您的 ModelScope 用户名。此参数会覆盖 `.env` 文件中的配置。
-   `--ms-repo-name <name>`: (可选) 在 ModelScope 上创建的仓库名称。
    > **注意:** 迁移多个仓库时，无法使用此选项。
-   `--private`: (可选) 将 ModelScope 仓库设为私有。默认为公开。
-   `--keep-dataset-infos`: (可选) 迁移数据集时，保留并上传 `dataset_infos.json` 文件。默认情况下，该文件不会被上传，因为它在使用 `load_datastes` 函数时可能会引发问题。
