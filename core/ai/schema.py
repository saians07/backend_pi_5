"""
Base model schema for all AI related input output
"""

from typing import List
from pydantic import BaseModel

class GeminiParts(BaseModel):
    """Gemini parts data"""
    text: str

class GeminiContet(BaseModel):
    """Gemini content output"""
    parts: List[GeminiParts]
    role: str

class GeminiCandidate(BaseModel):
    """Gemini candidate output"""
    content: GeminiContet
    finishReason: str
    index: int

class GeminiPromptTokenDetail(BaseModel):
    """Gemini prompt token detail output"""
    modality: str
    tokenCount: int

class GeminiUsageMetadata(BaseModel):
    """Gemini usage metadata output"""
    promptTokenCount: int
    candidatesTokenCount: int
    totalTokenCount: int
    promptTokensDetails: List[GeminiPromptTokenDetail]
    thoughtsTokenCount: int

class GeminiResponse(BaseModel):
    """Gemini basic output"""
    candidates: List[GeminiCandidate]
    usageMetadata: GeminiUsageMetadata
    modelVersion: str
    responseId: str
