class GlobalVariables:
    BASE_URL = "https://api.github.com"
    OWNER = "microsoft"
    REPO = "vscode"
    HEADERS = {
    "Authorization": f"Bearer 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",
    "Accept": "application/vnd.github.v3+json"
    }
    ISSUES_ENDPOINT = f"{BASE_URL}/repos/{OWNER}/{REPO}/issues"