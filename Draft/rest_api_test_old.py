import pytest
import requests
from venv import logger

from api_tests_old import github_api_get_flow, github_api_post_flow, github_api_retrieve_flow, github_api_update_flow
from global_veriables_old import GlobalVariables  # Import the GlobalVariables class
from fixtures_old import new_issue_payload

# Define the GitHub API endpoint for issues
#ISSUES_ENDPOINT = f"{GlobalVariables.BASE_URL}/repos/{GlobalVariables.OWNER}/{GlobalVariables.REPO}/issues"

########################## Retrieve a list of issues from a public repository ###################
def test_github_api_flow_get():
    github_api_get_flow(GlobalVariables.ISSUES_ENDPOINT)

########################## Create a new issue with a title and body ###################
def test_github_api_flow_post(new_issue_payload):
    github_api_post_flow(GlobalVariables.ISSUES_ENDPOINT, new_issue_payload)

########################## Retrieve the created issue and verify that the title and body are correct ###################
def test_github_api_flow_retrieve(new_issue_payload):
    github_api_retrieve_flow(GlobalVariables.ISSUES_ENDPOINT, new_issue_payload)

########################## Close the issue, and verify that its state is updated to close  ###################
def test_github_api_flow_update(new_issue_payload):
    github_api_update_flow(new_issue_payload)
    
########################## payload with missing parameters ###################
#def test_github_api_flow_invalidpayload(new_issue_payload):
@pytest.mark.parametrize("payload, expected_status_code, error_message",[
({"body": "Missing title"}, 422, "Validation Failed"),  # Missing title
({"title": "Missing body"}, 201, None),                # Missing body (optional field)
({}, 422, "Validation Failed"),                       # Missing both title and body
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
    assert response.status_code == expected_status_code, (
        f"Expected status code {expected_status_code}, got {response.status_code}")
    logger.info(f"Expected status code {expected_status_code}, got {response.status_code}")

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
    assert response.status_code == expected_status_code, (
        f"Expected status code {expected_status_code}, got {response.status_code}")
    logger.info(f"Expected status code {expected_status_code}, got {response.status_code}")

if __name__ == "__main__":
    # Run the pytest tests with verbosity and showing standard output
    pytest.main(["-v", "-s", __file__])