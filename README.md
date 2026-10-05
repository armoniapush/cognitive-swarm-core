# Cognitive Swarm Core

**Domain-Agnostic Cognitive Framework for Lateral Inference, RFC 6902 State Transactions, and Deterministic Graph Retrieval.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()

---

## What is Cognitive Swarm Core?

Standard Large Language Models (LLMs) and Vector RAG systems optimize for **statistical probability** (predicting the most frequent token based on surface proximity). This causes two structural failure modes in complex domain reasoning:

1. **Cosine Similarity Fallacy:** Vector embeddings measure superficial vocabulary co-occurrence. They fail at **Structure-Mapping (Gentner)**—detecting identical relational topologies $R(A, B) \to C$ across disparate domains (e.g., mapping phase cancellation in DSP to distributed network deadlocks).
2. **Convergence to Clichés:** Because LLMs are trained to minimize cross-entropy loss, they default to common, generic solutions and cheap verbal symmetries (*"not X, but Y"*).
3. **Decoupled Causality:** Generative models make mutations without state verification, feedback loops, or conservation laws.

**Cognitive Swarm Core** is an ultra-lightweight, zero-bloat Python engine that computationalizes cognitive science primitives (Edward de Bono's Lateral Thinking, Koestler's Bisociation, Fauconnier & Turner's Conceptual Blending, and RFC 6902 transactional integrity) to transform any LLM pipeline into a deterministic, high-fidelity reasoning engine.

---

## Architectural Pillars

```
┌────────────────────────────────────────────────────────────────────────┐
│                        COGNITIVE SWARM CORE                            │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
    ┌───────────────────────────────┴───────────────────────────────┐
    ▼                                                               ▼
[1. LATERAL ENGINE]                           [2. TRANSACTIONAL STATE]
• 5 Po Operators (Escape, Reversal, etc.)    • RFC 6902 JsonPatch engine
• 3-Way Dialectic (Veto A & B -> Eje C)      • Invariant callbacks & rollback
    │                                                               │
    └───────────────────────────────┬───────────────────────────────┘
                                    │
    ┌───────────────────────────────┴───────────────────────────────┐
    ▼                                                               ▼
[3. DETERMINISTIC GRAPH ENGINE]               [4. ZERO-TOKEN LINTERS]
• K-Hop neighborhood traversal               • Regex-based pre-commit guards
• Token-budgeted subgraphs (<400 tokens)     • Semantic anti-slop filters
```

### 1. Lateral Engine (`cognitive_swarm_core.lateral_engine`)
Implements Edward de Bono's **Po (Provocation)** operators and Hegelian triadic dialectics:
- **Escape:** Deny an essential attribute to break obvious paths.
- **Reversal:** Flip the direction of flow or agency.
- **Exaggeration:** Push quantities to extremes (zero or infinity).
- **Distortion:** Alter temporal sequences.
- **Wishful Thinking:** Introduce an impossible condition as an operational constraint.
- **3-Way Dialectic:** Systematically forms Thesis (Path A) and Antithesis (Path B), marks them both as **FORBIDDEN**, and forces generation along an orthogonal Synthesis axis (Axis C).

### 2. Transactional State Tracker (`cognitive_swarm_core.state_tracker`)
- Pure Python implementation of **RFC 6902 (JsonPatch)** (`add`, `remove`, `replace`, `test`).
- **Speculative Execution:** Applies deltas to a state clone.
- **Invariant Guards:** Validates conservation laws (mass, energy, domain constraints).
- **Automatic Rollback:** Reverts state instantaneously if any invariant fails, raising formal exceptions.

### 3. Graph Engine (`cognitive_swarm_core.graph_engine`)
- Deterministic relational graph built on **NetworkX**.
- **K-Hop Neighborhood Traversal:** Retrieves connected laws and relational triples within 1 to 2 hops of seed nodes.
- **Token Budgeting:** Serializes relational subgraphs compactly into formatted strings (<400 tokens) to prevent LLM context rot.

---

## Installation

```bash
pip install cognitive-swarm-core
```

Or install locally in editable mode:

```bash
git clone https://github.com/armoniapush/cognitive-swarm-core.git
cd cognitive-swarm-core
pip install -e .
```

---

## Quickstart

### 1. Provocation & 3-Way Dialectic
```python
from cognitive_swarm_core.lateral_engine import LateralEngine, ProvocationType

engine = LateralEngine()

# Apply a Po Escape operator
provocation = engine.apply_provocation("database connection pool", ProvocationType.ESCAPE)
print(provocation.constraint_directive)
# Output: Operational rule forcing the model to solve the scenario without the core assumption.

# Apply 3-Way Dialectic
dialectic = engine.three_way_dialectic({
    "problem": "cache invalidation in distributed consensus",
    "context": "high-throughput ledger"
})
print(dialectic["synthesis"])
# Rejects standard solutions A (TTL expiration) and B (centralized broadcast), forcing orthogonal Axis C.
```

### 2. Transactional State Management with RFC 6902
```python
from cognitive_swarm_core.state_tracker import CausalStateManager, InvariantViolationError

initial_state = {
    "cluster": {
        "active_nodes": 3,
        "max_capacity": 5
    }
}

sm = CausalStateManager(initial_state)

# Define an invariant guard
def capacity_guard(state, delta):
    if state["cluster"]["active_nodes"] > state["cluster"]["max_capacity"]:
        return False, "Cluster capacity exceeded"
    return True, "OK"

# Valid delta
sm.apply_delta([
    {"op": "replace", "path": "/cluster/active_nodes", "value": 4}
], invariants_check=capacity_guard)

print(sm.snapshot["cluster"]["active_nodes"])  # Output: 4

# Invalid delta (triggers rollback)
try:
    sm.apply_delta([
        {"op": "replace", "path": "/cluster/active_nodes", "value": 10}
    ], invariants_check=capacity_guard)
except InvariantViolationError as e:
    print(f"Rollback triggered: {e}")

print(sm.snapshot["cluster"]["active_nodes"])  # Output: 4 (State restored intact)
```

### 3. K-Hop Subgraph Retrieval
```python
from cognitive_swarm_core.graph_engine import GraphEngine

ge = GraphEngine()
ge.add_node("microservice.auth", {"name": "Auth Service", "layer": "security"})
ge.add_node("queue.events", {"name": "Audit Kafka Topic", "layer": "messaging"})
ge.add_edge("microservice.auth", "queue.events", "publishes_to", {"law": "Async at-least-once"})

# Retrieve relational context
subgraph_context = ge.retrieve_subgraph(["microservice.auth"], max_hops=1)
print(subgraph_context)
```

---

## Running Tests

Run the standalone unit test suite:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## Use Cases Beyond Writing

While originally born as an engine for hard worldbuilding and ontological consistency, `cognitive-swarm-core` is domain-agnostic and directly applicable to:

- **Distributed Systems & Architecture:** Enforce fault-tolerance invariants, forbid standard patterns A/B to discover novel distributed consensus topologies.
- **Scientific & Biochemical Research:** Map analogies between metabolic pathways and network routing; validate biochemical conservation equations before accepting model output.
- **Automated Refactoring & SWE Agents:** Apply RFC 6902 transactional patches to AST trees, reverting changes if unit tests or static linters fail.

---

## License

MIT License. Copyright (c) 2026 Armonia Push.
