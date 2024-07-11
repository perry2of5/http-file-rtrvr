from http_file_rtrvr.uploader.abstract_file_uploader import AbstractFileUploader
from http_file_rtrvr.uploader.abstract_file_tree_uploader import AbstractFileTreeUploader

class AlwaysSucceedFileTreeUploader(AbstractFileTreeUploader):
    upload_path_log = []

    def upload_file_tree(self, file_tree_path: str):
        self.upload_path_log.append(file_tree_path)
        return