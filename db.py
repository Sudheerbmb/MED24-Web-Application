import boto3
import subprocess
import os

# AWS S3 Configuration
bucket_name = 'devendrababu'
file_key = 'Dump20250312/your-mysql-dump-file.sql'  # Replace with the actual MySQL dump file name
local_file_path = 'database/mysql-dump-file.sql'  # Local directory to save the dump file

# Initialize the S3 client
s3 = boto3.client('s3', region_name='ap-south-1')

# Download the MySQL dump from S3 to local machine
try:
    s3.download_file(bucket_name, file_key, local_file_path)
    print(f"File downloaded successfully to {local_file_path}")
except Exception as e:
    print(f"Error downloading file: {e}")
    exit(1)

# Import the downloaded dump file into MySQL
try:
    # Make sure MySQL is running and replace with correct database name
    subprocess.run(['mysql', '-u', 'root', '-p', 'your_database_name', 
                    f'< {local_file_path}'], check=True)
    print(f"MySQL dump imported into your_database_name successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error importing MySQL dump: {e}")
    exit(1)