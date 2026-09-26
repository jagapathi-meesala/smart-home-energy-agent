from typing import List
from core.state import LifecycleState

class AgentLifecycleManager:
    """Enforces valid lifecycle state transitions."""

    ORDERED_STATES: List[LifecycleState] = [
        LifecycleState.INPUT,
        LifecycleState.REQUEST_VALIDATION,
        LifecycleState.PASSPORT_LOADING,
        LifecycleState.CAPABILITY_VALIDATION,
        LifecycleState.TOOL_DISCOVERY,
        LifecycleState.TOOL_EXECUTION,
        LifecycleState.RESULT_VALIDATION,
        LifecycleState.RESPONSE_GENERATION,
        LifecycleState.COMPLETED
    ]

    @classmethod
    def get_lifecycle_sequence(cls) -> List[str]:
        return [s.value for s in cls.ORDERED_STATES]
