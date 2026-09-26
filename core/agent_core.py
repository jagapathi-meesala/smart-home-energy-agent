from typing import Any, Dict, Optional
from contracts.behavior_contract import BehaviorContract
from core.execution_engine import ExecutionEngine
from core.state import ExecutionStateTracker, LifecycleState
from passport.passport_manager import PassportManager
from tools.appliance_energy_analyzer import ApplianceEnergyAnalyzerTool
from tools.energy_anomaly_detector import EnergyAnomalyDetectorTool
from tools.energy_consumption_analyzer import EnergyConsumptionAnalyzerTool
from tools.energy_cost_estimator import EnergyCostEstimatorTool
from tools.energy_pattern_detector import EnergyPatternDetectorTool
from tools.energy_recommendation import EnergyRecommendationTool
from tools.energy_report import EnergyReportTool
from tools.tool_registry import ToolRegistry

class AgentCore:
    """Central Execution Authority for SmartHomeEnergyAgent (Single Source of Truth)."""

    def __init__(self, passport_path: Optional[str] = None):
        self.passport_manager = PassportManager(passport_path) if passport_path else PassportManager()
        self.tool_registry = ToolRegistry()
        self.behavior_contract = BehaviorContract(self.passport_manager)

        self._register_default_tools()

        self.execution_engine = ExecutionEngine(
            passport_manager=self.passport_manager,
            tool_registry=self.tool_registry,
            behavior_contract=self.behavior_contract
        )

    def _register_default_tools(self) -> None:
        """Dynamically register all domain tools."""
        self.tool_registry.register(EnergyConsumptionAnalyzerTool())
        self.tool_registry.register(ApplianceEnergyAnalyzerTool())
        self.tool_registry.register(EnergyPatternDetectorTool())
        self.tool_registry.register(EnergyAnomalyDetectorTool())
        self.tool_registry.register(EnergyCostEstimatorTool())
        self.tool_registry.register(EnergyRecommendationTool())
        self.tool_registry.register(EnergyReportTool())

    def handle_request(self, capability: str, input_payload: Any, **kwargs) -> Dict[str, Any]:
        """Processes request through explicit lifecycle transitions."""
        tracker = ExecutionStateTracker()

        # INPUT -> REQUEST_VALIDATION
        tracker.transition_to(LifecycleState.REQUEST_VALIDATION)

        # PASSPORT_LOADING
        tracker.transition_to(LifecycleState.PASSPORT_LOADING)

        # CAPABILITY_VALIDATION
        tracker.transition_to(LifecycleState.CAPABILITY_VALIDATION)

        # TOOL_DISCOVERY
        tracker.transition_to(LifecycleState.TOOL_DISCOVERY)

        # TOOL_EXECUTION
        tracker.transition_to(LifecycleState.TOOL_EXECUTION)
        response = self.execution_engine.execute_request(capability, input_payload, **kwargs)

        # RESULT_VALIDATION
        tracker.transition_to(LifecycleState.RESULT_VALIDATION)

        # RESPONSE_GENERATION
        tracker.transition_to(LifecycleState.RESPONSE_GENERATION)

        if response.get("status") == "success":
            tracker.transition_to(LifecycleState.COMPLETED)
        else:
            tracker.transition_to(LifecycleState.FAILED)

        response["metadata"]["lifecycle"] = tracker.to_dict()
        return response
