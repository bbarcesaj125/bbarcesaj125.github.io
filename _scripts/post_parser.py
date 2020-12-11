import os
import re
import subprocess
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.error import URLError, HTTPError

""" 
This is a one-time script that automatically parse imported posts from Blogger. It does the following:
    - It converts Blogger thumbnail links into full size image links using regular expressions (of course xD)
    - It inserts those full size image links as teaser images into their respective posts
    - It performs some ImageMagick trickery on these full size images to create fancy header images for every posts
"""


def get_links():
    """ This function extracts the *.html files from the _posts directory and feeds then to the write_teaser_image() function. """

    directory = "../_posts"

    for file in os.scandir(directory):
        filename = os.fsdecode(file)
        print(f"The file's name with path is: {filename}")
        if filename.endswith(".html"):
            write_teaser_image(filename)
        else:
            print("Not an HTML file!")


def write_teaser_image(file):
    """ This function uses regex to convert a Blogger thumbnail link into a full size image that can be used as a header image for posts. """

    regex = r"(s72-c)"
    subst = "s1600"
    sed_base_command_1 = "sed -i '/blogger_orig_url/aexcerpt:\\ "
    sed_base_command_2 = "\\nheader:\\n\\  teaser:\\"
    sed_base_command_4 = '\\n\\  overlay_filter:\\ rgba(0, 255, 55, 0.4), rgba(9, 105, 17, 0.78)'
    sed_base_command_5 = '\\n\\  caption:\\ "Photo credit:\\ [**Unsplash**]\\(https://unsplash.com\\)"'

    with open(file, "r+") as f:
        full_basename = os.path.basename(file)
        basename = os.path.splitext(full_basename)[0]
        sed_base_command_3 = f'\\n\\  overlay_image:\\ "/images/posts/{basename}-final.webP"'
        print(f"The file's basename is {basename}")
        for line in f:
            if line.startswith("thumbnail"):
                thumbnail_link = line.replace("thumbnail:", "")
                header_image_link = re.sub(regex, subst, thumbnail_link, 1)
                print(header_image_link)
            elif line.startswith("blogger_orig_url"):
                post_link = line.replace("blogger_orig_url: ", "")
                excerpt = get_post_description(post_link)

        sed_command = sed_base_command_1 + '"' + excerpt + '"' + sed_base_command_2 + header_image_link.rstrip() + sed_base_command_3 + \
            sed_base_command_4 + sed_base_command_5 + "' " + file
        print(f"The bash command is {sed_command}")
        subprocess.Popen(sed_command,
                         shell=True,
                         stdout=subprocess.PIPE)
    # output, error = process.communicate()
    # print(output, error)

    # Invoking download_post_image() to save the images to the /scripts/images/download/ folder
    #saved_img_name = download_post_image(header_image_link, basename)

    # Using imagemagick() to create fancy header images
    #imagemagick(saved_img_name, basename)


def get_post_description(post_link):
    """ This functions extracts the post HTML meta descritpion from the post's URL. """

    post_url = post_link

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:11.0) Gecko Firefox/11.0 (via ggpht.com GoogleImageProxy)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    req = Request(post_url, headers=headers)

    try:
        response = urlopen(req)
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
    else:
        soup = BeautifulSoup(response.read(), 'html.parser')
        raw_description = soup.findAll("meta", {"name": "description"})[
            0]["content"]

        if "'" in raw_description:
            description = raw_description.replace("'", "´")
        else:
            description = raw_description

        print(f"The post's description is: {description}")
    return description


def download_post_image(image_link, filename):
    """ This function downloads the post images and puts them in a directory. """

    img_link = image_link
    basename = filename
    regex = r"(?<=\/).*"
    path = "./images/download/"

    check_directory = Path(path).is_dir()
    if check_directory:
        pass
    else:
        Path(path).mkdir(parents=True)

    # Downloading the images
    response = urlopen(img_link)
    data = response.read()  # a `bytes` object
    img_type = response.headers.get('content-type')
    matches = re.search(regex, img_type)
    ext = "." + matches.group() if matches else ".png"
    full_img_name = path + basename + ext
    print(f"The downloaded's image full path is: {full_img_name}")

    with open(full_img_name, "wb") as img_file:
        img_file.write(data)
    return full_img_name


def imagemagick(image_name, basename):
    """ This fucntion uses ImageMagick under the hoods to create a nice looking header for every post. It saves the resulting image in the /images/posts/ directory. """

    img_name = image_name
    img_basename = basename
    img_directory = "./images/"
    saved_img_path = "./images/posts/"
    check_directory = Path(saved_img_path).is_dir()

    if check_directory:
        pass
    else:
        Path(saved_img_path).mkdir(parents=True)

    imagemagick_cmd_1 = f"convert {img_name} -resize 1800x -blur 0x12 -background 'rgba(0,0,0,0)' -rotate 30.00 {img_directory}{img_basename}-resized-blurred-rotated.webP"
    imagemagick_cmd_2 = f"magick composite -gravity center {img_directory}{img_basename}-resized-blurred-rotated.webP {img_directory}background-pattern.webP {saved_img_path}{img_basename}-final.webP"
    bash_rm_blurred_images_cmd = f"rm -v {img_directory}{img_basename}-resized-blurred-rotated.webP"

    subprocess.Popen(imagemagick_cmd_1 + " && " + imagemagick_cmd_2 + " && " + bash_rm_blurred_images_cmd,
                     shell=True,
                     stdout=subprocess.PIPE)


if __name__ == "__main__":
    get_links()
    # get_post_description("http://www.tootips.com/2015/02/tox-distributed-and-secure-p2p-instant.html")
    #download_post_image("http://4.bp.blogspot.com/-v4zkhGfqo5Y/UQrLHbNkEQI/AAAAAAAABkI/GNNngyIU21I/s1600/Evince-Running-Inside-Chromium-Tootips.png", "hshshkdkdkdkshs")

    #imagemagick("./images/download/2012-05-26-anki-spaced-repitition-memory-program.png", "lololololo")
    # write_teaser_image("../_posts/2012-12-07-how-to-remove-disabled-on-upgrade-to.html")
