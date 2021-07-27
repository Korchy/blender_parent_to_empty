# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_parent_to_empty

from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .ptoe import PtoE


class PTOE_OT_parent_to_empty(Operator):
    bl_idname = 'ptoe.parent_to_empty'
    bl_label = 'Parent to Empty'
    bl_description = 'Parent to Empty'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        PtoE.parent_to_empty(
           context=context
        )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return bool(context.selected_objects)


def register():
    register_class(PTOE_OT_parent_to_empty)


def unregister():
    unregister_class(PTOE_OT_parent_to_empty)
