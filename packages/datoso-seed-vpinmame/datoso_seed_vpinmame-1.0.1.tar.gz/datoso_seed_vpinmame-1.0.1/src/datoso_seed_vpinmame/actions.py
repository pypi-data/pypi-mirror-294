"""Actions for the vpinmame seed."""
from datoso_seed_vpinmame.dats import VPinMameDat

actions = {
    '{dat_origin}': [
        {
            'action': 'LoadDatFile',
            '_class': VPinMameDat,
        },
        {
            'action': 'DeleteOld',
            'folder': '{dat_destination}',
        },
        {
            'action': 'Copy',
            'folder': '{dat_destination}',
        },
        {
            'action': 'SaveToDatabase',
        },
    ],
}

def get_actions() -> dict:
    """Get the actions dictionary."""
    return actions
