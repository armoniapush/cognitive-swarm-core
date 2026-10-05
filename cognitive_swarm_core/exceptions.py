"""
Cognitive Core Exceptions
Jerarquía centralizada de excepciones para el pipeline agnóstico.
"""

class CognitiveCoreError(Exception):
    """Excepción base para todos los errores del núcleo cognitivo."""
    pass


class PatchApplicationError(CognitiveCoreError):
    """Error al aplicar una operación RFC 6902 sobre el estado."""
    def __init__(self, operation: str, path: str, message: str):
        super().__init__(f"Error en patch [{operation}] en '{path}': {message}")
        self.operation = operation
        self.path = path
        self.message = message


class InvariantViolationError(CognitiveCoreError):
    """Error cuando una mutación de estado viola una regla invariante declarada."""
    def __init__(self, rule_id: str, message: str, delta=None):
        super().__init__(f"Violación de invariante [{rule_id}]: {message}")
        self.rule_id = rule_id
        self.message = message
        self.delta = delta


class GraphRetrievalError(CognitiveCoreError):
    """Error durante la consulta o recorrido del grafo ontológico."""
    pass


class LinterRuleError(CognitiveCoreError):
    """Error en la evaluación o parsing de reglas de estilo."""
    pass
