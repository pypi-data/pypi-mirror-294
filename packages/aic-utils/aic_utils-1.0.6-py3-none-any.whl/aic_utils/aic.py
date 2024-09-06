import requests
import json 
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from google.cloud import storage
from datetime import datetime
from .gitlab_manager import GitLabManager

class AIC():
    timestamp = datetime.today().strftime('%Y%m%d')
    
    def __init__(self, api_key, project, workspace, pipelines=[], gitlab_token=None):
        self.base_url = 'https://prod.jdpower.ai/apis/core/v1'
        self.api_key = api_key
        self.headers = {
            'accept': '*/*',
            'api-key': api_key
        }
        self.project_id = self.get_project(project)
        self.workspace = workspace
        self.workspace_id = self.get_workspace(workspace)
        self.drive_id = self.get_drive_id()
        # self.get_data()
        self.pipelines = self.pop_pipelines()
        self.pipeline_configs = self.pop_pipeline_config(pipelines)
        self.gitlab_manager = GitLabManager(self, gitlab_token=gitlab_token)
    
    def get_data(self):
        print(f'Project ID: {self.project_id}')
        print(f'Workspace ID: {self.workspace_id}')
        print(f'Drive ID: {self.drive_id}')
    
    
    def get_config(self):
        return self.pipeline_configs
    
    
    def get_project(self, project):
        url = f"{self.base_url}/projects"
        response = requests.get(url, headers=self.headers)
        for obj in response.json():
            if obj['name'] == project:
                return obj['$id']
        raise Exception(f'No project with name {project} found')
    
    
    def get_workspace(self, workspace):
        url = f"{self.base_url}/projects/{self.project_id}/workspaces"
        response = requests.get(url, headers=self.headers)
        for obj in response.json():
            if obj['name'] == workspace:
                return obj['$id']
        raise Exception(f'No workspace with name {workspace} found')
        
        
    def pop_pipelines(self): 
        pipelines = []
        url = f"{self.base_url}/projects/{self.project_id}/workspaces/{self.workspace_id}/jobs"
        response = requests.get(url, headers=self.headers)
        for obj in response.json()['jobs']:
            # print(f"Creating pipeline object: {obj['title']} ID: {obj['$id']}")
            pipelines.append({'name':obj.get('title','NO TITLE'), 'id':obj['$id']})
        return pipelines
    
    
    def fetch_pipeline_config(self, pipeline):
        """Fetch a single pipeline configuration."""
        name = pipeline['name']
        id = pipeline['id']
        url = f"{self.base_url}/projects/{self.project_id}/workspaces/{self.workspace_id}/jobs/{id}"
        print(f'Retrieving config for {name}...')
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return {'name': name, 'jobConfig': data['jobConfig'], 'id':data['jobConfig']['$id']}
        else:
            print(f'Failed to fetch {name}: {response.status_code}')
            return None

        
    def pop_pipeline_config(self, pipelines):
        """Fetch configurations for the given pipelines in parallel using ThreadPoolExecutor."""
        configs = []
        with ThreadPoolExecutor() as executor:
            pipeline_map = {pipeline_name.upper(): pipeline_name for pipeline_name in pipelines}
            futures = {executor.submit(self.fetch_pipeline_config, pipeline): pipeline['name'] for pipeline in self.pipelines if pipeline['name'].upper() in pipeline_map}
            for future in futures:
                result = future.result()
                if result:
                    configs.append(result)
                else:
                    print(f'Pipeline {futures[future]} not found or failed to fetch.')

        return configs
        
        
    def get_drive_id(self, drive_name="config"):
        url = f"{self.base_url}/projects/{self.project_id}/workspaces/{self.workspace_id}/drives"
        response = requests.get(url, headers=self.headers)
        drives = response.json()
        for drive in drives:
            if drive['name'] == drive_name:
                print(f'Drive location added: {drive_name}')
                return drive['$id']
        return None

    
    def upload_json(self, file_name, json_content):
        url = f"{self.base_url}/projects/{self.project_id}/workspaces/{self.workspace_id}/drives/{self.drive_id}/upload-file"
        # Adjusting the files parameter to match the expected format
       
        headers = {
        'accept': '*/*',  # Accept any response type
        'api-key': self.api_key,  # Include your API key
        'Content-Type': 'text/plain'  # Specify JSON content type
        }
        
        try:
            # Send the request with the json parameter to ensure JSON format
            response = requests.post(url, headers=headers, json=json_content, params={'path': '.', 'fileName': file_name})
            response.raise_for_status()  # Check for HTTP errors
            return response.json()  # Return the JSON response from the server
        except requests.exceptions.HTTPError as err:
            print(f'HTTP error occurred: {err}')  # Handle HTTP errors
            print(f'Status Code: {response.status_code}')
            print(f'Response Text: {response.text}')
        except Exception as err:
            print(f'Other error occurred: {err}')  # Handle other exceptions
        return None

    
     # Method to push pipeline configs to GitLab
    def push_to_gitlab(self, pipelines=[]):
        """Pushes pipeline configurations to GitLab concurrently."""
        if not pipelines:
            pipelines = self.pipeline_configs
        
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.gitlab_manager.push_file_to_repo, config['name'].replace(" ", "_"), 
                                f"{config['name']}.json", 
                                json.dumps(config['jobConfig'], indent=4)): config['name']
                for config in pipelines
            }

            for future in as_completed(futures):
                pipeline_name = futures[future]
                try:
                    future.result()  # Retrieve the result to raise any exceptions that occurred
                except Exception as e:
                    print(f"Failed to push pipeline: {pipeline_name} due to {e}")
    
    
    def upload_configs_to_drive(self):
        for config in self.pipeline_configs:
            json = config['config']
            file_name = f"{config['name']}_{AIC.timestamp}.json"
            response = self.upload_json(file_name, json)
            print(response)
    
    def get_files_from_drive(self, drive_id=None):
        if not drive_id:
            drive_id = self.drive_id
        url = f"{self.base_url}/projects/{self.project_id}/workspaces/{self.workspace_id}/drives/{drive_id}/files"
                
        params = {
            'path': '.','filePattern': '*.'}
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            files = response.json()
            for file in files:
                print(file['items'])
        else:
            print(response.json())
                
                
    def download_file(self, drive_id, file_name):
        """
        Download a file from the storage drive and return its content in memory.

        Args:
            drive_id (str): The ID of the drive to download the file from.
            file_name (str): The name of the file to be downloaded.

        Returns:
            str: The content of the file as a string if successful, otherwise None.
        """
        url = f"{self.base_url}/projects/{self.project_id}/workspaces/{self.workspace_id}/drives/{drive_id}/files"
        params = {
            'path': '.',
            'filePattern': file_name
        }
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            try:
                files = response.json()
                if files and 'items' in files and len(files['items']) > 0:
                    file_info = files['items'][0]
                    gs_path = file_info.get('gsPath')

                    if gs_path:
                        return self.download_from_gcs(gs_path)
                    else:
                        print(f"'gsPath' missing in file info: {file_info}")
                else:
                    print(f"No matching files found for pattern: {file_name}. Response: {files}")
            except ValueError as e:
                print(f"Failed to parse JSON response: {e}")
        else:
            print(f"Failed to download file {file_name}: {response.status_code}")
            print(f"Response Text: {response.text}")

        return None

    def download_from_gcs(self, gs_path):
        """
        Download content from Google Cloud Storage using the gs_path.

        Args:
            gs_path (str): The Google Cloud Storage path (gs://bucket_name/path/to/file).

        Returns:
            str: The content of the file as a string if successful, otherwise None.
        """
        # Extract the bucket name and blob name from the gs_path
        try:
            gcs_client = storage.Client()  # Ensure this client is correctly authenticated
            bucket_name, blob_name = gs_path.replace("gs://", "").split("/", 1)
            bucket = gcs_client.bucket(bucket_name)
            blob = bucket.blob(blob_name)

            # Download the content as a string
            content = blob.download_as_text()
            return content
        except Exception as e:
            print(f"Error downloading from GCS: {str(e)}")
        return None


    def delete_file(self, drive_id, file_id):
        url = f"{self.base_url}/projects/{self.project_id}/workspaces/{self.workspace_id}/drives/{drive_id}/delete-files"
        response = requests.post(url, headers=self.headers, json={"fileIds": [file_id]})
        return response.status_code == 200


        
    @staticmethod
    def push_source_code(AIC_prod, AIC_qa, prod_to_qa=False, qa_to_prod=False, pipelines=[]):
        """
        Overwrite pipeline configurations between production and QA based on the specified direction 
        and only for the specified pipelines.
        
        Args:
            AIC_prod: Instance of AIC with production pipeline configurations.
            AIC_qa: Instance of AIC with QA pipeline configurations.
            prod_to_qa: Boolean indicating whether to overwrite QA with production configurations.
            qa_to_prod: Boolean indicating whether to overwrite production with QA configurations.
            pipelines: List of pipeline names that should be processed for pushing configurations.
        """
        if not pipelines:
            raise ValueError("List of pipelines is empty. Please specify tables to push source code.")

        if (prod_to_qa and qa_to_prod) or (not prod_to_qa and not qa_to_prod):
            raise ValueError(f"Incorrect push configuration: prod_to_qa={prod_to_qa}, qa_to_prod={qa_to_prod}.")

        for prod_pipeline in AIC_prod.pipeline_configs:
            prod_name = prod_pipeline['name']
            
            # Continue only if the production pipeline is in the specified pipelines list
            if prod_name not in pipelines:
                continue  # Skip to the next pipeline if not in the list

            for qa_pipeline in AIC_qa.pipeline_configs:
                qa_name = qa_pipeline['name']

                # Continue only if the QA pipeline is in the specified pipelines list
                if qa_name not in pipelines:
                    continue  # Skip if not in the list

                if prod_name == qa_name:
                    if prod_to_qa:
                        # Overwrite QA config with Production config
                        print(f"Overwriting QA config with Production config for pipeline: {prod_name} -> {qa_name}")
                        original_id = qa_pipeline['jobConfig']['$id']
                        qa_pipeline['jobConfig'] = prod_pipeline['jobConfig']
                        
                        # Update the $id in QA jobConfig to match the source $id
                        qa_pipeline['jobConfig']['$id'] = original_id
                        
                        # Ensure QA variable is set to True
                        for variable in qa_pipeline['jobConfig']['variables']:
                            if variable['id'] == 'QA':
                                variable['value'] = 'True'
                                break

                        # Write the updated config to the QA pipeline
                        AIC_qa.write_config_to_pipeline(qa_pipeline)
                        
                    elif qa_to_prod:
                        # Overwrite Production config with QA config
                        print(f"Overwriting Production config with QA config for pipeline: {qa_name} -> {prod_name}")
                        original_id = prod_pipeline['jobConfig']['$id']
                        prod_pipeline['jobConfig'] = qa_pipeline['jobConfig']
                        
                        # Update the $id in Production jobConfig to match the source $id
                        prod_pipeline['jobConfig']['$id'] = original_id
                        
                        # Ensure QA variable is set to False
                        for variable in prod_pipeline['jobConfig']['variables']:
                            if variable['id'] == 'QA':
                                variable['value'] = 'False'
                                break

                        # Write the updated config to the Production pipeline
                        AIC_prod.write_config_to_pipeline(prod_pipeline)
                    break  # Stop searching once a match is found
            else:
                # If no matching pipeline is found
                print(f'No matching pipelines for {prod_name}')


    def write_config_to_pipeline(self, config):
        """
        Upload the given configuration to the corresponding pipeline job.
        
        Args:
            config: Dictionary containing the pipeline configuration and name.
        """
        # Extract the job ID and configuration details
        job_id = config.get('id')  # Ensure 'id' is part of the config dictionary
        job_config = config['jobConfig']
        name = config['name']
        
        # Construct the upload URL
        url = f"{self.base_url}/projects/{self.project_id}/workspaces/{self.workspace_id}/jobs"
        
        # Set headers for JSON content
        headers = {
            'accept': '*/*',
            'api-key': self.api_key,
            'Content-Type': 'application/json'
        }

        # Print debug information
        print(f"Attempting to update the pipeline: {name}")
        print(f"Job ID: {job_id}")
        # print(f"URL: {url}")
        # print(f"Headers: {headers}")
        # print(f"Payload: {json.dumps(job_config, indent=4)}")  # Print the payload for debugging

        try:
            # Send the request to update the pipeline configuration
            response = requests.post(url, headers=headers, json=job_config)
            response.raise_for_status()  # Check for HTTP errors
            print(f"Successfully updated the pipeline: {name}")
            if response.json()['jobId'] != job_id:
                print('PUSH CONFIGURATION INCORRECT. REVIEW DESTINATION TABLE')
            print(response.json())  # Print the server's response
        except requests.exceptions.HTTPError as err:
            print(f'HTTP error occurred while updating pipeline {name}: {err}')
            print(f'Status Code: {response.status_code}')
            print(f'Response Text: {response.text}')
        except Exception as err:
            print(f'Other error occurred while updating pipeline {name}: {err}')
        return None
    