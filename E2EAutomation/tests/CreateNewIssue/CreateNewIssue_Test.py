import pytest
from playwright.sync_api import Page, expect, sync_playwright
from E2EAutomation.src.pages.DashboardPage import DashboardPage
from E2EAutomation.src.pages.LoginPage import LoginPage
from E2EAutomation.src.pages.VSCodePage import VSCodePage, InnerTabs
import logging


@pytest.mark.parametrize(
    "user, pw, issue_tab, title, description",
    [
        (
            "danielbh2003@gmail.com",
            "sarit2608!",
            InnerTabs.ISSUES,
            "DanielBH Sample Bug Report Title",
            "This is a sample bug report description.\nSteps to reproduce:\n1. Step one\n2. Step two"
        )
    ]
)
def test_create_new_issue_user(set_up_tear_down, user, pw, issue_tab, title, description) -> None:
    # Prepare credentials
    credentials = {'username' : user, 'password' : pw}

    # Setup
    page = set_up_tear_down
    login_p = LoginPage(page)
    dashboard_p = login_p.do_login(credentials)

    vscode_page = dashboard_p.click_ms_vscode_btn()
    # Try clicking on the 'IDLING' tab
    try:
        vscode_page.click_on_tab(issue_tab)
    except NotImplementedError as e:
        logging.error(e)

    vscode_page_after_click_new_issue = vscode_page.click_new_issue_btn()
    vscode_page_after_click_new_issue.select_bug_report()

    # Add Title and Description
    info_for_issue = {'title': title, 'description': description}
    vscode_page.add_title_and_description_and_create_issue(info_for_issue)









