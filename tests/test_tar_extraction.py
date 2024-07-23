from http_file_rtrvr.extract.tar_extractor import TarExtractor
import os

class TestTarExtractor:
    test_temp_dir = "/tmp/extractor_test"
     
    def test_extract_tgz_to_temp_dir(self):
        #ensure temp directory exists
        already_exists = os.path.exists(self.test_temp_dir)
        if not already_exists:
            os.makedirs(self.test_temp_dir)

        print("current directory:", os.getcwd())
        test_archive_path = os.path.join(os.getcwd(), "tests/test_archives/tgz_archive.tgz")

        try:
            # get the name of the archive file
            extracted_to = TarExtractor().extract_to_temp_dir(test_archive_path, self.test_temp_dir)

            archive_name_with_ext = os.path.basename(test_archive_path)
            archive_name = os.path.splitext(archive_name_with_ext)[0]
            if archive_name_with_ext.endswith(".tar_gz"):
                # splitext doesn't know about .tar.gz as a single extension, so handle that case
                archive_name = archive_name_with_ext[:(-1 * 7)]
            expected_files = ["hi.txt", "bye.txt", "short_page.html"]
            # check to see all files were extracted
            extracted_to_expected = os.path.join(self.test_temp_dir, archive_name)
            print("Test extracting to:", extracted_to_expected)
            assert extracted_to_expected == extracted_to
            for file in os.listdir(extracted_to_expected):
                print("Found file:", file)
                expected_files.remove(file)
                # delete extract file, we don't need it any more
                os.remove(os.path.join(self.test_temp_dir, archive_name, file))
            # and delete extract directory, we don't need it any more either
            os.rmdir(os.path.join(self.test_temp_dir, archive_name))

            if len(expected_files) > 0:
                raise Exception(f"Not all files were extracted, missing files: {expected_files}")
        finally:
            if (not already_exists):
                os.rmdir(self.test_temp_dir)



        # TODO: need to test extracting a .tar.gz file
        # TODO: need to test extracting a .tar file

        # TODO: Test code raises an ExtractionException if the temp_dir does not exist.
        # TODO: Test code raises an ExtractionException if the archive does not exist.
        # TODO: Test code raises an ExtractionException if the extraction fails.
