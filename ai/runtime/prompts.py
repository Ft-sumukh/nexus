"""
NEXUS TITAN — Versioned Prompt Template Engine
Declarative prompt definitions with semver tracking, parameter validation, and safe interpolation.
"""

import re
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class PromptTemplate(BaseModel):
    """
    Encapsulates a versioned prompt template with input requirements.
    """
    name: str = Field(..., description="Unique template identifier (e.g. 'system_diagnosis')")
    version: str = Field(..., description="Semantic version string (e.g. '1.0.0')")
    template_str: str = Field(..., description="Template string containing {placeholders}")
    system_prompt: Optional[str] = Field(default=None, description="System instruction prompt")
    description: str = Field(default="", description="Description of the template purpose")

    @property
    def required_variables(self) -> List[str]:
        """Extracts all {variable} placeholder names from template_str."""
        return sorted(list(set(re.findall(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", self.template_str))))

    def format(self, variables: Dict[str, Any]) -> str:
        """
        Safely formats the prompt template with provided variables.
        Raises ValueError if any required placeholder is missing.
        """
        missing = [v for v in self.required_variables if v not in variables]
        if missing:
            raise ValueError(
                f"PromptTemplate '{self.name}:{self.version}' missing required variables: {missing}"
            )
        try:
            return self.template_str.format(**variables)
        except Exception as e:
            raise ValueError(f"Failed formatting PromptTemplate '{self.name}:{self.version}': {e}") from e


class PromptRegistry:
    """
    Thread-safe repository for registering, retrieving, and versioning prompt templates.
    """

    def __init__(self):
        # Maps name -> {version -> PromptTemplate}
        self._templates: Dict[str, Dict[str, PromptTemplate]] = {}

    def register(self, template: PromptTemplate) -> None:
        """Registers a versioned prompt template."""
        if template.name not in self._templates:
            self._templates[template.name] = {}
        self._templates[template.name][template.version] = template

    def get(self, name: str, version: Optional[str] = None) -> Optional[PromptTemplate]:
        """
        Retrieves a template by name and version.
        If version is omitted, returns the latest registered version alphabetically.
        """
        versions = self._templates.get(name)
        if not versions:
            return None
        if version:
            return versions.get(version)
        # Return highest semantic/alphanumeric version
        sorted_versions = sorted(versions.keys())
        return versions[sorted_versions[-1]]

    def list_templates(self) -> List[PromptTemplate]:
        """Returns all registered prompt templates across all versions."""
        result = []
        for version_dict in self._templates.values():
            result.extend(version_dict.values())
        return result
