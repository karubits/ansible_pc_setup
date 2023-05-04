"""
This Python script checks a list of GitHub repositories to get their latest release version,
saves the version as a variable in the format 'version_repo_name', and finds and replaces the
corresponding version variable in a YAML file called 'local.yml'. The script assumes that
'local.yml' is in the same directory as the script.

The list of repositories to check is defined in the 'repos' list. Each item in the list should
be a string in the format 'owner/repo', where 'owner' is the GitHub username or organization
name, and 'repo' is the repository name.

For each repository, the script sends an HTTP GET request to the GitHub API to retrieve the
latest release tag. If the request is successful, the script extracts the tag name from the
response JSON and saves it as a variable with the name 'version_repo_name'. It then searches
the 'local.yml' file for the version variable with the name 'version_repo_name', and replaces
its value with the latest release tag.

Note that this script requires the 'requests' library for sending HTTP requests to the GitHub
API, and the 'os' and 're' libraries for file I/O and text manipulation, respectively. Make
sure to install these libraries before running the script.
"""

import requests
import os
import re

# Define the list of repositories to check
repos = [
    "smallstep/cli",
    "bitwarden/cli",
    "restic/restic",
    "rancher/rke",
    "starship/starship",
    "kubernetes/kompose",
    "Peltoche/lsd",
    "derailed/k9s",
    "cert-manager/cert-manager",
    "datreeio/datree",
    "mozilla/sops"
]

# Loop through each repository and get the latest release tag
for repo in repos:
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        # Extract the tag name from the response JSON
        tag_name = response.json()["tag_name"]
        # Save the tag name as a variable with the repository name
        var_name = f"version_{repo.replace('/', '_')}"
        globals()[var_name] = tag_name
        print(f"Latest version for {repo}: {tag_name}")
        # Find and replace the version variable in local.yml
        filename = os.path.join(os.path.dirname(__file__), "local.yml")
        with open(filename, "r+") as file:
            content = file.read()
            # Replace the variable using regex
            content = re.sub(fr"version_{repo.replace('/', '_')}:\s*\".*\"", f"version_{repo.replace('/', '_')}: \"{tag_name}\"", content)
            # Move the file pointer back to the beginning of the file
            file.seek(0)
            file.write(content)
            file.truncate()
            print(f"Version variable updated in {filename}")
    else:
        print(f"Error getting latest release for {repo}: {response.text}")
