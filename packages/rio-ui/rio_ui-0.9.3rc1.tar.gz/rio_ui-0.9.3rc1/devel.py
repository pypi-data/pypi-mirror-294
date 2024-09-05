import rio
from typing import *  # type: ignore
import rio.components.class_container
from pathlib import Path
import pandas as pd
from datetime import datetime, timezone
import json
import asyncio
import gc
import random
import time
import cProfile
from datetime import timedelta
from dataclasses import dataclass, KW_ONLY
import json
import sys
from typing import Any
import uniserde

import rio.data_models
import rio.debug
import rio.debug
import rio.debug.dev_tools
import rio.debug.dev_tools.icons_page
import rio.debug.dev_tools.layout_display
import rio.debug.layouter
import os
from pathlib import Path
from typing import *  # type: ignore

import rio.components.class_container
import rio.debug.dev_tools.dev_tools_connector


class OtherComponent(rio.Component):
    def build(self) -> rio.Component:
        return rio.Row(
            rio.Spacer(width=0),
            rio.SwitcherBar(
                values=["foo"],
                allow_none=True,
                orientation="vertical",
                spacing=2,
                color="primary",
                selected_value="tree",
                margin=0.2,
            ),
        )


def filter_function(component: rio.Component) -> bool:
    # Don't care about the connection lost popup
    # if type(component).__name__ == "DefaultConnectionLostComponent":
    #     return False

    # Everything else is fine
    return True


class LoginBox(rio.Component):
    TEXT_STYLE = rio.TextStyle(fill=rio.Color.from_hex("02dac5"), font_size=0.9)

    def build(self) -> rio.Component:
        return rio.Rectangle(
            content=rio.Column(
                rio.TextInput(
                    text="",
                    label="Benutzername",
                    accessibility_label="Benutzername",
                    min_height=0.5,
                ),
                rio.TextInput(
                    text="",
                    label="Passwort",
                    accessibility_label="Passwort",
                    is_secret=True,
                ),
                rio.Column(
                    rio.Row(
                        rio.Button(
                            rio.Text("LOGIN", style=self.TEXT_STYLE),
                            shape="rectangle",
                            style="minor",
                            color="secondary",
                            margin_bottom=0.4,
                        )
                    ),
                    rio.Row(
                        rio.Button(
                            rio.Text("REG", style=self.TEXT_STYLE),
                            shape="rectangle",
                            style="minor",
                            color="secondary",
                        ),
                        rio.Spacer(),
                        rio.Button(
                            rio.Text("LST PWD", style=self.TEXT_STYLE),
                            shape="rectangle",
                            style="minor",
                            color="secondary",
                        ),
                        proportions=(49, 2, 49),
                    ),
                ),
                spacing=0.4,
            ),
            fill=rio.Color.TRANSPARENT,
            align_x=0.5,
            align_y=0.5,
        )


class MyRoot(rio.Component):
    messages: list[str] = [
        "Initial",
    ]
    text_value: str = "<->"
    number_value: float = 0

    is_on: bool = False

    entries: list[int] = list(range(10))

    async def on_randomize(self) -> None:
        random.shuffle(self.entries)
        await self.force_refresh()

    async def _find_dead_components(self) -> None:
        try:
            import objgraph  # type: ignore
        except ImportError:
            print("Please install `objgraph`")
            return
        key = ("Foobar",)
        # Make sure only real problem components exist
        gc.collect()

        # Find all components present in the app
        alive_component_ids: set[int] = set()
        to_do: list[rio.Component] = [self.session._root_component]

        while to_do:
            component = to_do.pop()
            alive_component_ids.add(id(component))
            to_do.extend(component._iter_direct_children())

        # Find all components which are alive according to Python, but aren't
        # part of the app
        zombie_component_ids: set[int] = (
            set(self.session._weak_components_by_id.keys())
            - alive_component_ids
        )

        # Select one component to debug
        component = None

        for cmp_id, component in self.session._weak_components_by_id.items():
            if cmp_id not in zombie_component_ids:
                continue

            if isinstance(component, rio.debug.dev_tools.icons_page.IconsPage):
                gc.collect()
                objgraph.show_backrefs(
                    [component],
                    filename="/home/jakob/Downloads/sample-graph.png",
                    max_depth=10,
                )

    def build_dialog(self) -> rio.Component:
        return rio.Card(
            rio.Button(
                "Hello, World!",
                on_press=lambda: print("Hello, World!"),
                margin=3,
            ),
            align_x=0.5,
            align_y=0.5,
        )

    async def on_press(self) -> None:
        self.is_on = not self.is_on

    async def on_button_press(self) -> None:
        await self.session.set_clipboard("Hello, World!")

    def build(self) -> rio.Component:
        return rio.Popup(
            anchor=rio.Button(
                "Toggle Popup",
                on_press=self.on_press,
            ),
            content=rio.Text("I'm here!"),
            is_open=self.is_on,
            # is_open=True,
            align_x=0.5,
            align_y=0.5,
            position="top",
        )

        table = rio.Table(
            # pd.DataFrame(
            {
                "a": [1, 2, 3],
                "b": [4, 5, 6],
                "c": [7, 8, 9],
                "d": [10, 11, 12],
            }
            # ),
        )

        table["header", -2:].style(
            font_weight="bold",
        )

        table[:2, 0].style(
            font_weight="bold",
        )

        return table

        return rio.Column(
            # blabla
            *([] if self.content is None else [self.content])
            # blabla
        )

        return rio.Column(
            # blabla
            rio.Switcher(self.content),
            # blabla
        )

        return rio.Button(
            "Open Dialog",
            on_press=self.on_press,
            align_x=0.5,
            align_y=0.5,
        )

        return rio.Row(
            rio.Popup(
                anchor=rio.Button(
                    "Toggle Popup",
                    on_press=lambda: setattr(self, "is_on", not self.is_on),
                ),
                content=rio.Button(
                    "Toggle Popup",
                    on_press=lambda: setattr(self, "is_on", not self.is_on),
                    margin=1,
                ),
                position="left",
                gap=10,
                # alignment=1,
                is_open=self.is_on,
                align_x=0.5,
                align_y=0.5,
            ),
            rio.Tooltip(
                anchor=rio.Text("Hover for Tooltip"),
                tip=rio.Text("This is a tooltip"),
                align_x=0.5,
                align_y=0.5,
            ),
            spacing=3,
        )

        return rio.Column(
            rio.FlowContainer(
                *[
                    rio.Text(
                        f"Entry {ii}",
                        key=f"entry_{ii}",
                        margin=0.5,
                    )
                    for ii in self.entries
                ],
                grow_y=True,
            ),
            rio.Button(
                "Randomize",
                on_press=self.on_randomize,
            ),
        )


class MyRoot(rio.Component):
    style_index: int = 0

    def advance_style(self) -> None:
        self.style_index += 1

    def build(
        self,
    ) -> rio.Column:
        styles = list(rio.CursorStyle)
        style = styles[self.style_index % len(styles)]

        return rio.Column(
            rio.Text(str(style)),
            rio.Rectangle(
                fill=rio.Color.GREEN,
                cursor=style,
                min_height=5,
            ),
            rio.Button(
                "Advance",
                on_press=self.advance_style,
            ),
            spacing=1,
            min_width=15,
            align_x=0.5,
            align_y=0.5,
        )


app = rio.App(
    build=MyRoot,
    default_attachments=[],
    pages=[
        rio.Page(
            name="Home",
            page_url="",
            build=MyRoot,
        ),
        rio.Page(
            name="Secret",
            page_url="secret",
            build=MyRoot,
        ),
    ],
)
