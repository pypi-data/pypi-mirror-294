from typing import List

from pydantic import BaseModel


class DiffusionInstructions(BaseModel):
    prompt: str
    negative_prompt: str | None = None
    num_inference_steps: int | None = None
    guidance_scale: float | None = None


class ImageToImageInstructions(DiffusionInstructions):
    base_image_identifier: str


class TextToImageInstructions(DiffusionInstructions):
    width: int | None = None
    height: int | None = None


class ChatInstructions(BaseModel):
    prompt: str
    history: List[str] = []
    system_instructions: str | None = None
    max_new_tokens: int | None = None
    temperature: float | None = None
    repetition_penalty: float | None = None


class Errand(BaseModel):
    instructions: (TextToImageInstructions |
                   ImageToImageInstructions |
                   ChatInstructions)
    origin: str
    destination: str
    identifier: str
    timestamp: float
