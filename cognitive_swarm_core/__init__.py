"""
Cognitive Core Module
Arquitectura agnóstica de pensamiento lateral, transacciones causales y grafos.
"""

from .lateral_engine import LateralEngine, ProvocationType
from .state_tracker import CausalStateManager, StateDelta
from .graph_engine import GraphEngine
from .exceptions import (
    CognitiveCoreError,
    PatchApplicationError,
    InvariantViolationError,
    GraphRetrievalError,
    LinterRuleError,
)

__all__ = [
    "LateralEngine",
    "ProvocationType",
    "CausalStateManager",
    "StateDelta",
    "GraphEngine",
    "CognitiveCoreError",
    "PatchApplicationError",
    "InvariantViolationError",
    "GraphRetrievalError",
    "LinterRuleError",
]
