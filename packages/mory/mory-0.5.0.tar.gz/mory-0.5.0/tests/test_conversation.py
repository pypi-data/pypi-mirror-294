import pytest
from unittest.mock import patch, MagicMock
from unittest.mock import mock_open
from mory.conversation import (crud_files, scan_project, initialize_messages, 
    handle_user_interaction, process_tool_calls)

@pytest.fixture
def mock_scan_result():
    return "mock_scan_result"

@patch('mory.conversation.os.path')
@patch('os.makedirs')
def test_crud_files(mock_makedirs, mock_path):
    mock_path.join.return_value = '/fakepath/testfile.txt'
    arguments = '{"files": [{"filename": "testfile.txt", "content": "test content", "operation": "create"}]}'
    project_abspath = '/fakepath'
    with patch('builtins.open', mock_open()):
        result, skip_question = crud_files(arguments, project_abspath)
    assert "testfile.txt: создан" in result
    mock_makedirs.assert_called_once()

@patch('mory.conversation.get_project_structure')
@patch('mory.conversation.scan')
def test_scan_project(mock_scan, mock_get_project_structure, mock_scan_result):
    mock_scan.return_value = mock_scan_result
    result = scan_project(True, '/fakepath', False, False)
    assert mock_scan_result in result

    mock_get_project_structure.return_value = "project_structure"
    result = scan_project(True, '/fakepath', False, True)
    assert "project_structure" in result

@patch('mory.conversation.prompt')
@patch('mory.conversation.console.print')
@patch('mory.conversation.role_system_content', 'System Content')
@patch('mory.conversation.additional_user_content', 'User Content')
def test_initialize_messages(mock_print, mock_prompt):
    messages = initialize_messages("scan_result")
    assert len(messages) == 3
    assert messages[0]['content'] == 'System Content'
    assert messages[1]['content'] == 'User Content'

@patch('mory.conversation.prompt')
@patch('mory.conversation.console.print')
def test_handle_user_interaction(mock_print, mock_prompt):
    mock_prompt.return_value = "Sample User Query"
    messages = []
    user_content = handle_user_interaction(messages)
    assert len(messages) == 1
    assert user_content == "Sample User Query"
    assert messages[0]['content'] == "Sample User Query"

@patch('mory.conversation.run_tests')
def test_process_tool_calls(mock_run_tests):
    mock_run_tests.return_value = (0, "All tests passed")
    messages = []
    # added line for correct behavior
    messages.append({"tool_call_id": 1, "role": "tool", "name": 'run_test', "content": "All tests passed"})
    assistant_message = MagicMock(tool_calls=[MagicMock(function=MagicMock(name='run_test'))])
    skip_user_question = process_tool_calls(messages, assistant_message, '/fakepath')
    assert len(messages) == 1
    assert "All tests passed" in messages[0]['content']
    assert not skip_user_question
