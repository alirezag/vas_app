from src.main import hello_function
import sys
import io


def test_hello_function():
    _stdout = sys.stdout
    sys.stdout = io.StringIO()
    hello_function()
    sys.stdout.seek(0)
    assert sys.stdout.read().strip() == "Hello Function"
    sys.stdout = _stdout
