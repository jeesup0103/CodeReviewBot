# Code Review Bot

## Introduction
Code review bot is to automate code reviews by using OpenAI's language model. It fetches code changes from GitHub pull requests on main branch, analyzes the changes using OpenAI's GPT model, and posts feedback directly to the corresponding GitHub pull request.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Documentation](#documentation)
- [Examples](#examples)

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/gflamep/CodeReviewBot.git
    cd CodeReviewBot
    
    ```

2. Install the required dependencies:
    ```sh
    pip install openai requests python-dotenv
    ```

3. Create a `.env` file in the root directory and add your GitHub token and OpenAI API key
    ```env
    GH_TOKEN=your_github_token
    OPENAI_API_KEY=your_openai_api_key
    ```

4. Make GitHub repository secrets named GH_TOKEN and OPENAI_API_KEY
    ```env
    GH_TOKEN=your_github_token
    OPENAI_API_KEY=your_openai_api_key
    ```

5.  Move .github file to target repository to run github actions:
    ```sh
    mv .github/ ..
    ```

## Usage
To run the code review manually, execute the following command:
```sh
python review_code.py <pr_url>
```
Replace <pr_url> with the URL of the pull request you want to review.

Example: https://api.github.com/repos/yourusername/yourrepo/pulls/1


## Features
- Automated Code Review: Automatically fetches code changes from a GitHub pull request and generates a review using OpenAI's GPT model.
- Feedback Posting: Posts the generated feedback as a comment on the GitHub pull request.
- GitHub Actions Integration: Set up as a GitHub Action to automate the review process on each pull request to the main branch.
## Dependencies
- requests
- openai
- python-dotenv
## Configuration
### GitHub Actions Workflow
The GitHub Actions workflow is defined in .github/workflows/main.yml. This workflow triggers on pull requests to the main branch and runs the code review:
```yaml
name: Code Review Workflow

on:
  pull_request:
    branches:
      - main

jobs:
  code-review:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install openai requests python-dotenv

      - name: Run Code Review
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python review_code.py ${{ github.event.pull_request.url }}
```
### Environment Variables
Ensure you have the following environment variables set in your .env file:

- GITHUB_TOKEN: Your GitHub personal access token.
- OPENAI_API_KEY: Your OpenAI API key.

## Examples
Run the code review on a specific pull request:

```sh
python review_code.py https://api.github.com/repos/yourusername/yourrepo/pulls/1
