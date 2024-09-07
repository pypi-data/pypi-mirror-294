# SPDX-FileCopyrightText: 2017-2023 Ivan Habunek et al <ivan@habunek.com>
# SPDX-FileCopyrightText: 2023-2024 Ngô Ngọc Đức Huy <huyngo@disroot.org>
#
# SPDX-License-Identifier: GPL-3.0-only

import os
import sys
from collections import namedtuple
from importlib.metadata import version
from os.path import expanduser, join

App = namedtuple('App', ['instance', 'base_url', 'client_id', 'client_secret'])
User = namedtuple('User', ['instance', 'username', 'access_token', 'optimized'])

DEFAULT_INSTANCE = 'https://mastodon.social'

CLIENT_NAME = 'witchie - an Akkoma CLI client'
CLIENT_WEBSITE = 'https://sr.ht/~huyngo/witchie'

CONFIG_DIR_NAME = "witchie"

__version__ = version('witchie')


def get_config_dir():
    """Returns the path to witchie config directory"""

    # On Windows, store the config in roaming appdata
    if sys.platform == "win32" and "APPDATA" in os.environ:
        return join(os.getenv("APPDATA"), CONFIG_DIR_NAME)

    # Respect XDG_CONFIG_HOME env variable if set
    # https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
    if "XDG_CONFIG_HOME" in os.environ:
        config_home = expanduser(os.environ["XDG_CONFIG_HOME"])
        return join(config_home, CONFIG_DIR_NAME)

    # Default to ~/.config/witchie/
    return join(expanduser("~"), ".config", CONFIG_DIR_NAME)


def get_cache_path():
    """Returns the path to witchie cache file"""

    # On Windows, store the config in roaming appdata
    if sys.platform == "win32" and "APPDATA" in os.environ:
        return join(os.getenv("APPDATA"), CONFIG_DIR_NAME, 'cache.db')

    # Respect XDG_CONFIG_HOME env variable if set
    # https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
    if "XDG_DATA_HOME" in os.environ:
        data_home = expanduser(os.environ["XDG_CACHE_HOME"])
        return join(data_home, CONFIG_DIR_NAME, 'cache.db')

    # Default to ~/.local/share/
    return join(expanduser("~"), ".cache", CONFIG_DIR_NAME, 'cache.db')
