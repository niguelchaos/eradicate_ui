import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty


class EradicateUIPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__

    default_hide_ui: BoolProperty(
        name="Default Hide UI",
        default=True,
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "default_hide_ui")
