import os
from pathlib import Path
from typing import Optional

class Settings:
    """Dynamic configuration manager for SmartHomeEnergyAgent."""
    
    def __init__(self, base_dir: Optional[Path] = None):
        if base_dir is None:
            self.BASE_DIR = Path(__file__).resolve().parent.parent
        else:
            self.BASE_DIR = Path(base_dir).resolve()
            
        self.PASSPORT_PATH = self.BASE_DIR / "agent.yaml"
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        self.OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
        self.DEFAULT_TARIFF = float(os.getenv("DEFAULT_TARIFF", "0.15"))
        self.ALLOW_EXTERNAL_PROVIDERS = os.getenv("ALLOW_EXTERNAL_PROVIDERS", "true").lower() in ("true", "1", "yes")

    def to_dict(self) -> dict:
        return {
            "BASE_DIR": str(self.BASE_DIR),
            "PASSPORT_PATH": str(self.PASSPORT_PATH),
            "OPENAI_MODEL": self.OPENAI_MODEL,
            "DEFAULT_TARIFF": self.DEFAULT_TARIFF,
            "HAS_OPENAI_KEY": bool(self.OPENAI_API_KEY.strip()),
            "ALLOW_EXTERNAL_PROVIDERS": self.ALLOW_EXTERNAL_PROVIDERS
        }

settings = Settings()
