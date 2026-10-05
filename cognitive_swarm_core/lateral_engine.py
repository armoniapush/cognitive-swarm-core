"""
Lateral Engine: Operadores Po de Edward de Bono y Dialéctica Tripartita.
Agnóstico, desacoplado y reutilizable en cualquier dominio cognitivo.
"""

from enum import Enum
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


class ProvocationType(str, Enum):
    ESCAPE = "escape"
    REVERSAL = "reversal"
    EXAGGERATION = "exaggeration"
    DISTORTION = "distortion"
    WISHFUL_THINKING = "wishful_thinking"


@dataclass(frozen=True)
class ProvocationResult:
    seed_concept: str
    operator: ProvocationType
    constraint_directive: str
    rationale: str


class LateralEngine:
    """Motor de provocación lateral y dialéctica ortogonal."""

    OPERATOR_TEMPLATES = {
        ProvocationType.ESCAPE: (
            "Axioma de Escape (Po): Se elimina por completo la premisa dada por sentada: '{seed}'. "
            "Resuelve el conflicto asumiendo que esa entidad/mecanismo NO existe ni puede ser invocado."
        ),
        ProvocationType.REVERSAL: (
            "Axioma de Inversión (Po): Se invierte la dirección causa-efecto o sujeto-objeto de '{seed}'. "
            "El receptor/entorno absorbe la agencia activa y el emisor padece la transformación."
        ),
        ProvocationType.EXAGGERATION: (
            "Axioma de Exageración (Po): La magnitud o coste de '{seed}' se lleva a un extremo asintótico. "
            "Cualquier intento de aplicación produce una resistencia masiva o un coste no lineal inmediato."
        ),
        ProvocationType.DISTORTION: (
            "Axioma de Distorsión (Po): Se altera la secuencia temporal o la topología de '{seed}'. "
            "El efecto precede al detonante, o la interacción ocurre a través de una consecuencia material imprevista."
        ),
        ProvocationType.WISHFUL_THINKING: (
            "Axioma de Deseo Fantasioso (Po): Se postula resuelto un imposible físico respecto a '{seed}', "
            "pero se deduce rígidamente el coste entrópico, biomecánico o colateral que esa solución engendra."
        ),
    }

    def apply_provocation(
        self,
        seed_concept: str,
        operator_mode: ProvocationType = ProvocationType.ESCAPE,
        domain_context: Optional[str] = None
    ) -> ProvocationResult:
        """
        Aplica un operador Po formalizado sobre un concepto semilla.
        """
        if not seed_concept or not seed_concept.strip():
            raise ValueError("El concepto semilla no puede estar vacío.")

        template = self.OPERATOR_TEMPLATES.get(operator_mode)
        if not template:
            raise ValueError(f"Operador no soportado: {operator_mode}")

        directive = template.format(seed=seed_concept.strip())
        if domain_context:
            directive += f" Contexto de frontera: {domain_context.strip()}."

        rationale = (
            f"Desvío de atención aplicado mediante operador '{operator_mode.value}' "
            f"para evitar la convergencia al promedio estadístico de '{seed_concept}'."
        )

        return ProvocationResult(
            seed_concept=seed_concept,
            operator=operator_mode,
            constraint_directive=directive,
            rationale=rationale
        )

    def three_way_dialectic(self, context: Dict[str, Any]) -> Dict[str, str]:
        """
        Genera una estructura dialéctica tripartita (Tesis -> Antítesis -> Salto Ortogonal).
        Veta formalmente la Tesis obvia y la Antítesis cliché, obligando a operar en el eje C.
        """
        topic = context.get("topic", "resolución del conflicto")
        characters = context.get("characters", [])
        chars_str = ", ".join(characters) if characters else "los involucrados"

        thesis = (
            f"Hipótesis A (Tesis Obvia / Promedio Estadístico): {chars_str} resuelven {topic} "
            f"mediante la vía directa, predecible y de menor resistencia temática."
        )
        antithesis = (
            f"Hipótesis B (Antítesis / Giro Predecible de Guión): Se invierte {topic} en un conflicto "
            f"abierto o traición convencional de efecto dramático superficial."
        )
        synthesis = (
            f"Salto Ortogonal C (Directiva Obligatoria): Quedan terminantemente PROHIBIDAS tanto la Hipótesis A "
            f"como la Hipótesis B. La resolución de {topic} debe ocurrir en un tercer eje inadvertido: "
            f"una consecuencia física, mineral, fisiológica o de desacoplamiento de impedancia del entorno."
        )

        return {
            "thesis": thesis,
            "antithesis": antithesis,
            "synthesis": synthesis,
            "prompt_directive": (
                f"[DIALÉCTICA DE TRES VÍAS OBLIGATORIA]\n"
                f"1. VETO A: {thesis}\n"
                f"2. VETO B: {antithesis}\n"
                f"3. EJECUCIÓN C: {synthesis}\n"
            )
        }
