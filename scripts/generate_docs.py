import ast
from pathlib import Path

# Define paths
PROJECT_ROOT = Path(__file__).parent.parent
SCRAPERS_DIR = PROJECT_ROOT / "src" / "webquest" / "scrapers"
DOCS_DIR = PROJECT_ROOT / "docs" / "scrapers"
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
    """Generates documentation for all scrapers."""

    # Ensure docs directory exists
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    scrapers = []

    # Iterate over directories in scrapers folder
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

            print(f"Processing {title} ({module_name})...")

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

    # Sort scrapers by name
    scrapers.sort(key=lambda x: x["name"])

    # Update mkdocs.yaml
    update_mkdocs_nav(scrapers)

    # Update index.md
    update_index_md(scrapers)


def update_mkdocs_nav(scrapers):
    """Updates the nav section in mkdocs.yaml."""
    import yaml

    with open(MKDOCS_FILE, "r", encoding="utf-8") as f:
        mkdocs_config = yaml.safe_load(f)

    # Find or create Scrapers section in nav
    nav = mkdocs_config.get("nav", [])
    scrapers_nav = None

    for item in nav:
        if isinstance(item, dict) and "Scrapers" in item:
            scrapers_nav = item["Scrapers"]
            break

    if scrapers_nav is None:
        scrapers_nav = []
        nav.append({"Scrapers": scrapers_nav})

    # Rebuild scrapers list to ensure it matches current state
    # We'll just replace the list with what we found
    new_scrapers_list = [{s["name"]: s["file"]} for s in scrapers]

    # Update the config
    for item in nav:
        if isinstance(item, dict) and "Scrapers" in item:
            item["Scrapers"] = new_scrapers_list
            break

    mkdocs_config["nav"] = nav

    with open(MKDOCS_FILE, "w", encoding="utf-8") as f:
        yaml.dump(mkdocs_config, f, sort_keys=False, allow_unicode=True)

    print("Updated mkdocs.yaml")


def update_index_md(scrapers):
    """Updates the Scrapers section in docs/index.md."""
    if not INDEX_FILE.exists():
        print(f"Warning: {INDEX_FILE} does not exist.")
        return

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    header = "## Scrapers"
    if header not in content:
        # Append if not found
        new_content = content.strip() + "\n\n" + header + "\n\n"
    else:
        # Keep content before header
        new_content = content.split(header)[0] + header + "\n\n"

    # Generate list
    links = []
    for scraper in scrapers:
        name = scraper["name"]
        file_path = scraper["file"]
        links.append(f"- [{name}]({file_path})")

    new_content += "\n".join(links) + "\n"

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Updated {INDEX_FILE}")


if __name__ == "__main__":
    generate_docs()
