"""Skill Loader - Dynamically discovers and loads skills from repositories."""
import os
import json
import logging
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class SkillDefinition:
    """Schema for a registered skill."""
    name: str
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    execution_handler: Optional[str] = None
    permissions: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    source: str = "local"
    version: str = "1.0.0"
    enabled: bool = True


class SkillLoader:
    """Dynamic skill discovery and loading system."""

    SKILL_FILE_PATTERNS = ["SKILL.md", "skill.json", "skill.yaml", "skill.yml"]

    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = skills_dir
        self.loaded_skills: Dict[str, SkillDefinition] = {}
        self._handlers: Dict[str, Callable] = {}

    def scan_directory(self, path: Optional[str] = None) -> List[SkillDefinition]:
        """Scan a directory tree for skill definitions."""
        scan_path = path or self.skills_dir
        discovered = []
        if not os.path.exists(scan_path):
            logger.warning(f"Skills directory not found: {scan_path}")
            return discovered
        for root, _dirs, files in os.walk(scan_path):
            for pattern in self.SKILL_FILE_PATTERNS:
                if pattern in files:
                    skill = self._parse_skill_file(os.path.join(root, pattern))
                    if skill:
                        discovered.append(skill)
                    break
        logger.info(f"Discovered {len(discovered)} skills in {scan_path}")
        return discovered

    def _parse_skill_file(self, filepath: str) -> Optional[SkillDefinition]:
        """Parse a skill definition file."""
        try:
            if filepath.endswith(".json"):
                with open(filepath, "r") as f:
                    data = json.load(f)
                return SkillDefinition(
                    name=data.get("name", os.path.basename(os.path.dirname(filepath))),
                    description=data.get("description", ""),
                    parameters=data.get("parameters", {}),
                    execution_handler=data.get("execution_handler"),
                    permissions=data.get("permissions", []),
                    dependencies=data.get("dependencies", []),
                    source=filepath,
                )
            elif filepath.endswith(".md"):
                with open(filepath, "r") as f:
                    content = f.read()
                name = os.path.basename(os.path.dirname(filepath))
                description = ""
                for line in content.split("\n"):
                    stripped = line.strip()
                    if stripped.startswith("# "):
                        name = stripped[2:].strip()
                    elif stripped and not stripped.startswith("#") and not description:
                        description = stripped
                return SkillDefinition(name=name, description=description or f"Skill from {filepath}", source=filepath)
        except Exception as e:
            logger.error(f"Error parsing skill file {filepath}: {e}")
        return None

    def register_skill(self, skill: SkillDefinition, handler: Optional[Callable] = None) -> bool:
        """Register a skill in the runtime."""
        self.loaded_skills[skill.name] = skill
        if handler:
            self._handlers[skill.name] = handler
        logger.info(f"Registered skill: {skill.name}")
        return True

    def load_all(self, path: Optional[str] = None) -> int:
        """Discover and register all skills."""
        skills = self.scan_directory(path)
        for skill in skills:
            self.register_skill(skill)
        return len(skills)

    def get_skill(self, name: str) -> Optional[SkillDefinition]:
        """Get a registered skill by name."""
        return self.loaded_skills.get(name)

    async def execute_skill(self, name: str, params: Dict[str, Any] = None) -> Any:
        """Execute a registered skill."""
        if name not in self.loaded_skills:
            raise ValueError(f"Skill not found: {name}")
        if name in self._handlers:
            handler = self._handlers[name]
            return await handler(**(params or {})) if asyncio.iscoroutinefunction(handler) else handler(**(params or {}))
        return {"status": "executed", "skill": name, "params": params}

    def list_skills(self) -> List[Dict[str, str]]:
        """List all registered skills."""
        return [{"name": s.name, "description": s.description, "source": s.source} for s in self.loaded_skills.values()]

    def export_registry(self) -> Dict[str, Any]:
        """Export the skill registry."""
        return {
            "total_skills": len(self.loaded_skills),
            "skills": {name: {"description": s.description, "version": s.version, "enabled": s.enabled}
                       for name, s in self.loaded_skills.items()},
        }


import asyncio  # noqa: E402 - needed for execute_skill
