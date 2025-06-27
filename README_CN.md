# Hugging Face to ModelScope Transfer (Hugging Face 模型迁移至 ModelScope)

一个用于将 Hugging Face Hub 上的模型迁移到 ModelScope 平台的工具。

## 安装

```bash
pip install hf-ms-transfer
```

## 使用方法

在您将要运行命令的目录中创建一个 `.env` 文件，并添加您的 ModelScope [令牌](https://www.modelscope.cn/my/myaccesstoken) 和用户名：
```
ms_token="your_modelscope_token"
ms_name="your_modelscope_username"
```

或者，您也可以通过命令行参数直接提供这些信息。
```bash
hf-ms-transfer <huggingface_model_id> [--private] [--ms-token <token>] [--ms-name <username>]
```

所有参数：
*   `<huggingface_model_id>`: 要迁移的 Hugging Face 模型 ID (例如, `bert-base-uncased`)。
*   `--private`: (可选) 将 ModelScope 仓库设为私有 (默认为公开)。
*   `--ms-token <token>`: (可选) 您的 ModelScope 访问令牌。会覆盖 `.env` 文件中的值。
*   `--ms-name <username>`: (可选) 您的 ModelScope 用户名。会覆盖 `.env` 文件中的值。
