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


def main():
    try:
        json_response = requests.get(health_api_url)
    except requests.exceptions.RequestException as e:
        print("{} is unreachable......... Please check if it's up and running! ".format(CLASSIFIER))
        print(e)
    else:
        if json_response.status_code == 200:
            folders = list_folders()
            for folder_name in folders:

                print("Started training for " + folder_name)

                for file in os.listdir(os.getcwd() + "/" + folder_name):
                    if file.endswith(('.jpg', '.png', '.jpeg')):
                        json_data = {
                            TARGET: folder_name,
                            "id": file
                        }

                        print(
                            "Training with file {} with tag = {}".format(file, folder_name)
                            )

                        json_response = (requests.post(
                            teach_api_url,
                            data=json_data,
                            files={'file': open(folder_name + '/' + file, 'rb')}
                        ))

                        if json_response.status_code == 200:
                            print("Training for " + file + " has succeeded! ")

                        elif json_response.status_code == 400:
                            print(json_response.text + " on the following image " + file)

                print(" The training for " + folder_name + " has completed")

        else:
            print("{} isn't ready! Please check if the docker instance is up an running!".format(CLASSIFIER))


if __name__ == '__main__':
    main()
