import nbformat
import unittest

from mock import call, patch

from . import get_notebook_path

from ..log import logger
from ..preprocess import PapermillExecutePreprocessor

class TestPapermillExecutePreprocessor(unittest.TestCase):
    def setUp(self):
        self.nb = nbformat.read(
            get_notebook_path('test_logging.ipynb'), as_version=4)
        self.preprocessor = PapermillExecutePreprocessor(log=logger)
        self.preprocessor.nb = self.nb

    def test_logging_stderr_msg(self):
        with patch.object(logger, 'warning') as warning_mock:
            for output in self.nb.cells[0].get("outputs", []):
                self.preprocessor.log_output_message(output)
            warning_mock.assert_called_once_with("INFO:test:test text\n")

    def test_logging_stdout_msg(self):
        with patch.object(logger, 'info') as info_mock:
            for output in self.nb.cells[1].get("outputs", []):
                self.preprocessor.log_output_message(output)
            info_mock.assert_called_once_with("hello world\n")

    def test_logging_data_msg(self):
        with patch.object(logger, 'info') as info_mock:
            for output in self.nb.cells[2].get("outputs", []):
                self.preprocessor.log_output_message(output)
            info_mock.assert_has_calls([
                call("<matplotlib.axes._subplots.AxesSubplot at 0x7f8391f10290>"),
                call("<matplotlib.figure.Figure at 0x7f830af7b350>"),
            ])
