
from src.utils import get_device_id

def test_get_device_id(mocker):
    mocker.patch('builtins.open', mocker.mock_open(read_data='Serial : 0000000000000000'))
    assert get_device_id() == 0
    mocker.patch('builtins.open', mocker.mock_open(read_data='Serial : 0000000000000001'))
    assert get_device_id() == 1
    mocker.patch('builtins.open', mocker.mock_open(read_data='Serial : 0000000000000002'))
    assert get_device_id() == 2
    mocker.patch('builtins.open', mocker.mock_open(read_data='Serial : 0000000000000003'))
    assert get_device_id() == 3
    mocker.patch('builtins.open', mocker.mock_open(read_data='Serial : 0000000000000004'))
    assert get_device_id() == 4
    mocker.patch('builtins.open', mocker.mock_open(read_data='Serial : 0000000000000005'))
    assert get_device_id() == 5
    mocker.patch('builtins.open', mocker.mock_open(read_data='Serial : 0000000000000006'))
    assert get_device_id() == 6
    mocker.patch('builtins.open', mocker.mock_open(read_data='Serial : 0000000000000007'))
    assert get_device_id() == 7
    mocker.patch('builtins.open', mocker.mock_open(read_data='Serial : 0000000000000008'))
    assert get_device_id() == 8
    mocker.patch('builtins.open', mocker.mock_open(read_data='Serial : 0000000000000009'))
    assert get_device_id() == 9
   