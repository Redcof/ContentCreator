from __future__ import division
from __future__ import print_function

import numpy as np
from easydict import EasyDict as edict
import yaml
import os

__C = edict()
cfg = __C

# Dataset name
__C.TOPIC = 'motivation'
__C.LENGTH_IN_MINUTE = 5
__C.TYPE = 'video'
__C.RESOLUTION = '720p'
__C.LANGUAGE = 'en'

# Video options
__C.VIDEO = edict()
__C.VIDEO.IMAGE_QUERY = 'cute cats'
__C.VIDEO.IMAGE_COUNT = 5
__C.VIDEO.TITLE = "A monday motivation"
__C.VIDEO.DESCRIPTION = "A monday motivation"
__C.VIDEO.HASH_TAGS = "motivation,youtubeshots,iphone"

# Video options
__C.AUDIO = edict()
__C.AUDIO.SPEED_X = 1.0
__C.AUDIO.VOICE = 'female'

# Create content using stock video and audio
__C.STOCK = edict()
__C.STOCK.AUDIO = ""
__C.STOCK.VIDEO = ""
__C.STOCK.REPEAT = 2


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        import errno
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def _merge_a_into_b(a, b):
    """Merge config dictionary a into config dictionary b, clobbering the
    options in b whenever they are also specified in a.
    """
    if type(a) is not edict:
        return

    for k, v in a.items():
        # a must specify keys that are in b
        if k not in b:
            raise KeyError('{} is not a valid config key'.format(k))

        # the types must match, too
        old_type = type(b[k])
        if old_type is not type(v):
            if isinstance(b[k], np.ndarray):
                v = np.array(v, dtype=b[k].dtype)
            else:
                raise ValueError(('Type mismatch ({} vs. {}) '
                                  'for config key: {}').format(type(b[k]),
                                                               type(v), k))

        # recursively merge dicts
        if type(v) is edict:
            try:
                _merge_a_into_b(a[k], b[k])
            except:
                print('Error under config key: {}'.format(k))
                raise
        else:
            b[k] = v


def validate_config():
    assert __C.TYPE in ['shorts', 'video'], __C.TYPE
    assert __C.RESOLUTION in ['480p', '720p', '1080p', '2K', '4K', '8K'], __C.RESOLUTION
    assert __C.AUDIO.SPEED_X in [0.25, 0.5, 0.75, 1., 1.25, 1.5, 1.75, 2.], __C.AUDIO.SPEED_X
    assert __C.AUDIO.VOICE in ['male', 'female'], __C.AUDIO.VOICE


def cfg_from_file(filename):
    """Load a config file and merge it into the default options."""
    with open(filename, 'r') as f:
        yaml_cfg = edict(yaml.full_load(f))
    _merge_a_into_b(yaml_cfg, __C)
    validate_config()
