import sys

import requests

# Define your repository and the file path
repo_owner = 'dasshims'
repo_name = 'CS416-Data-Vizualizations-FInal-Project'
file_path = 'README.md'
github_token = 'fillme'  # If your repo is private, use a personal access token

def get_github_data():
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    headers = {'Authorization': f'token {github_token}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        file_content = response.json()['content']
        # The file is base64 encoded, so decode it
        import base64
        file_content_decoded = base64.b64decode(file_content).decode('utf-8')
        return file_content_decoded
    else:
        print(f"Error: {response.status_code}")


def fetch_github_repos():
    url = f"https://api.github.com/users/{repo_owner}/repos"
    headers = {
        'Authorization': f'token {github_token}'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        repos = response.json()
        repo_names = [repo['name'] for repo in repos]
        return repo_names
    else:
        print("Error fetching repos from GitHub")
        return []

def initialize_data():
    print("Initializing data...")
    repos = fetch_github_repos()
    ##ou.feed_content_to_openai(f"These are the github repos I have {repos}")
    content = get_github_data()
    print(len(content))
    ##ou.feed_content_to_openai(content)

if __name__ == '__main__':
    repos = fetch_github_repos()
    print(repos)