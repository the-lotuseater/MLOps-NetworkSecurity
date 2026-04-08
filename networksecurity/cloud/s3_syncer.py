import os

class S3Syncer:

    def sync_folder_to_s3(self, local_folder: str, aws_bucket_url: str):
        try:
            command = f'aws s3 sync {local_folder} {aws_bucket_url}'
            os.system(command)
        except Exception as e:
            print(f"Error syncing folder to S3: {e}")
    
    def sync_folder_from_s3(self, local_folder: str, aws_bucket_url: str):
        try:
            command = f'aws s3 sync {aws_bucket_url} {local_folder}'
            os.system(command)
        except Exception as e:
            print(f"Error syncing folder from S3: {e}")

    