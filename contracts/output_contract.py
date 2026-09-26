from datetime import datetime, timezone
from typing import Any, Dict, Optional

class OutputContract:
    """Standardized output response formatter."""

    @staticmethod
    def success(
        capability: str,
        tool: str,
        result: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        base_meta = {
            "agent_id": "smart-home-energy-agent-01",
            "agent_name": "smart-home-energy-agent",
            "version": "1.0.0",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        if metadata:
            base_meta.update(metadata)

        return {
            "status": "success",
            "capability": capability,
            "tool": tool,
            "result": result,
            "metadata": base_meta
        }

    @staticmethod
    def error(
        code: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        capability: Optional[str] = None,
        tool: Optional[str] = None
    ) -> Dict[str, Any]:
        return {
            "status": "error",
            "code": code,
            "message": message,
            "details": details or {},
            "capability": capability,
            "tool": tool,
            "metadata": {
                "agent_id": "smart-home-energy-agent-01",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        }
