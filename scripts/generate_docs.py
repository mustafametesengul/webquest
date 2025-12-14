import importlib
import inspect
import pkgutil
import sys
from pathlib import Path

import yaml
from pydantic import BaseModel

import webquest.browsers
import webquest.scrapers
from webquest.browsers.browser import Browser
from webquest.scrapers.scraper import Scraper

# Define paths
PROJECT_ROOT = Path(__file__).parent.parent
DOCS_SCRAPERS_DIR = PROJECT_ROOT / "docs" / "scrapers"
DOCS_BROWSERS_DIR = PROJECT_ROOT / "docs" / "browsers"
MKDOCS_FILE = PROJECT_ROOT / "mkdocs.yaml"
INDEX_FILE = PROJECT_ROOT / "docs" / "index.md"

# Template for the scraper documentation
DOC_TEMPLATE = """# {title}

::: {scraper_full_path}
    options:
      heading_level: 3
      show_source: true
      show_root_heading: true
      show_root_full_path: false

## Settings

::: {settings_full_path}
    options:
      heading_level: 3
      show_source: true
      show_root_heading: true
      show_root_full_path: false

## Request

::: {request_full_path}
    options:
      heading_level: 3
      show_source: true
      show_root_heading: true
      show_root_full_path: false

## Response

::: {response_full_path}
    options:
      heading_level: 3
      show_source: true
      show_root_heading: true
      show_root_full_path: false

{response_models}
"""

BROWSER_DOC_TEMPLATE = """# {title}

::: {browser_full_path}
    options:
      heading_level: 3
      show_source: true
      show_root_heading: true
      show_root_full_path: false

## Settings

::: {settings_full_path}
    options:
      heading_level: 3
      show_source: true
      show_root_heading: true
      show_root_full_path: false
"""

RESPONSE_MODEL_TEMPLATE = """::: {model_full_path}
    options:
      heading_level: 3
      show_source: true
      show_root_heading: true
      show_root_full_path: false"""


def find_subclasses(package, base_class):
    """Recursively find all subclasses of base_class in the given package."""
    found = []
    if hasattr(package, "__path__"):
        for _, name, _ in pkgutil.walk_packages(
            package.__path__, package.__name__ + "."
        ):
            try:
                module = importlib.import_module(name)
                for _, obj in inspect.getmembers(module):
                    if (
                        inspect.isclass(obj)
                        and issubclass(obj, base_class)
                        and obj is not base_class
                    ):
                        # Check if the class is defined in this module (not imported)
                        # Or if it's defined in a sub-module of the package we are scanning
                        if obj.__module__.startswith(package.__name__):
                            found.append(obj)
            except Exception as e:
                print(f"Error importing {name}: {e}")
    return list(set(found))  # Deduplicate


def get_response_models(main_response_class: type[BaseModel]) -> list[type[BaseModel]]:
    """Extracts all BaseModel classes defined in the same module as the main response class."""
    module = sys.modules[main_response_class.__module__]
    models = []
    for _, obj in inspect.getmembers(module):
        if (
            inspect.isclass(obj)
            and issubclass(obj, BaseModel)
            and obj is not main_response_class
            and obj.__module__ == main_response_class.__module__
        ):
            models.append(obj)
    return models


def get_full_path(cls):
    return f"{cls.__module__}.{cls.__name__}"


def generate_docs():
    """Generates documentation for all scrapers and browsers."""

    # Ensure docs directories exist
    DOCS_SCRAPERS_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_BROWSERS_DIR.mkdir(parents=True, exist_ok=True)

    scrapers_list = []
    browsers_list = []

    # --- Scrapers ---
    print("Discovering scrapers...")
    found_scrapers = find_subclasses(webquest.scrapers, Scraper)

    for scraper_cls in found_scrapers:
        # Determine module name for file naming (e.g. youtube_search)
        # Assuming structure webquest.scrapers.<module_name>.scraper
        parts = scraper_cls.__module__.split(".")
        if "scrapers" in parts:
            idx = parts.index("scrapers")
            if idx + 1 < len(parts):
                module_name = parts[idx + 1]
            else:
                # Fallback if directly in scrapers or weird structure
                module_name = scraper_cls.__name__.lower()
        else:
            module_name = scraper_cls.__name__.lower()

        title = (
            module_name.replace("_", " ")
            .title()
            .replace("Youtube", "YouTube")
            .replace("Duckduckgo", "DuckDuckGo")
        )

        print(f"Processing Scraper: {title} ({scraper_cls.__name__})...")

        request_cls = scraper_cls.request_model
        response_cls = scraper_cls.response_model
        settings_cls = scraper_cls.settings_model

        # Get other response models
        other_models = get_response_models(response_cls)
        response_models_str = "\n\n".join(
            [
                RESPONSE_MODEL_TEMPLATE.format(model_full_path=get_full_path(model))
                for model in other_models
            ]
        )

        # Generate Markdown content
        doc_content = DOC_TEMPLATE.format(
            title=title,
            scraper_full_path=get_full_path(scraper_cls),
            request_full_path=get_full_path(request_cls),
            response_full_path=get_full_path(response_cls),
            settings_full_path=get_full_path(settings_cls),
            response_models=response_models_str,
        )

        # Write to file
        doc_path = DOCS_SCRAPERS_DIR / f"{module_name}.md"
        with open(doc_path, "w", encoding="utf-8") as f:
            f.write(doc_content)

        scrapers_list.append({"name": title, "file": f"scrapers/{module_name}.md"})
        print(f"Generated {doc_path}")

    # --- Browsers ---
    print("Discovering browsers...")
    found_browsers = find_subclasses(webquest.browsers, Browser)

    for browser_cls in found_browsers:
        # Determine module name
        # Assuming structure webquest.browsers.<module_name>
        parts = browser_cls.__module__.split(".")
        if "browsers" in parts:
            idx = parts.index("browsers")
            if idx + 1 < len(parts):
                module_name = parts[idx + 1]
            else:
                module_name = browser_cls.__name__.lower()
        else:
            module_name = browser_cls.__name__.lower()

        title = module_name.replace("_", " ").title()

        print(f"Processing Browser: {title} ({browser_cls.__name__})...")

        settings_cls = browser_cls.settings_model

        doc_content = BROWSER_DOC_TEMPLATE.format(
            title=title,
            browser_full_path=get_full_path(browser_cls),
            settings_full_path=get_full_path(settings_cls),
        )

        doc_path = DOCS_BROWSERS_DIR / f"{module_name}.md"
        with open(doc_path, "w", encoding="utf-8") as f:
            f.write(doc_content)

        browsers_list.append({"name": title, "file": f"browsers/{module_name}.md"})
        print(f"Generated {doc_path}")

    # Sort
    scrapers_list.sort(key=lambda x: x["name"])
    browsers_list.sort(key=lambda x: x["name"])

    # Update mkdocs.yaml
    update_mkdocs_nav(scrapers_list, browsers_list)

    # Update index.md
    update_index_md(scrapers_list, browsers_list)


def update_mkdocs_nav(scrapers, browsers):
    """Updates the nav section in mkdocs.yaml."""

    with open(MKDOCS_FILE, "r", encoding="utf-8") as f:
        mkdocs_config = yaml.safe_load(f)

    # Find or create Scrapers and Browsers section in nav
    nav = mkdocs_config.get("nav", [])

    # Helper to update a section
    def update_section(section_name, items):
        found = False
        new_list = [{item["name"]: item["file"]} for item in items]
        for nav_item in nav:
            if isinstance(nav_item, dict) and section_name in nav_item:
                nav_item[section_name] = new_list
                found = True
                break
        if not found:
            nav.append({section_name: new_list})

    update_section("Scrapers", scrapers)
    update_section("Browsers", browsers)

    mkdocs_config["nav"] = nav

    with open(MKDOCS_FILE, "w", encoding="utf-8") as f:
        yaml.dump(mkdocs_config, f, sort_keys=False, allow_unicode=True)

    print("Updated mkdocs.yaml")


def update_index_md(scrapers, browsers):
    """Updates the Scrapers and Browsers section in docs/index.md."""
    if not INDEX_FILE.exists():
        print(f"Warning: {INDEX_FILE} does not exist.")
        return

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # We need to reconstruct the file content.
    # Assuming the file starts with some intro, then has sections.
    # Simplest way is to find where "## Scrapers" starts and cut off everything after, then rebuild.
    # But now we have Browsers too.

    # Let's look for the first section header we manage.

    base_content = content
    if "## Scrapers" in content:
        base_content = content.split("## Scrapers")[0]
    elif "## Browsers" in content:
        base_content = content.split("## Browsers")[0]

    new_content = base_content.strip() + "\n\n"

    # Add Scrapers
    new_content += "## Scrapers\n\n"
    for scraper in scrapers:
        new_content += f"- [{scraper['name']}]({scraper['file']})\n"

    new_content += "\n"

    # Add Browsers
    new_content += "## Browsers\n\n"
    for browser in browsers:
        new_content += f"- [{browser['name']}]({browser['file']})\n"

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Updated {INDEX_FILE}")


if __name__ == "__main__":
    generate_docs()
