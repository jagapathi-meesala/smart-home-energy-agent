from typing import Any, Callable, Dict, List, Optional, Tuple

class BaseTool:
    """Abstract base interface for deterministic local domain tools."""

    name: str = ""
    description: str = ""
    capability: str = ""

    def execute(self, records: List[Dict[str, Any]], **kwargs) -> Tuple[bool, Dict[str, Any], Optional[Dict[str, Any]]]:
        raise NotImplementedError("Tool execution logic must be implemented in subclasses.")

class ToolRegistry:
    """Dynamic tool registry supporting tool registration, lookup, and execution."""

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        if not hasattr(tool, "name") or not tool.name:
            raise ValueError("Tool must have a non-empty 'name' attribute.")
        self._tools[tool.name] = tool

    def get(self, tool_name: str) -> Optional[BaseTool]:
        return self._tools.get(tool_name)

    def exists(self, tool_name: str) -> bool:
        return tool_name in self._tools

    def list(self) -> List[str]:
        return list(self._tools.keys())

    def get_tool_for_capability(self, capability: str) -> Optional[BaseTool]:
        for tool in self._tools.values():
            if getattr(tool, "capability", "") == capability:
                return tool
        return None

    def execute(self, tool_name: str, records: List[Dict[str, Any]], **kwargs) -> Tuple[bool, Dict[str, Any], Optional[Dict[str, Any]]]:
        tool = self.get(tool_name)
        if not tool:
            return False, {}, {
                "code": "TOOL_NOT_FOUND",
                "message": f"Tool '{tool_name}' is not registered in ToolRegistry."
            }
        try:
            return tool.execute(records, **kwargs)
        except Exception as e:
            return False, {}, {
                "code": "TOOL_EXECUTION_FAILED",
                "message": f"Error executing tool '{tool_name}': {str(e)}"
            }
