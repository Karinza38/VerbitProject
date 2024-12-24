# VerbitProject

This repository contains tests for both API interactions and end-to-end (E2E) user interactions with the GitHub platform.

### 1. **API Test**

The API tests interact with the GitHub REST API to perform the following actions:

	#### 1.1. GET a List of Issues

	In this part of the test, we GET a list of issues from the public repository `microsoft/vscode` using the GitHub API.

	- **API Endpoint**: `https://api.github.com/repos/microsoft/vscode/issues`

	The test verifies the response status code and print the tilte and case number for the issues.

	Method:
	get_issue(issue_number):
	"""
	Retrieve a GitHub issue by its number.

	Args:
		issue_number (int): The number of the issue to retrieve.

	Returns:
		dict: The response JSON containing the issue details.
	"""

	#### 1.2. Create New Issue

	In this part of the test, we create issue from the public repository `microsoft/vscode` using the GitHub API.

	- **API Endpoint**: `https://api.github.com/repos/microsoft/vscode/issues`

	The test verifies the response status code and ensures that the body of the response contains valid issue data.

	Method:
	create_issue(title, body):
	"""
	Create a new GitHub issue.

	Args:
		title (str): Title of the issue.
		body (str): Body of the issue.

	Returns:
		int: The issue number of the newly created issue.
	"""

	#### 1.3. Update Issue

	In this part of the test, we update existing issue state (open--> closed) from the public repository `microsoft/vscode` using the GitHub API.

	- **API Endpoint**: `https://api.github.com/repos/microsoft/vscode/issues`

	The test verifies the response status code and state.

	Method:
	update_issue(issue_number, state="closed"):
	"""
	Update the state of a GitHub issue.

	Args:
		issue_number (int): The number of the issue to update.
		state (str): The desired state ('open' or 'closed').

	Returns:
		str: The updated state of the issue.
	"""
### 1. **E2E Test**

	#### 1.1. Login Tests

	In this part of the test, we did login to URL with different credentials.

	The test verifies the response status code and print the tilte and case number for the issues.

	Method:
	test_login_with_private_user(set_up_tear_down, login_user, user, pw) 
	"""
	Test Case: Verify login functionality for a private user.

	Description:
	This test verifies that a private user can successfully log in to the application.
	After logging in, it checks that the dashboard page is displayed with the correct header.

	Parameters:
	- set_up_tear_down: Fixture to set up and tear down the test environment.
	- user (str): The username (email) of the private user.
	- pw (str): The password of the private user.

	Steps:
	1. Set up credentials using the provided username and password.
	2. Perform login using the LoginPage object.
	3. Verify that the dashboard header is visible.
	4. Confirm that the header text matches 'Dashboard'.

	Assertions:
	- Dashboard header is visible after login.
	- Dashboard header text is 'Dashboard'.
	"""
	################
	def test_login_with_invalid_user(set_up_tear_down, login_user, user, pw)
	"""
	Test Case: Verify login functionality with invalid credentials.

	Description:
	This test verifies that the application displays an error message when attempting to log in with invalid credentials.

	Parameters:
	- set_up_tear_down: Fixture to set up and tear down the test environment.
	- user (str): The invalid username (email) to be tested.
	- pw (str): The invalid password associated with the username.

	Steps:
	1. Prepare invalid credentials.
	2. Attempt login using the LoginPage object.
	3. Verify that an appropriate error message is displayed.

	Assertions:
	- Error message should contain the text 'Incorrect username or password'.
	"""
	################
	def test_login_with_no_user(set_up_tear_down) 
	"""
	Test Case: Verify login behavior when no credentials are provided.

	Description:
	This test verifies that attempting to log in without entering any username or password does not grant access to the dashboard page.

	Parameters:
	- set_up_tear_down: Fixture to set up and tear down the test environment.

	Steps:
	1. Attempt to log in without entering any credentials.
	2. Verify that the dashboard header is not visible, indicating the user is not logged in.

	Assertions:
	- Dashboard header should not be visible after attempting login without credentials.
	"""
	################
	def test_logout(set_up_tear_down, login_user, user, pw) 
	"""
	Test Case: Verify logout functionality for a logged-in user.

	Description:
	This test ensures that a user can successfully log out of the application.
	After logging in with valid credentials, the test clicks on the logout button,
	verifies that the logout option appears, and confirms that the sign-out page is displayed.

	Parameters:
	- set_up_tear_down: Fixture to set up and tear down the test environment.
	- user (str): The username (email) of the private user.
	- pw (str): The password of the private user.

	Steps:
	1. Log in with valid credentials.
	2. Click the logout button.
	3. Select the 'Sign Out' option.
	4. Verify that the sign-out confirmation page is displayed.

	Assertions:
	- Verify that the 'Sign out from all accounts' input button is enabled.
	"""
	###############
	def test_create_new_issue_user(set_up_tear_down, user, pw, issue_tab, title, description, query, target_text)
	"""
	Steps:
    1. Log in with the provided user credentials.
    2. Navigate to the specified Issue tab.
    3. Create a new bug report with a given title and description.
    4. Search for the created issue by title.
    5. Close the issue and verify that it is in the closed state.
	"""