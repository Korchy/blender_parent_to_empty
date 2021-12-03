# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_parent_to_empty

from .bpy_plus.bounding import Bounding


class PtoE:

    @classmethod
    def parent_to_empty(cls, context, objects: list, single=False, transfer_transforms=True,
                        empty_display_type='PLAIN_AXES', empty_name='Empty', empty_location='GEOMETRY',
                        collection=None):
        # set parent to empty
        single_empty = None
        # don't process empties
        objects = [obj for obj in objects if obj.type != 'EMPTY']
        if objects:
            # single/own empty
            if single:
                # get collection for empty
                if not collection:
                    collection = objects[0].users_collection[0]
                # create empty
                single_empty = cls.add_empty(
                    context=context,
                    display_type=empty_display_type,
                    location=cls.location_co(
                        context=context,
                        obj=objects,
                        location=empty_location
                    ),
                    name=empty_name,
                    collection=collection
                )
            for obj in objects:
                dest_collection = collection if collection else obj.users_collection[0]
                empty = single_empty if single else cls.add_empty(
                    context=context,
                    display_type=empty_display_type,
                    location=cls.location_co(
                        context=context,
                        obj=obj,
                        location=empty_location
                    ),
                    name=empty_name,
                    collection=dest_collection
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
                # move object to collection
                cls.move_object_to_collection(obj=obj, collection=dest_collection)

    @classmethod
    def remove_parent_empty(cls, context, objects, collection=None):
        # remove parent empty
        if not isinstance(objects, (list, tuple)):
            objects = [objects, ]
        # collect empties to future remove (maybe single empty or different empties on every objects)
        empties = []
        # clear parenting
        for obj in objects:
            if obj.parent:
                parent = obj.parent
                obj.parent = None
                obj.matrix_local @= parent.matrix_world.inverted()
                if parent.type == 'EMPTY' and parent not in empties:
                    empties.append(parent)
                # link objects to collection
                if collection:
                    cls.move_object_to_collection(obj=obj, collection=collection)
        # really remove empties
        for empty in empties:
            if not empty.children:
                context.blend_data.objects.remove(empty, do_unlink=True)

    @classmethod
    def collection_to_parent_empty(cls, context, collection, empty_display_type='PLAIN_AXES', empty_name='Empty',
                                   empty_location='GEOMETRY'):
        # convert collection to parent empty
        if collection:
            parent_collection = cls.parent_collection(
                context=context,
                collection=collection
            )
            collection_objects = collection.objects[:]
            if collection_objects:
                cls.parent_to_empty(
                    context=context,
                    objects=collection_objects,
                    single=True,
                    empty_display_type=empty_display_type,
                    empty_name=empty_name,
                    empty_location=empty_location,
                    collection=parent_collection
                )
            if len(collection.objects) == 0 and len(collection.children) == 0:
                context.blend_data.collections.remove(collection)

    @classmethod
    def parent_empty_to_collection(cls, context, empty):
        # convert parent empty to collection
        if empty and empty.children:
            # create collection
            collection = context.blend_data.collections.new(name=empty.name)
            collection.name = empty.name
            # link collection to empty parent collection
            empty.users_collection[0].children.link(collection)
            # remove parent empty for all objects
            cls.remove_parent_empty(
                context=context,
                objects=empty.children,
                collection=collection
            )

    @classmethod
    def track_to_empty(cls, context, objects: list, single=False, empty_display_type='PLAIN_AXES',
                       empty_name='Empty', empty_location='GEOMETRY', collection=None):
        # set track to empty
        single_empty = None
        # don't process empties
        objects = [obj for obj in objects if obj.type != 'EMPTY']
        if objects:
            # single/own empty
            if single:
                # get collection for empty
                if not collection:
                    collection = objects[0].users_collection[0]
                # create empty
                single_empty = cls.add_empty(
                    context=context,
                    display_type=empty_display_type,
                    location=cls.location_co(
                        context=context,
                        obj=objects,
                        location=empty_location
                    ),
                    name=empty_name,
                    collection=collection
                )
            for obj in objects:
                dest_collection = collection if collection else obj.users_collection[0]
                empty = single_empty if single else cls.add_empty(
                    context=context,
                    display_type=empty_display_type,
                    location=cls.location_co(
                        context=context,
                        obj=obj,
                        location=empty_location
                    ),
                    name=empty_name,
                    collection=dest_collection
                )
                if empty:
                    # remove old track if exists
                    cls.remove_track_empty(
                        context=context,
                        objects=obj
                    )
                    # add new track_to
                    cls.add_track_to_constraint(
                        obj=obj,
                        target=empty
                    )
                # move object to collection
                cls.move_object_to_collection(obj=obj, collection=dest_collection)

    @classmethod
    def remove_track_empty(cls, context, objects):
        # remove parent empty
        if not isinstance(objects, (list, tuple)):
            objects = [objects, ]
        # collect empties to future remove (maybe single empty or different empties on every objects)
        empties = []
        # clear tracking
        for obj in objects:
            track_to_constraint = next(
                (constraint for constraint in obj.constraints if constraint.type == 'TRACK_TO'), None
            )
            if track_to_constraint:
                target = track_to_constraint.target
                if target.type == 'EMPTY' and target not in empties:
                    empties.append(target)
                # save current transformations
                mat = obj.matrix_world.copy()
                # remove track_to constraint
                obj.constraints.remove(track_to_constraint)
                # set current transformation
                obj.matrix_local = mat
        # really remove empties
        if empties:
            all_track_to_targets = [
                constraint.target for constraints in
                (obj.constraints for obj in context.blend_data.objects if obj.constraints)
                for constraint in constraints if constraint.type == 'TRACK_TO'
            ]
            for empty in empties:
                if empty not in all_track_to_targets:
                    context.blend_data.objects.remove(empty, do_unlink=True)

    @classmethod
    def add_empty(cls, context, name='empty', display_type='PLAIN_AXES', location=(0.0, 0.0, 0.0), collection=None):
        # add new empty to collection
        empty = context.blend_data.objects.new(
            name=name,
            object_data=None
        )
        empty.empty_display_type = display_type
        empty.location = location
        cls.move_object_to_collection(
            obj=empty,
            collection=collection if collection else context.collection
        )
        return empty

    @staticmethod
    def location_co(context, obj, location):
        # get coordinates for empty location
        co = (0.0, 0.0, 0.0)    # WORLD_ORIGIN
        if location == 'GEOMETRY':
            # Center of selected objects geometry
            co, radius = Bounding.sphere(
                objects=obj,
                context=context,
                mode='BBOX'
            )
        elif location == 'ORIGIN':
            # Centre of objects origins
            if hasattr(obj, '__len__') and len(obj) > 1:
                co, radius = Bounding.sphere(
                    objects=obj,
                    context=context,
                    mode='ORIGIN'
                )
            else:
                if obj.parent:
                    co = obj.parent.location
                else:
                    co = obj.location
        elif location == 'ACTIVE':
            # active object
            if context.active_object:
                if context.active_object.parent:
                    co = context.active_object.parent.location
                else:
                    co = context.active_object.location
        elif location == 'CURSOR':
            # active object
            co = context.scene.cursor.location
        return co

    @staticmethod
    def collections(context):
        # get all scene collections
        collections = context.blend_data.collections[:]
        collections.append(context.scene.collection)    # add main scene collection
        return collections

    @classmethod
    def parent_collection(cls, context, collection):
        # get collection parent collection
        collections = cls.collections(
            context=context
        )
        return next((col for col in collections if collection.name in col.children), None)

    @staticmethod
    def move_object_to_collection(obj, collection):
        # move object to collection
        # current object collections
        current_collections = obj.users_collection[:]
        # link to new collection
        if collection not in obj.users_collection:
            collection.objects.link(object=obj)
        # unlink from old collections (after linking to new not to loose object from scene while moving)
        for col in current_collections:
            if col is not collection:
                col.objects.unlink(obj)

    @staticmethod
    def add_track_to_constraint(obj, target):
        # track object to target
        if obj and target:
            constraint = obj.constraints.new(type='TRACK_TO')
            constraint.target = target
