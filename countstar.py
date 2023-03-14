import os
import subprocess
import re
import requests

# Get the current working directory
cwd = os.getcwd()

# Get list of all directories in the current directory
dirs = [d for d in os.listdir(cwd) if os.path.isdir(os.path.join(cwd, d))]


# Function to count files in a folder
def get_git_url(folder):
    original_dir = os.getcwd()
    os.chdir(folder)
    cmd = "git remote show origin -n | grep 'Fetch URL' | awk '{print $3}'"
    output = subprocess.check_output(cmd, shell=True, universal_newlines=True)
    os.chdir(original_dir)
    return output.strip()    
    
def generate_git_api_url(git_url):
    pattern = r"([A-Za-z0-9_-]+)/([A-Za-z0-9_-]+)\.git"
    match = re.search(pattern, git_url)
    return f"https://api.github.com/repos/{match.group(1)}/{match.group(2)}"

def get_star(api_url):
    response = requests.get(api_url)
    pattern = r'"stargazers_count":([0-9]*)'
    match = re.search(pattern, response.text)
    stargazers_count = match.group(1)
    return stargazers_count

for folder in dirs:
    git_url = get_git_url(folder)
    api_url=generate_git_api_url(git_url)
    print(get_star(api_url))



