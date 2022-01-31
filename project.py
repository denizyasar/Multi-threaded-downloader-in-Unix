import os
from hashlib import sha256
from multiprocessing import Lock, Process
from pathlib import Path
from uuid import uuid4

import requests

# URL addresses
URL1 = "http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg"
URL2 = "https://upload.wikimedia.org/wikipedia/tr/9/98/Mu%C4%9Fla_S%C4%B1tk%C4%B1_Ko%C3%A7man_%C3%9Cniversitesi_logo.png"
URL3 = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg"
URL4 = "http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg"
URL5 = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg"


def download_file(url, file_name=None):
    r = requests.get(url, allow_redirects=True)
    if file_name:
        file = file_name
    else:
        file = str(uuid4())
    open(file, 'wb').write(r.content)


def child_func():    
    download_file(URL1, "url1.jpeg")
    download_file(URL2, "url2.png")
    download_file(URL3, "url3.jpg")
    download_file(URL4, "url4.jpeg")
    download_file(URL5, "url5.jpg")


def check_files(lock):
    lock.acquire()
    # generate dictionary for file and hash
    file_hash_list = {}
    # select files and folders in current folder
    for item in os.listdir():
        # check if item is file or not
        if os.path.isfile(os.path.join(".", item)):
            # check if the file is running script or downloaded files
            if item != Path(__file__).name:
                # open file
                with open(item, "rb") as f:
                    bytes = f.read()
                    # generate hash for file
                    hash = sha256(bytes).hexdigest()
                    # add file and hash to dictionary
                    file_hash_list[item] = hash

    # find duplicate hashes in dictionary and print
    new_dict = file_hash_list.copy()
    for key, value in file_hash_list.items():
        exist = False
        for k, v in new_dict.items():
            if key != k and value == v:
                print("Have same hash:", key, k, value)
                exist = True
                break
        if exist:
            new_dict.pop(k)
            new_dict.pop(key)
    lock.release()


if __name__ == '__main__':
    # Create a child process
    child_process = os.fork()

    # run child process
    if child_process == 0:
        print("Child Process ID: " + str(os.getpid()))
        child_func()

    # run main process
    else:
        print("Main Process ID: " + str(os.getpid()))
        # wait for child process
        os.wait()
        # check files process
        lock = Lock()
        p1 = Process(target=check_files(lock))
        p1.start()
