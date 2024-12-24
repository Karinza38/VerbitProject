import requests
import pytest
import logging
from common_functions_old import compare_title_and_body, create_issue, update_issue, verify_issue_state, get_issue
from global_veriables_old import GlobalVariables, configure_logger
from fixtures_old import new_issue_payload

# Logger Configuration
def configure_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logging.basicConfig()
    return logger

#region Test GitHub API GET flow
def test_github_api_get_flow(self):
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
        response = requests.get(self.endpoint)
        response.raise_for_status()

        for issue in response.json():
            self.logger.info(f"Issue Title: {issue.get('title')}, Issue Number: {issue.get('number')}")
    except Exception as e:
        self.logger.error(f"Failed to fetch list of issues: {e}")
        raise

    assert response.status_code == 200, "Failed to fetch issues"
#endregion

#region Test GitHub API POST flow
def test_github_api_post_flow(self, new_issue_payload):
    """
    Test GitHub API flow for creating an issue (POST Action).
    """
    try:
        response = requests.post(self.endpoint, headers=GlobalVariables.HEADERS, json=new_issue_payload)
        response.raise_for_status()

        self.logger.info(f"New Issue Title: {response.json().get('title')}, Issue Number: {response.json().get('number')}")
    except Exception as e:
        self.logger.error(f"Failed to create new issue: {e}")
        raise

    assert response.status_code == 201, "Failed to create issue"
#endregion

#region Test GitHub API RETRIEVE flow
def test_github_api_retrieve_flow(self, new_issue_payload):
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
        self.logger.error(f"Failed to retrieve issue: {e}")
        raise
#endregion

#region Test GitHub API UPDATE flow
def test_github_api_update_flow(self, new_issue_payload, state="closed"):
    """
    Test GitHub API flow for updating an issue state.
    """
    try:
        payload_title = new_issue_payload["title"]
        payload_body = new_issue_payload["body"]

        issue_number = create_issue(payload_title, payload_body)
        updated_state = update_issue(issue_number, state=state)

        current_state = verify_issue_state(issue_number)
        assert current_state == state, f"State verification failed. Expected '{state}', got '{current_state}'."

        self.logger.info("Issue creation, update, and verification succeeded.")
    except Exception as e:
        self.logger.error(f"Failed to update issue: {e}")
        raise
#endregion

