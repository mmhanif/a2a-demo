"""Centralized configuration for agent endpoints and ports."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class AgentEndpoint:
    """Represents a single agent endpoint definition."""

    name: str
    port: int

    def url(self, *, scheme: str = "http", host: str = "localhost") -> str:
        return f"{scheme}://{host}:{self.port}"


DEFAULT_AGENT_SCHEME = "http"
DEFAULT_AGENT_HOST = "localhost"

# Common agent endpoints
DEFAULT_AGENT = AgentEndpoint(name="DefaultAgent", port=5000)
ORCHESTRATOR_AGENT = AgentEndpoint(name="OrchestratorAgent", port=5003)
CALCULATOR_AGENT = AgentEndpoint(name="CalculatorAgent", port=5001)
TRANSLATOR_AGENT = AgentEndpoint(name="TranslatorAgent", port=5002)


def build_agent_url(endpoint: AgentEndpoint) -> str:
    """Build a URL for the given agent endpoint using default scheme/host."""

    return endpoint.url(scheme=DEFAULT_AGENT_SCHEME, host=DEFAULT_AGENT_HOST)


DEFAULT_AGENT_URL = build_agent_url(DEFAULT_AGENT)
ORCHESTRATOR_URL = build_agent_url(ORCHESTRATOR_AGENT)
CALCULATOR_URL = build_agent_url(CALCULATOR_AGENT)
TRANSLATOR_URL = build_agent_url(TRANSLATOR_AGENT)

AGENT_ENDPOINTS: Dict[str, AgentEndpoint] = {
    ORCHESTRATOR_AGENT.name: ORCHESTRATOR_AGENT,
    CALCULATOR_AGENT.name: CALCULATOR_AGENT,
    TRANSLATOR_AGENT.name: TRANSLATOR_AGENT,
}

AGENT_URLS: Dict[str, str] = {
    name: build_agent_url(endpoint) for name, endpoint in AGENT_ENDPOINTS.items()
}


def get_agent_url(agent_name: str) -> str:
    """Retrieve an agent URL by display name."""

    try:
        return AGENT_URLS[agent_name]
    except KeyError as exc:  # pragma: no cover - guard clause
        raise KeyError(f"Unknown agent '{agent_name}'") from exc

