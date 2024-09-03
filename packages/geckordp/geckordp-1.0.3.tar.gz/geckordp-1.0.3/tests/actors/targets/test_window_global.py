# pylint: disable=unused-import
import pytest

import tests.helpers.constants as constants
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.root import RootActor
from geckordp.actors.targets.window_global import WindowGlobalActor
from geckordp.logger import log, logdict
from geckordp.rdp_client import RDPClient
from tests.helpers.utils import *


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    current_tab = root.current_tab()
    tab = TabActor(cl, current_tab["actor"])
    actor_ids = tab.get_target()
    browser = WindowGlobalActor(cl, actor_ids["actor"])
    return cl, browser


def test_detach():
    cl = None
    try:
        cl, browser = init()
        val = browser.detach()
        assert response_valid("windowGlobalTarget", val), str(val)
    finally:
        cl.disconnect()


def test_focus():
    cl = None
    try:
        cl, browser = init()
        val = browser.focus()
        assert response_valid("windowGlobalTarget", val), str(val)
    finally:
        cl.disconnect()


def test_go_forward():
    cl = None
    try:
        cl, browser = init()
        val = browser.go_forward()
        assert response_valid("windowGlobalTarget", val), str(val)
    finally:
        cl.disconnect()


def test_go_back():
    cl = None
    try:
        cl, browser = init()
        val = browser.go_back()
        assert response_valid("windowGlobalTarget", val), str(val)
    finally:
        cl.disconnect()


def test_reload():
    cl = None
    try:
        cl, browser = init()
        val = browser.reload()
        assert response_valid("windowGlobalTarget", val), str(val)
    finally:
        cl.disconnect()


def test_navigate_to():
    cl = None
    try:
        cl, browser = init()
        val = browser.navigate_to("https://example.com/")
        assert response_valid("windowGlobalTarget", val), str(val)
    finally:
        cl.disconnect()


def test_list_frames():
    cl = None
    try:
        cl, browser = init()
        val = browser.list_frames()[0]["url"]
        assert "https://example.com/" in val
    finally:
        cl.disconnect()


def test_switch_to_frame():
    cl = None
    try:
        cl, browser = init()
        frame_id = browser.list_frames()[0]["id"]
        val = browser.switch_to_frame(frame_id)
        assert response_valid("windowGlobalTarget", val), str(val)
    finally:
        cl.disconnect()


def test_list_workers():
    cl = None
    try:
        cl, browser = init()
        val = browser.list_workers()
        assert response_valid("windowGlobalTarget", val), str(val)
    finally:
        cl.disconnect()


# todo dunno about this function
""" def test_log_in_page():
    cl = None
    try:
        cl, browser = init()
        val = browser.log_in_page()
    finally:
        cl.disconnect() """
