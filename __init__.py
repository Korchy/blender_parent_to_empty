# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_parent_to_empty

from . import ptoe_ops
from . import ptoe_ui
from . import ptoe_preferences
from . import ptoe_keymap
from .addon import Addon


bl_info = {
    'name': 'Parent to Empty',
    'category': 'All',
    'author': 'Nikita Akimov',
    'version': (1, 1, 0),
    'blender': (2, 93, 0),
    'location': 'View3D - N-panel - PtoE tab',
    'wiki_url': 'https://b3d.interplanety.org/en/blender-add-on-parent-to-empty/',
    'tracker_url': 'https://b3d.interplanety.org/en/blender-add-on-parent-to-empty/',
    'description': 'Quickly add en Empty to the Object as its parent'
}


def register():
    if not Addon.dev_mode():
        ptoe_preferences.register()
        ptoe_ops.register()
        ptoe_ui.register()
        ptoe_keymap.register()
    else:
        print('It seems you are trying to use the dev version of the ' + bl_info['name'] + ' add-on. It may work not properly. Please download and use the release version')


def unregister():
    if not Addon.dev_mode():
        ptoe_keymap.unregister()
        ptoe_ui.unregister()
        ptoe_ops.unregister()
        ptoe_preferences.unregister()


if __name__ == '__main__':
    register()
