import os
import requests

IP = 'localhost'
PORT = '8080'
CLASSIFIER = 'tagbox'
VALID_FILETYPES = ('.jpg', '.png', '.jpeg')

teach_api_url = "http://{}:{}/{}/teach".format(IP, PORT, CLASSIFIER)
health_api_url = "http://{}:{}/readyz".format(IP, PORT)


def list_folders(directiory='.'):
    """Returns a list of folders in a dir, defaults to current dir.
    These are not full paths, just the folder."""
    folders = [dir for dir in os.listdir(directiory)
               if os.path.isdir(os.path.join(directiory, dir))
               and not dir.startswith(directiory)
               and not dir.startswith('.')]
    folders.sort(key=str.lower)
    return folders


def test_classifier_health():
    """Check that classifier is reachable"""
    try:
        response = requests.get(health_api_url)
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


def main():
    if test_classifier_health():
        for folder_name in list_folders():
            folder_path = os.path.join(os.getcwd(), folder_name)
            for file in os.listdir(folder_path):
                if file.endswith(VALID_FILETYPES):
                    file_path = os.path.join(folder_path, file)
                    tag = folder_name
                    response = (requests.post(
                        teach_api_url,
                        data={'tag': tag, "id": file},
                        files={'file': open(file_path, 'rb')}
                        ))

                    if response.status_code == 200:
                        print("File:{} tagged with tag:{}".format(file, tag))

                    elif response.status_code == 400:
                        print("Tagging of file:{} failed with message:".format(
                            file, response.text))


if __name__ == '__main__':
    main()
