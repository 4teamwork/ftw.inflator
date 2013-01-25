from collective.transmogrifier.transmogrifier import Transmogrifier
import os


FOLDER_NAME = 'content_creation'


def content_creation(setup):
    """Create content based on json definitions with a folder
    "content_creation".
    """

    data = setup.isDirectory(FOLDER_NAME)
    if not data:
        return

    path = os.path.join(setup._profile_path, FOLDER_NAME).encode('utf-8')
    assert os.path.isdir(path)

    mogrifier = Transmogrifier(setup.getSite())
    mogrifier(u'ftw.inflator.creation.content_creation_config',
              jsonsource=dict(directory=path))
