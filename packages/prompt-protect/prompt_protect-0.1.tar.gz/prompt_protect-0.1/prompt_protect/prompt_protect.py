import os
from pathlib import Path
from transformers import PreTrainedModel, PretrainedConfig
import skops.hub_utils
from sklearn.pipeline import Pipeline
from skops.io import dump, load, get_untrusted_types
from skops.hub_utils import download


# Define the configuration for the Prompt Protect model
class PromptProtectModelConfig(PretrainedConfig):
    model_type = "prompt_protect_model"

# Define the Prompt Protect model class that wraps a scikit-learn model and vectorizer
class PromptProtectModel(PreTrainedModel):
    config_class = PromptProtectModelConfig

    def __init__(self, config, model=None):
        super().__init__(config)
        self.model = model
        
    def forward(self, input_texts) -> int:
        if not isinstance(input_texts, list):
            input_texts = [input_texts]
        
        # Predict using the model
        predictions = self.model.predict(input_texts)[0]
        return predictions

    @classmethod
    def from_pretrained(cls, model_path="./thevgergroup/"):

        # If the model path does not end with .skops, download the model
        if not model_path.endswith(".skops"):
            
            if not os.path.exists(model_path):
                os.makedirs(model_path)
            
            existing_files = os.listdir(model_path)    
            
            if "prompt_protect_model.skops" not in existing_files:
                if len(existing_files) > 0:
                    raise ValueError("The model path must be empty or contain a prompt_protect_model.skops file")    
                download(dst=model_path, repo_id='thevgergroup/prompt_protect')
                
            model_path = os.path.join(model_path, "prompt_protect_model.skops")
        
        config = PromptProtectModelConfig()
        gut = get_untrusted_types(file=model_path)
        model = load(file=model_path, trusted=gut)
        return cls(config, model=model)

    def save_pretrained(self, save_directory="."):
        model_path = os.path.join(save_directory, "thevgergroup")
        os.makedirs(model_path, exist_ok=True)
        
        dump(self.model, file=os.path.join(model_path, "prompt_protect_model.skops"))
        
        


