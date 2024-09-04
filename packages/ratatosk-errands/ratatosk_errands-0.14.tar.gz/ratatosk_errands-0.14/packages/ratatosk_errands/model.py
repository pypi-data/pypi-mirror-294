from typing import List

from pydantic import BaseModel


class ModelInstructions(BaseModel):
    pass


class DiffusionInstructions(ModelInstructions):
    prompt: str
    image_identifier: str
    negative_prompt: str | None = None
    num_inference_steps: int | None = None
    guidance_scale: float | None = None


class ImageToImageInstructions(DiffusionInstructions):
    base_image_identifier: str


class TextToImageInstructions(DiffusionInstructions):
    width: int | None = None
    height: int | None = None


class ChatInstructions(ModelInstructions):
    prompt: str
    history: List[str] = []
    system_instructions: str | None = None
    max_new_tokens: int | None = None
    temperature: float | None = None
    repetition_penalty: float | None = None


class Errand(BaseModel):
    instructions: ModelInstructions
    origin: str
    destination: str
    errand_identifier: str
    timestamp: float


class ModelResult(BaseModel):
    pass


class DiffusionResult(ModelResult):
    image_identifier: str


class ChatResult(ModelResult):
    message: str


class Reply(BaseModel):
    errand: Errand
    result: ModelResult
