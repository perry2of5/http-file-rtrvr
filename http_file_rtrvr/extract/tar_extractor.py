from http_file_rtrvr.extract.abstract_extractor import AbstractExtractor
from http_file_rtrvr.extract.extraction_exception import ExtractionException
import tarfile
import os

class TarExtractor(AbstractExtractor):
    tar_gz_long_form = ".tar.gz"

    def __init__(self):
        super().__init__()

    def extract_to_temp_dir(
            self,
            archive: str, 
            temp_dir: str) -> str:
        """
        Extracts the contents of an .tar, .tar.gz, or .tgz to a temporary directory.

        Args:
            archive: file to extract. Contents are extracted from <file>.tgz to <temp_dir>/<file>/*
            temp_dir: path to temporary directory to extract archive contents to. The directory "temp_dir"
                should exist and the contents will be extracted into a directory named by the archive file name 
                but with the extension removed. I.e., files from "archive.tgz" will be extracted to 
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
        
        if not tarfile.is_tarfile(archive):
            raise ExtractionException(f"File {archive} is not a tar file (.tar, .tar.gz, or .tgz).")

        try:
            archive_name_with_ext = os.path.basename(archive)
            archive_name = os.path.splitext(archive_name_with_ext)[0]
            if archive_name_with_ext.endswith(self.tar_gz_long_form):
                # splitext doesn't know about .tar.gz as a single extension, so handle that case
                archive_name = archive_name_with_ext[:(-1 * self.tar_gz_long_form.length)]
            extract_dir = os.path.join(temp_dir, archive_name)
            if not os.path.exists(extract_dir):
                os.makedirs(extract_dir)
            print("Extracting to:", extract_dir)
            with tarfile.open(archive, 'r') as archive_ref:
                # filter='data' protects against directory traversal attacks
                archive_ref.extractall(path=extract_dir, filter='data')
            return extract_dir
        except Exception as e:
            raise ExtractionException(f"Failed to extract {archive} to {extract_dir}.", e)
            