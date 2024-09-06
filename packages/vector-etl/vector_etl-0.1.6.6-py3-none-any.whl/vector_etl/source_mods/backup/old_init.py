from source_mods.s3_loader import S3Source
from source_mods.database_loader import DatabaseSource
from source_mods.dropbox_loader import DropboxSource
from source_mods.stripe_loader import StripeSource
from source_mods.zendesk_loader import ZendeskSource
from source_mods.google_drive import GoogleDriveSource
from source_mods.google_cloud_storage import GoogleCloudStorageSource


def get_source_class(config):
    source_type = config['source_data_type']
    if source_type in ['Amazon S3', 'File Upload']:
        return S3Source(config)
    elif source_type == 'database':
        return DatabaseSource(config)
    elif source_type == 'Dropbox':
        return DropboxSource(config)
    elif source_type == 'stripe':
        return StripeSource(config)
    elif source_type == 'zendesk':
        return ZendeskSource(config)
    elif source_type == 'Google Drive':
        return GoogleDriveSource(config)
    elif source_type == 'Google Cloud Storage':
        return GoogleCloudStorageSource(config)
    else:
        raise ValueError(f"Unsupported source type: {source_type}")
