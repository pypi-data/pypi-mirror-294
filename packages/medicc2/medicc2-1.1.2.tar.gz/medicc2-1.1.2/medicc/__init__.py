import logging.config
import os

from importlib.metadata import version, PackageNotFoundError
import yaml

import medicc.bootstrap
import medicc.core
import medicc.io
import medicc.nj
import medicc.plot
import medicc.sim
import medicc.stats
import medicc.tools
from medicc.ancestors import reconstruct_ancestors
from medicc.core import *
from medicc.factory import *

with open(os.path.join(os.path.dirname(__file__), 'logging_conf.yaml'), 'rt') as f:
    config = yaml.safe_load(f.read())
logging.config.dictConfig(config)

try:
    __version__ = version('medicc2')
except PackageNotFoundError:
    __version__ = 'not installed'
