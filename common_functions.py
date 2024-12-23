from venv import logger
import requests
import logging

import json
from global_veriables import GlobalVariables

def compare_title_and_body(actual_issue, expected_title, expected_body):
    """
    Compare the title and body of an issue with expected values.

    Args:
        expected_title (str): The expected title.
        expected_body (str): The expected body.
        actual_issue (dict): The actual issue details from the API.

    Raises:
        AssertionError: If the title or body does not match the expected values.
    """
    try:
        assert actual_issue["title"] == expected_title, (
            f"Title mismatch. Expected: {expected_title}, Got: {actual_issue['title']}"
        )
        assert actual_issue["body"] == expected_body, (
            f"Body mismatch. Expected: {expected_body}, Got: {actual_issue['body']}"
        )
        logger.info("Title and body match successfully.")
    except AssertionError as e:
        logger.error(f"Comparison failed: {e}")
        raise
def get_issue(issue_number):
    """
    Retrieve a GitHub issue by its number.

    Args:
        issue_number (int): The number of the issue to retrieve.

    Returns:
        dict: The response JSON containing the issue details.
    """
    url = f"{GlobalVariables.ISSUES_ENDPOINT}/{issue_number}"
    response = requests.get(url, headers=GlobalVariables.HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        logger.info(f"Failed to retrieve issue #{issue_number}. Status Code: {response.status_code}, Response: {response.text}")
        response.raise_for_status()
        
def create_issue(title, body):
    """
    Create a new GitHub issue.

    Args:
        title (str): Title of the issue.
        body (str): Body of the issue.

    Returns:
        int: The issue number of the newly created issue.
    """
    payload = {"title": title, "body": body}
    try:
        response = requests.post(GlobalVariables.ISSUES_ENDPOINT, headers = GlobalVariables.HEADERS, json=payload)
        if response.status_code == 201:
            issue_number = response.json().get("number")
            logger.info(f"Issue created successfully. Issue Number: {issue_number}")
            return issue_number
        else:
            logger.info(f"Failed to create issue. Status Code: {response.status_code}, Response: {response.text}")
            response.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to create issue: {e}")
    
def update_issue(issue_number, state="closed"):
    """
    Update the state of a GitHub issue.

    Args:
        issue_number (int): The number of the issue to update.
        state (str): The desired state ('open' or 'closed').

    Returns:
        str: The updated state of the issue.
    """
    try:
        url = f"{GlobalVariables.ISSUES_ENDPOINT}/{issue_number}"
        payload = {"state": state}
        response = requests.patch(url, headers = GlobalVariables.HEADERS, json=payload)
        if response.status_code == 200:
            updated_state = response.json().get("state")
            logger.info(f"Issue #{issue_number} successfully updated to state: '{updated_state}'.")
            return updated_state
        else:
            logger.info(f"Failed to update issue #{issue_number}. Status Code: {response.status_code}, Response: {response.text}")
            response.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to update issue: {e}")

def verify_issue_state(issue_number):
    """
    Verify the state of a GitHub issue.

    Args:
        issue_number (int): The number of the issue to verify.

    Returns:
        str: The current state of the issue.
    """
    try:
        url = f"{GlobalVariables.ISSUES_ENDPOINT}/{issue_number}"
        response = requests.get(url, GlobalVariables.HEADERS)
        if response.status_code == 200:
            current_state = response.json().get("state")
            logger.info(f"Issue #{issue_number} is currently in state: '{current_state}'.")
            return current_state
        else:
            logger.info(f"Failed to fetch issue #{issue_number}. Status Code: {response.status_code}, Response: {response.text}")
            response.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to fetch issue: {e}")

