from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown



def get_readme_content():
    readme_path = Path(__file__).parent.parent / 'README.md'
    return readme_path.read_text(encoding='utf-8')

MARKDOWN = get_readme_content()

# ...existing code...
console = Console()
md = Markdown(MARKDOWN)
md = console.print(md)