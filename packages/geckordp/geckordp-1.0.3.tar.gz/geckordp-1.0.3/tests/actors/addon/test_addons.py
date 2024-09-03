# pylint: disable=unused-import
import pytest

import tests.helpers.constants as constants
from geckordp.actors.addon.addons import AddonsActor
from geckordp.actors.root import RootActor
from geckordp.logger import log, logdict
from geckordp.rdp_client import RDPClient
from tests.helpers.utils import *


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    root_ids = root.get_root()
    addons = AddonsActor(cl, root_ids["addonsActor"])
    return cl, addons


def test_install_temporary_addon():
    cl = None
    try:
        cl, _addons = init()
        # todo may not change anyway
        # val = addons.install_temporary_addon("")
    finally:
        cl.disconnect()
