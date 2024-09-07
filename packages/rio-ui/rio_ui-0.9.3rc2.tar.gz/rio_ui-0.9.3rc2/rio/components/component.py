from __future__ import annotations

import abc
import io
import typing
from abc import abstractmethod
from collections.abc import Callable, Iterable
from dataclasses import KW_ONLY
from pathlib import Path
from typing import *  # type: ignore

from typing_extensions import Self
from uniserde import Jsonable, JsonDoc

import rio

from .. import global_state, inspection, utils
from ..component_meta import ComponentMeta
from ..data_models import BuildData
from ..dataclass import internal_field
from ..state_properties import AttributeBindingMaker

__all__ = ["Component"]


T = TypeVar("T")


# Using `metaclass=ComponentMeta` makes this an abstract class, but since
# pyright is too stupid to understand that, we have to additionally inherit from
# `abc.ABC`
class Component(abc.ABC, metaclass=ComponentMeta):
    """
    Base class for all Rio components.

    Components are the building blocks of all Rio apps. Rio already ships with
    many useful components out of the box, but you can also subclass
    `rio.Component` to create your own.

    Components all follow the same basic structure.

    - Class Header
    - Attribute (with type annotations!)
    - custom functions and event handlers
    - `build` method

    Here's a basic example

    ```python
    class HelloComponent(rio.Component):
        # List all of the components attributes here
        name: str

        # Define the build function. It is called when the component is created
        # or any of its attributes have changed
        def build(self) -> rio.Component:
            return rio.Text(f"Hello, {self.name}!")
    ```

    Notice that there is no `__init__` method. That's because all Rio components
    are automatically dataclasses. This means that you can just list the
    attributes of your component as class variables, and Rio will automatically
    create a constructor for you.

    In fact, **never write an `__init__` method for a Rio component** unless you
    know what you're doing. If you do need custom code to run during
    construction, **use the `__post_init__` method** instead. Here's another
    example, with a custom `__post_init__` method:

    ```python
    class HelloComponent(rio.Component):
        name: str
        greeting: str = ""

        # In order to run custom code during initialization, create a
        # `__post_init__` method. This method is called after all internal
        # setup is done, so you are free to access your finished component.
        def __post_init__(self) -> None:
            # If the caller hasn't provided a greeting, we'll make one up
            # based on the connected user's language
            if self.greeting:
                return

            if self.session.preferred_languages[0].startswith("de"):
                self.greeting = "Hallo"
            elif self.session.preferred_languages[0].startswith("es"):
                self.greeting = "Hola"
            elif self.session.preferred_languages[0].startswith("fr"):
                self.greeting = "Bonjour"
            else:
                self.greeting = "Hello"

        def build(self) -> rio.Component:
            return rio.Text(f"{self.greeting}, {self.name}!")
    ```

    This example initializes allows the user to provide a custom greeting, but
    if they don't, it will automatically choose a greeting based on the user's
    language. This needs custom code to run during initialization, so we use
    `__post_init__`.


    ## Attributes

    `key`: A unique identifier for this component. If two components with the
        same key are present during reconciliation they will be considered
        the same component and their state will be preserved. If no key is
        specified, reconciliation falls back to a less precise method, by
        comparing the location of the component in the component tree.

    `margin`: The margin around this component. This is a shorthand for
        setting `margin_left`, `margin_top`, `margin_right` and `margin_bottom`
        to the same value. If multiple conflicting margins are specified the
        most specific one wins. If for example `margin` and `margin_left` are
        both specified, `margin_left` is used for the left side, while the other
        sides use `margin`. Sizes are measured in "font heights", so a margin of
        1 is the height of a single line of text.

    `margin_x`: The horizontal margin around this component. This is a
        shorthand for setting `margin_left` and `margin_right` to the same
        value. If multiple conflicting margins are specified the most
        specific one wins. If for example `margin_x` and `margin_left` are
        both specified, `margin_left` is used for the left side, while the
        other side uses `margin_x`. Sizes are measured in "font heights", so a
        margin of 1 is the height of a single line of text.

    `margin_y`: The vertical margin around this component. This is a shorthand
        for setting `margin_top` and `margin_bottom` to the same value. If
        multiple conflicting margins are specified the most specific one
        wins. If for example `margin_y` and `margin_top` are both specified,
        `margin_top` is used for the top side, while the other side uses
        `margin_y`. Sizes are measured in "font heights", so a margin of 1 is
        the height of a single line of text.

    `margin_left`: The left margin around this component. If multiple
        conflicting margins are specified this one will be used, since it's
        the most specific. If for example `margin_left` and `margin` are
        both specified, `margin_left` is used for the left side, while the
        other sides use `margin`. Sizes are measured in "font heights", so a
        margin of 1 is the height of a single line of text.

    `margin_top`: The top margin around this component. If multiple
        conflicting margins are specified this one will be used, since it's
        the most specific. If for example `margin_top` and `margin` are both
        specified, `margin_top` is used for the top side, while the other
        sides use `margin`. Sizes are measured in "font heights", so a margin
        of 1 is the height of a single line of text.

    `margin_right`: The right margin around this component. If multiple
        conflicting margins are specified this one will be used, since it's
        the most specific. If for example `margin_right` and `margin` are
        both specified, `margin_right` is used for the right side, while the
        other sides use `margin`. Sizes are measured in "font heights", so a
        margin of 1 is the height of a single line of text.

    `margin_bottom`: The bottom margin around this component. If multiple
        conflicting margins are specified this one will be used, since it's
        the most specific. If for example `margin_bottom` and `margin` are
        both specified, `margin_bottom` is used for the bottom side, while
        the other sides use `margin`. Sizes are measured in "font heights", so
        a margin of 1 is the height of a single line of text.

    `min_width`: The minimum amount of horizontal space this component should
        request during layouting. The component will never be smaller than this
        size.

        Please note that the space a `Component` receives during layouting may
        not match the request. As a general rule, for example, containers try to
        pass on all available space to children. If you really want a
        `Component` to only take up as much space as requested, consider
        specifying an alignment.

        Sizes are measured in "font heights", so a width of 1 is the same as the
        height of a single line of text.

    `min_height`: The minimum amount of vertical space this component should
        request during layouting. The component will never be smaller than this
        size.

        Please note that the space a `Component` receives during layouting may
        not match the request. As a general rule, for example, containers try to
        pass on all available space to children. If you really want a
        `Component` to only take up as much space as requested, consider
        specifying an alignment.

        Sizes are measured in "font heights", so a width of 1 is the same as the
        height of a single line of text.

    `grow_x`: Whether this component should request all the superfluous
        horizontal space available in its parent. Containers normally divide up
        any extra space evenly between their children. However, if components
        have `grow_x`, some containers (such as `rio.Row`) will
        give all remaining space to those components first.

    `grow_y`: Whether this component should request all the superfluous
        vertical space available in its parent. Containers normally divide up
        any extra space evenly between their children. However, if components
        have `grow_y`, some containers (such as `rio.Column`) will
        give all remaining space to those components first.

    `align_x`: How this component should be aligned horizontally, if it
        receives more space than it requested. This can be a number between 0
        and 1, where 0 means left-aligned, 0.5 means centered, and 1 means
        right-aligned.

    `align_y`: How this component should be aligned vertically, if it receives
        more space than it requested. This can be a number between 0 and 1,
        where 0 means top-aligned, 0.5 means centered, and 1 means
        bottom-aligned.
    """

    _: KW_ONLY
    key: str | int | None = internal_field(default=None, init=True)

    min_width: float = 0
    min_height: float = 0

    # MAX-SIZE-BRANCH max_width: float | None = None
    # MAX-SIZE-BRANCH max_height: float | None = None

    grow_x: bool = False
    grow_y: bool = False

    align_x: float | None = None
    align_y: float | None = None

    # SCROLLING-REWORK scroll_x: Literal["never", "auto", "always"] = "never"
    # SCROLLING-REWORK scroll_y: Literal["never", "auto", "always"] = "never"

    margin_left: float | None = None
    margin_top: float | None = None
    margin_right: float | None = None
    margin_bottom: float | None = None

    margin_x: float | None = None
    margin_y: float | None = None
    margin: float | None = None

    _id: int = internal_field(init=False)

    # Weak reference to the component's builder. Used to check if the component
    # is still part of the component tree.
    #
    # Dataclasses like to turn this function into a method. Make sure it works
    # both with and without `self`.
    _weak_builder_: Callable[[], Component | None] = internal_field(
        default=lambda *args: None,
        init=False,
    )

    # Weak reference to the component's creator
    _weak_creator_: Callable[[], Component | None] = internal_field(
        init=False,
    )

    # Each time a component is built the build generation in that component's
    # COMPONENT DATA is incremented. If this value no longer matches the value
    # in its builder's COMPONENT DATA, the component is dead.
    _build_generation_: int = internal_field(default=-1, init=False)

    # Note: The BuildData used to be stored in a WeakKeyDictionary in the
    # Session, but because WeakKeyDictionaries hold *strong* references to their
    # values, this led to reference cycles that the garbage collector never
    # cleaned up. The GC essentially saw this:
    #
    # session -> WeakKeyDictionary -> build data -> child component -> parent component
    #
    # Which, notably, doesn't contain a cycle. Storing the BuildData as an
    # attribute solves this problem, because now the GC can see the cycle:
    #
    # parent component -> build data -> child component -> parent component
    _build_data_: BuildData | None = internal_field(default=None, init=False)

    _session_: rio.Session = internal_field(init=False)

    # Remember which properties were explicitly set in the constructor
    _properties_set_by_creator_: set[str] = internal_field(
        init=False, default_factory=set
    )

    # Remember which properties had new values assigned after the component's
    # construction
    _properties_assigned_after_creation_: set[str] = internal_field(init=False)

    # Whether the `on_populate` event has already been triggered for this
    # component
    _on_populate_triggered_: bool = internal_field(default=False, init=False)

    # Whether this instance is internal to Rio, e.g. because the spawning
    # component is a high-level component defined in Rio.
    #
    # In debug mode, this field is initialized by monkeypatches. When running in
    # release mode this value isn't set at all, and the default set below is
    # always used.
    _rio_internal_: bool = internal_field(init=False, default=False)

    # The stackframe which has created this component. Used by the dev tools.
    # Only initialized if in debugging mode.
    _creator_stackframe_: tuple[Path, int] = internal_field(init=False)

    # Whether this component's `__init__` has already been called. Used to
    # verify that the `__init__` doesn't try to read any state properties.
    _init_called_: bool = internal_field(init=False, default=False)

    # Any dialogs which are owned by this component. This keeps them alive until
    # the component is destroyed. The key is the id of the dialog's root
    # component.
    _owned_dialogs_: dict[int, rio.Dialog] = internal_field(
        default_factory=dict, init=False
    )

    # Hide this function from type checkers so they don't think that we accept
    # arbitrary args
    if not TYPE_CHECKING:
        # Make sure users don't inherit from rio components. Inheriting from
        # their own components is fine, though.
        def __init_subclass__(cls, *args, **kwargs):
            super().__init_subclass__(*args, **kwargs)

            if cls.__module__.startswith("rio."):
                return

            for base_cls in cls.__bases__:
                if (
                    base_cls is not __class__
                    and base_cls.__name__ != "FundamentalComponent"
                    and issubclass(base_cls, __class__)
                    and base_cls.__module__.startswith("rio.")
                ):
                    raise Exception(
                        "Inheriting from builtin rio components is not allowed"
                    )

    @property
    def session(self) -> rio.Session:
        """
        Return the session this component is part of.
        """
        return self._session_

    # There isn't really a good type annotation for this... Self is the closest
    # thing
    def bind(self) -> Self:
        return AttributeBindingMaker(self)  # type: ignore

    def _custom_serialize(self) -> JsonDoc:
        """
        Return any additional properties to be serialized, which cannot be
        deduced automatically from the type annotations.
        """
        return {}

    @abstractmethod
    def build(self) -> rio.Component:
        """
        Return a component tree which represents the UI of this component.

        Most components define their appearance and behavior by combining other,
        more basic components. This function's purpose is to do exactly that. It
        returns another component (typically a container) which will be
        displayed on the screen.

        The `build` function should be pure, meaning that it does not modify the
        component's state and returns the same result each time it's invoked.
        """
        raise NotImplementedError()  # pragma: no cover

    def _iter_direct_children(self) -> Iterable[Component]:
        for name in inspection.get_child_component_containing_attribute_names(
            type(self)
        ):
            try:
                value = getattr(self, name)
            except AttributeError:
                continue

            if isinstance(value, Component):
                yield value

            if isinstance(value, list):
                value = cast(list[object], value)

                for item in value:
                    if isinstance(item, Component):
                        yield item

    def _iter_direct_and_indirect_child_containing_attributes(
        self,
        *,
        include_self: bool,
        recurse_into_high_level_components: bool,
    ) -> Iterable[Component]:
        from . import fundamental_component  # Avoid circular import problem

        # Special case the component itself to handle `include_self`
        if include_self:
            yield self

        if not recurse_into_high_level_components and not isinstance(
            self, fundamental_component.FundamentalComponent
        ):
            return

        # Iteratively yield all children
        to_do = list(self._iter_direct_children())
        while to_do:
            cur = to_do.pop()
            yield cur

            if recurse_into_high_level_components or isinstance(
                cur, fundamental_component.FundamentalComponent
            ):
                to_do.extend(cur._iter_direct_children())

    def _iter_component_tree(
        self, *, include_root: bool = True
    ) -> Iterable[Component]:
        """
        Iterate over all components in the component tree, with this component as the root.
        """
        from . import fundamental_component  # Avoid circular import problem

        if include_root:
            yield self

        if isinstance(self, fundamental_component.FundamentalComponent):
            for child in self._iter_direct_children():
                yield from child._iter_component_tree()
        else:
            build_result = self._build_data_.build_result  # type: ignore
            yield from build_result._iter_component_tree()

    async def _on_message(self, msg: Jsonable, /) -> None:
        raise RuntimeError(
            f"{type(self).__name__} received unexpected message `{msg}`"
        )

    def _is_in_component_tree(self, cache: dict[rio.Component, bool]) -> bool:
        """
        Returns whether this component is directly or indirectly connected to
        the component tree of a session. Components inside of a
        `HighLevelDialogContainer` are also considered to be part of the
        component tree.

        This operation is fairly fast, but has to walk up the component tree to
        make sure the component's parent is also connected. Thus, when checking
        multiple components it can easily happen that the same components are
        checked over and over, resulting on O(n log n) runtime. To avoid this,
        pass a cache dictionary to this function, which will be used to memoize
        the result.

        Be careful not to reuse the cache if the component hierarchy might have
        changed (for example after an async yield).
        """

        # Already cached?
        try:
            return cache[self]
        except KeyError:
            pass

        # Root component?
        if self is self.session._root_component:
            result = True

        # Has the builder has been garbage collected?
        else:
            builder = self._weak_builder_()
            if builder is None:
                result = False

            # Has the builder since created new build output, and this component
            # isn't part of it anymore?
            else:
                parent_data: BuildData = builder._build_data_  # type: ignore
                result = (
                    parent_data.build_generation == self._build_generation_
                    and builder._is_in_component_tree(cache)
                )

        # Special case: DialogContainers are considered to be part of the
        # component tree as long as their owning component is
        if not result and isinstance(
            self, rio.components.dialog_container.DialogContainer
        ):
            try:
                owning_component = self.session._weak_components_by_id[
                    self.owning_component_id
                ]
            except KeyError:
                result = False
            else:
                result = (
                    owning_component._is_in_component_tree(cache)
                    and self._id in owning_component._owned_dialogs_
                )

        # Cache the result and return
        cache[self] = result
        return result

    @overload
    async def call_event_handler(
        self,
        handler: rio.EventHandler[[]],
    ) -> None: ...  # pragma: no cover

    @overload
    async def call_event_handler(
        self,
        handler: rio.EventHandler[[T]],
        event_data: T,
        /,
    ) -> None: ...  # pragma: no cover

    async def call_event_handler(
        self,
        handler: rio.EventHandler[...],
        *event_data: object,
    ) -> None:
        """
        Calls an even handler, awaiting it if necessary.

        Call an event handler, if one is present. Await it if necessary. Log and
        discard any exceptions. If `event_data` is present, it will be passed to
        the event handler.

        ## Parameters

        `handler`: The event handler (function) to call.

        `event_data`: Arguments to pass to the event handler.
        """
        await self.session._call_event_handler(
            handler, *event_data, refresh=False
        )

    async def force_refresh(self) -> None:
        """
        Force a rebuild of this component.

        Most of the time components update automatically when their state
        changes. However, some state mutations are invisible to `Rio`: For
        example, appending items to a list modifies the list, but since no list
        instance was actually assigned to th component, `Rio` will be unaware of
        this change.

        In these cases, you can force a rebuild of the component by calling
        `force_refresh`. This will trigger a rebuild of the component and
        display the updated version on the screen.

        Another common use case is if you wish to update an component while an
        event handler is still running. `Rio` will automatically detect changes
        after event handlers return, but if you are performing a long-running
        operation, you may wish to update the component while the event handler
        is still running. This allows you to e.g. update a progress bar while
        the operation is still running.
        """
        self.session._register_dirty_component(
            self,
            include_children_recursively=False,
        )

        await self.session._refresh()

    def _get_debug_details(self) -> dict[str, Any]:
        """
        Used by Rio's dev tools to decide which properties to display to a user,
        when they select a component.
        """
        result = {}

        for prop in self._state_properties_:
            # Consider properties starting with an underscore internal
            if prop.startswith("_"):
                continue

            # Keep it
            result[prop] = getattr(self, prop)

        return result

    def __repr__(self) -> str:
        result = f"<{type(self).__name__} id:{self._id}"

        child_strings: list[str] = []
        for child in self._iter_direct_children():
            child_strings.append(f" {type(child).__name__}:{child._id}")

        if child_strings:
            result += " -" + "".join(child_strings)

        return result + ">"

    def _repr_tree_worker(self, file: IO[str], indent: str) -> None:
        file.write(indent)
        file.write(repr(self))

        for child in self._iter_direct_children():
            file.write("\n")
            child._repr_tree_worker(file, indent + "    ")

    def _repr_tree(self) -> str:
        file = io.StringIO()
        self._repr_tree_worker(file, "")
        return file.getvalue()

    @property
    def _effective_margin_left(self) -> float:
        """
        Calculates the actual left margin of a component, taking into account
        the values of `margin`, `margin_x` and `margin_left`.
        """

        return utils.first_non_null(
            self.margin_left,
            self.margin_x,
            self.margin,
            0,
        )

    @property
    def _effective_margin_top(self) -> float:
        """
        Calculates the actual top margin of a component, taking into account
        the values of `margin`, `margin_y` and `margin_top`.
        """

        return utils.first_non_null(
            self.margin_top,
            self.margin_y,
            self.margin,
            0,
        )

    @property
    def _effective_margin_right(self) -> float:
        """
        Calculates the actual right margin of a component, taking into account
        the values of `margin`, `margin_right` and `margin_x`.
        """

        return utils.first_non_null(
            self.margin_right,
            self.margin_x,
            self.margin,
            0,
        )

    @property
    def _effective_margin_bottom(self) -> float:
        """
        Calculates the actual bottom margin of a component, taking into account
        the values of `margin`, `margin_y` and `margin_bottom`.
        """

        return utils.first_non_null(
            self.margin_bottom,
            self.margin_y,
            self.margin,
            0,
        )

    async def show_custom_dialog(
        self,
        build: Callable[[], rio.Component],
        *,
        modal: bool = True,
        user_closeable: bool = True,
        on_close: rio.EventHandler[[]] = None,
    ) -> rio.Dialog:
        """
        Displays a custom dialog.

        This function displays a dialog to the user. This will call the `build`
        function and use its result as the content of the dialog. The content
        will be assigned the full size of the screen. This allows you to
        position the dialog yourself, using the align and margin properties of
        your component.

        Note: Dialogs are useful if you need to show components without
            returning them from the `build` method. A good example is asking for
            confirmation from an event handler, without having to rebuild the
            component. **If you can return components from the `build` method,
            `rio.Popup` is often an easier choice** (set `position` to
            `"fullscreen"` to get a similar look to dialogs).

        Note: If spawning many dialogs (for example when creating one for each
            item inside of a CRUD application) dialogs can be faster than
            `rio.Popup`, because dialogs only have to build their children when
            they're opened, while `rio.Popup` has its children built
            immediately, for every single item in the list.

        The result of this function is an instance of `rio.Dialog`, which can be
        used to interact with the dialog programmatically. For example, you can
        close the dialog or wait for it to be closed.

        Dialogs can store a result value, which can be retrieved by calling
        `Dialog.wait_for_close`. This allows you to easily wait for the dialog
        to disappear, and also get a return value while you're at it. See the
        example below for details.


        ## Parameters

        `build`: A function which creates the component to be displayed in the
            dialog. Please note that this is a function, not a component. You
            can of course pass a component _class_ as this function, as long as
            the constructor doesn't require any arguments.

        `modal`: Whether the dialog should prevent interactions with the rest of
            the app while it is open. If this is set, the background will also
            be darkened, to guide the user's focus to the dialog.

        `user_closeable`: Whether the user can close the dialog, e.g by clicking
            outside of it.

        `on_close`: An event handler which is called when the dialog is closed.
            This will not be called if you explicitly remove the dialog by
            calling `dialog.close()`.


        ## Example

        This example demonstrates how to spawn a dialog that allows the user to
        select a value from a Dropdown menu. The asyncio.Future object is used
        to wait asynchronously for the user to make a selection. Once the user
        selects an option, the dialog closes, and the selected value is returned.

        ```python
        import asyncio

        class MyComponent(rio.Component):
            value: str = "Vanilla"

            async def _create_dialog(self, options: list[str]) -> str:
                # This function will be called to create the dialog's content.
                # It builds up a UI using Rio components, just like a regular
                # `build` function would.
                def build_dialog_content() -> rio.Component:
                    # Build the dialog
                    return rio.Card(
                        rio.Column(
                            rio.Text(
                                "Which ice cream would you like?",
                                align_x=0.5,
                            ),
                            rio.Dropdown(
                                label="ice cream",
                                options=options,
                                selected_value=self.value,
                                on_change=on_change_future,
                            ),
                            spacing=1,
                            margin=2,
                        ),
                        align_x=0.5,
                        align_y=0.5,
                    )

                # Show the dialog
                dialog = await self.show_custom_dialog(
                    build=build_dialog_content,
                    # Prevent the user from interacting with the rest of the app
                    # while the dialog is open
                    modal=True,
                    # Don't close the dialog if the user clicks outside of it
                    user_closeable=False,
                )

                # Wait for the user to select an option
                result = await dialog.wait_for_close()

                # Return the selected value
                return result

            async def on_spawn_dialog(self) -> None:
                # Show a dialog and wait for the user to make a choice
                self.value = await self._create_dialog(
                    options=["Vanilla", "Chocolate", "Strawberry"],
                )

            def build(self) -> rio.Component:
                return rio.Column(
                    rio.Button(
                        "Open Dialog",
                        on_press=self.on_spawn_dialog,
                    ),
                    rio.Text(f"You've chosen: {self.value}"),
                )
        ```


        ## Metadata

        `experimental`: True
        """
        # TODO: Verify that the passed build function is indeed a function, and
        # not already a component

        # Make sure nobody is building right now
        if (
            global_state.currently_building_component is not None
            or global_state.currently_building_session is not None
        ):
            raise RuntimeError(
                "Dialogs cannot be created inside of build functions. Create them in event handlers instead",
            )

        # Avoid an import cycle
        from . import dialog_container

        # Build the dialog container. This acts as a known, permanent root
        # component for the dialog. It is recognized by the client-side and
        # handled appropriately.
        global_state.currently_building_component = self
        global_state.currently_building_session = self.session

        dialog_container = dialog_container.DialogContainer(
            build_content=build,
            owning_component_id=self._id,
            is_modal=modal,
            is_user_closeable=user_closeable,
            on_close=on_close,
        )

        global_state.currently_building_component = None
        global_state.currently_building_session = None

        # Instantiate the dialog. This will act as a handle to the dialog and
        # returned so it can be used in future interactions.
        result = rio.Dialog._create(
            owning_component=self,
            root_component=dialog_container,
        )

        # Register the dialog with the component. This keeps it (and contained
        # components) alive until the component is destroyed.
        self._owned_dialogs_[dialog_container._id] = result

        # Refresh. This will build any components in the dialog and send them to
        # the client
        await self.session._refresh()

        # Done
        return result

    async def show_simple_dialog(
        self,
        *,
        title: str,
        content: rio.Component | str,
        options: Mapping[str, T] | Sequence[T],
        # default_option: T | None = None,
    ) -> T:
        """
        Display a simple dialog with a list of options.

        This function is highly experimental and **will change in the future.**
        Only use it if you feel adventurous.

        This is a convenience function which displays a simple dialog to the
        user, with a list of options to choose from. The user can select one of
        the options, and the function will return the value of the selected
        option.


        ## Parameters

        `title`: a heading to display at the top of the dialog.

        `content`: a component or markdown string to display below the title.

        `options`: a mapping of option names to their values. The user will be
            able to select one of these options.


        ## Example

        Here's a simple example that demonstrates how to spawn a dialog where
        the user can select multiple options:

        ```python
        class MyComponent(rio.Component):
            value: bool = False

            async def on_spawn_dialog(self) -> None:
                # Display a dialog and wait until the user makes a choice.
                # Since `show_simple_dialog` is an asynchronous function, the
                # `on_spawn_dialog` function must also be asynchronous.
                self.value = await self.show_simple_dialog(
                    title="This is a Dialog",
                    content="Which ice cream would you like?",
                    options=["Vanilla", "Chocolate", "Strawberry"],
                )

            def build(self) -> rio.Component:
                return rio.Column(
                    rio.Button(
                        "Open Dialog",
                        on_press=self.on_spawn_dialog,
                    ),
                    rio.Text(f"You've chosen: {self.value}"),
                )
        ```

        You can also pass a `rio.Component` as the `content` parameter. The content
        must be defined in your build method. This allows you to create more complex
        dialogs. Here's an example:

        ```python
        class MyComponent(rio.Component):
            value: str = ""

            async def on_spawn_dialog(self, content) -> None:
                # Display a dialog and wait until the user makes a choice.
                # Since `show_simple_dialog` is an asynchronous function, the
                # `on_spawn_dialog` function must also be asynchronous.
                self.value = await self.show_simple_dialog(
                    content=content,
                    options=["Vanilla", "Chocolate", "Strawberry"],
                    title="This is a Dialog",
                )

            def build(self) -> rio.Component:

                # content of the dialog must be defined in the build method
                content = rio.Column(
                    rio.Text("You can put any content here"),
                )
                return rio.Column(
                    rio.Button(
                        "Open Dialog",
                        # Note the use of `functools.partial` to pass the
                        # content to the event handler.
                        on_press=functools.partial(self.on_spawn_dialog, content),
                    ),
                    rio.Text(f"You've chosen: {self.value}"),
                )
        ```

        ## Metadata

        `experimental`: True
        """

        # Standardize the options
        if isinstance(options, Sequence):
            options = {str(value): value for value in options}

        # Prepare a build function
        #
        # TODO: Display the buttons below each other on small displays
        def build_content() -> rio.Component:
            outer_margin = 0.8
            inner_margin = 0.4

            if isinstance(content, str):
                wrapped_content = rio.Markdown(
                    content,
                    margin_x=outer_margin,
                )
            else:
                wrapped_content = rio.Container(
                    content,
                    margin_x=outer_margin,
                )

            return rio.Card(
                rio.Column(
                    # Title
                    rio.Text(
                        title,
                        style="heading2",
                        overflow="wrap",
                        margin_x=outer_margin,
                        margin_top=outer_margin,
                    ),
                    # Separator
                    rio.Rectangle(
                        fill=self.session.theme.primary_color,
                        min_height=0.2,
                    ),
                    # Content
                    wrapped_content,
                    # Buttons
                    rio.Row(
                        *[
                            rio.Button(
                                oname,
                                on_press=lambda ovalue=ovalue: dialog.close(
                                    ovalue
                                ),
                            )
                            for oname, ovalue in options.items()
                        ],
                        spacing=inner_margin,
                        margin=outer_margin,
                        margin_top=0,
                    ),
                    spacing=inner_margin,
                ),
                align_x=0.5,
                align_y=0.35,
            )

        # Display the dialog
        dialog = await self.show_custom_dialog(
            build=build_content,
        )

        # Wait for the user to select an option
        result = await dialog.wait_for_close()
        result = typing.cast(T, result)

        # Done!
        return result

    async def show_yes_no_dialog(
        self,
        text: str,
        *,
        title: str | None = None,
        icon: str | None = None,
        default: bool | None = None,
        yes_text: str = "Yes",
        no_text: str = "No",
        yes_color: rio.ColorSet = "keep",
        no_color: rio.ColorSet = "keep",
    ) -> bool | None:
        """
        Displays a simple dialog with a yes and no button.

        This is a convenience function which displays a simple dialog to the
        user, with a "Yes" and "No" button. The user can select one of the
        options, and the function will return `True` or `False` respectively. If
        the user closes the dialog without selecting an option, `None` is
        returned instead.

        The button texts and colors can be customized.

        ## Parameters

        `title`: A heading to display at the top of the dialog.

        `text`: A markdown string to display below the title. This should
            explain to the user what the dialog is about.

        `icon`: An icon to display next to the title.

        `default`: The option the user is likely to take. This will highlight
            the respective button.

        `yes_text`: The text to display on the "Yes" button.

        `no_text`: The text to display on the "No" button.

        `yes_color`: The color of the "Yes" button.

        `no_color`: The color of the "No" button.


        ## Example

        Here's a simple example that demonstrates how to spawn a dialog where
        the user can select a boolean value:

        ```python
        class MyComponent(rio.Component):
            value: bool = False

            async def on_spawn_dialog(self) -> None:
                # Display a dialog and wait until the user makes a choice.
                # Since `show_yes_no_dialog` is an asynchronous function, the
                # `on_spawn_dialog` function must also be asynchronous.
                self.value = await self.show_yes_no_dialog(
                    title="This is a Dialog",
                    text="Do you like ice cream?",
                )

            def build(self) -> rio.Component:
                return rio.Column(
                    rio.Button(
                        "Open Dialog",
                        on_press=self.on_spawn_dialog,
                    ),
                    rio.Text(f"You've selected: {self.value}"),
                )
        ```


        ## Metadata

        `experimental`: True
        """

        # Prepare a build function
        #
        # TODO: Display the buttons below each other on small displays
        def build_content() -> rio.Component:
            outer_margin = 0.8
            inner_margin = 0.4

            main_column = rio.Column(
                spacing=inner_margin,
            )

            # Title & Icon
            title_components: list[rio.Component] = []

            if icon is not None:
                icon_size = self.session.theme.heading2_style.font_size * 1.1

                title_components.append(
                    rio.Icon(
                        icon,
                        # FIXME: This is techincally wrong, since the heading
                        # style could be filled with something other than a
                        # valid icon color. What to do?
                        fill=self.session.theme.heading2_style.fill,  # type: ignore
                        min_width=icon_size,
                        min_height=icon_size,
                    )
                )

            if title is not None:
                title_components.append(
                    rio.Text(
                        title,
                        style="heading2",
                        overflow="wrap",
                        grow_x=True,
                    )
                )

            if title_components:
                main_column.add(
                    rio.Row(
                        *title_components,
                        spacing=inner_margin,
                        margin_x=outer_margin,
                        margin_top=outer_margin,
                    )
                )

                main_column.add(
                    rio.Rectangle(
                        fill=self.session.theme.primary_color,
                        min_height=0.2,
                    ),
                )

            # Content
            main_column.add(
                rio.Markdown(
                    text,
                    margin_x=outer_margin,
                    margin_top=0 if title_components else outer_margin,
                ),
            )

            # Buttons
            main_column.add(
                rio.Row(
                    rio.Button(
                        yes_text,
                        color=yes_color,
                        style="major" if default is True else "bold-text",
                        on_press=lambda: dialog.close(True),
                    ),
                    rio.Button(
                        no_text,
                        color=no_color,
                        style="major" if default is True else "bold-text",
                        on_press=lambda: dialog.close(False),
                    ),
                    spacing=inner_margin,
                    margin=outer_margin,
                    margin_top=0,
                ),
            )

            # Combine everything
            return rio.Card(
                main_column,
                align_x=0.5,
                align_y=0.35,
            )

        # Display the dialog
        dialog = await self.show_custom_dialog(
            build=build_content,
            modal=True,
            user_closeable=True,
        )

        # Wait for the user to select an option
        result = await dialog.wait_for_close()
        assert isinstance(result, bool) or result is None, result

        # Done!
        return result
