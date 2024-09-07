import os
import string
import pytest
from click.testing import CliRunner
from docutils.parsers.rst.directives import encoding
from src.main import pycat
from random import randbytes, choice

def abstraction_runner(cli, args):
    runner = CliRunner()
    result = runner.invoke(cli, args)
    return result

def test_file_single_line():
    result = abstraction_runner(pycat,['assets/multiple_lines.txt'])
    assert result.exit_code == 0
    assert result.output == "Test\n"

def test_empty_file():
    result = abstraction_runner(pycat,['assets/empty_file.txt'])
    print('type', type(result))
    assert result.exit_code == 0
    assert result.output == "\n"

def test_file_multiple_lines():
    result = abstraction_runner(pycat,['assets/multiple_lines.txt'])
    assert result.exit_code == 0
    assert result.output == "Line1\nLine2\n"

def test_file_not_found():
    result = abstraction_runner(pycat, ['assets/not_found.txt'])
    assert result.exit_code == 1
    assert result.output == "File not found\n"

def test_binary_file():
    with open('assets/temporary.dat', "wb") as file:
        result = abstraction_runner(pycat, ['assets/temporary.dat'])
        expected = randbytes(10)
        file.write(expected)
        file.flush()
        assert result.exit_code == 0
        # FIXME: fix the assert
        # assert bytes(result.output, 'ascii') == ''
#
# def test_huge_file():
#     runner = CliRunner()
#     try:
#         with open('assets/huge.txt', "w") as file:
#             text_data = ''
#             for _ in range(10**7):
#                 line_data = ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(100)) + '\n'
#                 file.write(line_data)
#                 file.flush()
#                 text_data += line_data
#
#
#             # result = runner.invoke(pycat, ['assets/huge.txt'])
#             # assert result.exit_code == 0
#             # assert result.output == text_data + '\n'
#     finally:
#         pass
#         # os.remove('assets/huge.txt')
#
def test_print_line():
    result = abstraction_runner(pycat, ['assets/single_file.txt', '-l 1'])
    assert result.exit_code == 0
    assert result.output == "hello"

def test_print_until():
    result = abstraction_runner(pycat, ['assets/multiple_lines.txt', '-l 2', '-p'])
    assert result.exit_code == 0
    assert result.output == "number line"

def test_show_end():
    result = abstraction_runner(pycat, ['assets/single_file.txt', '-E'])
    assert result.exit_code == 0
    assert result.output == "txt $\nhello $\n\n"

def test_number_lines():
    result = abstraction_runner(pycat, ['assets/single_file.txt', '-n'])
    assert result.exit_code == 0
    assert result.output == "number line\n"

def test_remove_blank_line():
    result = abstraction_runner(pycat, ['assets/multiple_lines.txt', '-R'])
    assert result.exit_code == 0
    assert result.output == "Line1\nLine2\nLine3\nLine4\nLine5\nLine6\n\n"