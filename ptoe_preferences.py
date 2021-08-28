# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_parent_to_empty

from bpy.types import AddonPreferences, Object
from bpy.props import BoolProperty, EnumProperty, StringProperty
from bpy.utils import register_class, unregister_class


class PTOE_preferences(AddonPreferences):
    bl_idname = __package__

    transfer_transforms: BoolProperty(
        name='Transfer Transforms to Empty',
        default=True
    )

    empty_display_type: EnumProperty(
        name='Empty Display Type',
        items=[(item[1].identifier, item[1].name, item[1].description, item[1].icon, item[0]) for item in
               enumerate(Object.bl_rna.properties['empty_display_type'].enum_items)],
        default='PLAIN_AXES'
    )

    empty_location: EnumProperty(
        name='Empty Location',
        items=[
            ('GEOMETRY', 'Geometry', 'Geometry', '', 0),
            ('ORIGIN', 'Origin', 'Origin', '', 1),
            ('ACTIVE', 'Active', 'Active Object', '', 2),
            ('CURSOR', 'Cursor', '3D Cursor', '', 3),
            ('WORLD_ORIGIN', 'World Origin', 'World Origin', '', 4)
        ],
        default='GEOMETRY'
    )

    empty_default_name: StringProperty(
        name='Empty Name',
        default='Empty'
    )

    parenting_scatter: EnumProperty(
        name='Scatter',
        items=[
            ('SINGLE', 'Single Empty', 'Single Empty to all objects', '', 0),
            ('EACH', 'Own Empty', 'Own Empty to Each object', '', 1)
        ],
        default='SINGLE'
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(data=self, property='empty_display_type')
        row = layout.row()
        row.prop(data=self, property='parenting_scatter', expand=True)
        if self.parenting_scatter == 'EACH':
            layout.prop(data=self, property='transfer_transforms')
        if self.parenting_scatter != 'EACH' or not self.transfer_transforms:
            row = layout.row()
            row.prop(data=self, property='empty_location', expand=True)
        layout.prop(data=self, property='empty_default_name')


def register():
    register_class(PTOE_preferences)


def unregister():
    unregister_class(PTOE_preferences)
