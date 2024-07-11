from http_file_rtrvr.extract.abstract_extractor import AbstractExtractor
from http_file_rtrvr.extract.extraction_exception import ExtractionException
from zipfile import ZipFile 
import os

class ZipExtractor(AbstractExtractor):
    def __init__(self):
        super().__init__()

    def extract_to_temp_dir(
            self,
            archive: str, 
            temp_dir: str) -> str:
        """
        Extracts the contents of an zip to a temporary directory.

        Args:
            archive: file to extract. Contents are extracted from <file>.zip to <temp_dir>/<file>/*
            temp_dir: path to temporary directory to extract archive contents to. The directory "temp_dir"
                should exist and the contents will be extracted into a directory named by the archive file name 
                but with the extension removed. I.e., files from "archive.zip" will be extracted to 
                "temp_dir/archive".

        returns:
            str: The path to the directory where the archive was extracted.
        """
        # throw ExtractionException if temp_dir does not exist
        if not os.path.exists(temp_dir):
            raise ExtractionException(f"Temporary directory {temp_dir} does not exist.")
        
        # throw ExtractionException if archive does not exist
        if not os.path.exists(archive):
            raise ExtractionException(f"Archive {archive} does not exist.")
        
        try:
            archive_name_with_ext = os.path.basename(archive)
            archive_name = os.path.splitext(archive_name_with_ext)[0]
            extract_dir = os.path.join(temp_dir, archive_name)
            if not os.path.exists(extract_dir):
                os.makedirs(extract_dir)
            with ZipFile(archive, 'r') as zip_ref:
                zip_ref.extractall(path=extract_dir)
            return extract_dir
        except Exception as e:
            raise ExtractionException(f"Failed to extract {archive} to {extract_dir}.", e)
