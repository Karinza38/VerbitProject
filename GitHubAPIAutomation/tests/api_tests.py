import requests
import pytest
import logging

from GitHubAPIAutomation.utils.common_functions import compare_title_and_body, create_issue, update_issue, \
    verify_issue_state, get_issue
from GitHubAPIAutomation.global_veriables.global_veriables import GlobalVariables, configure_logger
from GitHubAPIAutomation.config.fixtures import new_issue_payload

logger = configure_logger()

#region Test GitHub API GET flow
def test_github_api_get_flow():
    """
    Test GitHub API flow for retrieving issues (GET Action).

    Steps:
        1. Fetch the list of issues from the GitHub API.
        2. Log the title and number of each issue retrieved.
        3. Verify the response status code is 200.

    Raises:
        AssertionError: If the API response status code is not 200.
    """
    try:
        response = requests.get(GlobalVariables.ISSUES_ENDPOINT)
        response.raise_for_status() # This method checks the HTTP response status code.

        for issue in response.json():
            logging.info(f"Issue Title: {issue.get('title')}, Issue Number: {issue.get('number')}")
    except Exception as e:
        logging.error(f"Failed to fetch list of issues: {e}")
        raise

    assert response.status_code == 200, "Failed to fetch issues"
#endregion

#region Test GitHub API POST flow
def test_github_api_post_flow(new_issue_payload):
    """
    Test GitHub API flow for creating an issue (POST Action).
    """
    try:
        response = requests.post(
            GlobalVariables.ISSUES_ENDPOINT,
            headers=GlobalVariables.HEADERS,
            json=new_issue_payload
        )
        response.raise_for_status()

        logging.info(f"New Issue Title: {response.json().get('title')}, Issue Number: {response.json().get('number')}")
    except Exception as e:
        logging.error(f"Failed to create new issue: {e}")
        raise

    assert response.status_code == 201, "Failed to create issue"
#endregion

#region Test GitHub API RETRIEVE flow
def test_github_api_retrieve_flow(new_issue_payload):
    """
    Test GitHub API flow for retrieving a created issue.
    """
    try:
        payload_title = new_issue_payload["title"]
        payload_body = new_issue_payload["body"]

        issue_number = create_issue(payload_title, payload_body)
        retrieved_issue = get_issue(issue_number)
        compare_title_and_body(retrieved_issue, payload_title, payload_body)
    except Exception as e:
        logging.error(f"Failed to retrieve issue: {e}")
        raise
#endregion

#region Test GitHub API UPDATE flow
def test_github_api_update_flow(new_issue_payload, state="closed"):
    """
    Test GitHub API flow for updating an issue state.
    """
    try:
        payload_title = new_issue_payload["title"]
        payload_body = new_issue_payload["body"]

        issue_number = create_issue(payload_title, payload_body)
        update_issue(issue_number, state=state)

        current_state = verify_issue_state(issue_number)
        assert current_state == state, f"State verification failed. Expected '{state}', got '{current_state}'."

        logging.info("Issue creation, update, and verification succeeded.")
    except Exception as e:
        logging.error(f"Failed to update issue: {e}")
        raise
#endregion

@pytest.mark.parametrize("payload, expected_status_code, error_message", [
    ({"body": "Missing title"}, 422, "Validation Failed"),  # Missing title
    ({"title": "Missing body"}, 201, None),  # Missing body (optional field)
    ({}, 422, "Validation Failed"),  # Missing both title and body
])
def test_create_issue_invalid_payload(payload, expected_status_code, error_message):
    """
    Test creating GitHub issues with invalid payloads.

    Args:
        payload (dict): The issue payload to test.
        expected_status_code (int): The expected HTTP status code.
        error_message (str or None): The expected error message, if any.
    """
    response = requests.post(GlobalVariables.ISSUES_ENDPOINT, headers=GlobalVariables.HEADERS, json=payload)
    logging.info(f"Expected status code {expected_status_code}, got {response.status_code}")
    assert response.status_code == expected_status_code, (
        f"Expected status code {expected_status_code}, got {response.status_code}")

########################## wrong url ###################
@pytest.mark.parametrize("url, expected_status_code", [
    (f"{GlobalVariables.ISSUES_ENDPOINT}/wrong_endpoint", 404),  # Incorrect URL
    ("https://api.github.com/repos/invalid_owner/invalid_repo/issues", 404),  # Invalid repository
])
def test_create_issue_invalid_url(new_issue_payload, url, expected_status_code):
    """
    Test creating GitHub issues with invalid URLs.

    Args:
        url (str): The incorrect API URL to test.
        expected_status_code (int): The expected HTTP status code.
    """
    response = requests.post(url, headers=GlobalVariables.HEADERS, json=new_issue_payload)
    logging.info(f"Expected status code {expected_status_code}, got {response.status_code}")
    assert response.status_code == expected_status_code, (f"Expected status code {expected_status_code}, got {response.status_code}")

