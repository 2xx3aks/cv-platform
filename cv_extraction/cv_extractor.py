"""
CV extraction service using Cohere API.
"""
import os
import cohere
from typing import Optional
import PyPDF2
from docx import Document
from io import BytesIO
from django.conf import settings
from .schemas import CVExtract
import json


class CVExtractor:
    """CV extraction using Cohere API."""
    
    def __init__(self):
        api_key = settings.COHERE_API_KEY
        if not api_key:
            raise ValueError("COHERE_API_KEY not set in settings")
        self.client = cohere.Client(api_key)
    
    def extract_text_from_pdf(self, file_content: bytes) -> str:
        """Extract text from PDF file."""
        try:
            pdf_file = BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise ValueError(f"Error extracting text from PDF: {str(e)}")
    
    def extract_text_from_docx(self, file_content: bytes) -> str:
        """Extract text from DOCX file."""
        try:
            docx_file = BytesIO(file_content)
            doc = Document(docx_file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            raise ValueError(f"Error extracting text from DOCX: {str(e)}")
    
    def _normalize_extracted_data(self, data: dict) -> dict:
        """
        Normalize extracted data to match schema expectations.
        Converts dictionaries/objects in list fields to strings.
        """
        normalized = data.copy()
        
        # Fields that should be lists of strings
        list_fields = ['skills', 'education', 'experience', 'certifications', 'languages']
        
        for field in list_fields:
            if field in normalized and isinstance(normalized[field], list):
                normalized_list = []
                for item in normalized[field]:
                    if isinstance(item, dict):
                        # Convert dict to readable string
                        # Try common keys like 'position', 'title', 'name', 'description', 'text'
                        if 'position' in item and 'company' in item:
                            # Experience format: "Position at Company. Description"
                            parts = [item.get('position', ''), item.get('company', '')]
                            if item.get('description'):
                                parts.append(item.get('description'))
                            # Join with ". " instead of " - " to avoid dashes
                            normalized_list.append('. '.join(filter(None, parts)))
                        elif 'title' in item:
                            # Education/Certification format: "Title, Institution (Date)"
                            parts = [item.get('title', '')]
                            if item.get('institution') or item.get('organization'):
                                parts.append(item.get('institution') or item.get('organization'))
                            if item.get('date') or item.get('year'):
                                parts.append(f"({item.get('date') or item.get('year')})")
                            # Join with ", " instead of " - " to avoid dashes
                            normalized_list.append(', '.join(filter(None, parts)))
                        elif 'name' in item:
                            # Simple name field
                            normalized_list.append(str(item.get('name', '')))
                        elif 'text' in item or 'description' in item:
                            # Generic text field
                            normalized_list.append(str(item.get('text') or item.get('description', '')))
                        else:
                            # Fallback: convert entire dict to JSON string
                            normalized_list.append(json.dumps(item, ensure_ascii=False))
                    elif isinstance(item, str):
                        normalized_list.append(item)
                    else:
                        # Convert other types to string
                        normalized_list.append(str(item))
                normalized[field] = normalized_list
        
        return normalized
    
    def extract_text(self, file_content: bytes, filename: str) -> str:
        """Extract text from file based on extension."""
        filename_lower = filename.lower()
        if filename_lower.endswith('.pdf'):
            return self.extract_text_from_pdf(file_content)
        elif filename_lower.endswith('.docx') or filename_lower.endswith('.doc'):
            return self.extract_text_from_docx(file_content)
        else:
            raise ValueError(f"Unsupported file type: {filename}")
    
    def extract_cv_data(self, cv_text: str) -> CVExtract:
        """
        Extract structured CV data using Cohere Chat API.
        
        Args:
            cv_text: Raw text extracted from CV file
        
        Returns:
            CVExtract object with structured data
        """
        preamble = """You are an expert at extracting structured information from CVs and resumes. 
Extract the following information and return ONLY valid JSON matching this exact schema:
{
  "full_name": "string or null",
  "email": "string or null",
  "phone": "string or null",
  "summary": "string or null",
  "skills": ["array of strings - each skill as a simple string"],
  "education": ["array of strings - each education entry as a single string like 'Degree - Institution - Year'"],
  "experience": ["array of strings - each experience as a single string like 'Position - Company - Description'"],
  "certifications": ["array of strings - each certification as a single string"],
  "languages": ["array of strings - each language as a simple string"],
  "gpa": "float or null",
  "major": "string or null"
}

IMPORTANT: All array fields (skills, education, experience, certifications, languages) must contain ONLY strings, NOT objects or dictionaries.
Each array item should be a single string value.

Return ONLY the JSON object, no additional text, no markdown, no code blocks, no explanation."""

        user_message = f"""Extract information from this CV/resume text:

{cv_text}

Return ONLY the JSON object matching the schema above."""

        try:
            # Use Chat API instead of Generate API (migrated from deprecated Generate API)
            # Cohere Chat API uses: message (user input), preamble (system instructions)
            # Try available models - use current models that haven't been deprecated
            # As of Nov 2025, command-r and command-r-plus were removed
            # Try newer models first
            available_models = [
                'command-r7b-12-2024',  # Latest R7B model (Dec 2024)
                'command',              # Basic command model (should still be available)
            ]
            
            response = None
            last_error = None
            
            for model in available_models:
                try:
                    response = self.client.chat(
                        model=model,
                        message=user_message,
                        preamble=preamble,
                        temperature=0.1,
                        max_tokens=2000,
                    )
                    break  # Success, exit loop
                except Exception as model_error:
                    last_error = model_error
                    error_str = str(model_error).lower()
                    # If model was removed or not found, try next model
                    if 'removed' in error_str or 'not found' in error_str or '404' in error_str or 'was removed' in error_str:
                        continue
                    else:
                        # Other errors (auth, rate limit, etc.) should be raised
                        raise
            
            if response is None:
                raise ValueError(f"All models failed. Last error: {str(last_error)}")
            
            # Extract text from chat response
            response_text = response.text.strip()
            
            # Try to parse JSON - sometimes Cohere adds markdown code blocks
            if response_text.startswith('```'):
                # Remove markdown code blocks
                lines = response_text.split('\n')
                response_text = '\n'.join([line for line in lines if not line.strip().startswith('```')])
            
            # Parse JSON
            try:
                extracted_data = json.loads(response_text)
            except json.JSONDecodeError:
                # Try to extract JSON from the text
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    extracted_data = json.loads(json_match.group())
                else:
                    raise ValueError(f"Could not parse JSON from Cohere response. Response was: {response_text[:200]}")
            
            # Normalize data - convert dictionaries/objects to strings for list fields
            extracted_data = self._normalize_extracted_data(extracted_data)
            
            # Validate and return CVExtract object
            cv_extract = CVExtract(**extracted_data)
            return cv_extract
            
        except Exception as e:
            # Provide more detailed error information
            error_msg = str(e)
            if hasattr(e, 'response') and hasattr(e.response, 'body'):
                error_msg = f"{error_msg}. Response: {e.response.body}"
            raise ValueError(f"Error extracting CV data with Cohere: {error_msg}")
    
    def process_cv_file(self, file_content: bytes, filename: str) -> CVExtract:
        """
        Complete CV processing pipeline.
        
        Args:
            file_content: File content as bytes
            filename: Original filename
        
        Returns:
            CVExtract object with structured data
        """
        # Step 1: Extract text
        cv_text = self.extract_text(file_content, filename)
        
        if not cv_text or len(cv_text.strip()) < 50:
            raise ValueError("CV text is too short or empty")
        
        # Step 2: Extract structured data with Cohere
        cv_data = self.extract_cv_data(cv_text)
        
        return cv_data

