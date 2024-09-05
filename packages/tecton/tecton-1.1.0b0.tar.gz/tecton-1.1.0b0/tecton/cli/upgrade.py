from collections import defaultdict
from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple

import click
import yaspin.spinners

from tecton.cli import cli_utils
from tecton.cli import printer
from tecton.cli.command import TectonCommand
from tecton.repo_utils import _import_module_with_pretty_errors
from tecton_core import conf
from tecton_core import repo_file_handler


def analyze_tecton_imports(
    file_path: Path, repo_root: Path, py_files: List[Path]
) -> Tuple[Dict[str, List[str]], Set[str]]:
    module_path = cli_utils.py_path_to_module(file_path, repo_root)
    tecton_imports = defaultdict(list)
    tecton_objects = set()

    def before_error():
        # TODO: pretty_error
        print(f"\nError while processing: {file_path}")

    try:
        module = _import_module_with_pretty_errors(file_path, module_path, py_files, repo_root, before_error)

        for name, obj in module.__dict__.items():
            if hasattr(obj, "__module__") and obj.__module__.startswith("tecton"):
                tecton_imports[name].append(obj.__module__)
                tecton_objects.add(name)

    except Exception as e:
        print(f"Unexpected error processing {file_path}: {str(e)}")

    return dict(tecton_imports), tecton_objects


def process_files(py_files: List[Path], repo_root: Path):
    with printer.safe_yaspin(yaspin.spinners.Spinners.earth, text="Analyzing feature repository modules") as sp:
        for file_path in py_files:
            sp.text = f"Processing {file_path.relative_to(repo_root)}"
            tecton_imports, tecton_objects = analyze_tecton_imports(file_path, repo_root, py_files)

            # TODO: Print something useful for the customer here instead of printing something useful for myself
            print(f"\nAnalyzing: {file_path}")
            print("=" * 50)
            for obj, paths in tecton_imports.items():
                print(f"{obj}: {', '.join(paths)}")

            print("\nTecton objects used:")
            for obj in tecton_objects:
                print(f"- {obj}")
            print()

        num_files = len(py_files)
        sp.text = (
            f"Analyzed {num_files} Python {cli_utils.plural(num_files, 'file', 'files')} from the feature repository"
        )
        sp.ok(printer.safe_string("✅"))


@click.command(cls=TectonCommand)
@click.argument("path", required=False)
def upgrade(path: Optional[str] = None):
    """Analyze Tecton imports in the feature repository.

    If PATH is provided, analyze the specified file or directory.
    If PATH is not provided, analyze all Python files in the repository root.
    """
    repo_file_handler.ensure_prepare_repo()
    repo_root = repo_file_handler.repo_root()
    repo_files = repo_file_handler.repo_files()
    py_files = [p for p in repo_files if p.suffix == ".py"]

    if path:
        full_path = Path(path).resolve()
        if full_path.is_file():
            py_files = [full_path]
        elif full_path.is_dir():
            py_files = [p for p in full_path.rglob("*.py") if p.is_file()]
        else:
            print(f"Error: {full_path} is not a valid file or directory.")
            return

    # Skip `validate` so that it is safe to execute 0.9 objects
    with conf._temporary_set("TECTON_SKIP_OBJECT_VALIDATION", True), conf._temporary_set(
        "TECTON_REQUIRE_SCHEMA", False
    ):
        process_files(py_files, Path(repo_root))
