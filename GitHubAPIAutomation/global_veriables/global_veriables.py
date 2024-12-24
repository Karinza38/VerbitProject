import logging

class GlobalVariables:
    BASE_URL = "https://api.github.com"
    OWNER = "microsoft"
    REPO = "vscode"
    HEADERS = {
    "Authorization": f"Bearer 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",
    "Accept": "application/vnd.github.v3+json"
    }
    ISSUES_ENDPOINT = f"{BASE_URL}/repos/{OWNER}/{REPO}/issues"

# Logger Configuration
def configure_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logging.basicConfig()
    return logger