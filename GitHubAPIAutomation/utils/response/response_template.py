from datetime import datetime
from GitHubAPIAutomation.utils.response.user_template import UserTemplate
from GitHubAPIAutomation.utils.response.assignee_template import AssigneeTemplate
from GitHubAPIAutomation.utils.response.sub_issues_summary import SubIssuesSummary
from GitHubAPIAutomation.utils.response.reactions import Reactions

class ResponseTemplate:
    url: str
    repository_url: str
    comments_url: str
    events_url: str
    html_url: str
    id: int
    node_id: str
    number: int
    title:str
    user: UserTemplate
    labels: []
    state: str
    locked: str
    assignee: AssigneeTemplate
    assignees: list[AssigneeTemplate]
    milestone: None
    comments: str
    created_at: datetime
    updated_at: datetime
    closed_at: None
    author_association: str
    sub_issues_summary: SubIssuesSummary
    active_lock_reason: str
    body: str
    closed_by: str
    reactions: Reactions
    timeline_url: str
    performed_via_github_app: None
    state_reason: None