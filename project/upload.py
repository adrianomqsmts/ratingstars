from werkzeug.utils import secure_filename
import uuid as uuid
import os


PATH = "static/images"


def image_upload(file):
    if file:
        # FILENAME
        pic_filename = secure_filename(file.filename)
        pic_name = str(uuid.uuid1()) + "_" + pic_filename
        # SAVE IN FOLDER
        file.save(os.path.join(PATH, pic_name))

        return pic_name
    else:
        return None


def image_remove_and_upload(new_file, name_old_file):
    if new_file:
        if name_old_file and os.path.isfile(os.path.join(PATH, name_old_file)):
            os.remove(os.path.join(PATH, name_old_file))  # Remove file if exists

        # FILENAME
        pic_filename = secure_filename(new_file.filename)
        pic_name = str(uuid.uuid1()) + "_" + pic_filename
        # SAVE IN FOLDER
        new_file.save(os.path.join(PATH, pic_name))

        return pic_name
    else:
        if name_old_file and os.path.isfile(os.path.join(PATH, name_old_file)):
            os.remove(os.path.join(PATH, name_old_file))  # Remove file if exists
        return None
