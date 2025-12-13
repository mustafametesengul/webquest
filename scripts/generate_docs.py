import ast
from pathlib import Path

import yaml

# Define paths
PROJECT_ROOT = Path(__file__).parent.parent
SCRAPERS_DIR = PROJECT_ROOT / "src" / "webquest" / "scrapers"
BROWSERS_DIR = PROJECT_ROOT / "src" / "webquest" / "browsers"
DOCS_DIR = PROJECT_ROOT / "docs" / "scrapers"
DOCS_BROWSERS_DIR = PROJECT_ROOT / "docs" / "browsers"
MKDOCS_FILE = PROJECT_ROOT / "mkdocs.yaml"
INDEX_FILE = PROJECT_ROOT / "docs" / "index.md"

# Template for the scraper documentation
DOC_TEMPLATE = """# {title}

::: webquest.scrapers.{module_name}.scraper.{class_name}
    options:
      heading_level: 3
      show_source: true
      show_root_heading: true
      show_root_full_path: false

## Request

::: webquest.scrapers.{module_name}.request.{request_class}
    options:
      heading_level: 3
      show_source: true
      show_root_heading: true
      show_root_full_path: false

## Response

::: webquest.scrapers.{module_name}.response.{response_class}
    options:
      heading_level: 3
      show_source: true
      show_root_heading: true
      show_root_full_path: false

{response_models}

## Settings

::: webquest.scrapers.{module_name}.settings.{settings_class}
    options:
      heading_level: 3
      show_source: true
      show_root_heading: true
      show_root_full_path: false
"""

BROWSER_DOC_TEMPLATE = """# {title}

::: webquest.browsers.{module_name}.{class_name}
    options:
      heading_level: 3
      show_source: true
      show_root_heading: true
      show_root_full_path: false

## Settings

::: webquest.browsers.{module_name}.{settings_class}
    options:
      heading_level: 3
      show_source: true
      show_root_heading: true
      show_root_full_path: false
"""

RESPONSE_MODEL_TEMPLATE = """::: webquest.scrapers.{module_name}.response.{model_name}
    options:
      heading_level: 3
      show_source: true
      show_root_heading: true
      show_root_full_path: false"""


def get_class_name(file_path: Path, base_class_name: str) -> str | None:
    """Extracts the class name inheriting from a specific base class in a file using AST."""
    if not file_path.exists():
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError:
            return None

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                # Check for direct base class name
                if isinstance(base, ast.Name) and base.id == base_class_name:
                    return node.name
                # Check for subscripted base class (e.g. Scraper[...])
                elif isinstance(base, ast.Subscript):
                    if (
                        isinstance(base.value, ast.Name)
                        and base.value.id == base_class_name
                    ):
                        return node.name
    return None


def get_response_models(file_path: Path, main_response_class: str) -> list[str]:
    """Extracts all BaseModel classes from response.py except the main response class."""
    if not file_path.exists():
        return []

    models = []
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError:
            return []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            is_model = False
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id == "BaseModel":
                    is_model = True
                    break

            if is_model and node.name != main_response_class:
                models.append(node.name)
    return models


def get_main_response_class(file_path: Path) -> str | None:
    """Finds the class that likely represents the main response."""
    if not file_path.exists():
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError:
            return None

    # First pass: look for a class ending in "Response"
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name.endswith("Response"):
            return node.name

    # Fallback: return the first BaseModel
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id == "BaseModel":
                    return node.name
    return None


def generate_docs():
    """Generates documentation for all scrapers and browsers."""

    # Ensure docs directories exist
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_BROWSERS_DIR.mkdir(parents=True, exist_ok=True)

    scrapers = []
    browsers = []

    # --- Scrapers ---
    for item in SCRAPERS_DIR.iterdir():
        if (
            item.is_dir()
            and (item / "scraper.py").exists()
            and item.name != "__pycache__"
        ):
            module_name = item.name
            title = (
                module_name.replace("_", " ")
                .title()
                .replace("Youtube", "YouTube")
                .replace("Duckduckgo", "DuckDuckGo")
            )

            print(f"Processing Scraper: {title} ({module_name})...")

            # Extract class names
            scraper_class = get_class_name(item / "scraper.py", "Scraper")
            request_class = get_class_name(item / "request.py", "BaseModel")

            # For request, sometimes it might be named differently or there might be multiple.
            # Usually there is one main request model.
            # Let's try to find one ending in Request if get_class_name returns the first one which might be wrong?
            # Actually get_class_name returns the *first* match.
            # Let's refine request finding too.
            if not request_class:
                # Try finding any class ending in Request
                pass  # Logic inside get_class_name is simple.

            response_class = get_main_response_class(item / "response.py")
            settings_class = get_class_name(item / "settings.py", "BaseSettings")

            if not all([scraper_class, request_class, response_class, settings_class]):
                print(
                    f"Skipping {module_name}: Missing classes. Scraper: {scraper_class}, Req: {request_class}, Res: {response_class}, Set: {settings_class}"
                )
                continue

            # Get other response models
            other_models = get_response_models(item / "response.py", response_class)
            response_models_str = "\n\n".join(
                [
                    RESPONSE_MODEL_TEMPLATE.format(
                        module_name=module_name, model_name=model
                    )
                    for model in other_models
                ]
            )

            # Generate Markdown content
            doc_content = DOC_TEMPLATE.format(
                title=title,
                module_name=module_name,
                class_name=scraper_class,
                request_class=request_class,
                response_class=response_class,
                settings_class=settings_class,
                response_models=response_models_str,
            )

            # Write to file
            doc_path = DOCS_DIR / f"{module_name}.md"
            with open(doc_path, "w", encoding="utf-8") as f:
                f.write(doc_content)

            scrapers.append({"name": title, "file": f"scrapers/{module_name}.md"})
            print(f"Generated {doc_path}")

    # --- Browsers ---
    for item in BROWSERS_DIR.glob("*.py"):
        if item.name in ["__init__.py", "browser.py"]:
            continue

        module_name = item.stem
        title = module_name.replace("_", " ").title()

        print(f"Processing Browser: {title} ({module_name})...")

        browser_class = get_class_name(item, "Browser")
        settings_class = get_class_name(item, "BaseSettings")

        if not all([browser_class, settings_class]):
            print(
                f"Skipping {module_name}: Missing classes. Browser: {browser_class}, Settings: {settings_class}"
            )
            continue

        doc_content = BROWSER_DOC_TEMPLATE.format(
            title=title,
            module_name=module_name,
            class_name=browser_class,
            settings_class=settings_class,
        )

        doc_path = DOCS_BROWSERS_DIR / f"{module_name}.md"
        with open(doc_path, "w", encoding="utf-8") as f:
            f.write(doc_content)

        browsers.append({"name": title, "file": f"browsers/{module_name}.md"})
        print(f"Generated {doc_path}")

    # Sort
    scrapers.sort(key=lambda x: x["name"])
    browsers.sort(key=lambda x: x["name"])

    # Update mkdocs.yaml
    update_mkdocs_nav(scrapers, browsers)

    # Update index.md
    update_index_md(scrapers, browsers)


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
