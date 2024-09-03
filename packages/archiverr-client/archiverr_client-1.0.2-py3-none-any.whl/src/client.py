import requests
import zipfile
import os
import time

def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w') as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                
                print(os.path.join(root, file))
                print(os.path.relpath(os.path.join(root, file), folder_path))
                print("--------------------------------------------------")
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), folder_path))

def send_folder(folder_path, output_path):
    start_time = time.time()
    zip_folder(folder_path, zip_path)
    
    url = '/upload'
    
    # Ajouter le paramètre 'isCompressed' pour indiquer que le fichier est compressé
    files = {'file': open(zip_path, 'rb')}
    data = {'isCompressed': 'true'}
    response = requests.post(url, files=files, data=data)
    
    
    end_time = time.time()
    
    if response.text:
        try:
            print(response.json())
        except ValueError:
            print("Invalid JSON")
    else:
        print("Empty Response")
    print(f"API REST ZIP Transfer Time: {end_time - start_time:.2f} seconds")

folder_path = 'D:/Developpement/ArchiverR_Client/frontend/src'
zip_path = 'D:/Developpement/ArchiverR_Client/src.zip'