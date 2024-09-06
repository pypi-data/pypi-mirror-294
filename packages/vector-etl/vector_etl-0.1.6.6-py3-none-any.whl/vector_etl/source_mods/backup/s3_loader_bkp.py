import boto3
import pandas as pd
import os
import logging
from langchain_community.document_loaders import UnstructuredFileLoader
from source_mods.base import BaseSource

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class S3Source(BaseSource):
    def __init__(self, config):
        self.config = config
        self.s3_client = None

    def connect(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=self.config['aws_access_key_id'],
            aws_secret_access_key=self.config['aws_secret_access_key']
        )
        logger.info("Connected to Amazon S3")

    def fetch_data(self):
        if not self.s3_client:
            self.connect()

        bucket_name = self.config['bucket_name']
        prefix = self.config['key']
        file_type = self.config['file_type']
        chunk_size = self.config['chunk_size']
        chunk_overlap = self.config['chunk_overlap']

        paginator = self.s3_client.get_paginator('list_objects_v2')
        downloaded_files = []
        new_files = []

        logger.info("Downloading files from S3...")
        for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
            for obj in page.get('Contents', []):
                if obj['Key'].endswith(file_type):
                    new_files.append(obj['Key'])
                    file_path = os.path.join(os.getcwd(), obj['Key'].split('/')[-1])
                    self.s3_client.download_file(bucket_name, obj['Key'], file_path)
                    downloaded_files.append(file_path)
                    logger.info(f"Downloaded {obj['Key']} to {os.getcwd()}")

        logger.info("Processing downloaded files...")
        df = pd.DataFrame()
        for file in downloaded_files:

            if file_type == 'csv':
                temp_df = pd.read_csv(file)

            elif file_type in ['txt', 'pdf']:
                loader = UnstructuredFileLoader(
                    file, mode="elements", strategy="fast",
                )
                docs = loader.load()
                document = []
                category = []
                file_type = []
                source = []
                page_number = []

                for doc in docs:
                    document.append(doc.page_content)
                    category.append(doc.metadata['category'])
                    file_type.append(doc.metadata['filetype'])
                    source.append(doc.metadata['source'])
                    page_number.append(doc.metadata['page_number'] if 'page_number' in doc.metadata else 1)

                data = {
                    'text': document,
                    'category': category,
                    'file_type': file_type,
                    'source': source,
                    'page_number': page_number
                }

                temp_df = pd.DataFrame(data)

            if not df.empty:
                df = pd.concat([df, temp_df], ignore_index=True)

            else:
                df = temp_df

            os.remove(file)  # Clean up downloaded file

        return df#, new_files
