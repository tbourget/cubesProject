import pytest
from testfixtures import TempDirectory
from main import *

def test_retrieve_api_key_from_secrets(capfd):
    """
    Test function for retrieve_api_key_from_secrets()
    """
    retrieve_api_key_from_secrets('')
    out, err = capfd.readouterr()
    assert out == ''
