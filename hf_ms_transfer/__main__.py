
import os
import argparse
import sys
import tempfile
from pathlib import Path
from huggingface_hub import snapshot_download
from modelscope.hub.api import HubApi
from modelscope.hub.constants import ModelVisibility
from dotenv import load_dotenv

def main():
    parser = argparse.ArgumentParser(description="Transfer a Hugging Face model to ModelScope.")
    parser.add_argument("hf_model_id", type=str, help="The Hugging Face model ID (e.g., 'bert-base-uncased').")
    parser.add_argument("--private", action="store_true", help="Make the ModelScope repository private (default is public).")
    parser.add_argument("--ms-token", type=str, help="Your ModelScope access token.")
    parser.add_argument("--ms-name", type=str, help="Your ModelScope username.")
    parser.add_argument("--ms-model-name", type=str, help="The desired ModelScope model name. If not provided, it will be derived from the Hugging Face model ID.")
    args = parser.parse_args()

    hf_model_id = args.hf_model_id
    is_private = args.private

    # Load .env file from current directory or home directory
    load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))

    ms_token = args.ms_token if args.ms_token else os.getenv("ms_token")
    ms_username = args.ms_name if args.ms_name else os.getenv("ms_name")

    if not ms_token:
        print("Error: ModelScope token not found. Please provide it via --ms-token or in your .env file (key: ms_token).")
        sys.exit(1)

    if not ms_username:
        print("Error: ModelScope username not found. Please provide it via --ms-name or in your .env file (key: ms_name).")
        sys.exit(1)

    api = HubApi()
    api.login(ms_token)
    ms_model_name = args.ms_model_name if args.ms_model_name else hf_model_id.split('/')[-1]
    ms_model_id = f"{ms_username}/{ms_model_name}"

    try:
        api.create_model(
            model_id=ms_model_id,
            visibility=ModelVisibility.PRIVATE if is_private else ModelVisibility.PUBLIC,
        )
        print(f"Successfully created model repository '{ms_model_id}' on ModelScope.")
    except Exception as e:
        if "model already exists" in str(e):
            print(f"Model repository '{ms_model_id}' already exists on ModelScope.")
        else:
            print(f"Error creating model repository on ModelScope: {e}")
            sys.exit(1)


    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"Downloading model '{hf_model_id}' from Hugging Face...")
        try:
            snapshot_download(
                repo_id=hf_model_id,
                local_dir=tmpdir,
                local_dir_use_symlinks=False
            )
            print("Download complete.")
        except Exception as e:
            print(f"Error downloading model from Hugging Face: {e}")
            sys.exit(1)

        print(f"Uploading model to ModelScope repository '{ms_model_id}'...")
        try:
            api.upload_folder(
                repo_id=ms_model_id,
                folder_path=tmpdir,
                commit_message="Initial commit from Hugging Face"
            )
            print("Upload complete.")
        except Exception as e:
            print(f"Error uploading model to ModelScope: {e}")
            sys.exit(1)

    print("\nTransfer successful!")
    print(f"Model available at: https://modelscope.cn/models/{ms_model_id}")


if __name__ == "__main__":
    main()
