from bl_ui.space_toolsystem_common import (
    ToolDef, )

import bpy
import bl_ui
from addon_utils import check, paths, enable

import functools
import inspect


class WorkspaceTools_Override():

    def __init__(self) -> None:
        pass

    def tools_from_context_decorator(tools_from_context):
        """
        tools_from_context comes from bl_ui/space_toolsystem_common/ToolSelectPanelHelper.
        """

        @classmethod
        @functools.wraps(tools_from_context)
        def tools_from_context_wrapper(cls, context, mode=None):

            def custom_tools_from_context(cls, context, mode=None):
                """

                Args:
                    context (_type_): _description_
                    mode (_type_, optional): _description_. Defaults to None.

                Yields:
                    _type_: A workspace tool. Every yielded workspace tool is shown.
                """
                if context.scene.hide_ui:
                    return None

                if mode is None:
                    mode = context.mode

                tooldefs = {}
                tooldefs["callables"] = []

                # 1. Get all relevant tool definitions (tooldefs).
                for tools in (cls._tools[None], cls._tools.get(mode, ())):
                    separators = []

                    # item is a ToolDef or None. None is a visual separator.
                    for item in tools:
                        tool_idname = None
                        if not (type(item) is ToolDef) and callable(item):
                            tooldefs["callables"].append(item(context))
                        else:
                            # Ungrouped Tools
                            if (type(item) is ToolDef) and not callable(item):
                                tool_idname = item[0]

                            # Grouped Tools
                            elif item is not None:
                                tool_idname = item[0][0]

                            if tool_idname is None:
                                continue

                            if not can_show_tool(tool_idname):
                                continue

                            # 1a. Remember separators, put em with the same tool list in the next loop
                            if item is None:
                                separators.append(None)
                                continue

                            tooldefs[tool_idname] = []
                            if len(separators) > 0:
                                tooldefs[tool_idname].extend(separators)
                                separators = []

                            tooldefs[tool_idname].append(item)

                # 2. Sort the tools based on mode tool order
                sorted_tools = []

                for key, tooldef in tooldefs.items():
                    sorted_tools.extend(tooldef)

                # 3. Show by yielding all
                yield from sorted_tools

            def can_show_tool(tool_idname, tool_cls=None):
                return True

            # Before Function

            # Actual Function

            result = tools_from_context(context, mode)

            # After Function
            return result

        return tools_from_context_wrapper

    def draw_cls_decorator(draw_cls):

        @classmethod
        @functools.wraps(draw_cls)
        def draw_cls_wrapper(cls,
                             layout,
                             context,
                             detect_layout=True,
                             scale_y=1.75):

            result = draw_cls(layout, context, detect_layout, scale_y)

            # After Function
            return result

        return draw_cls_wrapper


class WorkspaceTools_Override_Classes():
    """
    Provides override classes for Blender's Properties area. 
    """

    def __init__(self) -> None:
        # Classes to override
        self.tool_select_panel_helper = bl_ui.space_toolsystem_common.ToolSelectPanelHelper
        self.tools_active_class = bl_ui.space_toolsystem_toolbar.VIEW3D_PT_tools_active

    def check_vars_exist(self):
        if not all(
                hasattr(self, var)
                for var in ["tools_active_class", "tool_select_panel_helper"]):
            return False

        return True

    def prerequisites_exist(self):
        if all(cls is None for cls in
               [self.tools_active_class, self.tool_select_panel_helper]):
            return False

        return True


override_classes = WorkspaceTools_Override_Classes()


def register():
    if override_classes.check_vars_exist(
    ) is False or override_classes.prerequisites_exist() is False:
        return

    else:
        # Decorate tabs, inject code
        override_classes.tools_active_class.tools_from_context = WorkspaceTools_Override.tools_from_context_decorator(
            override_classes.tools_active_class.tools_from_context)


def unregister():
    # Sets original draw functions in reverse order
    if hasattr(override_classes.tools_active_class.tools_from_context,
               "__wrapped__"):
        override_classes.tools_active_class.tools_from_context = inspect.unwrap(
            override_classes.tools_active_class.tools_from_context)
