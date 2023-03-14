import os
import subprocess
import re
import requests

# Get the current working directory
cwd = os.getcwd()

# Get list of all directories in the current directory (excluding the .git directory)
dirs = [d for d in os.listdir(cwd) if os.path.isdir(os.path.join(cwd, d)) and d != ".git"]

# Function to get the Git URL for a given folder
def get_git_url(folder):
    # Save the current directory
    original_dir = os.getcwd()
    # Change to the target directory
    os.chdir(folder)
    # Run the Git command to get the URL of the remote repository
    cmd = "git remote show origin -n | grep 'Fetch URL' | awk '{print $3}'"
    output = subprocess.check_output(cmd, shell=True, universal_newlines=True)
    # Change back to the original directory
    os.chdir(original_dir)
    # Return the Git URL
    return output.strip()

# Function to generate the GitHub API URL for a given Git URL
def generate_git_api_url(git_url):
    # Define a regular expression pattern to extract the username and repository name from the Git URL
    pattern = r"([A-Za-z0-9_-]+)/([A-Za-z0-9_-]+)\.git"
    # Use the regular expression to extract the username and repository name
    match = re.search(pattern, git_url)
    # Build the GitHub API URL using the extracted username and repository name
    return f"https://api.github.com/repos/{match.group(1)}/{match.group(2)}"

# Function to get the number of stars for a given GitHub API URL
def get_star(api_url):
    # Send a GET request to the GitHub API
    response = requests.get(api_url)
    # Define a regular expression pattern to extract the number of stars from the response
    pattern = r'"stargazers_count":([0-9]*)'
    # Use the regular expression to extract the number of stars
    match = re.search(pattern, response.text)
    # Return the number of stars as a string
    stargazers_count = match.group(1)
    return stargazers_count

# Loop through each directory and print the number of stars for its associated GitHub repository
for folder in dirs:
    # Get the Git URL for the directory
    git_url = get_git_url(folder)
    # Generate the GitHub API URL for the repository
    api_url = generate_git_api_url(git_url)
    # Get the number of stars for the repository
    stars = get_star(api_url)
    # Print the directory name and the number of stars
    print(f"{folder}: {stars} stars")