from geckordp.actors.actor import Actor


class WindowGlobalActor(Actor):
    """https://github.com/mozilla/gecko-dev/blob/c07fae4f8a15991f019d70cd7b9900338d72eba2/devtools/shared/specs/targets/browsing-context.js
    https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/targets/window-global.js
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def detach(self):
        return self.client.send_receive(
            {
                "to": self.actor_id,
                "type": "detach",
            }
        )

    def focus(self):
        return self.client.send_receive(
            {
                "to": self.actor_id,
                "type": "focus",
            }
        )

    def go_forward(self):
        return self.client.send_receive(
            {
                "to": self.actor_id,
                "type": "goForward",
            }
        )

    def go_back(self):
        return self.client.send_receive(
            {
                "to": self.actor_id,
                "type": "goBack",
            }
        )

    def reload(self):
        return self.client.send_receive(
            {
                "to": self.actor_id,
                "type": "reload",
            }
        )

    def navigate_to(self, url: str):
        return self.client.send_receive(
            {
                "to": self.actor_id,
                "type": "navigateTo",
                "url": url,
            }
        )

    def switch_to_frame(self, window_id: str):
        return self.client.send_receive(
            {
                "to": self.actor_id,
                "type": "switchToFrame",
                "windowId": window_id,
            }
        )

    def list_frames(self):
        # todo: replace with extract expression
        return self.client.send_receive(
            {
                "to": self.actor_id,
                "type": "listFrames",
            }
        )[
            "frames"
        ]  # type: ignore

    def list_workers(self):
        return self.client.send_receive(
            {
                "to": self.actor_id,
                "type": "listWorkers",
            }
        )

    def log_in_page(self, text="", category="", flags=""):
        return self.client.send_receive(
            {
                "to": self.actor_id,
                "type": "logInPage",
                "text": text,
                "category": category,
                "flags": flags,
            }
        )
