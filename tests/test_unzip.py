from http_file_rtrvr.extract.zip_extractor import ZipExtractor
import os

class TestZipExtractor:
    test_temp_dir = "/tmp/extractor_test"

    def test_extract_to_temp_dir(self):
        #ensure temp directory exists
        already_exists = os.path.exists(self.test_temp_dir)
        if not already_exists:
            os.makedirs(self.test_temp_dir)

        print("current directory:", os.getcwd())
        test_archive_path = os.path.join(os.getcwd(), "tests/test_archives/test_archive.zip")

        try:
            # get the name of the archive file
            extracted_to = ZipExtractor.extract_to_temp_dir(test_archive_path, self.test_temp_dir)


            archive_name_with_ext = os.path.basename(test_archive_path)
            archive_name = os.path.splitext(archive_name_with_ext)[0]
            expected_files = ["a.txt", "b.py"]
            # check to see all files were extracted
            extracted_to_expected = os.path.join(self.test_temp_dir, archive_name)
            assert extracted_to_expected == extracted_to
            for file in os.listdir(extracted_to_expected):
                print("Found file:", file)
                expected_files.remove(file)
                # delete extract file, we don't need it any more
                os.remove(os.path.join(self.test_temp_dir, archive_name, file))

            if len(expected_files) > 0:
                raise Exception(f"Not all files were extracted, missing files: {expected_files}")
        finally:
            if (not already_exists):
                os.rmdir(self.test_temp_dir)



        # Test that extract_to_temp_dir extracts the contents of the archive to the temporary directory.

        # Test that extract_to_temp_dir raises an ExtractionException if the temp_dir does not exist.
        # Test that extract_to_temp_dir raises an ExtractionException if the archive does not exist.
        # Test that extract_to_temp_dir raises an ExtractionException if the extraction fails.
