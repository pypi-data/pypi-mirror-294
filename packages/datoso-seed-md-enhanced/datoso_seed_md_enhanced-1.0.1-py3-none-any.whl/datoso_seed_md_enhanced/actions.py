"""Actions for the md enhanced seed."""
from datoso_seed_md_enhanced.dats import MdEnhancedDat

actions = {
    '{dat_origin}': [
        {
            'action': 'LoadDatFile',
            '_class': MdEnhancedDat,
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
