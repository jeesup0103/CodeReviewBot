import requests
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
client = OpenAI()

def get_pr_details(pr_url, REPO_GH_TOKEN):
    headers = {
        'Authorization': f'token {REPO_GH_TOKEN}',  # Using repository token for reading PR details
        'Accept': 'application/vnd.github.v3+json'
    }
    try:
        response = requests.get(pr_url, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error requesting data: {e}")

def get_code_changes(base_url, base_sha, head_sha, REPO_GH_TOKEN):
    headers = {
        'Authorization': f'token {REPO_GH_TOKEN}',  # Using repository token
        'Accept': 'application/vnd.github.v3.diff'
    }
    response = requests.get(f"{base_url}/compare/{base_sha}...{head_sha}", headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch code changes: {response.status_code} {response.text}")

def analyze_code(code_diff):
    # Read system prompt from review_prompt.txt file
    with open('review_prompt.txt', 'r') as file:
        system_prompt = file.read()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"{code_diff}"
            },
        ],
        max_tokens=2048
    )
    return response.choices[0].message.content.strip()

def post_feedback_to_github(pr_url, feedback, BOT_GH_TOKEN):
    parts = pr_url.split('/')
    repo = parts[4] + '/' + parts[5]
    pull_number = parts[7]

    pr_comments_url = f"https://api.github.com/repos/{repo}/issues/{pull_number}/comments"
    response = requests.post(pr_comments_url, json={
        "body": feedback
    }, headers={
        'Authorization': f'token {BOT_GH_TOKEN}',
        'Content-Type': 'application/json'
    })

    try:
        response.raise_for_status()
        print("Successfully posted feedback to GitHub.")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Other error occurred: {err}")

def main(pr_url):

    REPO_GH_TOKEN = os.getenv("REPO_GH_TOKEN")
    BOT_GH_TOKEN = os.getenv("BOT_GH_TOKEN")
    if not REPO_GH_TOKEN or not BOT_GH_TOKEN:
        raise ValueError("Missing required environment variables: REPO_GH_TOKEN or BOT_GH_TOKEN")

    pr_details = get_pr_details(pr_url, REPO_GH_TOKEN)
    base_sha = pr_details['base']['sha']
    head_sha = pr_details['head']['sha']
    repo_url = pr_details['base']['repo']['url']

    # Get the code changes between the base and head commit
    code_diff = get_code_changes(repo_url, base_sha, head_sha, REPO_GH_TOKEN)
    feedback = analyze_code(code_diff)
    post_feedback_to_github(pr_url, feedback, BOT_GH_TOKEN)

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
