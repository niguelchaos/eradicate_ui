import bpy


class MainPanel(bpy.types.Panel):
    bl_idname = "SCENE_PT_eradicate_ui_main_panel"
    bl_label = "Eradicate UI Main Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Eradicate UI"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "hide_ui")