"""assomem -- Associative Memory Benchmark + reference agent."""
from .agent import AssociativeMemoryAgent, AgentConfig
from .llm import LLM
from .schema import AgentAnswer, BenchItem, MemoryNote, TemporalEdge

__version__ = "0.1.0"
__all__ = [
    "AssociativeMemoryAgent", "AgentConfig", "LLM",
    "BenchItem", "AgentAnswer", "MemoryNote", "TemporalEdge",
]
