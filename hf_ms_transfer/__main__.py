

import os
import argparse
import sys
import tempfile
from pathlib import Path
from huggingface_hub import snapshot_download, HfApi
from modelscope.hub.api import HubApi
from modelscope.hub.constants import ModelVisibility
from dotenv import load_dotenv

def main():
    parser = argparse.ArgumentParser(description="Transfer a Hugging Face model or dataset to ModelScope.")
    parser.add_argument("hf_repo_id", type=str, help="The Hugging Face model or dataset ID (e.g., 'bert-base-uncased' or 'stanfordnlp/imdb').")
    parser.add_argument("--private", action="store_true", help="Make the ModelScope repository private (default is public).")
    parser.add_argument("--ms-token", type=str, help="Your ModelScope access token.")
    parser.add_argument("--ms-name", type=str, help="Your ModelScope username.")
    parser.add_argument("--ms-repo-name", type=str, help="The desired ModelScope repository name. If not provided, it will be derived from the Hugging Face repo ID.")
    args = parser.parse_args()

    hf_repo_id = args.hf_repo_id
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

    # Check repo type
    hf_api = HfApi()
    try:
        repo_info = hf_api.repo_info(repo_id=hf_repo_id, repo_type='dataset')
        repo_type = 'dataset'
    except Exception as e:
        try:
            repo_info = hf_api.repo_info(repo_id=hf_repo_id, repo_type='model')
            repo_type = 'model'
        except Exception as e:
            print(f"Error getting repo info from Hugging Face: {e}")
            sys.exit(1)

    api = HubApi()
    api.login(ms_token)
    ms_repo_name = args.ms_repo_name if args.ms_repo_name else hf_repo_id.split('/')[-1]
    ms_repo_id = f"{ms_username}/{ms_repo_name}"

    try:
        if repo_type == 'model':
            api.create_model(
                model_id=ms_repo_id,
                visibility=ModelVisibility.PRIVATE if is_private else ModelVisibility.PUBLIC,
            )
        elif repo_type == 'dataset':
            api.create_dataset(
                dataset_name=ms_repo_name,
                namespace=ms_username,
                visibility=ModelVisibility.PRIVATE if is_private else ModelVisibility.PUBLIC,
            )
        print(f"Successfully created {repo_type} repository '{ms_repo_id}' on ModelScope.")
    except Exception as e:
        if "already exists" in str(e):
            print(f"{repo_type.capitalize()} repository '{ms_repo_id}' already exists on ModelScope.")
        else:
            print(f"Error creating {repo_type} repository on ModelScope: {e}")
            sys.exit(1)


    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"Downloading {repo_type} '{hf_repo_id}' from Hugging Face...")
        try:
            snapshot_download(
                repo_id=hf_repo_id,
                repo_type=repo_type,
                local_dir=tmpdir,
                local_dir_use_symlinks=False
            )
            print("Download complete.")
        except Exception as e:
            print(f"Error downloading {repo_type} from Hugging Face: {e}")
            sys.exit(1)

        print(f"Uploading {repo_type} to ModelScope repository '{ms_repo_id}'...")
        try:
            api.upload_folder(
                repo_id=ms_repo_id,
                repo_type=repo_type,
                folder_path=tmpdir,
                commit_message="Initial commit from Hugging Face"
            )
            print("Upload complete.")
        except Exception as e:
            print(f"Error uploading {repo_type} to ModelScope: {e}")
            sys.exit(1)

    print("\nTransfer successful!")
    print(f"{repo_type.capitalize()} available at: https://modelscope.cn/{repo_type}s/{ms_repo_id}")


if __name__ == "__main__":
    main()

