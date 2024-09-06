import logging
import pandas as pd
import os
from source_mods.base import BaseSource

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LocalFileSource(BaseSource):
    def __init__(self, config):
        self.config = config
        self.file_path = config['file_path']
        self.file_type = config['file_type']
        self.chunk_size = config.get('chunk_size', 1000)
        self.chunk_overlap = config.get('chunk_overlap', 0)

    def connect(self):
        # For local files, we don't need to establish a connection
        # But we'll verify that the file exists
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"The file {self.file_path} does not exist.")
        logger.info(f"Verified existence of local file: {self.file_path}")

    def fetch_data(self):
        logger.info(f"Reading data from local file: {self.file_path}")

        if self.file_type.lower() == '.csv':
            df = pd.read_csv(self.file_path)
        elif self.file_type.lower() in ['.xlsx', '.xls']:
            df = pd.read_excel(self.file_path)
        elif self.file_type.lower() == '.json':
            df = pd.read_json(self.file_path)
        elif self.file_type.lower() == '.txt':
            with open(self.file_path, 'r') as file:
                content = file.read()
            df = pd.DataFrame({'text': [content]})
        else:
            raise ValueError(f"Unsupported file type: {self.file_type}")

        if not df.empty:
            df = self.split_dataframe_column(df, self.chunk_size, self.chunk_overlap)

        new_files = [self.file_path]  # For consistency with other source classes
        return df, new_files

    def split_dataframe_column(self, df, chunk_size, chunk_overlap, column='text'):
        logger.info("Splitting dataframe into chunks...")

        if column not in df.columns:
            logger.warning(f"Column '{column}' not found in dataframe. Skipping splitting.")
            return df

        def split_text(text, size, overlap):
            if not isinstance(text, str):
                return []
            return [text[i:i + size] for i in range(0, len(text), size - overlap) if text[i:i + size]]

        new_rows = []
        for _, row in df.iterrows():
            chunks = split_text(row[column], chunk_size, chunk_overlap)
            for chunk in chunks:
                if chunk:
                    new_row = row.copy()
                    new_row[column] = chunk
                    new_rows.append(new_row)

        return pd.DataFrame(new_rows, columns=df.columns)
