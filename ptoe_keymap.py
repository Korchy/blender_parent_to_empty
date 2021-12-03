# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_parent_to_empty

import bpy


class PTOE_KeyMap:

    _keymaps = []

    @classmethod
    def register(cls, context):
        if context.window_manager.keyconfigs.addon:
            keymap = context.window_manager.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
            # add keys
            keymap_item = keymap.keymap_items.new('ptoe.parent_to_empty', 'P', 'PRESS', ctrl=True, shift=True)
            cls._keymaps.append((keymap, keymap_item))
            keymap_item = keymap.keymap_items.new('ptoe.remove_parent_empty', 'P', 'PRESS', ctrl=True, alt=True)
            cls._keymaps.append((keymap, keymap_item))
            keymap_item = keymap.keymap_items.new('ptoe.track_to_empty', 'T', 'PRESS', ctrl=True, shift=True)
            cls._keymaps.append((keymap, keymap_item))
            keymap_item = keymap.keymap_items.new('ptoe.remove_track_empty', 'T', 'PRESS', ctrl=True, alt=True)
            cls._keymaps.append((keymap, keymap_item))

    @classmethod
    def unregister(cls):
        # clear keys
        for keymap, keymap_item in cls._keymaps:
            keymap.keymap_items.remove(keymap_item)
        cls._keymaps.clear()


def register():
    PTOE_KeyMap.register(context=bpy.context)


def unregister():
    PTOE_KeyMap.unregister()
