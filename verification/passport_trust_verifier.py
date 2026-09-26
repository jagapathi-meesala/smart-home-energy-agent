from typing import Any, Dict
from core.agent_core import AgentCore
from passport.passport_manager import PassportManager

class PassportTrustVerifier:
    """Dynamically verifies Passport trust, identity, capabilities, and tool consistency."""

    def verify(self) -> Dict[str, Any]:
        details = []
        try:
            mgr = PassportManager()
            agent_core = AgentCore()

            # 1. Identity & Version check
            agent_info = mgr.get_agent_info()
            if not agent_info.get("name") or not agent_info.get("id") or not agent_info.get("version"):
                details.append("Passport agent identity fields missing (name, id, or version).")
            else:
                details.append(f"Identity verified: {agent_info['name']} (ID: {agent_info['id']}, v{agent_info['version']})")

            # 2. Capabilities consistency
            caps = mgr.get_capabilities()
            if not caps:
                details.append("No capabilities defined in Agent Passport.")
            else:
                details.append(f"Discovered {len(caps)} capabilities dynamically: {caps}")

            # 3. Tools consistency & Registry matching
            tools = mgr.get_tools()
            if not tools:
                details.append("No tools defined in Agent Passport.")
            else:
                details.append(f"Discovered {len(tools)} tools dynamically: {tools}")

            registry_tools = agent_core.tool_registry.list()
            missing_in_registry = [t for t in tools if t not in registry_tools]
            if missing_in_registry:
                details.append(f"Tools in Passport missing from ToolRegistry: {missing_in_registry}")
            else:
                details.append("All Passport tools exist in ToolRegistry.")

            # 4. Capability -> Tool Mapping check
            unmapped_caps = []
            for cap in caps:
                mapped_tool = mgr.get_tool_for_capability(cap)
                if not mapped_tool or not agent_core.tool_registry.exists(mapped_tool):
                    unmapped_caps.append(cap)

            if unmapped_caps:
                details.append(f"Capabilities without registered tools: {unmapped_caps}")

            passed = (len(missing_in_registry) == 0 and len(unmapped_caps) == 0 and len(caps) > 0)
            status = "PASSED" if passed else "FAILED"

            return {
                "status": status,
                "verifier": "PassportTrustVerifier",
                "details": details,
                "dynamic_metrics": {
                    "capabilities_count": len(caps),
                    "tools_count": len(tools),
                    "registry_tools_count": len(registry_tools)
                }
            }
        except Exception as e:
            return {
                "status": "UNCERTAIN",
                "verifier": "PassportTrustVerifier",
                "details": [f"Verification encountered exception: {str(e)}"]
            }
