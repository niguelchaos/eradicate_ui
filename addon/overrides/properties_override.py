import bpy
import bl_ui
from addon_utils import check, paths, enable

import functools
import inspect

from bpy.types import Panel


class Properties_Space_Override():
    """
    Provides override functions for Blender's Properties area. 
    The defined functions are used in register().
    All overrides are decorators, which inject code before and after the actual function.
    """

    def options_draw_decorator(draw):

        @functools.wraps(draw)
        def options_draw_wrapper(self, context):
            # Before Function
            if context.scene.hide_ui:
                return None

            # Actual Function
            result = draw(self, context)

            # After Function
            return result

        return options_draw_wrapper

    def navbar_draw_decorator(draw):

        @functools.wraps(draw)
        def navbar_draw_wrapper(self, context):
            # Before Function
            if context.scene.hide_ui:
                return None

            # Actual Function
            result = draw(self, context)

            # After Function

            return result

        return navbar_draw_wrapper

    def world_buttons_panel_poll(poll):

        # Partially written by ChatGPT
        @classmethod
        @functools.wraps(poll)
        def poll_wrapper(cls, context):

            # Actual function
            return poll(context)

        return poll_wrapper

    def header_draw_decorator(draw):

        @functools.wraps(draw)
        def header_draw_wrapper(self, context):
            # Before Function

            def show_header_tabs(show_tab_text=True):
                HIDE_TEXT_SCALE_LIMIT = 0.6
                BUTTON_SIZE_MULTIPLIER = 1.4
                MAX_BUTTON_SCALE_SIZE = 1.2

                layout = self.layout
                region = context.region
                ui_scale = context.preferences.system.ui_scale

                # The following is an ugly attempt to make the item center-align better visually.
                # A dummy icon is inserted that has to be scaled as the available width changes.
                content_size_est = 160 * ui_scale
                layout_scale = min(
                    1, max(0, (region.width / content_size_est) - 1))

                tab_row = layout.row()
                show_text = False
                button_width = 0

                # Adjusts tab button size reactively depending on window width
                if show_tab_text and layout_scale > 0:
                    row = layout.row()
                    row.scale_x = layout_scale

                    # Only show icon if low width
                    if layout_scale < HIDE_TEXT_SCALE_LIMIT:
                        pass
                    else:
                        button_width = BUTTON_SIZE_MULTIPLIER * layout_scale

                    if layout_scale > MAX_BUTTON_SCALE_SIZE:
                        button_width = MAX_BUTTON_SCALE_SIZE

                tab_row.scale_x = button_width
                tab_row.scale_y = 1.2

                layout.separator_spacer()

                # Places items aligned to the right, close to the header popover.

            # ///////////////////////////////////////////////////
            if context.scene.hide_ui:
                return None

            # Actual Function
            result = draw(self, context)

            return result

        return header_draw_wrapper


class Properties_Space_Override_Classes():
    """
        Provides override classes for Blender's Properties area. 
    """

    def __init__(self) -> None:
        # Classes to override
        self.navbar_class = bl_ui.space_properties.PROPERTIES_PT_navigation_bar
        self.header_class = bl_ui.space_properties.PROPERTIES_HT_header
        self.options_class = bl_ui.space_properties.PROPERTIES_PT_options

        # Panels to hide
        self.world_prop_panels = [
            cls for cls in bl_ui.properties_world.classes
            if issubclass(cls, Panel)
        ]

        # Affected Addons
        self.cycles = self.get_addon("cycles")
        self.cycles_world_panels = self.get_cycles_world_panels(self.cycles)

    def get_addon(self, addon_name=""):
        """
        Gets the desired addon module. 
        """
        import sys
        import os

        paths_list = paths()
        addon_list = []
        for path in paths_list:
            for mod_name, mod_path in bpy.path.module_names(path):
                is_enabled, is_loaded = check(mod_name)
                addon_list.append(mod_name)

                if mod_name == addon_name and is_enabled and is_loaded:
                    mod = sys.modules.get(addon_name)
                    # chances of the file _not_ existing are low, but it could be removed
                    if mod and os.path.exists(mod.__file__):
                        return mod

        return None

    def get_cycles_world_panels(self, cycles):
        cycles_panels = []

        if cycles is not None:
            for cls in cycles.ui.classes:
                if hasattr(cls, "bl_context") and cls.bl_context == "world":
                    cycles_panels.append(cls)
        else:
            print("Cycles not found!")

        return cycles_panels

    def check_vars_exist(self):
        if not all(
                hasattr(self, var) for var in [
                    "navbar_class", "header_class", "options_class", "cycles",
                    "world_prop_panels", "cycles_world_panels"
                ]):
            return False

        return True


def prerequisites_exist():
    if all(cls is None for cls in [
            override_classes.navbar_class, override_classes.header_class,
            override_classes.options_class
    ]):
        return False

    if all(panel is None for panel in [
            override_classes.world_prop_panels,
            override_classes.cycles_world_panels
    ]):
        return False

    return True


# //////////////////////////////////////////////////////
override_classes = Properties_Space_Override_Classes()


def register():
    if override_classes.check_vars_exist() is False or prerequisites_exist(
    ) is False:
        return None

    else:
        override_classes.navbar_class.draw = Properties_Space_Override.navbar_draw_decorator(
            override_classes.navbar_class.draw)
        override_classes.header_class.draw = Properties_Space_Override.header_draw_decorator(
            override_classes.header_class.draw)
        override_classes.options_class.draw = Properties_Space_Override.options_draw_decorator(
            override_classes.options_class.draw)

        for cls in override_classes.world_prop_panels:
            setattr(
                cls, "poll",
                Properties_Space_Override.world_buttons_panel_poll(cls.poll))
        for cls in override_classes.cycles_world_panels:
            setattr(
                cls, "poll",
                Properties_Space_Override.world_buttons_panel_poll(cls.poll))


def unregister():
    # Note: This only works with the functools.wraps decorator. ChatGPT says so.
    if override_classes.check_vars_exist() is False or prerequisites_exist(
    ) is False:
        return None

    else:
        if hasattr(override_classes.options_class.draw, "__wrapped__"):
            override_classes.options_class.draw = inspect.unwrap(
                override_classes.options_class.draw)
        if hasattr(override_classes.header_class.draw, "__wrapped__"):
            override_classes.header_class.draw = inspect.unwrap(
                override_classes.header_class.draw)
        if hasattr(override_classes.navbar_class.draw, "__wrapped__"):
            override_classes.navbar_class.draw = inspect.unwrap(
                override_classes.navbar_class.draw)

        for cls in reversed(override_classes.world_prop_panels):
            if hasattr(cls.poll, "__wrapped__"):
                cls.poll = inspect.unwrap(cls.poll)

        for cls in reversed(override_classes.cycles_world_panels):
            if hasattr(cls.poll, "__wrapped__"):
                cls.poll = inspect.unwrap(cls.poll)
