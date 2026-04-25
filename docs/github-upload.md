GitHub Upload Helper
This project includes a helper script to create a GitHub repository and wire up the remote, making it easy to push your local repo to GitHub.

Prerequisites
- A GitHub account and a Personal Access Token (PAT) with repo scope if you want to create the repo via API.
- Git installed on your machine.

Usage
- Set your GitHub username and PAT as environment variables:
  export GITHUB_USERNAME="your-username"
  export GITHUB_TOKEN="your-pat"
- From the repo root, run:
  ./scripts/setup_github_remote.sh ffb-rc-project --private
- The script will attempt to create the repo on GitHub under your account, set the remote origin, rename the local branch to main, and push.
- If you prefer not to create via API, create the repo on GitHub manually and then push:
  git remote add origin https://github.com/your-username/ffb-rc-project.git
  git branch -M main
  git push -u origin main

Notes
- The script uses the GitHub REST API when GITHUB_TOKEN is provided. It stores no credentials in the repo.
- If you encounter authentication prompts, ensure your PAT is valid and has the required scopes, or configure SSH keys for GitHub.
