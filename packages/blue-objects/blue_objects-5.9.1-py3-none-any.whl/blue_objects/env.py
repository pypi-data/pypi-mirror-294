import os
from abcli.env import load_env, load_config

load_env(__name__)
load_config(__name__)


BLUE_OBJECTS_SECRET = os.getenv(
    "BLUE_OBJECTS_SECRET",
    "",
)

ABCLI_PUBLIC_PREFIX = os.getenv(
    "ABCLI_PUBLIC_PREFIX",
    "",
)
