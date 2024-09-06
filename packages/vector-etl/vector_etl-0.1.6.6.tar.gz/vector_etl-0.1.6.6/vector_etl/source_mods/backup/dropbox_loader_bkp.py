import dropbox
import pandas as pd
import os
import logging
from langchain_community.document_loaders import UnstructuredFileLoader
from source_mods.base import BaseSource

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DropboxSource(BaseSource):
    def __init__(self, config):
        self.config = config
        self.dbx = None

    def connect(self):
        self.dbx = dropbox.Dropbox(self.config["key"])
        # logger.info("Connected to Dropbox")
        logger.info("{} {} {}".format("=" * 10, "Connected to Dropbox", "=" * 10))

    def fetch_data(self):
        if not self.dbx:
            self.connect()

        folder_path = self.config["folder_path"]
        file_type = self.config["file_type"]
        chunk_size = self.config['chunk_size']
        chunk_overlap = self.config['chunk_overlap']

        download_folder = 'dropbox_downloads'
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        files = self.list_files(folder_path, file_type)
        new_files = []
        downloaded_files = []

        for file_path in files:
            new_files.append(file_path)
            local_path = os.path.join('dropbox_downloads', os.path.basename(file_path))
            with open(local_path, "wb") as f:
                metadata, res = self.dbx.files_download(path=file_path)
                f.write(res.content)
            downloaded_files.append(local_path)

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

        os.rmdir('dropbox_downloads')

        return df#, new_files

    def list_files(self, folder_path, filetype):
        try:
            response = self.dbx.files_list_folder(folder_path, recursive=True)
            files = []
            while True:
                for entry in response.entries:
                    if isinstance(entry, dropbox.files.FileMetadata):
                        if entry.name.endswith(filetype):
                            files.append(entry.path_lower)
                if response.has_more:
                    response = self.dbx.files_list_folder_continue(response.cursor)
                else:
                    break
            return files
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            return []
