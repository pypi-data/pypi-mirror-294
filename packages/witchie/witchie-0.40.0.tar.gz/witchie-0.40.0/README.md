<!--
SPDX-FileCopyrightText: 2023-2024 Ngô Ngọc Đức Huy <huyngo@disroot.org>

SPDX-License-Identifier: GPL-3.0-only
-->

# Witchie - an Akkoma CLI client

Witchie is a CLI and TUI tool for interacting with Akkoma instances from the
command line.  It is a fork of [ibuhanek's toot](https://github.com/ihabunek/toot)
for Mastodon to add Akkoma-specific features, such as custom emoji reacts or quote.

[![builds.sr.ht status](https://builds.sr.ht/~huyngo/witchie.svg)](https://builds.sr.ht/~huyngo/witchie?)

Requires python 3.9 or later

## Resources

* Homepage: https://sr.ht/~huyngo/witchie
* Mailing list for discussion: https://lists.sr.ht/~huyngo/witchie
* Bugs/feature requests: https://todo.sr.ht/~huyngo/witchie

## Features

* Posting, replying, deleting statuses
* Support for media uploads, spoiler text, sensitive content
* Search by account or hash tag
* Following, muting and blocking accounts
* Simple switching between authenticated accounts

## Terminal User Interface

witchie includes a terminal user interface (TUI). Run it with `witchie tui`.

For now, the TUI is not maintained.

![TUI timeline](https://raw.githubusercontent.com/ihabunek/toot/master/docs/images/tui_list.png)

![compose post in TUI](https://raw.githubusercontent.com/ihabunek/toot/master/docs/images/tui_compose.png)

## License

Copyright 2017-2023 Ivan Habunek <ivan@habunek.com> and contributors.
Copyright 2023-2024 Ngô Ngọc Đức Huy <huyngo@disroot.org>

Licensed under [GPLv3](http://www.gnu.org/licenses/gpl-3.0.html).
