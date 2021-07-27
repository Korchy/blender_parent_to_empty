# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_parent_to_empty

from bpy.types import AddonPreferences
from bpy.props import StringProperty
from bpy.utils import register_class, unregister_class


class PTOE_preferences(AddonPreferences):
    bl_idname = __package__

    pref1: StringProperty(
        name='pref1',
        default='ptoe'
    )

    def draw(self, context):
        self.layout.prop(self, 'pref1')


def register():
    register_class(PTOE_preferences)


def unregister():
    unregister_class(PTOE_preferences)
