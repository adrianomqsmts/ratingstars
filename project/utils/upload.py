"""Módulo de controle de  upload de imagens."""

import os
import uuid as uuid
from typing import Optional
from project.configs.server import server

from werkzeug.utils import secure_filename

PATH = "project/static/images/"


def image_upload(file: object) -> Optional[str]:
    """Upload da imagem no servidor.

    Args:
        file (object): Arquivo a ser inserido no banco de dados

    Returns:
        Optional[str]: O nome do arquivo inserido, caso contrário, None.
    """
    if file:
        # FILENAME
        pic_filename = secure_filename(file.filename)
        pic_name = str(uuid.uuid1()) + "_" + pic_filename
        # SAVE IN FOLDER
        file.save(os.path.join(PATH, pic_name))

        return pic_name
    else:
        return None


def image_remove(name_old_file: str) -> Optional[str]:
    if name_old_file and os.path.isfile(os.path.join(PATH, name_old_file)):
        os.remove(os.path.join(PATH, name_old_file))  # Remove file if exists
        return name_old_file
    else:
        return None

def image_remove_and_upload(new_file: object, name_old_file: str) -> Optional[str]:
    """Remove a imagem antiga, e adicionar uma nova imagem no servidor.

    Args:
        new_file (object): A imagem a ser inserida no servidor
        name_old_file (str): o nome do arquivo a ser removido

    Returns:
        Optional[str]: O nome do arquivo inserido, caso contrário, None
    """
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
