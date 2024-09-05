import dataclasses
from pathlib import Path


@dataclasses.dataclass
class NotebookPath:
    path: Path

    def __post_init__(self) -> None:
        if not self.path.exists():
            raise FileNotFoundError(f"The notebook file {self.path} does not exist.")
        if not self.path.is_file():
            raise ValueError(f"The path {self.path} is not a file.")
        if self.path.suffix != ".ipynb":
            raise ValueError(
                f"The file {self.path} is not a Jupyter Notebook (.ipynb)."
            )
