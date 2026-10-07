from unittest.mock import MagicMock, patch
from app.db import get_db, Base


def test_db_get_db():
    mock_session = MagicMock()
    with patch("app.db.SessionLocal", return_value=mock_session):
        gen = get_db()
        db = next(gen)
        assert db == mock_session
        try:
            next(gen)
        except StopIteration:
            pass
        mock_session.close.assert_called_once()


def test_db_base():
    assert Base is not None
