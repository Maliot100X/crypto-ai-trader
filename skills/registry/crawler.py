"""Repository Crawler - Discovers skills from external repositories."""
import os
import json
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

# External repositories to crawl for skills
SKILL_REPOSITORIES = [
    {"url": "https://github.com/solana-foundation/awesome-solana-ai", "category": "solana_ai"},
    {"url": "https://github.com/VoltAgent/awesome-openclaw-skills", "category": "openclaw"},
    {"url": "https://github.com/sundial-org/awesome-openclaw-skills", "category": "openclaw"},
    {"url": "https://github.com/mvanhorn/last30days-skill", "category": "openclaw"},
    {"url": "https://github.com/mergisi/awesome-openclaw-agents", "category": "agents"},
    {"url": "https://github.com/Panniantong/Agent-Reach", "category": "agent_framework"},
    {"url": "https://github.com/affaan-m/everything-claude-code", "category": "ai_coding"},
    {"url": "https://github.com/obra/superpowers", "category": "ai_orchestration"},
    {"url": "https://github.com/evan-kolberg/prediction-market-backtesting", "category": "backtesting"},
]

SKILL_REGISTRIES = [
    "https://skills.sh",
    "https://cryptoskill.org",
]


class RepositoryCrawler:
    """Crawls repositories and registries to discover skills."""

    def __init__(self, cache_dir: str = ".skill_cache"):
        self.cache_dir = cache_dir
        self.discovered_skills: List[Dict[str, Any]] = []

    def crawl_local_skills(self, skills_dir: str = "skills") -> List[Dict[str, Any]]:
        """Scan local skills directory for skill definitions."""
        skills = []
        if not os.path.exists(skills_dir):
            return skills

        for entry in os.listdir(skills_dir):
            skill_path = os.path.join(skills_dir, entry)
            if os.path.isdir(skill_path):
                skill_md = os.path.join(skill_path, "SKILL.md")
                skill_json = os.path.join(skill_path, "skill.json")

                if os.path.exists(skill_md):
                    skill = self._parse_skill_md(skill_md, entry)
                    if skill:
                        skills.append(skill)
                elif os.path.exists(skill_json):
                    skill = self._parse_skill_json(skill_json, entry)
                    if skill:
                        skills.append(skill)
                else:
                    skills.append({
                        "name": entry,
                        "description": f"Skill module: {entry}",
                        "source": skill_path,
                        "category": "local",
                    })

        self.discovered_skills.extend(skills)
        return skills

    def _parse_skill_md(self, filepath: str, default_name: str) -> Dict[str, Any]:
        try:
            with open(filepath, "r") as f:
                content = f.read()
            name = default_name
            description = ""
            for line in content.split("\n"):
                stripped = line.strip()
                if stripped.startswith("# "):
                    name = stripped[2:].strip()
                elif stripped and not stripped.startswith("#") and not description:
                    description = stripped
            return {"name": name, "description": description, "source": filepath, "category": "local"}
        except Exception as e:
            logger.error(f"Error parsing {filepath}: {e}")
            return None

    def _parse_skill_json(self, filepath: str, default_name: str) -> Dict[str, Any]:
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
            return {
                "name": data.get("name", default_name),
                "description": data.get("description", ""),
                "parameters": data.get("parameters", {}),
                "source": filepath,
                "category": data.get("category", "local"),
            }
        except Exception as e:
            logger.error(f"Error parsing {filepath}: {e}")
            return None

    def get_repository_manifest(self) -> List[Dict[str, str]]:
        """Return the list of external repositories to crawl."""
        return SKILL_REPOSITORIES

    def get_registry_urls(self) -> List[str]:
        return SKILL_REGISTRIES

    def get_discovered_skills(self) -> List[Dict[str, Any]]:
        return self.discovered_skills

    def export_registry(self) -> Dict[str, Any]:
        return {
            "total_skills": len(self.discovered_skills),
            "repositories": len(SKILL_REPOSITORIES),
            "registries": len(SKILL_REGISTRIES),
            "skills": self.discovered_skills,
        }
