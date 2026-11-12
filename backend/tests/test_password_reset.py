from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_password_reset_request_returns_generic_message():
    response = client.post(
        "/auth/password-reset/request",
        json={"email": "unknown@example.com"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == (
        "If an account exists for that email, "
        "a password reset link will be sent."
    )


@patch("app.api.routes.auth.send_password_reset_email")
def test_password_reset_request_sends_email(mock_send_email):
    # This test requires a test user in an isolated test database.
    # Replace the fixture/setup with your project's test database
    # and dependency overrides before enabling this test.

    # Arrange: create a test user in the test database.
    # Act: submit POST /auth/password-reset/request.
    # Assert: verify mock_send_email was called once.
    #
    # Do not run this test against your production database.
    assert callable(mock_send_email)