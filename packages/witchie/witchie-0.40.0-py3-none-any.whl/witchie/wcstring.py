# SPDX-FileCopyrightText: 2017-2023 Ivan Habunek et al <ivan@habunek.com>
# SPDX-FileCopyrightText: 2023-2024 Ngô Ngọc Đức Huy <huyngo@disroot.org>
#
# SPDX-License-Identifier: GPL-3.0-only

"""
Utilities for dealing with string containing wide characters.
"""

import re
from typing import Generator, List

from wcwidth import wcswidth, wcwidth

STYLE_TAG_PATTERN = re.compile(r"""
    (
    (?<!\\)     # not preceeded by a backslash - allows escaping
    <           # literal
    (/)?        # optional closing - first group
    (.*?)       # style names - ungreedy - second group
    >)          # literal
""", re.X)

STYLES = {'reset', 'bold', 'dim', 'italic', 'underline',
          'red', 'green', 'yellow', 'blue', 'magenta', 'cyan'}


def _wc_hard_wrap(line: str, length: int) -> Generator[str, None, None]:
    """
    Wrap text to length characters, breaking when target length is reached,
    taking into account character width.

    Used to wrap lines which cannot be wrapped on whitespace.
    """
    chars = []
    chars_len = 0
    for char in line:
        char_len = wcwidth(char)
        if chars_len + char_len > length:
            yield "".join(chars)
            chars: List[str] = []
            chars_len = 0

        chars.append(char)
        chars_len += char_len

    if chars:
        yield "".join(chars)


def wc_wrap(text: str, length: int) -> Generator[str, None, None]:
    """
    Wrap text to given length, breaking on whitespace and taking into account
    character width.

    Meant for use on a single line or paragraph. Will destroy spacing between
    words and paragraphs and any indentation.
    """
    line_words: List[str] = []
    line_len = 0

    words = re.split(r"\s+", text.strip())
    stack = []  # stack to ensure enclosure of style tags
    temp_length = length
    for word in words:
        word_len = wcswidth(word)
        matches = re.findall(STYLE_TAG_PATTERN, word)
        last_popped = ''
        for match in matches:
            last_popped = ''
            full, end, name = match
            if name in STYLES:
                temp_length += len(full)
                if end != '/':
                    stack.append(name)
                elif len(stack) and name == stack[-1]:
                    last_popped = stack.pop()

        should_join = False
        if line_words and line_len + word_len > temp_length:
            if last_popped != '':
                stack.append(last_popped)
            line = " ".join(line_words)
            for style in reversed(stack):
                line += '</' + style + '>'
                line_len += len(style) + 3
                temp_length += len(style) + 3
            if line_len <= temp_length:
                yield line
            else:
                yield from _wc_hard_wrap(line, temp_length)

            line_len = 0
            line_words = []
            temp_length = length

            styles = ''
            for style in stack:
                styles += '<' + style + '>'
            temp_length += len(styles)
            line_len += len(styles)
            line_words = [styles]
            should_join = True
            if last_popped != '':
                stack.pop()

        if should_join:
            line_words[0] += word
        else:
            line_words.append(word)
        line_len += word_len + 1  # add 1 to account for space between words

    if line_words:
        line = " ".join(line_words)
        if line_len <= temp_length:
            yield line
        else:
            yield from _wc_hard_wrap(line, temp_length)


def trunc(text: str, length: int) -> str:
    """
    Truncates text to given length, taking into account wide characters.

    If truncated, the last char is replaced by an ellipsis.
    """
    if length < 1:
        raise ValueError("length should be 1 or larger")

    # Remove whitespace first so no unnecessary truncation is done.
    text = text.strip()
    text_length = wcswidth(text)

    if text_length <= length:
        return text

    # We cannot just remove n characters from the end since we don't know how
    # wide these characters are and how it will affect text length.
    # Use wcwidth to determine how many characters need to be truncated.
    chars_to_truncate = 0
    trunc_length = 0
    for char in reversed(text):
        chars_to_truncate += 1
        trunc_length += wcwidth(char)
        if text_length - trunc_length <= length:
            break

    # Additional char to make room for ellipsis
    n = chars_to_truncate + 1
    return text[:-n].strip() + '…'


def pad(text: str, length: int) -> str:
    """Pads text to given length, taking into account wide characters."""
    text_length = wcswidth(text)

    if text_length < length:
        return text + ' ' * (length - text_length)

    return text


def fit_text(text: str, length: int) -> str:
    """Makes text fit the given length by padding or truncating it."""
    text_length = wcswidth(text)

    if text_length > length:
        return trunc(text, length)

    if text_length < length:
        return pad(text, length)

    return text
