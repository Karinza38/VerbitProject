import requests
import logging
import pytest

from common_functions import compare_title_and_body, create_issue, update_issue, verify_issue_state, get_issue
from global_veriables import GlobalVariables  
#from fixtures import new_issue_payload

# Logger Configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig()

#region Test GitHub API  GET flow
def github_api_get_flow(endpoint):
    """
    Test GitHub API flow for retrieving issues (GET Action).

    Args:
        endpoint (str): The GitHub API endpoint to fetch issues from.

    Steps:
        1. Fetch the list of issues from the GitHub API.
        2. Log the title and number of each issue retrieved.
        3. Verify the response status code is 200.

    Raises:
        AssertionError: If the API response status code is not 200.
    """
    try:
        # Retrieve a list of issues
        response = requests.get(endpoint)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Iterate over each issue in the response JSON and log the title and number of each issue
        for issue in response.json():
            logger.info(f"Issue Title: {issue.get('title')}, Issue Number: {issue.get('number')}")
    except Exception as e:
        logger.error(f"Failed to fetch list of issues: {e}")
        raise

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200, "Failed to fetch issues"
#endregion

#region Test GitHub API POST flow    
def github_api_post_flow(endpoint, new_issue_payload):
    try:
        # Create a new issue
        response = requests.post(endpoint, headers=GlobalVariables.HEADERS, json=new_issue_payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        # Log the title and number of the new issue
        logger.info(f"New Issue Title: {response.json().get('title')}, New Issue Number: {response.json().get('number')}")
    except Exception as e:
        logger.error(f"Failed to create new issue: {e}")
        raise
        
    assert response.status_code == 201, "Failed to create issue"
#endregion

#region Test GitHub API retrive flow    
def github_api_retrieve_flow(endpoint, new_issue_payload):
    try:
        payload_title = new_issue_payload["title"]
        payload_body  = new_issue_payload["body"]
        # Step 1: Create a new issue
        issue_number = create_issue(payload_title, payload_body)
         # Step 2: Retrieve the newly created issue
        retrieved_issue = get_issue(issue_number)
        # Step 3: Compare the title and body of the created issue
        compare_title_and_body(retrieved_issue, payload_title, payload_body)
    except Exception as e:
        logger.error(f"Failed to retrieve issue: {e}")
        raise
#endregion

#region Test GitHub API update flow    
def github_api_update_flow(new_issue_payload, state="closed"):
    try:
        #payload_data = new_issue_payload()
        payload_title = new_issue_payload["title"]
        payload_body  = new_issue_payload["body"]
            
        # Step 1: Create a new issue
        issue_number = create_issue(payload_title, payload_body)
        # Step 2: Update the issue's state to 'closed'
        updated_state = update_issue(issue_number, state="closed")
        # Step 3: Verify the issue's state is 'closed'
        current_state = verify_issue_state(issue_number)
        assert current_state == "closed", f"State verification failed. Expected 'closed', got '{current_state}'."
        logger.error("Issue creation, update, and verification succeeded.")
    except Exception as e:
        logger.error(f"Failed to update issue: {e}")
#endregion

