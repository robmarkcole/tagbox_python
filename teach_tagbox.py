import base64
import os
import requests

IP = 'localhost'
PORT = '8080'
CLASSIFIER = 'tagbox'
TARGET = 'tag'

teach_api_url = "http://{}:{}/{}/teach".format(IP, PORT, CLASSIFIER)
health_api_url = "http://{}:{}/readyz".format(IP, PORT)


def _extract_base64_contents(image_file):
    """Extract image contents."""
    return base64.b64encode(image_file.read()).decode('ascii')


def list_folders(directiory='.'):
    """Returns a list of folders in a dir, defaults to current dir."""
    folders = [dir for dir in os.listdir(directiory)
               if os.path.isdir(os.path.join(directiory, dir))
               and not dir.startswith(directiory)]
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
        tags = list_folders()
        for tag in tags:
            for file in os.listdir(os.getcwd() + "/" + tag):
                if file.endswith(('.jpg', '.png', '.jpeg')):
                    print(
                        "Training with file {} with tag = {}".format(file, tag)
                        )

                    json_data = {TARGET: tag, "id": file}
                    json_response = (requests.post(
                        teach_api_url,
                        data=json_data,
                        files={'file': open(tag + '/' + file, 'rb')}
                        ))

                    if json_response.status_code == 200:
                        print("Training for " + file + " has succeeded! ")

                    elif json_response.status_code == 400:
                        print(json_response.text + " on image " + file)

                print(" The training for " + tag + " has completed")


if __name__ == '__main__':
    main()
