import os
import requests

IP = 'localhost'
PORT = '8080'
CLASSIFIER = 'tagbox'

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
        for folder in list_folders():
            tag = folder
            for file in os.listdir(os.getcwd() + "/" + tag):
                if file.endswith(('.jpg', '.png', '.jpeg')):
                    response = (requests.post(
                        teach_api_url,
                        data={'tag': tag, "id": file},
                        files={'file': open(tag + '/' + file, 'rb')}
                        ))

                    if response.status_code == 200:
                        print("File: {} tagged with tag: {}".format(file, tag))

                    elif response.status_code == 400:
                        print("Tagging of file: {} failed with message: image ".format(
                            file, response.text))


if __name__ == '__main__':
    main()
