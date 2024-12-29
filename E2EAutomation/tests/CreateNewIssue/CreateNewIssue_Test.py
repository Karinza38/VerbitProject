import pytest
from playwright.sync_api import Page, expect, sync_playwright
from E2EAutomation.src.pages.LoginPage import LoginPage
from E2EAutomation.src.pages.VSCodePage import VSCodePage, InnerTabs
from GitHubAPIAutomation.utils.common_functions import get_issue, get_issue_number_by_title, verify_issue_state
import logging

#region used data for test
@pytest.mark.parametrize(
    "user, pw, issue_tab, title, description, query, target_text",
    [
        (
            "danielbh2003@gmail.com",
            "sarit2608!",
            InnerTabs.ISSUES,
            "DanielBH Sample Bug Report Title",
            "This is a sample bug report description.\nSteps to reproduce:\n1. Step one\n2. Step two",  # <-- Add comma here
            "is:issue state:open danielbh",  # This is now a separate parameter
            "danielbh"
        )
    ]
)
#endregion
def test_create_new_issue_user(set_up_tear_down, user, pw, issue_tab, title, description, query, target_text) -> None:
    """
        Steps:
        1. Log in with the provided user credentials.
        2. Navigate to the specified Issue tab.
        3. Create a new bug report with a given title and description.
        4. Search for the created issue by title.
        5. Close the issue and verify that it is in the closed state.
    """
    # Prepare credentials
    credentials = {'username' : user, 'password' : pw}

    # region Setup
    page = set_up_tear_down
    login_p = LoginPage(page)
    dashboard_p = login_p.do_login(credentials)
    #endregion

    # region move to Issue tab
    vscode_page = dashboard_p.click_ms_vscode_btn()
    try:
        vscode_page.click_on_tab(issue_tab)
    except NotImplementedError as e:
        logging.error(e)
    #endregion

    #region create new issue
    vscode_page_after_click_new_issue = vscode_page.click_new_issue_btn()
    vscode_page_after_click_new_issue.select_bug_report()
    # Add Title and Description
    info_for_issue = {'title': title, 'description': description}
    vscode_page.add_title_and_description_and_create_issue(info_for_issue)
    #endregion

    #region back to issue tab
    vscode_page.click_on_tab(issue_tab)
    #endregion

    #region close new issue
        # Search the new issue by title name
    vscode_page.issue_tab_component.search_issue(query)
    issue_number = get_issue_number_by_title(title)
    vscode_page.issue_tab_component.select_ul_element(target_text)
    vscode_page.issue_tab_component.click_close_issue_btn()
    #endregion

    #region assertion to validate issue is in closed state from UI side
    expect(vscode_page.issue_tab_component.close_issue_btn_loc).to_contain_text("Closed")
    #endregion

    #region verify issue status from api
    current_state = verify_issue_state(issue_number)
    assert "closed" in current_state, f"Expected 'Closed' but got '{current_state}'"
    #endregion






