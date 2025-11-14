from pydantic import BaseModel
from typing import List

class BoundingBox(BaseModel):
    xmin: float
    ymin: float
    xmax: float
    ymax: float

class FruitInfo(BaseModel):
    fruitType: str
    boundingBox: BoundingBox
    confidence: float

class FruitRecognitionDTO(BaseModel):
    fruits: List[FruitInfo]
    totalFruits: int
    timestamp: str
