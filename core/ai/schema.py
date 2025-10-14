"""
Base model schema for all AI related input output
"""

from typing import List, Optional, Any
from pydantic import BaseModel, Field

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

class OpenAIChoice(BaseModel):
    """OpenAI Choice output"""
    finish_reason: str
    index: int
    logprobs: Optional[Any]

class OpenAICompletionUsage(BaseModel):
    """OpenAI Usage output"""
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int
    completion_tokens_details: Optional[Any] = None
    prompt_tokens_details: Optional[Any] = None

class OpenAIChatCompletion(BaseModel):
    """OpenAI Chat completion output"""
    id: str
    choices: List[OpenAIChoice]
    created: int
    model: str
    object_: str = Field(..., alias="object")
    service_tier: Optional[Any] = None
    system_fingerprint: Optional[Any] = None
    usage: OpenAICompletionUsage

class OpenAIContent(BaseModel):
    """OpenAI content output"""
    type: str
    text: str
    annotations: Optional[List[Any]] = []
    logprobs: Optional[List[Any]] = []

class OpenAIOutput(BaseModel):
    """OpenAI basic output"""
    type: str
    id: Optional[str] = None
    status: Optional[str] = None
    role: Optional[str] = None
    content: Optional[OpenAIContent] = None

class OpenAIStandardResponse(BaseModel):
    """OpenAI raw output"""
    id: Optional[str] = None
    model: str
    output: OpenAIOutput
