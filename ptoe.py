# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_parent_to_empty

from .bpy_plus.bounding import Bounding


class PtoE:

    @classmethod
    def parent_to_empty(cls, context, objects, single=False, transfer_transforms=True, empty_display_type='PLAIN_AXES',
                        empty_name='Empty', empty_location='CENTER'):
        # set parent to empty
        single_empty = None
        if single:
            # print(empty_location)
            single_empty = cls.add_empty(
                context=context,
                display_type=empty_display_type,
                location=cls.location_co(
                    context=context,
                    obj=objects,
                    location=empty_location
                ),
                name=empty_name
            )
        for obj in objects:
            empty = single_empty if single else cls.add_empty(
                context=context,
                display_type=empty_display_type,
                location=cls.location_co(
                    context=context,
                    obj=obj,
                    location=empty_location
                ),
                name=empty_name,
                collection=obj.users_collection[0]
            )
            if empty:
                cls.remove_parent_empty(
                    context=context,
                    objects=obj
                )
                context.view_layer.update()
                if not single and transfer_transforms:
                    # copy transforms to empty and clear to object
                    empty.matrix_world = obj.matrix_world.copy()
                    obj.matrix_world.identity()
                    obj.parent = empty

                else:
                    # only location
                    obj.parent = empty
                    obj.matrix_local @= empty.matrix_world.inverted()

    @classmethod
    def remove_parent_empty(cls, context, objects):
        # remove parent empty
        if not isinstance(objects, (list, tuple)):
            objects = [objects,]
        # collect empties to future remove (maybe single empty or different empties on every objects)
        empties = []
        # clear parenting
        for obj in objects:
            # if obj.parent and obj.parent.type == 'EMPTY':
            if obj.parent:
                parent = obj.parent
                obj.parent = None
                obj.matrix_local @= parent.matrix_world.inverted()
                if parent.type == 'EMPTY' and parent not in empties:
                    empties.append(parent)
        # really remove empties
        for empty in empties:
            if not empty.children:
                context.blend_data.objects.remove(empty, do_unlink=True)

    @classmethod
    def collection_to_parent_empty(cls, context, collection, empty_display_type='PLAIN_AXES', empty_name='Empty',
                                   empty_location='CENTER'):
        # convert collection to parent empty
        if collection:
            collection_objects = [obj for obj in collection.collection.objects if obj.type != 'EMPTY']
            cls.parent_to_empty(
                context=context,
                objects=collection_objects,
                single=True,
                empty_display_type=empty_display_type,
                empty_name=empty_name,
                empty_location=empty_location
            )

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

    @staticmethod
    def location_co(context, obj, location):
        # get coordinates by location
        co = (0.0, 0.0, 0.0)    # WORLD_ORIGIN
        if location == 'CENTER':
            # Center of selected objects geometry
            co, radius = Bounding.sphere(
                objects=obj,
                mode='BBOX'
            )
        elif location == 'ACTIVE':
            # active object
            if context.active_object.parent:
                co = context.active_object.parent.location
            else:
                co = context.active_object.location
        elif location == 'CURSOR':
            # active object
            co = context.scene.cursor.location
        return co
