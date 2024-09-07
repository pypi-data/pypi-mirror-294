import unittest
from unittest.mock import patch, mock_open
import supervisor_tee

class TestSupervisorStdout(unittest.TestCase):

    @patch('sys.stdout.write')
    def test_write_stdout(self, mock_write):
        supervisor_tee.write_stdout('test')
        mock_write.assert_called_once_with('test')

    @patch('sys.stderr.write')
    def test_write_stderr(self, mock_write):
        supervisor_tee.write_stderr('error')
        mock_write.assert_called_once_with('error')

    @patch('sys.stdout.write')
    def test_formatted_event_handler(self, mock_write):
        event = 'event'
        response = 'processname:myprocess channel:stdout\nThis is a log message'
        expected_output = 'myprocess stdout | This is a log message\n'
        
        with patch('builtins.print') as mock_print:
            supervisor_tee.formatted_event_handler(event, response.encode(), '{0} {1} | ')
            mock_print.assert_called_once_with(expected_output, flush=True)

    @patch('sys.stdout.write')
    def test_plain_event_handler(self, mock_write):
        event = 'event'
        response = 'processname:myprocess channel:stdout\nThis is a log message'
        expected_output = 'This is a log message\n'
        
        with patch('builtins.print') as mock_print:
            supervisor_tee.plain_event_handler(event, response.encode())
            mock_print.assert_called_once_with(expected_output, flush=True)

if __name__ == '__main__':
    unittest.main()
