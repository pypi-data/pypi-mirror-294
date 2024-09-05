import argparse
from pathlib import Path

import nbformat
from nbformat import NotebookNode

from jupyterclearcheck.utils.notebook_exception import NotebookOutputFoundException
from jupyterclearcheck.utils.notebook_path import NotebookPath


def read_notebook(notebook_path: NotebookPath) -> NotebookNode:
    with notebook_path.path.open(encoding="utf-8") as f:
        return nbformat.read(f, as_version=4)  # type: ignore


def has_output_cells(nb: NotebookNode) -> bool:
    return any(cell.cell_type == "code" and cell.outputs for cell in nb.cells)


def check_notebook_outputs(notebook_path: NotebookPath) -> None:
    nb = read_notebook(notebook_path)
    if has_output_cells(nb):
        raise NotebookOutputFoundException("Output cells found in the notebook.")
    print("No output cells found in the notebook.")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="jupyterclearcheck",
        description="Check a Jupyter Notebook for output cells.",
    )
    parser.add_argument(
        "--notebook", type=Path, help="Path to the Jupyter Notebook file", required=True
    )
    args: argparse.Namespace = parser.parse_args()

    notebook_path = NotebookPath(args.notebook)
    check_notebook_outputs(notebook_path)


if __name__ == "__main__":
    main()
