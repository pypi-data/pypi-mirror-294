import logging
import pandas as pd
import os
from google.cloud import storage
from io import BytesIO
from source_mods.base import BaseSource

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GoogleCloudStorageSource(BaseSource):
    def __init__(self, config):
        self.config = config
        self.client = None

    def connect(self):
        logger.info("Connecting to Google Cloud Storage...")
        self.client = storage.Client.from_service_account_json(self.config['credentials_path'])
        logger.info("Connected to Google Cloud Storage successfully.")

    def fetch_data(self):
        if not self.client:
            self.connect()

        bucket_name = self.config['bucket_name']
        prefix = self.config.get('prefix', '')
        file_type = self.config['file_type']
        chunk_size = self.config.get('chunk_size', 1000)
        chunk_overlap = self.config.get('chunk_overlap', 0)

        bucket = self.client.get_bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=prefix)

        df = pd.DataFrame()
        new_files = []

        for blob in blobs:
            if blob.name.endswith(file_type) and blob.name not in self.config.get('loaded_files', []):
                new_files.append(blob.name)

                content = blob.download_as_bytes()
                fh = BytesIO(content)

                temp_df = None
                try:
                    if file_type.lower() in ['xlsx', 'xls']:
                        temp_df = pd.read_excel(fh)
                    elif file_type.lower() == 'csv':
                        temp_df = pd.read_csv(fh)
                    elif file_type.lower() in ['txt', 'pdf']:
                        # Implement text processing logic here
                        # For now, we'll just read it as a string
                        temp_df = pd.DataFrame({'text': [fh.getvalue().decode('utf-8')]})
                    else:
                        logger.warning(f"Unsupported file type: {file_type}")
                        continue
                except Exception as e:
                    logger.error(f"Error processing file {blob.name}: {str(e)}")
                    continue

                if temp_df is not None and not temp_df.empty:
                    if df.empty:
                        df = temp_df
                    else:
                        df = pd.concat([df, temp_df], ignore_index=True)

        # if not df.empty:
        #     df = self.split_dataframe_column(df, chunk_size, chunk_overlap)

        return df#, new_files

    # def split_dataframe_column(self, df, chunk_size, chunk_overlap, column='__concat_final'):
    #     logger.info("Splitting dataframe into chunks...")
    #
    #     if column not in df.columns:
    #         logger.warning(f"Column '{column}' not found in dataframe. Skipping splitting.")
    #         return df
    #
    #     def split_text(text, size, overlap):
    #         if not isinstance(text, str):
    #             return []
    #         return [text[i:i + size] for i in range(0, len(text), size - overlap) if text[i:i + size]]
    #
    #     new_rows = []
    #     for _, row in df.iterrows():
    #         chunks = split_text(row[column], chunk_size, chunk_overlap)
    #         for chunk in chunks:
    #             if chunk:
    #                 new_row = row.copy()
    #                 new_row[column] = chunk
    #                 new_rows.append(new_row)
    #
    #     return pd.DataFrame(new_rows, columns=df.columns)
