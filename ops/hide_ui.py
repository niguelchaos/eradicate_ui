import bpy

class OT_HideUI(bpy.types.Operator):
    bl_idname = "view3d.hide_ui"
    bl_label = "Hide/Show UI"

    def execute(self, context):
        return {"FINISHED"}

