from typing import List
from pydantic import BaseModel

class GeminiParts(BaseModel):
    text: str

class GeminiContet(BaseModel):
    parts: List[GeminiParts]
    role: str

class GeminiCandidate(BaseModel):
    content: GeminiContet
    finishReason: str
    index: int

class GeminiPromptTokenDetail(BaseModel):
    modality: str
    tokenCount: int

class GeminiUsageMetadata(BaseModel):
    promptTokenCount: int
    candidatesTokenCount: int
    totalTokenCount: int
    promptTokensDetails: List[GeminiPromptTokenDetail]
    thoughtsTokenCount: int

class GeminiResponse(BaseModel):
    candidates: List[GeminiCandidate]
    usageMetadata: GeminiUsageMetadata
    modelVersion: str
    responseId: str
