# pylint: disable=unused-import
import pytest

import tests.helpers.constants as constants
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.root import RootActor
from geckordp.actors.source import SourceActor
from geckordp.actors.thread import ThreadActor
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
    thread = ThreadActor(cl, actor_ids["threadActor"])
    thread.attach()
    sources = thread.sources()
    source = None
    for s in sources:
        if s.get("actor", None) is not None:
            source = SourceActor(cl, s["actor"])
            break
    if source is None:
        print("WARNING: no source available")
    return cl, source


def test_get_breakpoint_positions():
    cl = None
    try:
        cl, source = init()
        if source is None:
            return
        val = source.get_breakpoint_positions()
        assert len(val) > 0
    finally:
        cl.disconnect()


def test_get_breakpoint_positions_compressed():
    cl = None
    try:
        cl, source = init()
        if source is None:
            return
        val = source.get_breakpoint_positions_compressed()
        assert len(val) > 0
    finally:
        cl.disconnect()


def test_get_breakable_lines():
    cl = None
    try:
        cl, source = init()
        if source is None:
            return
        val = source.get_breakable_lines()
        assert len(val) > 0
    finally:
        cl.disconnect()


def test_source():
    cl = None
    try:
        cl, source = init()
        if source is None:
            return
        val = source.source()["source"]
        assert len(val) > 3
    finally:
        cl.disconnect()


def test_set_pause_point():
    cl = None
    try:
        cl, source = init()
        if source is None:
            return
        val = source.set_pause_point(0, 0)
        assert response_valid("source", val), str(val)
    finally:
        cl.disconnect()


def test_blackbox():
    cl = None
    try:
        cl, source = init()
        if source is None:
            return
        val = source.blackbox(0, 0, 10000, 0).get("pausedInSource", "0")
        assert val != "0"
    finally:
        cl.disconnect()


def test_unblackbox():
    cl = None
    try:
        cl, source = init()
        if source is None:
            return
        val = source.unblackbox(0, 0, 10000, 0)
        assert response_valid("source", val), str(val)
    finally:
        cl.disconnect()
