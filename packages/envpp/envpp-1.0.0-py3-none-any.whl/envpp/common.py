from pathlib import Path

from .api import Api

# Path
path = Path(__file__).parent

# Api
token_file = path / "token.txt"

try:
    token = token_file.read_text()

    _api = Api(token)
except Exception:
    raise Exception("Please set token first")
