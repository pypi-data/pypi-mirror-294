import json
import os
from typing import Dict, Any, List
from datetime import datetime
import hashlib
from .models import Experiment, Run, Prompt, Model, ModelVersion

class ExperimentManager:
    def __init__(self, storage_path: str = "experiments"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)

    def create_experiment(self, name: str, description: str = "") -> str:
        experiment = Experiment(name=name, description=description)
        self._save_experiment(experiment)
        return experiment.id

    def add_run(self, experiment_id: str, run_data: Dict[str, Any]) -> str:
        experiment = self._load_experiment(experiment_id)

        # Handle prompt versioning
        prompt_info = run_data.get("prompt_info", {})
        prompt_text = prompt_info.get("text", "")
        prompt = self._get_or_create_prompt(experiment, prompt_text)
        run_data["prompt_info"] = {
            "id": prompt.id,
            "text": prompt.text,
            "version": prompt.version,
            "created_at": prompt.created_at.isoformat(),
            "modified_at": prompt.modified_at.isoformat()
        }

        # Handle model versioning
        model_info = run_data.get("model_info", {})
        model_name = model_info.get("name", "")
        model_version = model_info.get("version", "")
        self._update_model_info(experiment, model_name, model_version)

        run = Run(**run_data)
        experiment.runs.append(run)
        self._save_experiment(experiment)
        return run.id

    def _get_or_create_prompt(self, experiment: Experiment, prompt_text: str) -> Prompt:
        prompt_hash = hashlib.md5(prompt_text.encode()).hexdigest()
        
        if prompt_hash not in experiment.prompts:
            version = f"1.0.{len(experiment.prompts)}"
            prompt = Prompt(text=prompt_text, version=version)
            experiment.prompts[prompt_hash] = prompt
        else:
            prompt = experiment.prompts[prompt_hash]
            prompt.modified_at = datetime.now()
        
        return prompt

    def _update_model_info(self, experiment: Experiment, model_name: str, model_version: str):
        if model_name not in experiment.models:
            experiment.models[model_name] = Model(name=model_name)
        
        model = experiment.models[model_name]
        if model_version not in model.versions:
            model.versions[model_version] = ModelVersion(version=model_version)
        
        version_info = model.versions[model_version]
        version_info.last_used = datetime.now()
        version_info.run_count += 1

    def get_experiment(self, experiment_id: str) -> Experiment:
        return self._load_experiment(experiment_id)

    def get_all_experiments(self) -> List[Experiment]:
        experiments = []
        for filename in os.listdir(self.storage_path):
            if filename.endswith(".json"):
                experiments.append(self._load_experiment(filename[:-5]))  # Remove .json extension
        return experiments

    def get_prompt_history(self, experiment_id: str) -> List[Prompt]:
        experiment = self._load_experiment(experiment_id)
        return list(experiment.prompts.values())

    def get_model_history(self, experiment_id: str) -> Dict[str, Model]:
        experiment = self._load_experiment(experiment_id)
        return experiment.models

    def _save_experiment(self, experiment: Experiment):
        filename = f"{experiment.id}.json"
        with open(os.path.join(self.storage_path, filename), "w") as f:
            json.dump(experiment.model_dump(), f, indent=2, default=self._json_serializer)

    @staticmethod
    def _json_serializer(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")

    def _load_experiment(self, experiment_id: str) -> Experiment:
        filename = f"{experiment_id}.json"
        with open(os.path.join(self.storage_path, filename), "r") as f:
            data = json.load(f)
        return Experiment.model_validate(data)
