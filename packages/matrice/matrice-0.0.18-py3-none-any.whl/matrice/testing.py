import os
import requests
import shutil
import zipfile
import tarfile
import yaml
import math
from pycocotools.coco import COCO
import json
from pydantic import BaseModel
from typing import List
from PIL import Image, ImageDraw
from io import BytesIO

from matrice.session import Session

class SplitMetricStruct(BaseModel):
    splitType: str
    metricName: str
    metricValue: float

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class TestingActionTracker():

    def __init__(self, model_family_info_path , model_info_path, config_path):

        self.logs = []
        self.testing_logs_folder_path = "./testing_logs"
        os.makedirs(self.testing_logs_folder_path, exist_ok=True)

        self.model_family_info_path = model_family_info_path
        self.model_info_path = model_info_path
        self.config_path = config_path

        session = Session()
        self.rpc = session.rpc

        self.load_model_family_info()
        self.load_model_info()
        self.load_action_config()

        self.action_doc = self.mock_action_doc()
        self.action_details = self.action_doc['actionDetails']


        self.checkpoint_path, self.pretrained = self.get_checkpoint_path()
        self.prepare_dataset() # Download the dataset and prepare it for the action type in the specific format

    def get_main_action_logs_path(self):
        if "train" in self.config_path:
            return os.path.join(self.testing_logs_folder_path, "train.json")
        elif "export" in self.config_path:
            return os.path.join(self.testing_logs_folder_path, os.path.basename(self.config_path).replace("-config",""))
        elif "eval" in self.config_path:
            return os.path.join(self.testing_logs_folder_path, "eval.json")

    def log_to_json(self, file_path, payload):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        except json.JSONDecodeError:
            data = []
        data.append(payload)
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def add_logs(self, step, status, description):
        self.logs.append({"step" : step, "status" : status, "description" : description})
        self.log_to_json(self.get_main_action_logs_path(), {"step" : step, "status" : status, "description" : description})

    def log_decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
                self.add_logs(func.__name__, "SUCCESS", "SUCCESS")
                return result
            except Exception as e:
                print(f"ERROR occurred in: {func.__name__} : {str(e)}")
                self.add_logs(func.__name__, "ERROR", str(e))
                raise e
        return wrapper

    @log_decorator
    def load_model_family_info(self):
        with open(self.model_family_info_path) as f:
            self.model_family_info = json.load(f)
        self.input_type = self.model_family_info["modelInputs"].lower()
        self.output_type = self.model_family_info["modelOutputs"].lower()
        self.models_family_name = self.model_family_info["modelFamily"]

    @log_decorator
    def load_model_info(self):
        with open(self.model_info_path) as f:
            self.model_info = json.load(f)
        self.model_key = self.model_info["modelKey"]
        self.model_name = self.model_info["modelName"]

    @log_decorator
    def mock_action_doc(self ):
        api_url = f"/v1/system/get_dataset_url?inputType={self.input_type}&outputType={self.output_type}"
        response = self.rpc.get(
            path=api_url,
            params={
                "inputType": self.input_type,
                "outputType": self.output_type
            }
        )
        if response and 'data' in response:
            mock_dataset = response['data']
        else:
            raise ValueError("Invalid response from the API call")

        action_details = {
        '_idModel': 'mocked_model_id',
        'runtimeFramework': 'Pytorch',
        'datasetVersion': 'v1.0',
        'dataset_url': mock_dataset,
        'project_type': self.output_type,
        'input_type': self.input_type,
        'output_type': self.output_type
        }
        # Store _idModel as an instance variable
        self._idModel = action_details['_idModel']
        return {
            'actionDetails': action_details,
            'action': self.action_type,
            'serviceName': 'mocked_service_name',
            '_idProject': 'mocked_project_id'
        }


    @log_decorator
    def get_checkpoint_path(self):
        checkpoint_dir = "./checkpoints"
        # Ensure the checkpoints directory exists
        if not os.path.exists(checkpoint_dir):
            os.makedirs(checkpoint_dir)
            print(f"Created checkpoint directory: {checkpoint_dir}")
            return None, False  # No checkpoints available
        # List all files in the checkpoints directory
        checkpoint_files = [f for f in os.listdir(checkpoint_dir) if f.endswith('.pt')]
        if not checkpoint_files:
            print("No checkpoint files found in the checkpoints directory.")
            return None, False
        # If there are multiple checkpoints, you might want to choose the most recent one
        # For simplicity, we're just choosing the first one here
        checkpoint_path = os.path.join(checkpoint_dir, checkpoint_files[0])
        print(f"Found checkpoint: {checkpoint_path}")
        return checkpoint_path, True


    @log_decorator
    def load_action_config(self):
        self.model_config = {}

        if "train" in self.config_path and self.config_path.endswith('-config.json'):
            self.action_type = "model_train"
            with open(self.config_path, 'r') as config_file:
                self.config_file = json.load(config_file)
            print(f"Loaded train config for model {self.model_name}: {self.config_file}")
            for config in self.config_file.get('actionConfig', []):
                key_name = config.get('keyName')
                default_value = config.get('defaultValue')
                if key_name and default_value is not None:
                    self.model_config[key_name] = self.cast_value(config.get('valueType'), default_value)
            print(f"Model config: {self.model_config}")

        elif "export" in self.config_path and self.config_path.endswith('-config.json'):
            self.action_type = "model_export"
            with open(self.config_path, 'r') as config_file:
                self.config_file = json.load(config_file)
            self.action_details['exportFormats'] = [self.config_file["exportFormat"]]
            for config in self.config_file.get('actionConfig', []):
                key_name = config.get('keyName')
                default_value = config.get('defaultValue')
                if key_name and default_value is not None:
                    self.model_config[key_name] = self.cast_value(config.get('valueType'), default_value)
            print(f"Model config: {self.model_config}")
            print(f"Loaded export config for format {self.action_details['exportFormats']}")

        elif "eval" in self.config_path:
            self.action_type = "model_eval"
            self.model_config["split_types"] = ["vel", "test"]
            print(f"Model config: {self.model_config}")

        else:
            raise Exception("Couldn't load action config, Make sure config path is one of [train-config.json, export-export_format-config, eval]")

    def cast_value(self, value_type, value):
        if value_type == "int32":
            return int(value)
        elif value_type == "float32":
            return float(value)
        elif value_type == "string":
            return str(value)
        elif value_type == 'bool':
            return bool(value)
        else:
            return value

    def update_status(self, stepCode, status, status_description):
        print(f"Mock update status: {stepCode}, {status}, {status_description}")
        self.add_logs(stepCode, status, status_description)

    @log_decorator
    def upload_checkpoint(self, checkpoint_path, model_type="trained"):
        print(f"Mock upload checkpoint: {checkpoint_path}, {model_type}")
        file_path, ext = os.path.splitext(checkpoint_path)
        if model_type == "trained":
            new_name = os.path.join(self.testing_logs_folder_path, "model_" + model_type + ext)
        elif model_type == "exported":
            new_name = os.path.join(self.testing_logs_folder_path,"model_" + self.action_details['exportFormats'][0] + model_type + ext)
        shutil.move(checkpoint_path, new_name)
        return True

    @log_decorator
    def download_model(self, model_path, model_type = "trained", runtime_framework = ""):
        print(f"Mock download model to: {model_path}, {model_type}")
        file_path, ext = os.path.splitext(model_path)
        if model_type == "trained":
            local_model_file = [path for path in os.listdir(self.testing_logs_folder_path) if path.endswith(f"{model_type}{ext}")][0]
        elif model_type == "exported":
            local_model_file = [path for path in os.listdir(self.testing_logs_folder_path) if path.endswith(f"{model_type}{ext}")][0]
            
        local_model_file = self.testing_logs_folder_path + "/" + local_model_file
        print(f"Local model file: {local_model_file}")
        # TODO: adding the exportFormat into considration for loading the saved model checkpoint path, by including runtime_framework
        with open(local_model_file, 'rb') as src, open(model_path, 'wb') as dest:
            dest.write(src.read())
        return True

    @log_decorator
    def get_job_params(self):
        dataset_path = 'dataset'
        model_config = dotdict({
        "dataset_path" : dataset_path,
        'data': f"workspace/{dataset_path}/images",
        'arch': self.model_key,
        'pretrained': self.pretrained,
        'dataset_path': dataset_path,
        'model_key': self.model_key,
        'model_name' : self.model_name,
        'checkpoint_path':self.checkpoint_path
        })

        # Create a new dictionary with combined content, adding only non-existing keys from dict2
        self.model_config = dotdict({**model_config, **{k: v for k, v in self.model_config.items() if k not in model_config}})
        return self.model_config

    @log_decorator
    def add_index_to_category(self, indexToCat):
        print(f"Mock add index to category: {indexToCat}")
        file_path = os.path.join(self.testing_logs_folder_path, "index_to_category.json")
        with open(file_path, 'w') as file:
            json.dump(indexToCat, file, indent=4)
        return indexToCat

    @log_decorator
    def get_index_to_category(self, is_exported=False):
        file_path = os.path.join(self.testing_logs_folder_path, "index_to_category.json")
        with open(file_path, 'r') as file:
            return json.load(file)

    @log_decorator
    def log_epoch_results(self, epoch, epoch_result_list: List[SplitMetricStruct]):
        epoch_result_list = self.validate_metrics_structure(epoch_result_list)
        epoch_result_list = self.round_metrics(epoch_result_list)
        model_log_payload = {"epoch": epoch, "epochDetails": epoch_result_list,}

        file_path = os.path.join(self.testing_logs_folder_path, "epochs_results.json")
        self.log_to_json(file_path, model_log_payload)

    @log_decorator
    def save_evaluation_results(self, list_of_result_dicts: List[SplitMetricStruct]):
        list_of_result_dicts = self.validate_metrics_structure(list_of_result_dicts)
        print(f"Mock save evaluation results: {list_of_result_dicts}")
        file_path = os.path.join(self.testing_logs_folder_path, "evaluation_results.json")
        with open(file_path, 'w') as file:
            json.dump(list_of_result_dicts, file, indent=4)

    def validate_metrics_structure(self, metrics_list: List[SplitMetricStruct]):
        return [SplitMetricStruct.model_validate(x).model_dump() for x in metrics_list]

    def round_metrics(self, epoch_result_list):
        for metric in epoch_result_list:
            if metric["metricValue"] == None or math.isinf(metric["metricValue"]) or math.isnan(metric["metricValue"]):
                metric["metricValue"] = 0
            metric["metricValue"] = round(metric["metricValue"], 4)
            if metric["metricValue"] == 0:
                metric["metricValue"] = 0.0001
        return epoch_result_list

    @log_decorator
    def prepare_dataset(self):
        dataset_images_dir = 'workspace/dataset'

        if os.path.exists(dataset_images_dir):
            print(f"Dataset directory {dataset_images_dir} already exists. Skipping download and preparation.")
        else:
            dataset_url = self.action_details.get('dataset_url')
            project_type = self.action_details.get('project_type')
            input_type = self.action_details.get('input_type')
            output_type = self.action_details.get('output_type')

            print(f"Preparing dataset from {dataset_url} for project type {project_type} with input type {input_type} and output type {output_type}")

            dataset_dir = 'workspace/dataset'
            os.makedirs(dataset_dir, exist_ok=True)
            self.download_and_extract_dataset(dataset_url, dataset_dir)

            # Prepare the dataset according to the project type
            if project_type == 'classification':
                self.prepare_classification_dataset(dataset_dir)

            elif project_type == 'detection':
                if "yolo" in self.model_name.lower():
                    self.prepare_yolo_dataset(dataset_dir)
                else:
                    self.prepare_detection_dataset(dataset_dir)
            else:
                print(f"Unsupported project type: {project_type}")


    def download_and_extract_dataset(self, dataset_url, dataset_dir):
        # Extract the file name from the URL
        file_name = os.path.basename(dataset_url)
        local_file_path = os.path.join(dataset_dir, file_name)

        try:
            # Download the file
            with requests.get(dataset_url, stream=True) as r:
                r.raise_for_status()

                print(f"Response status code: {r.status_code}")
                print(f"Response headers: {r.headers}")

                content_type = r.headers.get('Content-Type', 'Unknown')
                print(f"Content-Type: {content_type}")

                # Save the file
                with open(local_file_path, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)

            print(f"File downloaded successfully from {dataset_url}")
            print(f"Saved as: {local_file_path}")

            # Extract the file based on its extension
            if file_name.endswith('.zip'):
                with zipfile.ZipFile(local_file_path, 'r') as zip_ref:
                    zip_ref.extractall(dataset_dir)
                print("Zip file extracted successfully")
            elif file_name.endswith('.tar.gz') or file_name.endswith('.tgz'):
                with tarfile.open(local_file_path, "r:gz") as tar:
                    tar.extractall(path=dataset_dir)
                print("Tar.gz file extracted successfully")
            else:
                print(f"Unsupported file format: {file_name}")
                return

            # Remove the compressed file after extraction
            os.remove(local_file_path)
            print(f"Removed the compressed file: {local_file_path}")

        except requests.exceptions.RequestException as e:
            print(f"Error downloading dataset from {dataset_url}: {e}")
        except (zipfile.BadZipFile, tarfile.TarError) as e:
            print(f"Error extracting dataset from {local_file_path}: {e}")

    def get_file_extension(self, content_type):
        content_type = content_type.lower()
        if 'zip' in content_type:
            return '.zip'
        elif 'gzip' in content_type or 'x-gzip' in content_type:
            return '.gz'
        elif 'tar' in content_type:
            return '.tar'
        elif 'octet-stream' in content_type:
            return ''  # Binary file, no specific extension
        else:
            return ''  # Unknown type, no extension

    def prepare_classification_dataset(self, dataset_dir):
        print("Preparing classification dataset...")

        # Locate the vehicle-c10-20 directory
        sub_dirs = [os.path.join(dataset_dir, d) for d in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, d))]
        if len(sub_dirs) != 1:
            raise ValueError("Expected a single subdirectory in the dataset directory")
        vehicle_dir = sub_dirs[0]
        print(f"Main Sub directory: {vehicle_dir}")

        images_dir = os.path.join(dataset_dir, 'images')
        os.makedirs(images_dir, exist_ok=True)
        print(f"Images directory: {images_dir}")

        class_names = set()
        split_info = {}  # To keep track of which images belong to which split

        # Iterate through train, val, and test splits
        for split in ['train', 'val', 'test']:
            split_dir = os.path.join(vehicle_dir, split)
            dst_split_dir = os.path.join(images_dir, split)
            os.makedirs(dst_split_dir, exist_ok=True)
            split_info[split] = {}

            for class_name in os.listdir(split_dir):
                class_dir = os.path.join(split_dir, class_name)
                if os.path.isdir(class_dir):
                    class_names.add(class_name)
                    dst_class_dir = os.path.join(dst_split_dir, class_name)
                    os.makedirs(dst_class_dir, exist_ok=True)

                    # Copy images and keep track of which split they belong to
                    for img in os.listdir(class_dir):
                        src_path = os.path.join(class_dir, img)
                        dst_path = os.path.join(dst_class_dir, img)
                        shutil.copy2(src_path, dst_path)

                        if class_name not in split_info[split]:
                            split_info[split][class_name] = []
                        split_info[split][class_name].append(dst_path)

        # Retrieve class names and count
        self.num_classes = len(class_names)
        self.class_names = list(class_names)

        print(f"Number of classes: {self.num_classes}")
        print(f"Class names: {self.class_names}")

        # Optionally, you can save the split information for later use
        # For example, you could save it as a JSON file
        with open(os.path.join(dataset_dir, 'split_info.json'), 'w') as f:
            json.dump(split_info, f, indent=4)

    def prepare_detection_dataset(self, dataset_dir):
        print("Preparing detection dataset...")

        # Find the downloaded folder
        contents = os.listdir(dataset_dir)
        downloaded_dirs = [d for d in contents if os.path.isdir(os.path.join(dataset_dir, d))
                        and d not in ('images', 'annotations')]

        if not downloaded_dirs:
            print("No suitable subdirectory found in the dataset directory.")
            return

        if len(downloaded_dirs) > 1:
            print(f"Multiple subdirectories found: {downloaded_dirs}. Using the first one.")

        downloaded_dir = os.path.join(dataset_dir, downloaded_dirs[0])
        print(f"Found downloaded directory: {downloaded_dir}")

        # Source paths
        src_images_dir = os.path.join(downloaded_dir, 'images')
        src_annotations_dir = os.path.join(downloaded_dir, 'annotations')

        # Destination paths
        dst_images_dir = os.path.join(dataset_dir, 'images')
        dst_annotations_dir = os.path.join(dataset_dir, 'annotations')

        # Move images folder
        if os.path.exists(src_images_dir):
            if os.path.exists(dst_images_dir):
                shutil.rmtree(dst_images_dir)
            shutil.move(src_images_dir, dst_images_dir)
            print(f"Moved images folder to {dst_images_dir}")
        else:
            print("Images folder not found in the downloaded directory")

        # Move annotations folder
        if os.path.exists(src_annotations_dir):
            if os.path.exists(dst_annotations_dir):
                shutil.rmtree(dst_annotations_dir)
            shutil.move(src_annotations_dir, dst_annotations_dir)
            print(f"Moved annotations folder to {dst_annotations_dir}")
        else:
            print("Annotations folder not found in the downloaded directory")

        # Remove the downloaded folder if it's empty
        if os.path.exists(downloaded_dir) and not os.listdir(downloaded_dir):
            os.rmdir(downloaded_dir)
            print(f"Removed empty downloaded folder: {downloaded_dir}")

        print("Dataset preparation completed.")


    def convert_bbox_to_yolo(self, size, box):
        dw = 1. / size[0]
        dh = 1. / size[1]
        x = (box[0] + box[2] / 2.0) * dw
        y = (box[1] + box[3] / 2.0) * dh
        w = box[2] * dw
        h = box[3] * dh
        return (x, y, w, h)

    def create_data_yaml(self, dataset_dir, class_names):
        data_yaml = {
            'path': dataset_dir,
            'train': 'images/train2017',
            'val': 'images/val2017',
            'test': 'images/test2017',
            'names': class_names
        }

        yaml_path = os.path.join(dataset_dir, 'data.yaml')
        with open(yaml_path, 'w') as file:
            yaml.dump(data_yaml, file, default_flow_style=False)

        print(f"Created data.yaml file at {yaml_path}")

    def prepare_yolo_dataset(self, dataset_dir):
        print("Preparing YOLO dataset...")

        # Create the 'datasets' directory one level above the 'workspace' directory
        root_dir = os.path.abspath(os.path.join(dataset_dir, os.pardir, os.pardir)) 
        datasets_dir = os.path.join(root_dir, 'datasets')
        if not os.path.exists(datasets_dir):
            os.makedirs(datasets_dir)

        # New directory structure: datasets/workspace/dataset                       #TODO : keep the directory as /workspace/dataset by commenting these lines  
        workspace_dir = os.path.basename(os.path.dirname(dataset_dir))
        new_workspace_dir = os.path.join(datasets_dir, workspace_dir)
        if not os.path.exists(new_workspace_dir):
            os.makedirs(new_workspace_dir)

        new_dataset_dir = os.path.join(new_workspace_dir, os.path.basename(dataset_dir))
        if os.path.exists(new_dataset_dir):
            shutil.rmtree(new_dataset_dir)
        shutil.move(dataset_dir, new_dataset_dir)
        dataset_dir = new_dataset_dir

        # Find the downloaded folder
        contents = os.listdir(dataset_dir)
        downloaded_dirs = [d for d in contents if os.path.isdir(os.path.join(dataset_dir, d))
                           and d not in ('images', 'annotations')]

        if not downloaded_dirs:
            print("No suitable subdirectory found in the dataset directory.")
            return

        if len(downloaded_dirs) > 1:
            print(f"Multiple subdirectories found: {downloaded_dirs}. Using the first one.")

        downloaded_dir = os.path.join(dataset_dir, downloaded_dirs[0])
        print(f"Found downloaded directory: {downloaded_dir}")

        # Source paths
        src_images_dir = os.path.join(downloaded_dir, 'images')
        src_annotations_dir = os.path.join(downloaded_dir, 'annotations')

        # Destination paths
        dst_images_dir = os.path.join(dataset_dir, 'images')
        dst_annotations_dir = os.path.join(dataset_dir, 'annotations')

        # Move images folder
        if os.path.exists(src_images_dir):
            if os.path.exists(dst_images_dir):
                shutil.rmtree(dst_images_dir)
            shutil.move(src_images_dir, dst_images_dir)
            print(f"Moved images folder to {dst_images_dir}")
        else:
            print("Images folder not found in the downloaded directory")

        # Move annotations folder
        if os.path.exists(src_annotations_dir):
            if os.path.exists(dst_annotations_dir):
                shutil.rmtree(dst_annotations_dir)
            shutil.move(src_annotations_dir, dst_annotations_dir)
            print(f"Moved annotations folder to {dst_annotations_dir}")
        else:
            print("Annotations folder not found in the downloaded directory")

        class_names = self.create_yolo_labels_from_mscoco_ann(dataset_dir, dst_images_dir, dst_annotations_dir, os.path.join(dst_annotations_dir, 'instances_train2017.json'))     
        self.create_yolo_labels_from_mscoco_ann(dataset_dir, dst_images_dir, dst_annotations_dir, os.path.join(dst_annotations_dir, 'instances_val2017.json')) 
        self.create_yolo_labels_from_mscoco_ann(dataset_dir, dst_images_dir, dst_annotations_dir, os.path.join(dst_annotations_dir, 'instances_test2017.json')) 
        
        # Create the data.yaml file
        self.create_data_yaml(dataset_dir, class_names)

        # Remove the downloaded folder if it's empty
        if os.path.exists(downloaded_dir) and not os.listdir(downloaded_dir):
            os.rmdir(downloaded_dir)
            print(f"Removed empty downloaded folder: {downloaded_dir}")
        print("Dataset preparation completed.")

    def create_yolo_labels_from_mscoco_ann(self,dataset_dir, dst_images_dir, dst_annotations_dir, annotation_file):
        # Convert annotations to YOLO format
            
            coco = COCO(annotation_file)
            img_dir = dst_images_dir
            ann_dir = os.path.join(dataset_dir, 'labels')
            if not os.path.exists(ann_dir):
                os.makedirs(ann_dir)

            # Subdirectories for labels
            label_dirs = {
                'train': os.path.join(ann_dir, 'train2017'),
                'val': os.path.join(ann_dir, 'val2017'),
                'test': os.path.join(ann_dir, 'test2017')
            }
            for dir_path in label_dirs.values():
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)

            # Get class names
            categories = coco.loadCats(coco.getCatIds())
            class_names = [category['name'] for category in categories]

            for img_id in coco.getImgIds():
                img_info = coco.loadImgs(img_id)[0]
                img_filename = img_info['file_name']
                img_width = img_info['width']
                img_height = img_info['height']

                ann_ids = coco.getAnnIds(imgIds=img_id)
                anns = coco.loadAnns(ann_ids)

                if 'train' in annotation_file:
                    label_path = os.path.join(label_dirs['train'], img_filename.replace('.jpg', '.txt'))
                elif 'val' in annotation_file:
                    label_path = os.path.join(label_dirs['val'], img_filename.replace('.jpg', '.txt'))
                elif 'test' in annotation_file:
                    label_path = os.path.join(label_dirs['test'], img_filename.replace('.jpg', '.txt'))

                with open(label_path, 'w') as f:
                    for ann in anns:
                        bbox = ann['bbox']
                        yolo_bbox = self.convert_bbox_to_yolo((img_width, img_height), bbox)
                        category_id = ann['category_id'] - 1
                        f.write(f"{category_id} {' '.join(map(str, yolo_bbox))}\n")

            if 'train' in annotation_file:
                return class_names

class ModelDownloadMock:
    def __init__(self):
        self.testing_logs_folder_path = "./testing_logs"

    def download_model(self, model_path, model_type = "trained", runtime_framework = ""):
        print(f"Mock download model to: {model_path}, {model_type}")
        file_path, ext = os.path.splitext(model_path)
        if model_type == "trained":
            local_model_file = [path for path in os.listdir(self.testing_logs_folder_path) if path.endswith(f"{model_type}{ext}")][0]
        elif model_type == "exported":
            local_model_file = [path for path in os.listdir(self.testing_logs_folder_path) if path.endswith(f"{model_type}{ext}")][0] 
        # TODO: adding the exportFormat into considration for loading the saved model checkpoint path, by including runtime_framework
        with open(local_model_file, 'rb') as src, open(model_path, 'wb') as dest:
            dest.write(src.read())
        return True
    
class TestingMatriceDeploy:
    def __init__(self, load_model, predict):
        
        self.logs = []
        self.testing_logs_folder_path = "./testing_logs"
        os.makedirs(self.testing_logs_folder_path, exist_ok=True)
        self.main_action_logs_path = os.path.join(self.testing_logs_folder_path, "deploy.json")

        self.model_downloader = ModelDownloadMock()
        self.load_model = lambda model_downloader : load_model(model_downloader)
        self.predict = lambda model, image : predict(model, image)
        self.model = None

        self.inference(self.create_image_bytes())

    def log_to_json(self, file_path, payload):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        except json.JSONDecodeError:
            data = []
        data.append(payload)
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def add_logs(self, step, status, description):
        self.logs.append({"step" : step, "status" : status, "description" : description})
        self.log_to_json(self.main_action_logs_path, {"step" : step, "status" : status, "description" : description})

    def log_decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
                self.add_logs(func.__name__, "SUCCESS", "SUCCESS")
                return result
            except Exception as e:
                print(f"ERROR occurred in: {func.__name__} : {str(e)}")
                self.add_logs(func.__name__, "ERROR", str(e))
                raise e
        return wrapper

    @log_decorator
    def load_predictor_model(self):
        self.model = self.load_model(self.model_downloader)
        
    @log_decorator
    def inference(self, image):
        if self.model is None:
            self.load_predictor_model()
        results = self.predict(self.model, image)
        return results, True
    
    def create_image_bytes(self):
        # Create a simple image with RGB mode and size 224x224
        image = Image.new('RGB', (224, 224), color = 'blue')
        draw = ImageDraw.Draw(image)
        draw.text((50, 100), "Test", fill='white')

        # Save the image to a BytesIO object
        image_bytes_io = BytesIO()
        image.save(image_bytes_io, format='JPEG')
        image_bytes_io.seek(0)

        return image_bytes_io.read()
