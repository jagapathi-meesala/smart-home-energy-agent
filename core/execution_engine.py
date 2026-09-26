from typing import Any, Dict, List, Optional, Tuple
from contracts.behavior_contract import BehaviorContract
from contracts.input_contract import InputContract
from contracts.output_contract import OutputContract
from passport.passport_manager import PassportManager
from tools.tool_registry import ToolRegistry

class ExecutionEngine:
    """Generic Execution Engine for capability validation, tool discovery, and execution."""

    def __init__(
        self,
        passport_manager: Optional[PassportManager] = None,
        tool_registry: Optional[ToolRegistry] = None,
        behavior_contract: Optional[BehaviorContract] = None
    ):
        self.passport_manager = passport_manager or PassportManager()
        self.tool_registry = tool_registry or ToolRegistry()
        self.behavior_contract = behavior_contract or BehaviorContract(self.passport_manager)

    def execute_request(self, capability: str, input_payload: Any, **kwargs) -> Dict[str, Any]:
        # 1. Capability Validation
        if not self.passport_manager.validate_capability(capability):
            return OutputContract.error(
                code="CAPABILITY_NOT_FOUND",
                message=f"Capability '{capability}' is not defined in Agent Passport capabilities.",
                capability=capability
            )

        # 2. Tool Discovery
        tool_name = self.passport_manager.get_tool_for_capability(capability)
        if not tool_name:
            return OutputContract.error(
                code="TOOL_NOT_FOUND",
                message=f"No tool mapped to capability '{capability}' in Passport configuration.",
                capability=capability
            )

        tool = self.tool_registry.get(tool_name)
        if not tool:
            return OutputContract.error(
                code="TOOL_NOT_FOUND",
                message=f"Mapped tool '{tool_name}' is not registered in ToolRegistry.",
                capability=capability,
                tool=tool_name
            )

        # 3. Input parsing and dataset validation
        is_parsed, records, parse_err = InputContract.parse_input_records(input_payload)
        if not is_parsed or parse_err:
            return OutputContract.error(
                code=parse_err.get("code", "INVALID_INPUT"),
                message=parse_err.get("message", "Input validation failed."),
                capability=capability,
                tool=tool_name
            )

        require_device = (capability == "appliance_energy_analysis")
        is_clean, clean_records, rec_err = InputContract.validate_records(records, require_device=require_device)
        if not is_clean or rec_err:
            return OutputContract.error(
                code=rec_err.get("code", "INVALID_INPUT"),
                message=rec_err.get("message", "Record validation failed."),
                capability=capability,
                tool=tool_name
            )

        # 4. Tool Execution
        success, result, tool_err = tool.execute(clean_records, **kwargs)
        if not success or tool_err:
            return OutputContract.error(
                code=tool_err.get("code", "TOOL_EXECUTION_FAILED"),
                message=tool_err.get("message", "Tool execution returned an error."),
                details=tool_err,
                capability=capability,
                tool=tool_name
            )

        # 5. Return formatted output
        return OutputContract.success(
            capability=capability,
            tool=tool_name,
            result=result
        )
