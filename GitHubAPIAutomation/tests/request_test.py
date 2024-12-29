import pytest
import logging

from GitHubAPIAutomation.utils.common_functions import create_github_issue
from GitHubAPIAutomation.utils.request.common_request import CommonRequest


@pytest.mark.parametrize(
    "title, body, assignee, assignees",
    [
        ("RequestFromClass Issue", "This is request from class template", "DanielBH", ["DanielBH2"]),
    ]
)
#region used data for test
def test_crete_issue_with_request_template(title, body, assignee, assignees):
    """
    Test creating a GitHub issue and verifying the response fields.
    """
    request_data = CommonRequest(
        title=title,
        body=body,
        assignee=assignee,
        assignees=assignees
    )
    #region Step 1: Create the issue
    try:
        response = create_github_issue(request_data)
        response.raise_for_status()  # Raise an exception for HTTP error codes
    except Exception as e:
        assert False, f"Exception occurred while creating issue: {str(e)}"
    #endregion

    #region Step 2: Validate response status code
    assert response.status_code == 201, f"Failed to create issue. Status: {response.status_code}, Response: {response.text}"
    #endregion

    #region Step 3: Parse the JSON response
    try:
        # Parse the json data from response
        response_data = response.json()
    except ValueError as e:
        assert False, f"Failed to parse JSON response: {str(e)}"
    #endregion

    #region Step 4: Validate response fields
    try:
        # Compare fields from response
        assert response_data["title"] == request_data.title, "Title mismatch"
        assert response_data["body"] == request_data.body,   "Body mismatch"

        #region Check if response_data is empty first for assignee
        if not response_data["assignee"]:
            # If response_data is empty, expect assignee to be empty
            assert "assignee" not in response_data or not response_data["assignee"], "Only users with push access can set the assignee for new issues."
        else:
            # Check for assignee if response_data is not empty
            if hasattr(request_data, "assignee") and request_data.assignee:
                # Check if response has assignee data
                assert "assignee" in response_data, "Expected assignee in response but got missing"
                assert response_data["assignee"], "Assignee should not be empty in response"
                assert response_data["assignee"]["login"] == request_data.assignee.login, "Assignee login mismatch"
                assert response_data["assignee"]["id"] == request_data.assignee.id, "Assignee ID mismatch"
                assert response_data["assignee"]["node_id"] == request_data.assignee.node_id, "Assignee node_id mismatch"
                assert response_data["assignee"]["avatar_url"] == request_data.assignee.avatar_url, "Assignee avatar_url mismatch"
            else:
                # Expect assignee to be empty in response (assignee is either not present or empty)
                assert "assignee" not in response_data or not response_data["assignee"], "Only users with push access can set the assignee for new issues."
        #endregion

        #region Check if response_data is empty first for assignees
        if not response_data["assignees"]:
            # If response_data is empty, expect assignees to be empty
            assert "assignees" not in response_data or not response_data.get("assignees"), "Only users with push access can set the assignee for new issues."
        else:
            # Check for assignees if response_data is not empty
            if hasattr(request_data, 'assignees') and request_data.assignees:
                # Check if response has assignees data
                assert "assignees" in response_data and response_data["assignees"], "Expected assignees in response but got empty"
                assert len(response_data["assignees"]) == len(request_data.assignees), "Number of assignees mismatch"

                for expected_assignee, actual_assignee in zip(request_data.assignees, response_data["assignees"]):
                    assert actual_assignee["login"] == expected_assignee.login, "Assignees login mismatch"
                    assert actual_assignee["id"] == expected_assignee.id, "Assignees ID mismatch"
                    assert actual_assignee["node_id"] == expected_assignee.node_id, "Assignees node_id mismatch"
                    assert actual_assignee["avatar_url"] == expected_assignee.avatar_url, "Assignees avatar_url mismatch"
            else:
                # Expect no assignees in response (assignees is either not present or empty)
                assert "assignees" not in response_data or not response_data.get("assignees"), "Only users with push access can set the assignee for new issues."
        #endregion

    # Raised when attempting to access a dictionary key that does not exist.
    except KeyError as e:
        assert False, f"Missing key in response data: {str(e)}"
    #endregion

    except AssertionError as e:
        assert False, f"Validation failed: {str(e)}"
#endregion

@pytest.mark.parametrize(
    "title, body, assignee, assignees, expected_status_code",
    [
        (None, "This issue has no title", "DanielBH", [], 422),  # Invalid case (no title)
    ]
)
def test_crete_issue_without_title(title, body, assignee, assignees, expected_status_code):
    """
    Test creating a GitHub issue and verifying the response fields.
    """
    request_data = CommonRequest(
        title=title,
        body=body,
        assignee=assignee,
        assignees=assignees
    )
    #region Step 1: Create the issue
    try:
        response = create_github_issue(request_data)

        # Step 2: Verify the status code
        assert response.status_code == expected_status_code, f"Expected status code {expected_status_code} but got {response.status_code}"

    except AssertionError as e:
        assert False, f"Validation failed: {str(e)}"
    #endregion


def test():
    sampledict = {
        "name": "Kelly",
        "age": 25,
        "salary": 8000,
        "city": "New york"}

    keys = ["name", "salary"]

    newdict = {k: sampledict[k] for k in keys}
    print(newdict)


