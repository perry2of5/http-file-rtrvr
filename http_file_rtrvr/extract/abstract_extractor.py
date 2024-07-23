
class AbstractExtractor:
    def __init__(self):
        pass

    def extract_to_temp_dir(
            archive: str, 
            temp_dir: str) -> str:
        """
        Extracts the contents of an archive to a temporary directory.

        Args:
            archive: path to archive such as zip file, tar file, or gzipped-tar file.
            temp_dir: path to temporary directory to extract archive contents to. The directory "temp_dir"
                should exist and the contents will be extracted into a directory named by the archive file name 
                but with the extension removed. I.e., files from "archive.zip" will be extracted to 
                "temp_dir/archive".
        returns:
            str: The path to the directory where the archive was extracted.

        Usage:
            None: use a subclass such as DirectoryToBlobUploader

        Raises:
            ExtractionException: If the extraction fails.
        """
        pass
