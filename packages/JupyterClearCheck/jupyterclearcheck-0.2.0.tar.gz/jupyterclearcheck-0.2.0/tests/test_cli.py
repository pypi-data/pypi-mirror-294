from pathlib import Path

import pytest
import pytest_mock
from nbformat import NotebookNode
from nbformat import v4 as nbf

from jupyterclearcheck.cli import (
    check_notebook_outputs,
    has_output_cells,
    read_notebook,
)
from jupyterclearcheck.utils.notebook_exception import NotebookOutputFoundException
from jupyterclearcheck.utils.notebook_path import NotebookPath


class TestReadNotebook:
    def test_read_valid_notebook(self, mocker: pytest_mock.MockerFixture) -> None:
        # Given
        mock_path = mocker.Mock(spec=Path)
        mock_path.suffix = ".ipynb"
        mock_path.exists.return_value = True
        mock_path.is_file.return_value = True
        mock_path.open = mocker.mock_open(
            read_data='{"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 5}'  # noqa: E501
        )
        notebook_path = NotebookPath(path=mock_path)

        # When
        result = read_notebook(notebook_path)

        # Then
        assert isinstance(result, NotebookNode)


class TestCodeUnderTest:
    def test_returns_true_if_notebook_has_output_cells(self) -> None:
        # Given
        nb = nbf.new_notebook()  # type: ignore
        nb.cells.append(
            nbf.new_code_cell(  # type: ignore
                "print('Hello, world!')",
                outputs=[nbf.new_output(output_type="stream", text="Hello, world!")],  # type: ignore
            )
        )

        # When
        result = has_output_cells(nb)

        # Then
        assert result is True

    def test_returns_false_if_notebook_has_no_output_cells(self) -> None:
        # Given
        nb = nbf.new_notebook()  # type: ignore

        # When
        result = has_output_cells(nb)

        # Then
        assert result is False


class TestCheckNotebookOutputs:
    def test_raises_exception_when_output_cells_present(
        self, mocker: pytest_mock.MockerFixture
    ) -> None:
        # Given
        mock_path = mocker.Mock(spec=Path)
        mock_path.exists.return_value = True
        mock_path.is_file.return_value = True
        mock_path.suffix = ".ipynb"

        notebook_path = NotebookPath(path=mock_path)

        mock_cell = mocker.Mock(spec=NotebookNode)
        mock_cell.cell_type = "code"
        mock_cell.outputs = ["output"]

        mock_notebook = mocker.Mock(spec=NotebookNode)
        mock_notebook.cells = [mock_cell]

        mocker.patch("jupyterclearcheck.cli.read_notebook", return_value=mock_notebook)

        # When / Then
        with pytest.raises(
            NotebookOutputFoundException, match="Output cells found in the notebook."
        ):
            check_notebook_outputs(notebook_path)

    def test_prints_confirmation_message_when_no_output_cells_found(
        self, mocker: pytest_mock.MockerFixture, capsys: pytest.CaptureFixture[str]
    ) -> None:
        # Given
        mock_path = mocker.Mock(spec=Path)
        mock_path.exists.return_value = True
        mock_path.is_file.return_value = True
        mock_path.suffix = ".ipynb"

        notebook_path = NotebookPath(path=mock_path)
        mock_notebook = mocker.Mock(spec=NotebookNode)
        mock_notebook.cells = []

        mocker.patch("jupyterclearcheck.cli.read_notebook", return_value=mock_notebook)

        # When
        check_notebook_outputs(notebook_path)

        # Then
        assert "No output cells found in the notebook." in capsys.readouterr().out
