from typing import Optional, Union, List
import requests
from GitHubAPIAutomation.global_veriables.global_veriables import GlobalVariables, configure_logger
from GitHubAPIAutomation.utils.response.assignee_template import AssigneeTemplate


class CommonRequest:
    def __init__(
        self,
        title: Optional[str] = "",
        body: str = "",
        assignee: str = "",
        milestone: Optional[str | int] = None,
        labels: Optional[List[str]] = None,
        assignees: Optional[list[str]] = None,
    ):
        #if not title:
            #raise ValueError("Title is required field")

        self.title = title
        self.body = body
        self.assignee = assignee or []
        self.milestone = milestone
        self.labels = labels or []
        self.assignees = assignees or []

    def request_to_dict(self):
        """Convert object to dictionary for API request."""
        return {
        "title": self.title,
        "body": self.body,
        "assignee": self.assignee,
        "milestone": self.milestone,
        "labels": self.labels,
        "assignees": self.assignees if self.assignees else [],
        }








