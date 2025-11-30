"""
Pydantic schema for CV extraction.
"""
from pydantic import BaseModel
from typing import List, Optional


class CVExtract(BaseModel):
    """Schema for extracted CV data."""
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    summary: Optional[str] = None
    skills: List[str] = []
    education: List[str] = []
    experience: List[str] = []
    certifications: List[str] = []
    languages: List[str] = []
    gpa: Optional[float] = None
    major: Optional[str] = None

