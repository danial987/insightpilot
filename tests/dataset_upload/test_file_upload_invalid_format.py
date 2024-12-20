import pytest
from unittest.mock import patch, MagicMock
from pages.dataset_upload import DatasetUploadManager
from dataset import Dataset


@pytest.fixture
def setup_manager():
    """
    Fixture to set up the DatasetUploadManager instance and mock dependencies.
    """
    manager = DatasetUploadManager()
    manager.dataset_db = MagicMock(spec=Dataset)
    return manager


@patch("streamlit.error")
@patch("streamlit.file_uploader")
@patch.dict("streamlit.session_state", {"user_id": 1}, clear=True)
def test_file_upload_invalid_format(mock_file_uploader, mock_error, setup_manager):
    """
    Test handling of a file with an unsupported format upload.
    """
    manager = setup_manager

    mock_uploaded_file = MagicMock()
    mock_uploaded_file.name = "unsupported_file.txt"
    mock_uploaded_file.size = 1024  
    mock_uploaded_file.getvalue.return_value = b"Some content" 
    mock_file_uploader.return_value = mock_uploaded_file

    manager.dataset_db.dataset_exists.return_value = False

    manager.dataset_upload_page()

    mock_error.assert_called_once_with("Unsupported file type")
