import os
import re
import shutil
from os.path import join, isdir, isfile
from urllib.parse import urlparse

from script_house.utils.FileSystemUtils import assert_is_file

try:
    import requests
    import markdown
    from bs4 import BeautifulSoup
except ImportError as e:
    raise ImportError(f"Required dependencies for this utility are not installed: {e.name}. "
                      f"Please install them using `pip install requests markdown beautifulsoup4`")


def read_markdown(filename):
    assert_is_file(filename)
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def extract_image_urls(filename) -> list[str]:
    """
    return all the image links in the markdown file
    (may contain duplicate links).
    :param filename: path to markdown file
    :return: list of image links
    """
    markdown_text = read_markdown(filename)
    # Convert markdown to HTML
    html = markdown.markdown(markdown_text)

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find all image tags and extract the src attribute
    image_urls = [img['src'] for img in soup.find_all('img')]

    return image_urls


def parse_filename_from_url(url: str) -> str:
    scheme = urlparse(url).scheme
    if scheme in ['', 'file']:  # local
        # nobody uses / as the root path in Windows, so treat it as a relative path
        if url.startswith('/'):
            url = url[1:]
        _, filename = os.path.split(url)
    elif scheme in ['http', 'https']:  # remote
        filename = url.split('/')[-1]
    else:
        # Do common markdown editors support other schemes?
        raise Exception(f'unsupported url scheme: {scheme}')
    return filename


def copy_images(markdown_file, target_dir) -> tuple[list[str], list[str]]:
    """
    Copy all the images referred by the markdown file to the target directory.

    If the image is on the Internet, this function will download it.

    If the target directory is not empty, an exception is raised, because the content will be messy.

    Warning: this function only works on Windows.
    :param markdown_file: path to markdown file
    :param target_dir: target directory
    :return: [urls of images successful to copy, urls of images failed to copy]
    """
    if isdir(target_dir) and len(os.listdir(target_dir)) > 0:
        raise Exception(f'there are files/directories in {target_dir}, move them or choose another target_dir')

    if not isdir(target_dir):
        os.makedirs(target_dir)

    cwd = os.path.dirname(markdown_file)  # for reference images on the local filesystem
    image_urls = set(extract_image_urls(markdown_file))

    failed_urls = []
    successful_urls = []

    for url in image_urls:
        filename = parse_filename_from_url(url)
        if isfile(join(target_dir, filename)):
            print(f'Duplicate Filename: {filename}')
            failed_urls.append(url)
            continue

        scheme = urlparse(url).scheme
        if scheme in ['', 'file']:  # local
            img_abspath = url
            # nobody uses / as the root path in Windows, so treat it as a relative path
            if img_abspath.startswith('/'):
                img_abspath = img_abspath[1:]
            img_abspath = os.path.abspath(join(cwd, img_abspath))
            if not os.path.isfile(img_abspath):
                failed_urls.append(url)
                continue

            shutil.copy(img_abspath, join(target_dir, filename))
            successful_urls.append(url)

        elif scheme in ['http', 'https']:  # remote
            try:
                bytes = requests.get(url).content
                with open(join(target_dir, filename), 'wb') as f:
                    f.write(bytes)
                successful_urls.append(url)
            except Exception as e:
                print(e)
                failed_urls.append(url)
        else:
            # Do common markdown editors support other schemes?
            raise Exception(f'unsupported url scheme: {scheme}')

    return successful_urls, failed_urls


def update_markdown_image_links(markdown_file: str, new_image_dir: str) -> bool:
    """
    This function updates the image links in the markdown file by keeping the filename
    while updating the dir path. After the update, the original markdown file will be
    renamed to '<filename>.old'.

    Warning: this function only works on Windows.

    :param markdown_file: path to markdown file
    :param new_image_dir: new dir of the images
    :return: succeed or not
    """

    if new_image_dir.endswith('/'):
        new_image_dir = new_image_dir[:-1]

    regex_list = [
        # <img src="MarkDownImages/b.jpg" alt="b" style="zoom:50%;" />
        r'<img src="(.*?)" alt=(.*?) ',
        # ![img](MarkDownImages/a.png)
        r'!\[(.*?)\]\((.*?)\)'
    ]

    def replace_img_tag(match):
        return f'<img src="{new_image_dir}/{parse_filename_from_url(match.group(1))}" alt={match.group(2)} '

    def replace_markdown_img(match):
        return f'![{match.group(1)}]({new_image_dir}/{parse_filename_from_url(match.group(2))})'

    replacement_functions = {
        regex_list[0]: replace_img_tag,
        regex_list[1]: replace_markdown_img
    }

    # update image links in the markdown
    new_file = markdown_file + '.new'
    with open(markdown_file, 'r', encoding='utf-8') as infile:
        with open(new_file, 'w', encoding='utf-8') as outfile:
            for line in infile:
                for regex in regex_list:
                    line = re.sub(regex, replacement_functions[regex], line)
                outfile.write(line)

    old_file = markdown_file + '.old'
    os.rename(markdown_file, old_file)
    os.rename(new_file, markdown_file)

    return True


if __name__ == '__main__':
    pass
