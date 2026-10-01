import pytest
from ai.runtime.prompts import PromptTemplate, PromptRegistry


def test_prompt_template_variable_extraction():
    tmpl = PromptTemplate(
        name="test_tmpl",
        version="1.0.0",
        template_str="Hello {name}, your task on {host} is to analyze {metric}."
    )
    assert tmpl.required_variables == ["host", "metric", "name"]


def test_prompt_template_formatting_success():
    tmpl = PromptTemplate(
        name="test_tmpl",
        version="1.0.0",
        template_str="Host: {host}, Cores: {cores}"
    )
    rendered = tmpl.format({"host": "titan-node-01", "cores": 16})
    assert rendered == "Host: titan-node-01, Cores: 16"


def test_prompt_template_missing_variable_raises():
    tmpl = PromptTemplate(
        name="test_tmpl",
        version="1.0.0",
        template_str="Host: {host}, Cores: {cores}"
    )
    with pytest.raises(ValueError, match="missing required variables"):
        tmpl.format({"host": "titan-node-01"})


def test_prompt_registry_versioning():
    registry = PromptRegistry()
    tmpl_v1 = PromptTemplate(name="diag", version="1.0.0", template_str="V1: {data}")
    tmpl_v2 = PromptTemplate(name="diag", version="1.1.0", template_str="V2: {data}")
    registry.register(tmpl_v1)
    registry.register(tmpl_v2)

    # Fetch explicit version
    assert registry.get("diag", "1.0.0").version == "1.0.0"
    assert registry.get("diag", "1.1.0").version == "1.1.0"

    # Fetch default (latest)
    latest = registry.get("diag")
    assert latest.version == "1.1.0"
