import pytest
@pytest.fixture
def new_issue_payload():
    """
    Fixture that returns a payload for creating a new GitHub issue.

    Returns:
        A dictionary containing the title and body of the new issue.
    """
    return {
        "title": "Test Issue",
        "body": "This is a test issue created by an API test."
    }
