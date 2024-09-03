"""Actions for the sfc speedhacks seed."""
from datoso_seed_sfc_speedhacks.dats import SFCSpeedHacksDat

actions = {
    '{dat_origin}': [
        {
            'action': 'LoadDatFile',
            '_class': SFCSpeedHacksDat,
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
