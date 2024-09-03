import socket
from concurrent.futures import Future
from contextlib import closing

import tests.helpers.constants as constants
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.events import Events
from geckordp.actors.root import RootActor
from geckordp.actors.targets.window_global import WindowGlobalActor
from geckordp.actors.watcher import WatcherActor
from geckordp.rdp_client import RDPClient


def is_port_open(host: str, port: int):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        return sock.connect_ex((host, port)) == 0


def get_client_vars():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    current_tab = root.current_tab()
    tab = TabActor(cl, current_tab["actor"])
    descriptors = tab.get_target()
    browser = WindowGlobalActor(cl, descriptors["actor"])
    return cl, root, current_tab, tab, descriptors, browser


def get_available_target(
    cl: RDPClient,
    watcher: WatcherActor,
    browsing_context_id: str,
) -> dict:
    target = {}
    target_fut = Future()

    async def on_target(data: dict):
        if "target" not in data or "browsingContextID" not in data["target"]:
            return
        if browsing_context_id == data["target"]["browsingContextID"]:
            target_fut.set_result(data["target"])

    cl.add_event_listener(
        watcher.actor_id, Events.Watcher.TARGET_AVAILABLE_FORM, on_target
    )

    try:
        watcher.watch_targets(WatcherActor.Targets.FRAME)
        target = target_fut.result(3.0)
    finally:
        cl.remove_event_listener(
            watcher.actor_id, Events.Watcher.TARGET_AVAILABLE_FORM, on_target
        )

    return target


def response_valid(actor_id: str, response: dict, allow_null=False) -> bool:
    response_string = str(response).lower()
    return (
        actor_id in response.get("from", "")
        and "no such actor" not in response_string
        and (allow_null or " is null" not in response_string)
        and "unrecognized" not in response_string
    )
