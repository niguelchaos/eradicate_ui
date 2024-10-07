import bpy
import bl_ui

import functools
import inspect


class View3d_Space_Override():

    def header_draw_decorator(draw):
        """
        Decorator that injects code for the top header in View3D.
        """

        @functools.wraps(draw)
        def header_draw_wrapper(self, context):
            """
            Wrapper for the header's draw function.
            """
            # Before Function
            if context.scene.hide_ui:
                return None
            
            # Actual Function
            result = draw(self, context)

            # After Function

            return result

        return header_draw_wrapper

    def tool_header_draw_decorator(draw):
        """
        Decorator for the lower header in View3D.
        """
        @functools.wraps(draw)
        def tool_header_draw_wrapper(self, context):
            """
            Wrapper for the tool header's draw().

            Args:
                context (_type_): _description_
            """
            # Before Function

            # LEFT STAGE

            if context.scene.hide_ui:
                # Left
                # Center Stage
                # Right
                return None

            # CENTER STAGE for Blender UI
  
            # Actual Function
            result = draw(self, context)
            return result

        return tool_header_draw_wrapper


class View3d_Space_Override_Classes():
    """
    Provides override classes for Blender's Properties area. 
    """

    def __init__(self) -> None:
        # Classes to override
        self.header_class = bl_ui.space_view3d.VIEW3D_HT_header
        self.tool_header_class = bl_ui.space_view3d.VIEW3D_HT_tool_header

    def check_vars_exist(self):
        if not all(
                hasattr(self, var)
                for var in ["tool_header_class", "header_class"]):
            print("Class missing! WG View3d will be not used.")
            return False

        return True

    def prerequisites_exist(self):
        if all(cls is None
               for cls in [self.header_class, self.tool_header_class]):
            print("UI Class missing! WG View3d will be not used.")
            return False

        return True


override_classes = View3d_Space_Override_Classes()


def register():

    if override_classes.check_vars_exist(
    ) is False or override_classes.prerequisites_exist() is False:
        return

    else:
        override_classes.header_class.draw = View3d_Space_Override.header_draw_decorator(
            override_classes.header_class.draw)
        override_classes.tool_header_class.draw = View3d_Space_Override.tool_header_draw_decorator(
            override_classes.tool_header_class.draw)


def unregister():
    # Sets original draw functions in reverse order
    if hasattr(override_classes.tool_header_class.draw, "__wrapped__"):
        override_classes.tool_header_class.draw = inspect.unwrap(
            override_classes.tool_header_class.draw)
    if hasattr(override_classes.header_class.draw, "__wrapped__"):
        override_classes.header_class.draw = inspect.unwrap(
            override_classes.header_class.draw)
