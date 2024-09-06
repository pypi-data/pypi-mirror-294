import torch
from craft_arch import CRAFT

def load_model(model_path):
    model = CRAFT()
    state_dict = torch.load(model_path)
    model.load_state_dict(state_dict, strict=False)
    model.eval()
    return model
