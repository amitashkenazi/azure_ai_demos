from huggingface_hub import snapshot_download
model_id="mistralai/Mistral-7B-v0.1"
snapshot_download(repo_id=model_id, local_dir="mistralai-Mistral-7B-v0.1",
                  local_dir_use_symlinks=False, revision="main")