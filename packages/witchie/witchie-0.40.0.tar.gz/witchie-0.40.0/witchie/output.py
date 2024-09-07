# SPDX-FileCopyrightText: 2017-2023 Ivan Habunek et al <ivan@habunek.com>
# SPDX-FileCopyrightText: 2023-2024 Ngô Ngọc Đức Huy <huyngo@disroot.org>
#
# SPDX-License-Identifier: GPL-3.0-only

import os
import re
import shutil
import sys
import textwrap
from functools import lru_cache
from typing import Iterable, List

from wcwidth import wcswidth

from witchie import settings
from witchie.entities import Account, Instance, Notification, Poll, Status
from witchie.utils import html_to_paragraphs
from witchie.wcstring import trunc, wc_wrap

STYLES = {
    'reset': '\033[0m',
    'bold': '\033[1m',
    'dim': '\033[2m',
    'italic': '\033[3m',
    'underline': '\033[4m',
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
}

STYLE_TAG_PATTERN = re.compile(r"""
    (?<!\\)     # not preceeded by a backslash - allows escaping
    <           # literal
    (/)?        # optional closing - first group
    (.*?)       # style names - ungreedy - second group
    >           # literal
""", re.X)


def get_term_width():
    term_width = os.getenv('TERM_WIDTH')
    try:
        term_width = int(term_width)
    except Exception:
        terminal_size = shutil.get_terminal_size()
        term_width = terminal_size.columns
    return term_width


def colorize(message):
    """
    Replaces style tags in `message` with ANSI escape codes.

    Markup is inspired by HTML, but you can use multiple words pre tag, e.g.:

        <red bold>alert!</red bold> a thing happened

    Empty closing tag will reset all styes:

        <red bold>alert!</> a thing happened

    Styles can be nested:

        <red>red <underline>red and underline</underline> red</red>
    """

    def _codes(styles):
        for style in styles:
            yield STYLES.get(style, "")

    def _generator(message):
        # A list is used instead of a set because we want to keep style order
        # This allows nesting colors, e.g. "<blue>foo<red>bar</red>baz</blue>"
        position = 0
        active_styles = []

        for match in re.finditer(STYLE_TAG_PATTERN, message):
            is_closing = bool(match.group(1))
            styles = match.group(2).strip().split()

            start, end = match.span()
            # Replace backslash for escaped <
            yield message[position:start].replace("\\<", "<")

            if is_closing:
                yield STYLES["reset"]

                # Empty closing tag resets all styles
                if styles == []:
                    active_styles = []
                else:
                    active_styles = [s for s in active_styles if s not in styles]
                    yield from _codes(active_styles)
            else:
                active_styles = active_styles + styles
                yield from _codes(styles)

            position = end

        if position == 0:
            # Nothing matched, yield the original string
            yield message
        else:
            # Yield the remaining fragment
            yield message[position:]
            # Reset styles at the end to prevent leaking
            yield STYLES["reset"]

    return "".join(_generator(message)).replace('\\<', '<')


def strip_tags(message):
    return re.sub(STYLE_TAG_PATTERN, "", message)
    return message


@lru_cache(maxsize=None)
def use_ansi_color():
    """Returns True if ANSI color codes should be used."""

    # Windows doesn't support color unless ansicon is installed
    # See: http://adoxa.altervista.org/ansicon/
    if sys.platform == 'win32' and 'ANSICON' not in os.environ:
        return False

    # Don't show color if stdout is not a tty, e.g. if output is piped on
    if not sys.stdout.isatty():
        return False

    # Don't show color if explicitly specified in options
    if "--no-color" in sys.argv:
        return False

    # Check in settings
    color = settings.get_setting("common.color", bool)
    if color is not None:
        return color

    # Use color by default
    return True


def print_out(*args, **kwargs):
    if not settings.get_quiet():
        args = [colorize(a) if use_ansi_color() else strip_tags(a) for a in args]
        print(*args, **kwargs)


def print_err(*args, **kwargs):
    args = [f"<red>{a}</red>" for a in args]
    args = [colorize(a) if use_ansi_color() else strip_tags(a) for a in args]
    print(*args, file=sys.stderr, **kwargs)


def print_instance(instance: Instance):
    print_out(f"<green>{instance.title}</green>")
    print_out(f"<blue>{instance.uri}</blue>")
    print_out(f"running Mastodon API v{instance.version}")
    print_out()

    if instance.description:
        for paragraph in re.split(r"[\r\n]+", instance.description.strip()):
            paragraph = '\n'.join(html_to_paragraphs(paragraph))
            print_out(textwrap.fill(paragraph, width=get_term_width()))
            print_out()

    if instance.rules:
        print_out("Rules:")
        for ordinal, rule in enumerate(instance.rules):
            ordinal = f"{ordinal + 1}."
            lines = textwrap.wrap(rule.text, get_term_width() - len(ordinal))
            first = True
            for line in lines:
                if first:
                    print_out(f"{ordinal} {line}")
                    first = False
                else:
                    print_out(f"{' ' * len(ordinal)} {line}")
        print_out()

    contact = instance.contact_account
    if contact:
        print_out(f"Contact: {contact.display_name} @{contact.acct}")


def print_account(account: Account):
    print_out(("[BOT] " if account.bot else "")
              + f"<green>@{account.acct}</green> {account.display_name}")

    if account.note:
        print_out("")
        print_html(account.note)

    since = account.created_at.strftime('%Y-%m-%d')

    print_out("")
    print_out(f"ID: <green>{account.id}</green>")
    print_out(f"Since: <green>{since}</green>")
    print_out("")
    print_out(f"Followers: <yellow>{account.followers_count}</yellow>")
    print_out(f"Following: <yellow>{account.following_count}</yellow>")
    print_out(f"Statuses: <yellow>{account.statuses_count}</yellow>")

    if account.fields:
        for field in account.fields:
            name = field.name.title()
            print_out(f'\n<yellow>{name}</yellow>:')
            print_html(field.value)
            if field.verified_at:
                print_out("<green>✓ Verified</green>")

    print_out("")
    print_out(account.url)


HASHTAG_PATTERN = re.compile(r'(?<!\w)(#\w+)\b')
USERTAG_PATTERN = re.compile(r'(@[\w\.\-]+)\b')


def print_acct_list(accounts):
    for account in accounts:
        print_out(f"* <green>@{account['acct']}</green> {account['display_name']}")


def print_user_list(users):
    for user in users:
        print_out(f"* {user}")


def print_tag_list(tags):
    if tags:
        for tag in tags:
            print_out(f"* <green>#{tag['name']}\t</green>{tag['url']}")
    else:
        print_out("You're not following any hashtags.")


def print_lists(lists):
    headers = ["ID", "Title", "Replies"]
    data = [[lst["id"], lst["title"], lst.get("replies_policy", "")] for lst in lists]
    print_table(headers, data)


def print_table(headers: List[str], data: List[List[str]]):
    widths = [[len(cell) for cell in row] for row in data + [headers]]
    widths = [max(width) for width in zip(*widths)]

    def style(string, tag):
        return f"<{tag}>{string}</{tag}>" if tag else string

    def print_row(row, tag=None):
        for idx, cell in enumerate(row):
            width = widths[idx]
            print_out(style(cell.ljust(width), tag), end="")
            print_out("  ", end="")
        print_out()

    underlines = ["-" * width for width in widths]

    print_row(headers, "bold")
    print_row(underlines, "dim")

    for row in data:
        print_row(row)


def print_list_accounts(accounts):
    if accounts:
        print_out("Accounts in list</green>:\n")
        print_acct_list(accounts)
    else:
        print_out("This list has no accounts.")


def print_search_results(results):
    accounts = results['accounts']
    hashtags = results['hashtags']

    if accounts:
        print_out("\nAccounts:")
        print_acct_list(accounts)

    if hashtags:
        print_out("\nHashtags:")
        print_out(", ".join([f"<green>#{t['name']}</green>" for t in hashtags]))

    if not accounts and not hashtags:
        print_out("<yellow>Nothing found</yellow>")


def _remove_invisible_chars(word: str) -> str:
    """Strip a string off invisible characters that might mess up the terminal if it's windows."""
    if sys.platform == 'win32' or 'WSL' in os.uname().release:
        # Zero Width Space
        word = word.replace('\u200b', '')
        # Word Joiner
        word = word.replace('\u2060', '')
        word = word.replace('\u200c', '')
        word = word.replace('\u200d', '')
        word = word.replace('\u200e', '')
        # Right-To-Left Mark
        word = word.replace('\u200f', '')
    return word


def print_status(status: Status, width: int = get_term_width(), padding: int = 0):
    status_id = status.original.id
    in_reply_to_id = status.in_reply_to_id
    reblogged_by = status.account if status.reblog else None

    status = status.original

    time = status.created_at.strftime('%Y-%m-%d %H:%M %Z')
    username = "@" + status.account.acct
    spacing = width - wcswidth(username) - wcswidth(time) - 2

    display_name = _remove_invisible_chars(status.account.display_name)
    if display_name:
        spacing -= wcswidth(display_name) + 1

    if spacing <= 0:
        display_name = trunc(display_name, width - wcswidth(username) - wcswidth(time) - 3)

    paddings = "│" * padding

    print_out(
        paddings + (f"<green>{display_name}</green>" if display_name else ""),
        f"<blue>{username}</blue>",
        " " * spacing,
        f"<yellow>{time}</yellow>",
    )

    print_out(paddings)
    if status.spoiler_text:
        print_out(paddings + "<yellow>Subject</yellow>: ", end="")
        print_html(status.spoiler_text)
        print_out(paddings)
    print_html(status.content, width, padding)

    if status.media_attachments:
        print_out(f"{paddings}\n{paddings}Media:")
        for count, attachment in enumerate(status.media_attachments):
            url = attachment.url
            description = f'Description: {attachment.description}'
            print_out(f'{paddings}{count + 1}. <yellow>URL</yellow>: {url}')
            for i, line in enumerate(wc_wrap(description, width - padding)):
                if i == 0:
                    line = line.replace('Description', '<yellow>Description</yellow>')
                print_out(paddings + line)

    if status.quote_id:
        print_out(paddings)
        print_out(f'{paddings}<green>Quoting</green>: <yellow>{status.quote_id}')

    if status.poll:
        print_poll(status.poll)

    print_out(paddings)

    reacts = ('\n' + paddings).join([f'{react.count} × {react.name}'
                                     for react in status.emoji_reactions or []])
    if reacts:
        reacts = paddings + reacts
        print_out(paddings + (f"<yellow>Reacts:</yellow>\n{reacts}\n{paddings}"))

    print_out(
        paddings + f"ID <yellow>{status_id}</yellow> ",
        f"↲ In reply to <yellow>{in_reply_to_id}</yellow> " if in_reply_to_id else "",
        f"↻ <blue>@{reblogged_by.acct}</blue> boosted " if reblogged_by else "",
    )


def print_html(text, width=get_term_width(), padding=0):
    is_in_pre = False
    for line in html_to_paragraphs(text):
        if line == '<blockquote>':
            print_out("│" * padding + "┌<yellow>Quote</yellow>" + "─" * (width - 6))
            width -= 1
            padding += 1
        elif line == '</blockquote>':
            width += 1
            padding -= 1
            print_out("│" * padding + "└" + "─" * (width - 1))
        elif line == '<pre>':
            print_out("│" * padding + "┌<yellow>Code</yellow>" + "─" * (width - 5))
            width -= 1
            padding += 1
            is_in_pre = True
        elif line == '</pre>':
            width += 1
            padding -= 1
            print_out("│" * padding + "└" + "─" * (width - 1))
            is_in_pre = False
        elif line == '<refs>':
            is_in_pre = True
        elif is_in_pre:
            print_out("│" * padding + line)
        else:
            for subline in wc_wrap(line, width):
                print_out("│" * padding + subline)


def print_poll(poll: Poll):
    print_out()
    for idx, option in enumerate(poll.options):
        perc = (round(100 * option.votes_count / poll.votes_count)
                if poll.votes_count and option.votes_count is not None else 0)

        if poll.voted and poll.own_votes and idx in poll.own_votes:
            voted_for = " <yellow>✓</yellow>"
        else:
            voted_for = ""

        print_out(f'{option.title} - {perc}% {voted_for}')

    poll_footer = (f'Poll ({"multi-choice" if poll.multiple else "single-choice"})'
                   f' · {poll.votes_count} votes')

    if poll.expired:
        poll_footer += " · Closed"

    if poll.expires_at:
        expires_at = poll.expires_at.strftime("%Y-%m-%d %H:%M")
        poll_footer += f" · Closes on {expires_at}"

    print_out()
    print_out(poll_footer)


def print_timeline(items: Iterable[Status], padding=0):
    width = get_term_width()
    width -= padding
    if padding:
        first_paddings = "│" * (padding - 1) + "┌"
        paddings = "│" * (padding - 1) + "├"
    else:
        first_paddings = ""
        paddings = ""
    print_out(first_paddings + "─" * width)
    for item in items:
        print_status(item, width - padding, padding)
        print_out(paddings + "─" * width)


def print_tree(tree, depth=0):
    """Print a thread tree"""
    if depth >= 20:
        print_out("└" + "┴" * 17 + "(Thread goes too deep)")
        return
    if depth:
        paddings = "│" * (depth - 1) + "└"
    else:
        paddings = ""
    print_status(tree['status'], get_term_width() - depth, padding=depth)
    print_out(paddings + "─" * (get_term_width() - depth))
    for reply in tree['replies']:
        print_tree(reply, depth + 1)


notification_msgs = {
    "follow": "{account} now follows you",
    "mention": "{account} mentioned you in",
    "reblog": "{account} reblogged your status",
    "favourite": "{account} favourited your status",
    "favourite": "{account} favourited your status",
    "pleroma:emoji_reaction": "{account} reacted on your status: {react}",
}


def print_notification(notification: Notification):
    width = get_term_width()
    display_name = _remove_invisible_chars(notification.account.display_name)
    account = f"{display_name} @{notification.account.acct}"
    msg = notification_msgs.get(notification.type)
    if msg is None:
        return

    print_out("─" * width)
    if notification.type == "pleroma:emoji_reaction":
        react = notification.emoji
        print_out(msg.format(account=account, react=react))
    else:
        print_out(msg.format(account=account))
    if notification.status:
        print_status(notification.status, width)


def print_notifications(notifications: List[Notification]):
    width = get_term_width()
    for notification in notifications:
        print_notification(notification)
    print_out("─" * width)
