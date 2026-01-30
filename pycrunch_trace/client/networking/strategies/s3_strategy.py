import logging
import os
from typing import List
from pathlib import Path

from pycrunch_trace.client.networking.strategies.native_write_strategy import NativeLocalRecordingStrategy
from pycrunch_trace.config import config
from pycrunch_trace.file_system.persisted_session import PersistedSession

logger = logging.getLogger(__name__)

class S3RecordingStrategy(NativeLocalRecordingStrategy):
    def __init__(self):
        super().__init__()
        self.bucket_name = config.s3_bucket
        self.prefix = config.s3_prefix
        self._s3_client = None

    @property
    def s3_client(self):
        if self._s3_client is None:
            import boto3
            self._s3_client = boto3.client('s3')
        return self._s3_client

    def recording_stop(self, session_id: str, files_included: List[str], files_excluded: List[str]):
        # First, ensure local files are completed via NativeLocalRecordingStrategy
        super().recording_stop(session_id, files_included, files_excluded)
        
        # Now upload the results to S3
        self.upload_session_to_s3(session_id)

    def upload_session_to_s3(self, session_id: str):
        if not self.bucket_name:
            logger.error("S3 bucket name not configured. Cannot upload session.")
            return

        session_dir = Path(self.persistence.rec_dir).joinpath(session_id)
        
        files_to_upload = [
            PersistedSession.chunked_recording_filename,
            PersistedSession.metadata_filename
        ]

        for filename in files_to_upload:
            local_path = session_dir.joinpath(filename)
            if local_path.exists():
                s3_key = os.path.join(self.prefix, session_id, filename)
                logger.info(f"Uploading session results to S3: s3://{self.bucket_name}/{s3_key}")
                try:
                    self.s3_client.upload_file(str(local_path), self.bucket_name, s3_key)
                except Exception as e:
                    logger.error(f"Failed to upload {filename} to S3: {str(e)}", exc_info=True)
            else:
                logger.warning(f"Skipping S3 upload: Local file not found at {local_path}.")
