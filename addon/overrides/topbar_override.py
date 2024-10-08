import bl_ui

import functools
import inspect


class Topbar_Space_Override():

    def upper_bar_draw_left_decorator(draw_left):
        """
        Decorator that injects code for the top-left (main) header of Blender.
        The left side contains the menus and the layouts.
        """

        @functools.wraps(draw_left)
        def upper_bar_draw_left_wrapper(self, context):

            def draw_left_custom_upper_bar(self, context):
                layout = self.layout
                screen = context.screen

                bl_ui.space_topbar.TOPBAR_MT_editor_menus.draw_collapsible(
                    context, layout)

                layout.separator()

                if not screen.show_fullscreen:
                    pass

                else:
                    layout.operator(
                        "screen.back_to_previous",
                        icon='SCREEN_BACK',
                        text="Back to Previous",
                    )

            # Before Function
            if context.scene.hide_ui:
                return None

            # Actual Function
            result = draw_left(self, context)

            # After Function
            return result

        return upper_bar_draw_left_wrapper

    def upper_bar_draw_right_decorator(draw_right):
        """
        Decorator that injects code for the top-right (main) header of Blender.
        The left side contains the Scene and Viewlayers.
        """

        @functools.wraps(draw_right)
        def upper_bar_draw_right_wrapper(self, context):

            # Before Function
            if context.scene.hide_ui:
                return None

            # Actual Function
            result = draw_right(self, context)

            # After Function
            return result

        return upper_bar_draw_right_wrapper

    def topbar_menu_draw_decorator(draw):
        """
        Decorator that injects code for the top (main) header of Blender.
        """

        @functools.wraps(draw)
        def topbar_menu_draw_wrapper(self, context):

            def custom_topbar_menu_draw(self, context):
                pass

            if context.scene.hide_ui:
                return None

            # Actual Function
            result = draw(self, context)

            # After Function
            return result

        return topbar_menu_draw_wrapper


class Topbar_Space_Override_Classes():

    def __init__(self) -> None:
        # Classes to override
        self.upper_bar = bl_ui.space_topbar.TOPBAR_HT_upper_bar
        self.topbar_menus = bl_ui.space_topbar.TOPBAR_MT_editor_menus

    def check_vars_exist(self):
        if not all(
                hasattr(self, var) for var in ["upper_bar", "topbar_menus"]):
            return False

        return True

    def prerequisites_exist(self):
        if all(cls is None for cls in [self.upper_bar, self.topbar_menus]):
            return False

        return True


override_classes = Topbar_Space_Override_Classes()


def register():

    if override_classes.check_vars_exist(
    ) is False or override_classes.prerequisites_exist() is False:
        return

    else:
        override_classes.upper_bar.draw_right = Topbar_Space_Override.upper_bar_draw_right_decorator(
            override_classes.upper_bar.draw_right)
        override_classes.upper_bar.draw_left = Topbar_Space_Override.upper_bar_draw_left_decorator(
            override_classes.upper_bar.draw_left)
        override_classes.topbar_menus.draw = Topbar_Space_Override.topbar_menu_draw_decorator(
            override_classes.topbar_menus.draw)


def unregister():
    # Sets original draw functions in reverse order
    if hasattr(override_classes.topbar_menus.draw, "__wrapped__"):
        override_classes.topbar_menus.draw = inspect.unwrap(
            override_classes.topbar_menus.draw)
    if hasattr(override_classes.upper_bar.draw_left, "__wrapped__"):
        override_classes.upper_bar.draw_left = inspect.unwrap(
            override_classes.upper_bar.draw_left)
    if hasattr(override_classes.upper_bar.draw_right, "__wrapped__"):
        override_classes.upper_bar.draw_right = inspect.unwrap(
            override_classes.upper_bar.draw_right)
