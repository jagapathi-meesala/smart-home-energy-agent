from enum import Enum
from typing import Any, Dict, Optional

class LifecycleState(Enum):
    INPUT = "INPUT"
    REQUEST_VALIDATION = "REQUEST_VALIDATION"
    PASSPORT_LOADING = "PASSPORT_LOADING"
    CAPABILITY_VALIDATION = "CAPABILITY_VALIDATION"
    TOOL_DISCOVERY = "TOOL_DISCOVERY"
    TOOL_EXECUTION = "TOOL_EXECUTION"
    RESULT_VALIDATION = "RESULT_VALIDATION"
    RESPONSE_GENERATION = "RESPONSE_GENERATION"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class ExecutionStateTracker:
    """Tracks state transitions during agent request processing."""

    def __init__(self):
        self.current_state = LifecycleState.INPUT
        self.history = [self.current_state.value]

    def transition_to(self, new_state: LifecycleState) -> None:
        self.current_state = new_state
        self.history.append(new_state.value)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "current_state": self.current_state.value,
            "state_history": self.history
        }
