from pathlib import Path
from typing import Callable

import pytest

from jupyterclearcheck.utils.notebook_path import NotebookPath


@pytest.fixture
def temp_file(tmp_path: Path) -> Callable[[str], Path]:
    def _create_temp_file(filename: str) -> Path:
        path = tmp_path / filename
        path.touch()  # Create the file for testing
        return path

    return _create_temp_file


@pytest.fixture
def temp_dir(tmp_path: Path) -> Callable[[str], Path]:
    def _create_temp_dir(dirname: str) -> Path:
        dir_path = tmp_path / dirname
        dir_path.mkdir(parents=True, exist_ok=True)  # Create the directory
        return dir_path

    return _create_temp_dir


class TestNotebookPath:
    def test_initializes_with_valid_ipynb_path(
        self, temp_file: Callable[[str], Path]
    ) -> None:
        # Given
        valid_file_path = temp_file("valid_notebook.ipynb")

        # When
        notebook_path = NotebookPath(path=valid_file_path)

        # Then
        assert notebook_path.path == valid_file_path

    def test_raises_file_not_found_error_for_non_existing_path(self) -> None:
        # Given
        non_existing_path = Path("non_existing.ipynb")

        # When, Then
        with pytest.raises(FileNotFoundError):
            NotebookPath(path=non_existing_path)

    def test_raises_value_error_for_non_file_path(
        self, temp_dir: Callable[[str], Path]
    ) -> None:
        # Given
        non_file_path = temp_dir("non_file")

        # When, Then
        with pytest.raises(ValueError):
            NotebookPath(path=non_file_path)

    def test_raises_value_error_for_non_ipynb_file(
        self, temp_file: Callable[[str], Path]
    ) -> None:
        # Given
        non_ipynb_path = temp_file("non_ipynb_file.txt")

        # When, Then
        with pytest.raises(ValueError):
            NotebookPath(path=non_ipynb_path)
