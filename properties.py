import bpy


def register():
    bpy.types.Scene.hide_ui = bpy.props.BoolProperty(
        name="Hide UI",
        default=bpy.context.preferences.addons[__package__].preferences.
        default_hide_ui)
