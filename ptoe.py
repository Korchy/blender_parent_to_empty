# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_parent_to_empty

class PtoE:

    @classmethod
    def parent_to_empty(cls, context, objects, single=False, copy_transforms=True, empty_display_type='PLAIN_AXES',
                        empty_name='empty'):
        # set parent to empty
        single_empty = None
        if single:
            single_empty = cls.add_empty(
                context=context,
                display_type=empty_display_type,
                name=empty_name
            )
        for obj in objects:
            empty = single_empty if single else cls.add_empty(
                context=context,
                display_type=empty_display_type,
                name=empty_name
            )
            if empty:
                if copy_transforms:
                    # copy transforms to empty and clear to object
                    obj.parent = empty
                else:
                    # only location
                    obj.parent = empty

    @staticmethod
    def add_empty(context, name='empty', display_type='PLAIN_AXES', location=(0.0, 0.0, 0.0), collection=None):
        # add new empty to collection
        empty = context.blend_data.objects.new(
            name=name,
            object_data=None
        )
        empty.empty_display_type = display_type
        empty.location = location
        collection = collection if collection else context.collection
        collection.objects.link(
            object=empty
        )
        return empty
