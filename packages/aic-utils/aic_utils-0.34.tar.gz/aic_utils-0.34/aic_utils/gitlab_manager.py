import hashlib
import requests
from datetime import datetime

class GitLabManager:
    def __init__(self, aic_instance, gitlab_namespace='pin/pin-analytics/pin-fusion-2.0/pipelines', 
                 gitlab_base_url='https://git.autodatacorp.org/api/v4', use_hash=False):
        self.aic = aic_instance
        self.gitlab_base_url = gitlab_base_url
        self.gitlab_namespace = gitlab_namespace
        self.use_hash_comparison = use_hash
        self.gitlab_token = self.read_gitlab_token()
        self.headers = {
            'Private-Token': self.gitlab_token,
            'Content-Type': 'application/json'
        }

        # Check and report the token expiration status immediately upon creation
        print('GitLab instance created.')
        self.check_token_expiration()


    def read_gitlab_token(self):
        """Reads the GitLab token from the storage drive."""
        try:
            content = self.aic.download_file(self.aic.drive_id, 'gitlab_token.txt')
            if content:
                return content.strip()
            else:
                raise ValueError("GitLab token file is empty or not found.")
        except Exception as e:
            print(f"Error reading GitLab token: {str(e)}")
            raise ValueError("Failed to read GitLab token from storage.")


    def generate_hash(self, content):
        """Generates a hash for the given content."""
        return hashlib.md5(content.encode('utf-8')).hexdigest()


    def get_existing_file_content(self, repo_name, file_name):
        """Fetches the existing content of a file from the specified repository in GitLab."""
        project_url = f"{self.gitlab_base_url}/projects/{repo_name.replace('/', '%2F')}/repository/files/{file_name}?ref=main"
        try:
            response = requests.get(project_url, headers=self.headers)
            if response.status_code == 200:
                file_info = response.json()
                return file_info.get('content')
            else:
                print(f"Failed to fetch existing file content: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except Exception as e:
            print(f"Error fetching existing file content: {str(e)}")
            return None


    def push_file(self, repo_name, file_name, file_content):
        """Pushes a file to the specified repository in GitLab, only if the content has changed."""
        if self.use_hash_comparison:
            # Fetch existing content and compare hashes
            existing_content = self.get_existing_file_content(repo_name, file_name)
            if existing_content:
                existing_hash = self.generate_hash(existing_content)
                current_hash = self.generate_hash(file_content)
                
                # Compare hashes
                if existing_hash == current_hash:
                    print(f"No changes detected for {file_name}. Skipping push.")
                    return

        print(f"Configuration has changed for {file_name}. Pushing update.")
        project_url = f"{self.gitlab_base_url}/projects/{repo_name.replace('/', '%2F')}/repository/files/{file_name}"
        data = {
            'branch': 'main',
            'content': file_content,
            'commit_message': f"Update {file_name} - {datetime.now().strftime('%Y-%m-%d')}"
        }
        
        try:
            # Attempt to create or update the file
            response = requests.post(project_url, headers=self.headers, json=data)
            if response.status_code == 201:
                print(f"Successfully created {file_name} in repository: {repo_name}")
            elif response.status_code == 400 and "already exists" in response.text:
                # File exists; try updating instead
                response = requests.put(project_url, headers=self.headers, json=data)
                if response.status_code == 200:
                    print(f"Successfully updated {file_name} in repository: {repo_name}")
                else:
                    print(f"Failed to update {file_name} in repository: {repo_name}")
                    print(f"Response: {response.text}")
            else:
                print(f"Failed to push {file_name} to repository: {repo_name}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error pushing file to GitLab: {str(e)}")
