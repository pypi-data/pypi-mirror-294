from mkdocs.commands import serve
from pathlib import Path

config_file = str(Path(__file__).parent / "mkdocs.yml")

kwargs = {
    "dev_addr": None,
    "open_in_browser": False,
    "livereload": True,
    "build_type": None,
    "watch_theme": True,
    "config_file": config_file,
    "strict": None,
    "theme": None,
    "use_directory_urls": None,
}
serve.serve(**kwargs)
