import os
import requests

IP = 'localhost'
PORT = '8080'
CLASSIFIER = 'tagbox'
VALID_FILETYPES = ('.jpg', '.png', '.jpeg')

TEACH_URL = "http://{}:{}/{}/teach".format(IP, PORT, CLASSIFIER)
HEALTH_URL = "http://{}:{}/readyz".format(IP, PORT)


def check_classifier_health():
    """Check that classifier is reachable"""
    try:
        response = requests.get(HEALTH_URL)
        if response.status_code == 200:
            print("{} health-check passed".format(CLASSIFIER))
            return True
        else:
            print("{} health-check failed".format(CLASSIFIER))
            print(response.status_code)
            return False
    except requests.exceptions.RequestException as exception:
        print("{} is unreachable".format(CLASSIFIER))
        print(exception)


def list_folders(directiory='.'):
    """Returns a list of folders in a dir, defaults to current dir.
    These are not full paths, just the folder."""
    folders = [dir for dir in os.listdir(directiory)
               if os.path.isdir(os.path.join(directiory, dir))
               and not dir.startswith(directiory)
               and not dir.startswith('.')]
    folders.sort(key=str.lower)
    return folders


def teach_tag_by_file(teach_url, tag, file_path):
    """Teach tagbox a single tag using a single file."""
    file_name = file_path.split("/")[-1]
    file = {'file': open(file_path, 'rb')}
    data = {'tag': tag, "id": file_name}

    response = requests.post(teach_url, files=file, data=data)

    if response.status_code == 200:
        print("File:{} tagged with tag:{}".format(file_name, tag))
        return True

    elif response.status_code == 400:
        print("Tagging of file:{} failed with message:".format(
            file_name, response.text))
        return False


def main():
    if check_classifier_health():
        for folder_name in list_folders():
            folder_path = os.path.join(os.getcwd(), folder_name)
            for file in os.listdir(folder_path):
                if file.endswith(VALID_FILETYPES):
                    file_path = os.path.join(folder_path, file)
                    teach_tag_by_file(teach_url=TEACH_URL,
                                      tag=folder_name,
                                      file_path=file_path)


if __name__ == '__main__':
    main()
