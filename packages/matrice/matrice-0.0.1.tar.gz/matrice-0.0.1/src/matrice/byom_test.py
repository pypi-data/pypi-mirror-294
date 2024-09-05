import os
import subprocess
REPO_CONFIGS_AND_INFO_FOLDER_PATH = "/models_configs"

def run(python_path, model_family_info_path , model_info_path, config_path):
    if "deploy" not in python_path:
        command = ['python', python_path, 'Testing', model_family_info_path, model_info_path, config_path]
    else:
        local_port = 8000
        command = ['python', python_path, 'Testing', local_port ,model_family_info_path, model_info_path, config_path]
    try:
        subprocess.run(command)
    except Exception as e:
        print(f"Error in with {command}. Error is: {e}")

def main(repo_configs_and_info_folder_path):

    models_info_paths = []
    train_path = None
    export_config_paths = []

    for filename in os.listdir(repo_configs_and_info_folder_path):
        file_path = os.path.join(repo_configs_and_info_folder_path, filename)
        if filename.endswith(".json"):
            if filename == "family_info.json":
                model_family_info_path = file_path
            elif filename == 'train-config.json':
                train_config_path = file_path
            elif filename.startswith("export-"):
                export_config_paths.append(file_path)
            else:
                models_info_paths.append(file_path)

    for model_info_path in models_info_paths:
        
        run("train.py", model_family_info_path, model_info_path, train_config_path)
        run("eval.py", model_family_info_path, model_info_path, "eval")
        run("deploy.py", model_family_info_path, model_info_path, "deploy")
        for export_config_path in export_config_paths:
            run("export.py", model_family_info_path, model_info_path, export_config_path)

if __name__ == "__main__":
    main(REPO_CONFIGS_AND_INFO_FOLDER_PATH)
