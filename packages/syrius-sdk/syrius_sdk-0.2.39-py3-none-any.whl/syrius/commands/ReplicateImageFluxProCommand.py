from typing import Literal
from syrius.commands.LoopInputCommand import loopType
from syrius.commands.abstract import AbstractCommand, Command


class ReplicateFluxProCommand(Command):
    id: int = 51
    prompt: str | AbstractCommand | loopType
    aspect_ratio: Literal["1:1", "16:9", "2:3", "3:2", "4:5", "5:4", "9:16"] | AbstractCommand | loopType = "1:1"
    guidance_scale: int | AbstractCommand | loopType = 3
    interval: int | AbstractCommand | loopType = 2
    safety_tolerance: int | AbstractCommand | loopType = 2
    output_format: str | AbstractCommand | loopType = "png"
    quality: int | AbstractCommand | loopType = 80
    num_inference_steps: int | AbstractCommand | loopType = 25
    api_key: str | AbstractCommand | loopType