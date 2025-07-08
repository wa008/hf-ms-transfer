import os
import argparse
import sys
import tempfile
from pathlib import Path
from datetime import datetime
from huggingface_hub import snapshot_download, HfApi
from modelscope.hub.api import HubApi
from modelscope.hub.constants import ModelVisibility
from dotenv import load_dotenv

def transfer_repo(hf_repo_id, ms_username, api, is_private, keep_dataset_infos, ms_repo_name=None):
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
            print(f"Error getting repo info for {hf_repo_id} from Hugging Face: {e}")
            return

    base_repo_name = ms_repo_name if ms_repo_name else hf_repo_id.split('/')[-1]
    ms_repo_id = f"{ms_username}/{base_repo_name}"

    try:
        if repo_type == 'model':
            api.create_model(
                model_id=ms_repo_id,
                visibility=ModelVisibility.PRIVATE if is_private else ModelVisibility.PUBLIC,
            )
        elif repo_type == 'dataset':
            api.create_dataset(
                dataset_name=base_repo_name,
                namespace=ms_username,
                visibility=ModelVisibility.PRIVATE if is_private else ModelVisibility.PUBLIC,
            )
        print(f"Successfully created {repo_type} repository '{ms_repo_id}' on ModelScope.")
    except Exception as e:
        if "该名称已被注册使用" in str(e):
            if ms_repo_name:
                print(f"{repo_type.capitalize()} repository '{ms_repo_id}' already exists on ModelScope. Please choose a different name.")
                return
            else:
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                base_repo_name = f"{base_repo_name}_{timestamp}"
                ms_repo_id = f"{ms_username}/{base_repo_name}"
                print(f"Repository exists, creating a new one with timestamp: {ms_repo_id}")
                try:
                    if repo_type == 'model':
                        api.create_model(
                            model_id=ms_repo_id,
                            visibility=ModelVisibility.PRIVATE if is_private else ModelVisibility.PUBLIC,
                        )
                    elif repo_type == 'dataset':
                        api.create_dataset(
                            dataset_name=base_repo_name,
                            namespace=ms_username,
                            visibility=ModelVisibility.PRIVATE if is_private else ModelVisibility.PUBLIC,
                        )
                    print(f"Successfully created {repo_type} repository '{ms_repo_id}' on ModelScope.")
                except Exception as e2:
                    print(f"Error creating timestamped {repo_type} repository on ModelScope: {e2}")
                    return
        else:
            print(f"Error creating {repo_type} repository on ModelScope: {e}")
            return

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
            return

        if repo_type == 'dataset' and not keep_dataset_infos:
            dataset_infos_path = Path(tmpdir) / 'dataset_infos.json'
            if dataset_infos_path.exists():
                print("Removing dataset_infos.json...")
                dataset_infos_path.unlink()

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
            return

    print(f"\nTransfer successful for {hf_repo_id}!")
    print(f"{repo_type.capitalize()} available at: https://modelscope.cn/{repo_type}s/{ms_repo_id}")


def main():
    parser = argparse.ArgumentParser(description="Transfer Hugging Face models or datasets to ModelScope.")
    parser.add_argument("hf_repo_ids", type=str, help="The Hugging Face model or dataset IDs, separated by commas (e.g., 'bert-base-uncased,stanfordnlp/imdb').")
    parser.add_argument("--private", action="store_true", help="Make the ModelScope repositories private (default is public).")
    parser.add_argument("--ms-token", type=str, help="Your ModelScope access token.")
    parser.add_argument("--ms-name", type=str, help="Your ModelScope username.")
    parser.add_argument("--ms-repo-name", type=str, help="The desired repository name on ModelScope.")
    parser.add_argument("--keep-dataset-infos", action="store_true", help="Keep the dataset_infos.json file.")
    args = parser.parse_args()

    hf_repo_ids = [repo_id.strip() for repo_id in args.hf_repo_ids.split(',')]
    is_private = args.private
    keep_dataset_infos = args.keep_dataset_infos
    ms_repo_name = args.ms_repo_name

    if len(hf_repo_ids) > 1 and ms_repo_name:
        raise ValueError("Cannot provide a custom ModelScope repository name (--ms-repo-name) when transferring multiple Hugging Face repositories.")

    # Load .env file from current directory or home directory
    load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))

    ms_token = args.ms_token if args.ms_token else os.getenv("ms_token")
    ms_username = args.ms_name if args.ms_name else os.getenv("ms_name")

    if not ms_token:
        raise ValueError("ModelScope token not found. Please provide it via --ms-token or in your .env file (key: ms_token).")

    if not ms_username:
        raise ValueError("ModelScope username not found. Please provide it via --ms-name or in your .env file (key: ms_name).")

    api = HubApi()
    api.login(ms_token)

    for hf_repo_id in hf_repo_ids:
        print(f"\n----- Starting transfer for {hf_repo_id} -----")
        transfer_repo(hf_repo_id, ms_username, api, is_private, keep_dataset_infos, ms_repo_name)
        print(f"----- Finished transfer for {hf_repo_id} -----")


if __name__ == "__main__":
    main()
