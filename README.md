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

[Run Tagbox in tag only mode with](https://machinebox.io/docs/tagbox/recognizing-images):
```
MB_KEY="INSERT-YOUR-KEY-HERE"
sudo docker run -p 8080:8080 -e "MB_KEY=$MB_KEY" -e MB_TAGBOX_ONLY_CUSTOM_TAGS=true machinebox/tagbox
```
You should see a message on startup `pretrained tags are disabled, only custom tags will be returned`

# Limitations and Image Selection
On the free plan, you can only train/tag 20 images, therefore you will probably want to limit use to binary classification, with 10 images for ON and 10 for OFF.
Experiment with the images you use to teach tagbox, as you want to cover a range of views, magnifications, backgrounds etc. I noticed that when I taught a small number of images, that in some cases it was the background (a wooden floor) which was being identified by likely tags, not the subject!
