import sys
from jira import JIRA
import os

# JIRA server URL
jira_url = "https://latha.atlassian.net"

# Mapping of Jenkins jobs to JIRA project keys
nav_projects = {
    "jira_stages": "JEN",
    # Add more if needed
}

def update_jira(proj, build_status):
    # Login to JIRA using API token
    jira_login = JIRA(server=jira_url, basic_auth=(
        os.environ.get('ATLASSIAN_CLOUD_USER'),
        os.environ.get('ATLASSIAN_CLOUD_APIKEY')
    ))

    # Search for issues in "To Do" status
    jql = f'project = "{JEN}" AND status = "To Do" AND Sprint in openSprints()'
    jira_issues = jira_login.search_issues(jql, maxResults=50)

    for issue in jira_issues:
        issue_key = issue.key
        print(f"Processing issue: {issue_key}")

        try:
            if build_status == "SUCCESS":
                # Get all available transitions for the issue
                transitions = jira_login.transitions(issue)

                # Debug print: list all transitions
                for t in transitions:
                    print(f"Available Transition: {t['name']} (ID: {t['id']})")

                # Find the transition to "In Progress"
                target_transition = next(
                    (t for t in transitions if t['name'].lower() == 'in progress'), None
                )

                if target_transition:
                    jira_login.transition_issue(issue, target_transition['id'])
                    print(f"Issue {issue_key} moved to '{target_transition['name']}'")
                else:
                    print(f"No 'In Progress' transition found for {issue_key}")

        except Exception as e:
            print(f"Error updating JIRA issue {issue_key}: {str(e)}")
            continue

if __name__ == "__main__":
    # Check for build result input
    if len(sys.argv) < 2:
        print("Usage: python script.py <SUCCESS|FAILED>")
        sys.exit(1)

    result = sys.argv[1].upper()

    for jenkins_job, jira_project in nav_projects.items():
        update_jira(jira_project, result)
