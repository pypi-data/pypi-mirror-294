from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Any, List
from datetime import datetime
from uuid import uuid4

class Prompt(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    text: str
    version: str
    created_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(default_factory=datetime.now)

class ModelVersion(BaseModel):
    version: str
    first_used: datetime = Field(default_factory=datetime.now)
    last_used: datetime = Field(default_factory=datetime.now)
    run_count: int = 0

class Model(BaseModel):
    name: str
    versions: Dict[str, ModelVersion] = Field(default_factory=dict)

class Run(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)
    metrics: Dict[str, Any]
    details: Dict[str, Any]
    num_samples: int
    model_info: Dict[str, Any]
    prompt_info: Dict[str, Any]

    model_config = ConfigDict(protected_namespaces=())

class Experiment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    description: str = ""
    created_at: datetime = Field(default_factory=datetime.now)
    runs: List[Run] = Field(default_factory=list)
    prompts: Dict[str, Prompt] = Field(default_factory=dict)
    models: Dict[str, Model] = Field(default_factory=dict)