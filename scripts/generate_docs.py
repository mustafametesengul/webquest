import importlib
import inspect
import pkgutil
import re
import sys
from pathlib import Path
from typing import Any

from pydantic import BaseModel
from pydantic_core import PydanticUndefined

import webquest.browsers
import webquest.scrapers
from webquest.browsers.browser import Browser
from webquest.scrapers.scraper import Scraper

# Define paths
PROJECT_ROOT = Path(__file__).parent.parent
DOCS_SCRAPERS_DIR = PROJECT_ROOT / "docs" / "scrapers"
DOCS_BROWSERS_DIR = PROJECT_ROOT / "docs" / "browsers"


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


def format_type(annotation: Any) -> str:
    """Formats a type annotation into a readable string."""
    if annotation is None:
        return "None"

    type_str = str(annotation)
    type_str = type_str.replace("typing.", "")
    type_str = type_str.replace("<class '", "").replace("'>", "")

    # Remove module paths
    type_str = re.sub(r"(?:[\w]+\.)+([\w]+)", r"\1", type_str)

    return type_str


def model_to_markdown(model_cls: type[BaseModel]) -> str:
    """Generates Markdown documentation for a Pydantic model."""
    if not issubclass(model_cls, BaseModel):
        return ""

    # Use __doc__ directly to avoid inheriting docstrings from BaseSettings/BaseModel
    doc = model_cls.__doc__ or ""
    if doc:
        doc = inspect.cleandoc(doc)

    lines = [f"**{model_cls.__name__}**", "", doc, ""]

    fields = model_cls.model_fields
    if not fields:
        lines.append("_No fields_")
        return "\n".join(lines)

    lines.append("| Name | Type | Default | Description |")
    lines.append("|---|---|---|---|")

    for name, field in fields.items():
        type_str = format_type(field.annotation)

        if field.default == PydanticUndefined:
            if field.default_factory:
                default_str = "_Factory_"
            else:
                default_str = "**Required**"
        else:
            default_str = f"`{field.default}`"

        description = field.description or ""
        description = description.replace("\n", " ")

        lines.append(f"| `{name}` | `{type_str}` | {default_str} | {description} |")

    return "\n".join(lines)


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
        parts = scraper_cls.__module__.split(".")
        if "scrapers" in parts:
            idx = parts.index("scrapers")
            if idx + 1 < len(parts):
                module_name = parts[idx + 1]
            else:
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

        scraper_doc = scraper_cls.__doc__ or ""
        if scraper_doc:
            scraper_doc = inspect.cleandoc(scraper_doc)

        content_parts = [
            f"# {title}",
            "",
            scraper_doc,
            "",
            "## Settings",
            "",
            model_to_markdown(settings_cls),
            "",
            "## Request",
            "",
            model_to_markdown(request_cls),
            "",
            "## Response",
            "",
            model_to_markdown(response_cls),
        ]

        other_models = get_response_models(response_cls)
        if other_models:
            content_parts.append("")
            for model in other_models:
                content_parts.append(model_to_markdown(model))
                content_parts.append("")

        doc_content = "\n".join(content_parts)

        doc_path = DOCS_SCRAPERS_DIR / f"{module_name}.md"
        with open(doc_path, "w", encoding="utf-8") as f:
            f.write(doc_content)

        scrapers_list.append({"name": title, "file": f"scrapers/{module_name}.md"})
        print(f"Generated {doc_path}")

    # --- Browsers ---
    print("Discovering browsers...")
    found_browsers = find_subclasses(webquest.browsers, Browser)

    for browser_cls in found_browsers:
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

        browser_doc = browser_cls.__doc__ or ""
        if browser_doc:
            browser_doc = inspect.cleandoc(browser_doc)

        content_parts = [
            f"# {title}",
            "",
            browser_doc,
            "",
            "## Settings",
            "",
            model_to_markdown(settings_cls),
        ]

        doc_content = "\n".join(content_parts)

        doc_path = DOCS_BROWSERS_DIR / f"{module_name}.md"
        with open(doc_path, "w", encoding="utf-8") as f:
            f.write(doc_content)

        browsers_list.append({"name": title, "file": f"browsers/{module_name}.md"})
        print(f"Generated {doc_path}")

    # Sort
    scrapers_list.sort(key=lambda x: x["name"])
    browsers_list.sort(key=lambda x: x["name"])


if __name__ == "__main__":
    generate_docs()
