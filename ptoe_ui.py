# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_parent_to_empty

from bpy.types import Panel
from bpy.utils import register_class, unregister_class


class PTOE_PT_panel(Panel):
    bl_idname = 'PTOE_PT_panel'
    bl_label = 'Parent to Empty'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'PtoE'

    def draw(self, context):
        layout = self.layout
        pref = context.preferences.addons[__package__].preferences
        layout.prop(data=pref, property='empty_display_type', text='')
        layout.prop(data=pref, property='parenting_scatter', expand=True)
        layout.prop(data=pref, property='empty_default_name')
        layout.operator('ptoe.parent_to_empty', icon='BLENDER')


def register():
    register_class(PTOE_PT_panel)


def unregister():
    unregister_class(PTOE_PT_panel)