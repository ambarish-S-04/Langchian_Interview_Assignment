import os
from pathlib import Path
from typing import List, Optional

def ensure_directory_exists(directory: str) -> None:
    Path(directory).mkdir(parents=True, exist_ok=True)

def get_story_files(stories_dir: str = "../data/stories") -> List[str]:
    stories_dir_path = Path(stories_dir)
    story_files = list(stories_dir_path.glob("*.txt"))
    return [str(file) for file in story_files]

def validate_character_name(name: str) -> bool:
    if not name or not name.strip():
        return False
    return all(c.isalpha() or c.isspace() or c in "-'" for c in name)

def format_character_info(info: dict) -> str:
    if "error" in info:
        return f"Error: {info['error']}"

    if not isinstance(info, dict):
        return f"Error: Invalid data format received"

    formatted = []

    if 'name' in info:
        formatted.append(f"Name: {info['name']}")

    if 'storyTitle' in info:
        formatted.append(f"Story: {info['storyTitle']}")
    elif 'story' in info:
        formatted.append(f"Story: {info['story']}")

    if 'characterType' in info:
        formatted.append(f"Type: {info['characterType'].title()}")
    elif 'type' in info:
        formatted.append(f"Type: {info['type'].title()}")

    if 'occupation' in info:
        formatted.append(f"Occupation: {info['occupation']}")

    if 'summary' in info:
        formatted.append("\nSummary:")
        formatted.append(info['summary'])

    if 'responsibilities' in info:
        formatted.append("\nResponsibilities:")
        if isinstance(info['responsibilities'], list):
            for resp in info['responsibilities']:
                formatted.append(f"- {resp}")
        else:
            formatted.append(str(info['responsibilities']))

    if 'skills' in info:
        formatted.append("\nSkills:")
        if isinstance(info['skills'], list):
            for skill in info['skills']:
                formatted.append(f"- {skill}")
        else:
            formatted.append(str(info['skills']))

    if 'characteristics' in info:
        formatted.append("\nCharacteristics:")
        if isinstance(info['characteristics'], list):
            for char in info['characteristics']:
                formatted.append(f"- {char}")
        else:
            formatted.append(str(info['characteristics']))

    relations_key = None
    if 'relations' in info:
        relations_key = 'relations'
    elif 'relationships' in info:
        relations_key = 'relationships'

    if relations_key:
        formatted.append("\nRelations:")
        if isinstance(info[relations_key], list):
            for rel in info[relations_key]:
                if isinstance(rel, dict):
                    if 'name' in rel and 'relation' in rel:
                        formatted.append(f"- {rel['name']}: {rel['relation']}")
                    elif 'name' in rel:
                        formatted.append(f"- {rel['name']}")
                    else:
                        formatted.append(f"- {rel}")
                else:
                    formatted.append(f"- {rel}")
        else:
            formatted.append(str(info[relations_key]))

    if 'significant_actions' in info:
        formatted.append("\nSignificant Actions:")
        if isinstance(info['significant_actions'], list):
            for action in info['significant_actions']:
                formatted.append(f"- {action}")
        else:
            formatted.append(str(info['significant_actions']))

    for key, value in info.items():
        if key not in ['name', 'storyTitle', 'story', 'characterType', 'type', 'occupation', 
                      'summary', 'responsibilities', 'skills', 'characteristics', 'relations', 
                      'relationships', 'significant_actions', 'error']:
            formatted.append(f"\n{key.title()}:")
            if isinstance(value, list):
                for item in value:
                    formatted.append(f"- {item}")
            else:
                formatted.append(str(value))

    return "\n".join(formatted) if formatted else "No character information available."