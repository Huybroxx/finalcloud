from unittest.mock import MagicMock, patch
import io
from app.s3 import upload_file_to_s3


def test_upload_file_to_s3_helper():
    mock_s3 = MagicMock()
    with patch("app.s3.s3_client", mock_s3):
        file_obj = io.BytesIO(b"test data")
        url = upload_file_to_s3(file_obj, "test.txt")
        assert "test.txt" in url
        mock_s3.upload_fileobj.assert_called_once()


def test_upload_endpoint(client):
    dummy_url = "https://fastapi-app-files-huynn69.s3.ap-southeast-1.amazonaws.com/test.txt"
    with patch("app.main.upload_file_to_s3", return_value=dummy_url):
        files = {"file": ("test.txt", b"dummy content", "text/plain")}
        response = client.post("/upload", files=files)
        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "test.txt"
        assert data["url"] == dummy_url
