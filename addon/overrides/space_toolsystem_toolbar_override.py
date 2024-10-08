from bl_ui.space_toolsystem_common import (
    ToolDef, )

import bpy
import bl_ui
from addon_utils import check, paths, enable

import functools
import inspect


class ToolSystemToolbar_Override():

    def draw_decorator(draw):

        # @classmethod
        @functools.wraps(draw)
        def draw_wrapper(self, context):
            if context.scene.hide_ui:
                return None

            result = draw(self, context)

            # After Function
            return result

        return draw_wrapper


class ToolSystemToolbar_Override_Classes():
    """
    Provides override classes for Blender's Properties area. 
    """

    def __init__(self) -> None:
        # Classes to override
        self.tools_active_panel = bl_ui.space_toolsystem_toolbar.VIEW3D_PT_tools_active

    def check_vars_exist(self):
        if not all(hasattr(self, var) for var in ["tools_active_panel"]):
            return False
        return True

    def prerequisites_exist(self):
        if all(cls is None for cls in [self.tools_active_panel]):
            return False
        return True


override_classes = ToolSystemToolbar_Override_Classes()


def register():
    if override_classes.check_vars_exist(
    ) is False or override_classes.prerequisites_exist() is False:
        return

    else:
        override_classes.tools_active_panel.draw = ToolSystemToolbar_Override.draw_decorator(
            override_classes.tools_active_panel.draw)


def unregister():
    # Sets original draw functions in reverse order
    if hasattr(override_classes.tools_active_panel.draw, "__wrapped__"):
        override_classes.tools_active_panel.draw = inspect.unwrap(
            override_classes.tools_active_panel.draw)
