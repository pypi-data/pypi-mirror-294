from typing import List

from pydantic import BaseModel


class DiffusionInstructions(BaseModel):
    prompt: str
    negative_prompt: str = ""
    num_inference_steps: int = 28
    guidance_scale: float = 7.0


class ImageToImageInstructions(DiffusionInstructions):
    base_image_identifier: str


class TextToImageInstructions(DiffusionInstructions):
    width: int = 1024
    height: int = 1024


class ChatInstructions(BaseModel):
    prompt: str
    history: List[str] = []
    system_instructions: str = ""
    max_new_tokens: int = 750
    temperature: float = 0.8
    repetition_penalty: float = 1.1


class Errand(BaseModel):
    instructions: (TextToImageInstructions |
                   ImageToImageInstructions |
                   ChatInstructions)
    origin: str
    destination: str
    identifier: str
    timestamp: float
