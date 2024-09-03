from datetime import datetime
from click import echo
import zipfile
from os import walk, makedirs
from os.path import abspath, basename, dirname, getctime, getmtime, relpath, join, expanduser
import platform

class Utilities:
    @staticmethod
    def handle_response(response):
        if not str(response.status_code).startswith('2'):
            error_message = response.json().get('error', 'An unknown error occurred')
            echo(f'Error: {error_message}', err=True)
            return False
        return True

    @staticmethod
    def get_download_folder():
        system = platform.system()

        if system == 'Windows':
            import winreg as reg
            sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'

            with reg.OpenKey(reg.HKEY_CURRENT_USER, sub_key) as key:
                downloads_folder = reg.QueryValueEx(key, downloads_guid)[0]

        else:  # Linux and other Unix-like systems like macOS
            downloads_folder = join(expanduser('~'), 'Downloads')

        return downloads_folder

    @staticmethod
    def zip_folder(folder_path):
        # Array associatif with path, modification time, and creation time
        file_details = {} 
        
        abs_folder_path = abspath(folder_path)
        
        # Output path is temp folder / folder_name.zip
        output_path = join(dirname(folder_path) + "/temp/", basename(folder_path) + '.zip')
        
        print("Output path: ", folder_path)
        #Create Dictionary with file details
        folder_details = {
            'path_abs': abs_folder_path,
            'path_rel': folder_path, 
            'date_modification': Utilities.get_date_modification(folder_path).isoformat(),
            'date_creation': Utilities.get_date_creation(folder_path).isoformat()
        }
        
        file_details["folder"] = folder_details  

        #Print file details
        
        with zipfile.ZipFile(output_path, 'w') as zipf:
            for root, dirs, files in walk(folder_path):
                for file in files:
                    print("FILE: ", file)
                    print("ROOT: ", root)
                    file_path = join(root, file)

                    zipf.write(file_path, relpath(file_path, folder_path))

                    file_details[file_path] = {
                        'path_abs': abspath(file_path),
                        'path_rel': file_path,
                        'date_modification': Utilities.get_date_modification(file_path).isoformat(),
                        'date_creation': Utilities.get_date_creation(file_path).isoformat()
                    }

        return output_path, file_details
    
    @staticmethod
    def unzip_folder(zip_path):
        # create a folder in the same directory as the zip file
        folder = zip_path.split('.')[0]
        makedirs(folder, exist_ok=True)

       #unzip the zip into the folder
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(folder)

    @staticmethod
    def get_date_modification(path):
        date = datetime.fromtimestamp(getmtime(path))
        return date
    
    @staticmethod
    def get_date_creation(path):
        creation_time_seconds = getctime(path)
        return datetime.fromtimestamp(creation_time_seconds)