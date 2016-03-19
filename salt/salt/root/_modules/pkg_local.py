import logging
from os.path import expanduser

TBD_APP_DIRECTORY = expanduser('~/apps/')

log = logging.getLogger(__name__)

try:
    from archiveinstaller.installer import create_installer
    HAS_ARCHIVEINSTALLER = True
except ImportError:
    HAS_ARCHIVEINSTALLER = False

__virtualname__ = 'pkg_local'


def __virtual__():
    if HAS_ARCHIVEINSTALLER:
        return __virtualname__
    return (False, 'Archiveinstaller module could not get imported')


def properly_loaded():
    pass


def environment_setup():
    log.info('Checking if environment is setup')
    return False

def setup_environment():
    log.info('setup environment')
    create_installer(TBD_APP_DIRECTORY).ensure_environment_is_setup()
    pass
