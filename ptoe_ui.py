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
        box = layout.box()
        box.label(text='Add Parent Empty')
        box.prop(data=pref, property='empty_display_type', text='')
        row = box.row()
        row.prop(data=pref, property='parenting_scatter', expand=True)
        if pref.parenting_scatter == 'EACH':
            box.prop(data=pref, property='transfer_transforms')
        if pref.parenting_scatter != 'EACH' or not pref.transfer_transforms:
            row = box.row()
            row.prop(data=pref, property='empty_location', expand=True)
        box.prop(data=pref, property='empty_default_name')
        box.operator('ptoe.parent_to_empty', icon='DECORATE_LINKED')
        box = layout.box()
        box.label(text='Remove Parent Empty')
        box.operator('ptoe.remove_parent_empty', icon='DECORATE_LIBRARY_OVERRIDE')
        box = layout.box()
        box.label(text='Tools')
        box.operator('ptoe.collection_to_parent_empty', icon='DECORATE_LINKED')
        box.operator('ptoe.parent_empty_to_collection', icon='COLLECTION_NEW')


def register():
    register_class(PTOE_PT_panel)


def unregister():
    unregister_class(PTOE_PT_panel)
