# SPDX-FileCopyrightText: 2017-2023 Ivan Habunek et al <ivan@habunek.com>
# SPDX-FileCopyrightText: 2023-2024 Ngô Ngọc Đức Huy <huyngo@disroot.org>
#
# SPDX-License-Identifier: GPL-3.0-only

import os
import socket
import subprocess
import tempfile
from collections import deque
from html.parser import HTMLParser
from typing import Dict
from urllib.parse import quote, unquote, urlencode, urlparse

from witchie.exceptions import ConsoleError


def str_bool(b):
    """Convert boolean to string, in the way expected by the API."""
    return "true" if b else "false"


def str_bool_nullable(b):
    """Similar to str_bool, but leave None as None"""
    return None if b is None else str_bool(b)


class List:
    def __init__(self, list_type):
        self.type = list_type
        self.count = 0


class HTMLTextParser(HTMLParser):
    """Parse HTML to text"""
    def __init__(self):
        super().__init__()

        # for state checks
        self.is_in_a = False
        self.current_a = ''
        self.list_stack = deque()
        self.list_level = -1
        self.is_in_pre = False

        # for output
        self.links = []
        self.image_links = []
        self.lines = []
        self.line = ''
        self.pre_lines = []
        self.pre_line = ''

    def commit(self):
        """Commit any dangling lines."""
        if self.line != '':
            self.lines.append(self.line)
            self.line = ''

    def handle_starttag(self, tag, attrs):
        if tag in ('img', 'br', 'hr', 'wbr'):
            # just in case they're not closed
            return self.handle_startendtag(tag, attrs)
        attrs = dict(attrs)
        if self.is_in_pre:
            self.pre_line += '\\<' + tag + '>'
        elif tag == 'p':
            self.commit()
        elif tag == 'a':
            self.line += '<cyan>'
            self.is_in_a = True
            has_href = 'href' in attrs
            is_mention = 'mention' in attrs.get('class', [])
            is_tag = ('hashtag' in attrs.get('class', [])
                      or 'tag' in attrs.get('rel', []))
            if all([has_href, not is_mention, not is_tag]):
                self.links.append(attrs['href'])
            else:
                self.links.append(None)
        elif tag in ('ul', 'ol'):
            self.commit()
            self.list_stack.append(List(tag))
            self.list_level += 1
        elif tag == 'li':
            current_list = self.list_stack[-1]
            if self.list_level > 0:
                self.line += '<dim>' + '..' * self.list_level + '</dim>'
            if current_list.type == 'ul':
                self.line += '- '
            else:
                current_list.count += 1
                self.line += str(current_list.count) + '. '
        elif tag in ('i', 'em'):
            self.line += '<italic>'
        elif tag in ('b', 'strong'):
            self.line += '<bold>'
        elif tag in ('s', 'del'):
            self.line += '<strikethrough>'
        elif tag == 'u':
            self.line += '<underline>'
        elif tag in ('blockquote', 'pre'):
            self.commit()
            self.lines.append(f'<{tag}>')
            if tag == 'pre':
                self.is_in_pre = True
        elif tag == 'code':
            self.line += '<green>'

    def handle_endtag(self, tag):
        if tag != 'pre' and self.is_in_pre:
            self.pre_line += '\\</' + tag + '>'
        elif tag == 'p':
            self.commit()
            self.lines.append('')
        elif tag == 'a':
            current_link = self.links[-1]
            if current_link is None:
                self.links.pop()
            elif current_link == self.current_a:
                if len(current_link) <= 40:
                    self.links.pop()
                else:
                    self.current_a = current_link[:40] + f'…[{len(self.links)}]'
                    self.current_a = self.current_a.removeprefix("https://")
                    self.current_a = self.current_a.removeprefix("http://")
            else:
                ref = f'[{len(self.links)}]'
                self.current_a += ref
            self.line += self.current_a
            self.current_a = ''
            self.line += '</cyan>'
            self.is_in_a = False
        elif tag in ('ul', 'ol'):
            self.list_stack.pop()
            self.list_level -= 1
        elif tag == 'li':
            self.commit()
        elif tag in ('i', 'em'):
            if self.is_in_a:
                self.current_a += '</italic>'
            else:
                self.line += '</italic>'
        elif tag in ('b', 'strong'):
            if self.is_in_a:
                self.current_a += '</bold>'
            else:
                self.line += '</bold>'
        elif tag in ('s', 'del'):
            if self.is_in_a:
                self.current_a += '</strikethrough>'
            else:
                self.line += '</strikethrough>'
        elif tag == 'u':
            if self.is_in_a:
                self.current_a += '</underline>'
            else:
                self.line += '</underline>'
        elif tag in ('blockquote', 'pre'):
            if tag == 'pre':
                self.is_in_pre = False
                if self.pre_line != '':
                    self.pre_lines.append(self.pre_line)
                    self.pre_line = ''
                self.lines.extend(self.pre_lines)
                self.pre_lines = []
            self.commit()
            self.lines.append(f'</{tag}>')
        elif tag == 'code':
            self.line += '</green>'

    def handle_data(self, data):
        data = data.replace('<', '\\<')
        if self.is_in_pre:
            for c in data:
                if c == '\n':
                    self.pre_lines.append(self.pre_line)
                    self.pre_line = ''
                else:
                    self.pre_line += c
        elif self.is_in_a:
            self.current_a += data
        else:
            self.line += data

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.commit()
        if tag == 'hr':
            self.commit()
            self.lines.append('─────────────────────')
        if tag == 'img':
            attrs = dict(attrs)
            src = attrs.get('src')
            alt = 'image: ' + attrs.get('alt')
            self.image_links.append(src)
            self.line += f'<cyan>{alt}[{len(self.image_links)}]</cyan>'


def html_to_paragraphs(html):
    """Parse html properly and output texts with hard linebreaks.

    - bold (b/strong), italic (i/em), strikethrough (s/del), underline (u) are presented as such
    - link (a) is presented as underlined blue and numbered reference, which is linked at bottom
        e.g. This is an example link[1]

        [1]: https://example.com
    - blockquotes and code blocks are fenced with note
    - inline images are presented as [img#n "alt text"] and linked at bottom
    - ul lists are presented with hyphen-bullet
    - ol lists are presented with numbers
    """
    parser = HTMLTextParser()
    parser.feed(html)
    parser.commit()

    paragraphs = parser.lines
    while len(paragraphs) > 0 and paragraphs[-1] == '':
        paragraphs.pop()
    links = parser.links
    images = parser.image_links
    if len(images) or len(links):
        paragraphs.append('')
        paragraphs.append('<refs>')
    for i, link in enumerate(links):
        paragraphs.append(f'[{i + 1}]: {link}')
    for i, link in enumerate(images):
        paragraphs.append(f'[img#{i + 1}]: {link}')
    return paragraphs


def format_content(content):
    """Given a Status contents in HTML, converts it into lines of plain text.

    Returns a generator yielding lines of content.
    """

    paragraphs = html_to_paragraphs(content)

    first = True

    for paragraph in paragraphs:
        if not first:
            yield ""

        for line in paragraph:
            yield line

        first = False


def domain_exists(name):
    try:
        socket.gethostbyname(name)
        return True
    except OSError:
        return False


def assert_domain_exists(domain):
    if not domain_exists(domain):
        raise ConsoleError("Domain {} not found".format(domain))


EOF_KEY = "Ctrl-Z" if os.name == 'nt' else "Ctrl-D"


def multiline_input():
    """Lets user input multiple lines of text, terminated by EOF."""
    lines = []
    while True:
        try:
            lines.append(input())
        except EOFError:
            break

    return "\n".join(lines).strip()


EDITOR_DIVIDER = "------------------------ >8 ------------------------"

EDITOR_INPUT_INSTRUCTIONS = f"""
{EDITOR_DIVIDER}
Do not modify or remove the line above.
Enter your post above it.
Everything below it will be ignored.
"""


def editor_input(editor: str, initial_text: str, mentions: list[str]):
    """Lets user input text using an editor."""
    tmp_path = _tmp_status_path()
    mention_text = ' '.join(mentions) + ' \n'
    initial_text = mention_text + (initial_text or "") + EDITOR_INPUT_INSTRUCTIONS

    if not _use_existing_tmp_file(tmp_path):
        with open(tmp_path, "w") as f:
            f.write(initial_text)
            f.flush()

    subprocess.run([editor, tmp_path])

    with open(tmp_path) as f:
        return f.read().split(EDITOR_DIVIDER)[0].strip()


def read_char(values, default):
    values = [v.lower() for v in values]

    while True:
        value = input().lower()
        if value == "":
            return default
        if value in values:
            return value


def delete_tmp_status_file():
    try:
        os.unlink(_tmp_status_path())
    except FileNotFoundError:
        pass


def _tmp_status_path() -> str:
    tmp_dir = tempfile.gettempdir()
    return f"{tmp_dir}/.status.post"


def _use_existing_tmp_file(tmp_path) -> bool:
    from witchie.output import print_out

    if os.path.exists(tmp_path):
        print_out(f"<cyan>Found a draft status at: {tmp_path}</cyan>")
        print_out("<cyan>[O]pen (default) or [D]elete?</cyan> ", end="")
        char = read_char(["o", "d"], "o")
        return char == "o"

    return False


def drop_empty_values(data: Dict) -> Dict:
    """Remove keys whose values are null"""
    return {k: v for k, v in data.items() if v is not None}


def args_get_instance(instance, scheme, default=None):
    if not instance:
        return default

    if scheme == "http":
        _warn_scheme_deprecated()

    if instance.startswith("http"):
        return instance.rstrip("/")
    else:
        return f"{scheme}://{instance}"


def _warn_scheme_deprecated():
    from witchie.output import print_err

    print_err("\n".join([
        "--disable-https flag is deprecated and will be removed.",
        "Please specify the instance as URL instead.",
        "e.g. instead of writing:",
        "  witchie instance unsafehost.com --disable-https",
        "instead write:",
        "  witchie instance http://unsafehost.com\n"
    ]))


def urlencode_url(url):
    parsed_url = urlparse(url)

    # unencode before encoding, to prevent double-urlencoding
    encoded_path = quote(unquote(parsed_url.path), safe="-._~()'!*:@,;+&=/")
    encoded_query = urlencode({k: quote(unquote(v), safe="-._~()'!*:@,;?/")
                               for k, v in parsed_url.params})
    encoded_url = parsed_url._replace(path=encoded_path, params=encoded_query).geturl()

    return encoded_url
