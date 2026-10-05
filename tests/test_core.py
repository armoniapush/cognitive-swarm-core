"""
Unit test suite for Cognitive Swarm Core (Domain-Agnostic).
Tests Lateral Thinking (Po operators), 3-Way Dialectic, RFC 6902 JsonPatch,
State Transactions with rollback, and K-Hop Subgraph Retrieval.
"""

import unittest
from pathlib import Path

from cognitive_swarm_core.lateral_engine import LateralEngine, ProvocationType
from cognitive_swarm_core.state_tracker import CausalStateManager, InvariantViolationError, JsonPatcher
from cognitive_swarm_core.graph_engine import GraphEngine


class TestLateralEngine(unittest.TestCase):

    def setUp(self):
        self.engine = LateralEngine()

    def test_apply_provocation_escape(self):
        res = self.engine.apply_provocation("authentication token", ProvocationType.ESCAPE)
        self.assertIn("Axioma de Escape (Po)", res.constraint_directive)
        self.assertIn("authentication token", res.constraint_directive)

    def test_apply_provocation_reversal(self):
        res = self.engine.apply_provocation("client server request", ProvocationType.REVERSAL)
        self.assertIn("Axioma de Inversión (Po)", res.constraint_directive)

    def test_three_way_dialectic(self):
        ctx = {"topic": "cache invalidation", "domain": "distributed systems"}
        res = self.engine.three_way_dialectic(ctx)
        self.assertIn("Hipótesis A", res["thesis"])
        self.assertIn("Hipótesis B", res["antithesis"])
        self.assertIn("Salto Ortogonal C", res["synthesis"])
        self.assertIn("PROHIBIDAS", res["synthesis"])


class TestStateTracker(unittest.TestCase):

    def test_json_patcher_add_replace_remove(self):
        doc = {"system": {"version": 1, "services": ["auth"]}}
        
        patch_add = [{"op": "add", "path": "/system/services/-", "value": "billing"}]
        doc2 = JsonPatcher.apply_patch(doc, patch_add)
        self.assertEqual(doc2["system"]["services"], ["auth", "billing"])

        patch_rep = [{"op": "replace", "path": "/system/version", "value": 2}]
        doc3 = JsonPatcher.apply_patch(doc2, patch_rep)
        self.assertEqual(doc3["system"]["version"], 2)

        patch_rem = [{"op": "remove", "path": "/system/services/0"}]
        doc4 = JsonPatcher.apply_patch(doc3, patch_rem)
        self.assertEqual(doc4["system"]["services"], ["billing"])

    def test_causal_state_manager_commit_and_rollback(self):
        sm = CausalStateManager({"level": 1})
        self.assertEqual(sm.snapshot, {"level": 1})

        delta = [{"op": "replace", "path": "/level", "value": 2}]
        sm.apply_delta(delta)
        self.assertEqual(sm.snapshot, {"level": 2})

        sm.rollback()
        self.assertEqual(sm.snapshot, {"level": 1})

    def test_invariant_violation_triggers_rollback(self):
        sm = CausalStateManager({"balance": 100})
        delta = [{"op": "replace", "path": "/balance", "value": -50}]

        def guard(st, d):
            if st.get("balance", 0) < 0:
                return False, "Balance cannot be negative"
            return True, "OK"

        with self.assertRaises(InvariantViolationError):
            sm.apply_delta(delta, invariants_check=guard)

        self.assertEqual(sm.snapshot, {"balance": 100})


class TestGraphEngine(unittest.TestCase):

    def setUp(self):
        self.ge = GraphEngine()
        self.ge.add_node("A", {"name": "Node A"})
        self.ge.add_node("B", {"name": "Node B"})
        self.ge.add_node("C", {"name": "Node C"})
        self.ge.add_edge("A", "B", "calls", {"law": "A invokes B synchronously"})
        self.ge.add_edge("B", "C", "persists_to", {"law": "B writes to C"})

    def test_retrieve_subgraph_khop(self):
        subgraph_txt = self.ge.retrieve_subgraph(["A"], max_hops=1)
        self.assertIn("Node A", subgraph_txt)
        self.assertIn("Node B", subgraph_txt)
        self.assertIn("A invokes B", subgraph_txt)


if __name__ == "__main__":
    unittest.main()
