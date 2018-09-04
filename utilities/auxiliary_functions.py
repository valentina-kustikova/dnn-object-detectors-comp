import os


def list_images(image_directory):
    if not os.path.isdir(image_directory):
        raise Exception('Directory \'{0}\' does not exists'.
                        format(image_directory))
    images = [os.path.join(image_directory, img) \
        for img in os.listdir(image_directory) \
            if os.path.isfile(os.path.join(image_directory, img))]
    return images
