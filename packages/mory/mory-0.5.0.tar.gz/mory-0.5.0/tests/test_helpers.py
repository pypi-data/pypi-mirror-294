import pytest
from unittest.mock import patch, mock_open
from mory.helpers import check_api_key, get_string_size_kb, save_response_to_file, read_file_content

@patch('mory.helpers.os.getenv')
def test_check_api_key(mock_getenv):
    mock_getenv.return_value = "fake_api_key"
    assert check_api_key() == "fake_api_key"

    mock_getenv.return_value = None
    with pytest.raises(SystemExit):
        check_api_key()

@patch('os.path.join', side_effect=lambda *args: "/".join(args))
@patch('os.listdir', return_value=[])
def test_save_response_to_file(mock_listdir, mock_join, tmpdir):
    temp_dir = tmpdir.mkdir("sub")
    file_path = str(temp_dir.join('response_1.md'))
    with patch('builtins.open', mock_open()) as mock_file:
        save_response_to_file('sample response', str(temp_dir))
        mock_file.assert_called_once_with(file_path, 'w', encoding='utf-8')
        mock_file().write.assert_called_once_with('sample response')

@patch('builtins.open', new_callable=mock_open, read_data='file content')
def test_read_file_content(mock_open):
    result = read_file_content('/fakepath/file.txt')
    assert result == 'file content'

    mock_open.side_effect = IOError("File not found")
    result = read_file_content('/nonexistent/file.txt')
    assert result == ""

def test_get_string_size_kb():
    string = "12345"
    size_kb = get_string_size_kb(string)
    assert size_kb == pytest.approx(0.0048828125, rel=1e-9)
