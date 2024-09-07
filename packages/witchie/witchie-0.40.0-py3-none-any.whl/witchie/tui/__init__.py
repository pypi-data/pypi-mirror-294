# SPDX-FileCopyrightText: 2017-2023 Ivan Habunek et al <ivan@habunek.com>
# SPDX-FileCopyrightText: 2023-2024 Ngô Ngọc Đức Huy <huyngo@disroot.org>
#
# SPDX-License-Identifier: GPL-3.0-only

from urwid.command_map import (CURSOR_DOWN, CURSOR_LEFT, CURSOR_RIGHT,
                               CURSOR_UP, command_map)

# Add movement using h/j/k/l to default command map
command_map._command.update({
    'k': CURSOR_UP,
    'j': CURSOR_DOWN,
    'h': CURSOR_LEFT,
    'l': CURSOR_RIGHT,
})
