from geckordp.actors.actor import Actor


class TargetConfigurationActor(Actor):
    """https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/target-configuration.js"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_configuration(
        self,
        cache_disabled: bool | None = None,
        custom_formatters: bool | None = None,
        color_scheme_simulation: bool | None = None,
        custom_user_agent="",
        javascript_enabled: bool | None = None,
        override_dppx=-1,
        paint_flashing: bool | None = None,
        print_simulation_enabled: bool | None = None,
        restore_focus: bool | None = None,
        service_workers_testing_enabled: bool | None = None,
        use_simple_highlighters_for_reduced_motion: bool | None = None,
        touch_events_override="",
    ):
        args = {}

        if cache_disabled is not None:
            args["cacheDisabled"] = cache_disabled

        if custom_formatters is not None:
            args["customFormatters"] = custom_formatters

        if color_scheme_simulation is not None:
            args["colorSchemeSimulation"] = color_scheme_simulation

        if custom_user_agent != "":
            args["customUserAgent"] = custom_user_agent

        if javascript_enabled is not None:
            args["javascriptEnabled"] = javascript_enabled

        if override_dppx != -1:
            args["overrideDPPX"] = override_dppx

        if paint_flashing is not None:
            args["paintFlashing"] = paint_flashing

        if print_simulation_enabled is not None:
            args["printSimulationEnabled"] = print_simulation_enabled

        if restore_focus is not None:
            args["restoreFocus"] = restore_focus

        if service_workers_testing_enabled is not None:
            args["serviceWorkersTestingEnabled"] = service_workers_testing_enabled

        if use_simple_highlighters_for_reduced_motion is not None:
            args["useSimpleHighlightersForReducedMotion"] = (
                use_simple_highlighters_for_reduced_motion
            )

        if touch_events_override != "":
            args["touchEventsOverride"] = touch_events_override

        return self.client.send_receive(
            {
                "to": self.actor_id,
                "type": "updateConfiguration",
                "configuration": args,
            }
        )
