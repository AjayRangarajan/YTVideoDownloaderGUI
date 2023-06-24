import logging
from logging import Logger
from datetime import datetime
from pathlib import Path
import shutil


class LogHelper:

    MAX_LOG_SIZE = 10 * 1024 * 1024
    LOG_DELETE_SUCCESS = "SUCCESS"
    LOG_FOLDER = Path(__file__).resolve().parent.parent / "logs"

    @staticmethod
    def get_formatted_file_size(size_in_bytes: int) -> str:
        if size_in_bytes < 1024 * 1024:
            size_str = f"{size_in_bytes / 1024:.2f} KB"
        elif size_in_bytes < 1024 * 1024 * 1024:
            size_str = f"{size_in_bytes / (1024 * 1024):.2f} MB"
        else:
            size_str = f"{size_in_bytes / (1024 * 1024 * 1024):.2f} GB"
        return size_str

    def get_log_folder_size(self) -> int:
        total_size = 0
        for file in self.LOG_FOLDER.glob('**/*'):
            if file.is_file():
                total_size += file.stat().st_size
        return total_size
    
    def delete_logs(self) -> str:
        try:
            shutil.rmtree(self.LOG_FOLDER)
        except:
            return
        
        try:
            self.LOG_FOLDER.mkdir(parents=True)      
        except:
            self.LOG_FOLDER = Path(__file__).resolve().parent.parent / "logs"
        
        print(self.LOG_DELETE_SUCCESS)
        return self.LOG_DELETE_SUCCESS

    def get_logger(self, module) -> Logger:
        
        log_folder_size = self.get_log_folder_size()
        deleted_success = self.LOG_DELETE_SUCCESS
        if log_folder_size > self.MAX_LOG_SIZE:
            deleted_success = self.delete_logs()

        current_date = datetime.now()
        formatted_date = current_date.strftime('%d_%m_%Y')
        logging.basicConfig(
            filename=self.LOG_FOLDER.joinpath(f"{formatted_date}_logs.txt"), 
            filemode='a', 
            format='%(asctime)s %(name)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s', 
            datefmt='%d %B %Y %H:%M:%S', 
            level=logging.DEBUG
        )
        logger = logging.getLogger(module)
        if deleted_success != self.LOG_DELETE_SUCCESS:
            log_folder_size = self.get_log_folder_size()
            formatted_log_folder_size = self.get_formatted_file_size(log_folder_size)
            logger.error(f"FAILED TO DELETE SOME LOG FILES! EXISTING LOG FOLDER SIZE: {formatted_log_folder_size}")

        return logger