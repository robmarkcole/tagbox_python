# tagbox_python
A python script to teach Machinebox/Tagbox from a directory containing folders with images of tags, where the folder name is the tag to teach. The directory must contain folders of images with the structure:

```bash
tag_1/
    img1.jpg
    img2.jpg
    ........
tag_2/
    image1.png
    image2.png
    ..........
tag_3/
    image1.jpeg
    image2.jpeg
    ..........    
```
Allowed extensions for images are: `.jpg`, `.jpeg` and `.png`.

**Usage** Run `teach_tagbox.py` from the command line in the directory containing all the folders of images. The script assumes your Facebox is running on `localhost`, if this isn't the case you will need to edit `teach_api_url` and `health_api_url` in `teach_tagbox.py`.

**Limits** With a free license of Tagbox you are limited to teaching 20 tags.

**Output** At the end of the teaching process the file `failed_log.txt` will be written. This file logs all failed teaching, allowing you to check why an image has failed to be taught.
