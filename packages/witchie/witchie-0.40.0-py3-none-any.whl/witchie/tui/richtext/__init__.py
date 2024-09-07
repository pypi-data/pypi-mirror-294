# SPDX-FileCopyrightText: 2017-2023 Ivan Habunek et al <ivan@habunek.com>
# SPDX-FileCopyrightText: 2023-2024 Ngô Ngọc Đức Huy <huyngo@disroot.org>
#
# SPDX-License-Identifier: GPL-3.0-only

from typing import List

import urwid

from witchie.tui.utils import highlight_hashtags
from witchie.utils import format_content

try:
    from .richtext import html_to_widgets, url_to_widget
except ImportError:
    # Fallback if urwidgets are not available
    def html_to_widgets(html: str) -> List[urwid.Widget]:
        return [
            urwid.Text(highlight_hashtags(line))
            for line in format_content(html)
        ]

    def url_to_widget(url: str):
        return urwid.Text(("link", url))
