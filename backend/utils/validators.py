# backend/utils/validators.py
"""
Input validation functions.

Why validate?
- Prevent bad data from reaching agents
- Give clear error messages to users
- Protect the system from abuse
"""

from backend.config import settings

def validate_task(task: str) -> tuple[bool, str]:
    """
    Validate a task input.
    
    Args:
        task: The task to validate
        
    Returns:
        (is_valid, error_message) tuple
    """
    # Check if task is empty
    if not task or task.strip() == "":
        return False, "Task cannot be empty"
    
    # Check length
    if len(task) > settings.MAX_TASK_LENGTH:
        return False, f"Task too long. Max {settings.MAX_TASK_LENGTH} characters"
    
    # Check minimum length
    if len(task) < 5:
        return False, "Task must be at least 5 characters long"
    
    return True, ""


def validate_language(language: str) -> tuple[bool, str]:
    """
    Validate a programming language input.
    
    Args:
        language: The programming language
        
    Returns:
        (is_valid, error_message) tuple
    """
    supported = ["python", "javascript", "java", "cpp", "go", "rust", "typescript"]
    
    if language.lower() not in supported:
        return False, f"Language not supported. Supported: {', '.join(supported)}"
    
    return True, ""


def validate_model(model: str) -> tuple[bool, str]:
    """
    Validate a model name.
    
    Args:
        model: The model name
        
    Returns:
        (is_valid, error_message) tuple
    """
    supported = ["gpt-4", "gpt-3.5-turbo", "claude-3-opus", "claude-3-sonnet"]
    
    if model not in supported:
        return False, f"Model not supported. Supported: {', '.join(supported)}"
    
    return True, ""