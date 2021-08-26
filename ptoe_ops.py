# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_parent_to_empty

from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .ptoe import PtoE


# todo convert: collection to parenting, parenting to collection


class PTOE_OT_parent_to_empty(Operator):
    bl_idname = 'ptoe.parent_to_empty'
    bl_label = 'Parent to Empty'
    bl_description = 'Parent to Empty'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        pref_vars = context.preferences.addons[__package__].preferences
        PtoE.parent_to_empty(
            context=context,
            objects=context.selected_objects,
            single=True if pref_vars.parenting_scatter == 'SINGLE' else False,
            transfer_transforms=pref_vars.transfer_transforms,
            empty_display_type=pref_vars.empty_display_type,
            empty_name=pref_vars.empty_default_name,
            empty_location=pref_vars.empty_location
        )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return bool(context.selected_objects)


class PTOE_OT_remove_parent_empty(Operator):
    bl_idname = 'ptoe.remove_parent_empty'
    bl_label = 'Remove Parent Empty'
    bl_description = 'Remove Parent Empty'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        PtoE.remove_parent_empty(
            context=context,
            objects=context.selected_objects
        )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return bool(context.selected_objects)


def register():
    register_class(PTOE_OT_parent_to_empty)
    register_class(PTOE_OT_remove_parent_empty)


def unregister():
    unregister_class(PTOE_OT_remove_parent_empty)
    unregister_class(PTOE_OT_parent_to_empty)
