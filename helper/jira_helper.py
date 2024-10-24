import requests
from requests.auth import HTTPBasicAuth
import json
from decouple import config

# Environment variables
JIRA_URL = config('JIRA_URL')  # Jira base URL, e.g., "https://your-domain.atlassian.net"
JIRA_EMAIL = config('JIRA_EMAIL')  # Your Jira email address
JIRA_API_TOKEN = config('JIRA_API_TOKEN')  # Your Jira API token

# Jira REST API endpoint to get issues
JIRA_ISSUES_ENDPOINT = f"{JIRA_URL}/rest/api/2/search"

# Function to get list of Jira issues
def get_jira_issues(jql_query=""):
    # Headers and authentication
    headers = {
        "Accept": "application/json"
    }
    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

    # Parameters for the Jira search query
    query = {
        'jql': jql_query,  # Jira Query Language (JQL) to filter issues
        'maxResults': 50   # Limit the number of issues returned (can adjust)
    }

    # Send the GET request
    response = requests.get(JIRA_ISSUES_ENDPOINT, headers=headers, params=query, auth=auth)

    # Handle response
    if response.status_code == 200:
        issues = response.json()
        return issues['issues']
    else:
        print(f"Failed to retrieve issues. Status Code: {response.status_code}")
        return None

# Example: Fetch all issues in a specific project
jql_query = "project = YOUR_PROJECT_KEY"  # Replace with your Jira project key (e.g., 'PROJ')
issues = get_jira_issues(jql_query)

# Displaying issue details
if issues:
    for issue in issues:
        key = issue['key']
        summary = issue['fields']['summary']
        status = issue['fields']['status']['name']
        print(f"Issue: {key}, Summary: {summary}, Status: {status}")
else:
    print("No issues found.")
