"""
State Tracker: Gestión de transacciones atómicas de estado con RFC 6902 (JSON Patch).
Agnóstico, desacoplado, sin dependencias externas complejas, con rollback automático.
"""

import copy
from typing import Dict, Any, List, Callable, Optional
from dataclasses import dataclass, field


from .exceptions import InvariantViolationError, PatchApplicationError


@dataclass
class StateDelta:
    patch: List[Dict[str, Any]]
    origin_agent: str
    rationale: str
    timestamp: Optional[str] = None


class JsonPointer:
    """Implementación ligera de RFC 6901 (JSON Pointer) para Python estándar."""
    
    @staticmethod
    def parse_path(path: str) -> List[str]:
        if not path or path == "/":
            return []
        if not path.startswith("/"):
            raise ValueError(f"JSON Pointer debe comenzar con '/': {path}")
        tokens = path[1:].split("/")
        return [t.replace("~1", "/").replace("~0", "~") for t in tokens]

    @classmethod
    def resolve_parent(cls, doc: Any, path: str) -> tuple[Any, str]:
        tokens = cls.parse_path(path)
        if not tokens:
            raise ValueError("No se puede obtener padre de la raíz.")
        parent = doc
        for token in tokens[:-1]:
            if isinstance(parent, dict):
                if token not in parent:
                    raise KeyError(f"Clave '{token}' no encontrada en el documento.")
                parent = parent[token]
            elif isinstance(parent, list):
                idx = int(token)
                parent = parent[idx]
            else:
                raise TypeError(f"Contenedor intermedio no es dict o list en ruta: {path}")
        return parent, tokens[-1]


class JsonPatcher:
    """Implementación en Python puro de RFC 6902 (add, remove, replace, test)."""

    @classmethod
    def apply_patch(cls, doc: Any, patch: List[Dict[str, Any]]) -> Any:
        res = copy.deepcopy(doc)
        for op_idx, op in enumerate(patch):
            action = op.get("op")
            path = op.get("path")
            if not action or path is None:
                raise ValueError(f"Operación RFC 6902 inválida en índice {op_idx}: {op}")

            if action == "add":
                res = cls._op_add(res, path, op.get("value"))
            elif action == "remove":
                res = cls._op_remove(res, path)
            elif action == "replace":
                res = cls._op_replace(res, path, op.get("value"))
            elif action == "test":
                cls._op_test(res, path, op.get("value"))
            else:
                raise NotImplementedError(f"Operación '{action}' no implementada.")
        return res

    @classmethod
    def _op_add(cls, doc: Any, path: str, value: Any) -> Any:
        if path == "":
            return value
        parent, key = JsonPointer.resolve_parent(doc, path)
        if isinstance(parent, dict):
            parent[key] = value
        elif isinstance(parent, list):
            if key == "-":
                parent.append(value)
            else:
                idx = int(key)
                parent.insert(idx, value)
        return doc

    @classmethod
    def _op_remove(cls, doc: Any, path: str) -> Any:
        parent, key = JsonPointer.resolve_parent(doc, path)
        if isinstance(parent, dict):
            if key not in parent:
                raise KeyError(f"Clave '{key}' a remover no existe.")
            del parent[key]
        elif isinstance(parent, list):
            idx = int(key)
            parent.pop(idx)
        return doc

    @classmethod
    def _op_replace(cls, doc: Any, path: str, value: Any) -> Any:
        if path == "":
            return value
        parent, key = JsonPointer.resolve_parent(doc, path)
        if isinstance(parent, dict):
            if key not in parent:
                raise KeyError(f"Clave '{key}' a reemplazar no existe.")
            parent[key] = value
        elif isinstance(parent, list):
            idx = int(key)
            if idx < 0 or idx >= len(parent):
                raise IndexError(f"Índice {idx} fuera de rango en lista.")
            parent[idx] = value
        return doc

    @classmethod
    def _op_test(cls, doc: Any, path: str, expected: Any) -> None:
        if path == "":
            curr = doc
        else:
            parent, key = JsonPointer.resolve_parent(doc, path)
            curr = parent[key] if isinstance(parent, dict) else parent[int(key)]
        if curr != expected:
            raise PatchApplicationError("test", path, f"esperado {expected!r}, actual {curr!r}")


class CausalStateManager:
    """Gestor de estado transaccional con reversión automática."""

    def __init__(self, initial_state: Optional[Dict[str, Any]] = None):
        self._current_state: Dict[str, Any] = copy.deepcopy(initial_state) if initial_state else {}
        self._history: List[Dict[str, Any]] = [copy.deepcopy(self._current_state)]
        self._applied_deltas: List[List[Dict[str, Any]]] = []

    @property
    def snapshot(self) -> Dict[str, Any]:
        """Retorna una copia profunda del estado consolidado actual."""
        return copy.deepcopy(self._current_state)

    def apply_delta(
        self,
        delta: List[Dict[str, Any]],
        invariants_check: Optional[Callable[[Dict[str, Any], List[Dict[str, Any]]], tuple[bool, str]]] = None
    ) -> bool:
        """
        Aplica un delta de forma especulativa sobre una copia de trabajo.
        Si la guarda o invariant_check falla, no se modifica el estado actual y se lanza InvariantViolationError.
        """
        if not delta:
            return True

        # Copia especulativa
        speculative_state = JsonPatcher.apply_patch(self._current_state, delta)

        # Validación de invariantes
        if invariants_check:
            is_valid, reason = invariants_check(speculative_state, delta)
            if not is_valid:
                raise InvariantViolationError(
                    rule_id="INVARIANT_GUARD_FAILED",
                    message=reason,
                    delta=delta
                )

        # Confirmación transaccional (Commit)
        self._current_state = speculative_state
        self._history.append(copy.deepcopy(self._current_state))
        self._applied_deltas.append(delta)
        return True

    def rollback(self) -> bool:
        """Revierte al snapshot anterior si existe."""
        if len(self._history) > 1:
            self._history.pop()
            if self._applied_deltas:
                self._applied_deltas.pop()
            self._current_state = copy.deepcopy(self._history[-1])
            return True
        return False
