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


ALL_IMAGES = [
    rio.URL(
        "https://fastly.picsum.photos/id/13/2500/1667.jpg?hmac=SoX9UoHhN8HyklRA4A3vcCWJMVtiBXUg0W4ljWTor7s"
    ),
    rio.URL(
        "https://fastly.picsum.photos/id/19/2500/1667.jpg?hmac=7epGozH4QjToGaBf_xb2HbFTXoV5o8n_cYzB7I4lt6g"
    ),
    rio.URL(
        "https://fastly.picsum.photos/id/28/4928/3264.jpg?hmac=GnYF-RnBUg44PFfU5pcw_Qs0ReOyStdnZ8MtQWJqTfA"
    ),
    rio.URL(
        "https://fastly.picsum.photos/id/29/4000/2670.jpg?hmac=rCbRAl24FzrSzwlR5tL-Aqzyu5tX_PA95VJtnUXegGU"
    ),
]


class MyRoot(rio.Component):
    images: list[rio.ImageLike] = [
        # ALL_IMAGES.pop(),
        # ALL_IMAGES.pop(),
    ]

    async def _on_button_press(self) -> None:
        # Add the image
        try:
            self.images.append(ALL_IMAGES.pop())
        except IndexError:
            pass

        print(f"There are now {len(self.images)} images")

        # Rio automatically detect when we assign to the component. However, the
        # code above doesn't assign anything - it just modifies the list in
        # place. To make sure the page updates, tell Rio about it explicitly.
        await self.force_refresh()

    def build(self) -> rio.Component:
        return rio.Column(
            rio.Slideshow(
                *[
                    rio.Image(
                        img,
                        fill_mode="zoom",
                    )
                    for img in self.images
                ],
                linger_time=1,
                grow_y=True,
            ),
            rio.Button(
                "Add Image",
                on_press=self._on_button_press,
            ),
            spacing=1,
            min_width=30,
            min_height=20,
            align_x=0.5,
            align_y=0.5,
        )


app = rio.App(
    # build=MyRoot,
    default_attachments=[],
    pages=[
        rio.Page(
            name="Home",
            page_url="",
            build=MyRoot,
        ),
        rio.Page(
            name="Page 2",
            page_url="secret",
            build=MyRoot,
        ),
    ],
)
