import pytest
from unittest.mock import patch, MagicMock
from mory.chat.complection import chat_completion_request

@patch('mory.chat.complection.client.chat.completions.create')
def test_chat_completion_request(mock_create):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Response content"
    mock_create.return_value = mock_response

    messages = [{"role": "user", "content": "Hello"}]
    response = chat_completion_request(messages)
    assert response.choices[0].message.content == "Response content"

    mock_create.side_effect = Exception("API Error")
    with pytest.raises(SystemExit):
        chat_completion_request(messages)
