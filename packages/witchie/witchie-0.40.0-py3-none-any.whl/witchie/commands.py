# SPDX-FileCopyrightText: 2017-2023 Ivan Habunek et al <ivan@habunek.com>
# SPDX-FileCopyrightText: 2023-2024 Ngô Ngọc Đức Huy <huyngo@disroot.org>
#
# SPDX-License-Identifier: GPL-3.0-only

import json
import platform
import sys
from datetime import datetime, timedelta, timezone
from itertools import chain
from time import sleep, time

from witchie import __version__, api, config
from witchie.auth import (create_app_interactive, login_browser_interactive,
                          login_interactive)
from witchie.cache import cache_status, get_cached_status
from witchie.entities import Account, Instance, Notification, Poll, Status, from_dict
from witchie.exceptions import ApiError, ConsoleError
from witchie.output import (print_account, print_acct_list, print_instance,
                            print_list_accounts, print_lists,
                            print_notifications, print_out, print_poll,
                            print_search_results, print_status, print_table,
                            print_tag_list, print_timeline, print_tree,
                            print_user_list)
from witchie.utils import (EOF_KEY, args_get_instance, delete_tmp_status_file,
                           editor_input, multiline_input)
from witchie.utils.datetime import parse_datetime


def get_timeline_generator(app, user, args):
    if len([arg for arg in [args.tag, args.list, args.public, args.account] if arg]) > 1:
        raise ConsoleError("Only one of --public, --bubble, --tag, --account,"
                           " or --list can be used at one time.")

    if args.local and not (args.public or args.tag or args.bubble):
        raise ConsoleError("The --local option is only valid alongside --public or --tag.")

    if args.instance and not (args.public or args.tag or args.bubble):
        raise ConsoleError("The --instance option is only valid alongside --public or --tag.")

    common_args = {
        'limit': args.count,
        'min_id': args.from_id,
        'max_id': args.up_to_id,
        'since_id': args.since_id,
    }
    common_args = {k: v for k, v in common_args.items() if v is not None}
    if user.optimized and not args.once:
        # prefetch maximum number of posts
        common_args['limit'] = 40

    if args.bubble:
        return api.bubble_timeline_generator(app, user, public=args.public, **common_args)
    elif args.public:
        if args.instance:
            return api.anon_public_timeline_generator(args.instance,
                                                      local=args.local,
                                                      **common_args)
        else:
            return api.public_timeline_generator(app, user, local=args.local, **common_args)
    elif args.tag:
        if args.instance:
            return api.anon_tag_timeline_generator(args.instance, args.tag, **common_args)
        else:
            return api.tag_timeline_generator(app, user, args.tag, local=args.local, **common_args)
    elif args.account:
        return api.account_timeline_generator(app, user, args.account, **common_args)
    elif args.list:
        return api.timeline_list_generator(app, user, args.list, **common_args)
    else:
        return api.home_timeline_generator(app, user, **common_args)


def _get_items_from_generator(generator):
    try:
        items = next(generator)
    except StopIteration:
        return []
    return items


def timeline(app, user, args, generator=None):
    if not generator:
        generator = get_timeline_generator(app, user, args)

    prefetch = user.optimized and not args.once
    items = []
    _items = []
    items_to_print = []
    while True:
        if prefetch:
            if len(items) < args.count:
                _items = _get_items_from_generator(generator)
                if _items:
                    items.extend(_items)
            if len(items) <= args.count:
                items_to_print = items
                items = []
            else:
                items_to_print = items[:args.count]
                items = items[args.count:]
        else:
            items = _get_items_from_generator(generator)
            items_to_print = items

        if args.reverse:
            items_to_print = reversed(items_to_print)
        statuses = [from_dict(Status, item, user.optimized) for item in items_to_print]
        print_timeline(statuses)

        if args.once or not sys.stdout.isatty():
            break

        try:
            char = input("\nContinue? [Y/n] ")
            if char.lower() == "n":
                break
        except Exception:
            break

        if prefetch and len(items) < args.count:
            _items = _get_items_from_generator(generator)
            if _items:
                items.extend(_items)

        if len(items) == 0:
            print("That's all folks.")
            return


def status(app, user, args):
    if args.json:
        response = api.fetch_status(app, user, args.status_id)
        print(response.text)
    else:
        response_json = get_cached_status(args.status_id)
        use_cache = False
        if response_json is None:
            use_cache = user.optimized
            response = api.fetch_status(app, user, args.status_id)
            response_json = response.json()
        status = from_dict(Status, response_json, use_cache)
        print_status(status)


def _get_replies_tree(status_id: int, descendants: list, cache: bool):
    tree = []
    for d in descendants:
        if d['in_reply_to_id'] == status_id:
            tree.append({
                'status': from_dict(Status, d, cache),
                'replies': _get_replies_tree(d['id'], descendants, cache)
            })
    return tree


def thread(app, user, args):
    context_response = api.context(app, user, args.status_id)

    if args.json:
        print(context_response.text)
    else:
        post = get_cached_status(args.status_id)
        if post is None:
            post = api.fetch_status(app, user, args.status_id).json()
            cache_status(post)
        context = context_response.json()

        if args.tree:
            reply_to = post["in_reply_to_id"]
            ancestors_map = {status['id']: status for status in context["ancestors"]}
            ancestors = []
            while reply_to:
                parent = ancestors_map.get(reply_to)
                if parent is None:
                    print('Full thread not available beyond this point')
                    break
                ancestors.append(parent)
                reply_to = ancestors_map[reply_to]['in_reply_to_id']
            ancestors = reversed(ancestors)

            descendants = {
                'status': from_dict(Status, post, user.optimized),
                'replies': _get_replies_tree(args.status_id, context["descendants"],
                                             cache=user.optimized)
            }
            print_timeline([from_dict(Status, s, user.optimized) for s in ancestors], padding=1)

            print_tree(descendants)
        else:
            statuses = chain(context["ancestors"], [post], context["descendants"])
            print_timeline(from_dict(Status, s, user.optimized) for s in statuses)


def configure(app, user, args):
    if args.optimize is None:
        return
    user = user._replace(optimized=args.optimize)
    config.save_user(user, False)


def post(app, user, args):
    if args.editor and not sys.stdin.isatty():
        raise ConsoleError("Cannot run editor if not in tty.")

    mentions = []
    spoiler_text = args.spoiler_text
    parent_id = args.reply_to
    if parent_id:
        parent_json = get_cached_status(parent_id)
        use_cache = False
        if parent_json is None:
            use_cache = user.optimized
            parent = api.fetch_status(app, user, parent_id)
            parent_json = parent.json()
        parent = from_dict(Status, parent_json, use_cache)
        if args.include_mentions:
            own = '@' + user.username
            reply_to_mention = '@' + parent.account.acct
            if reply_to_mention != own:
                mentions.append(reply_to_mention)
            for mention in parent.mentions:
                mention = '@' + mention.acct
                if mention not in mentions and mention != own:
                    mentions.append(mention)

        if parent.spoiler_text and not spoiler_text:
            spoiler_text = parent.spoiler_text
            if not spoiler_text.startswith('re:'):
                spoiler_text = 're: ' + spoiler_text

    media_ids = _upload_media(app, user, args)
    status_text = _get_status_text(args.text, args.editor, args.media, mentions)
    scheduled_at = _get_scheduled_at(args.scheduled_at, args.scheduled_in)

    if not status_text and not media_ids:
        raise ConsoleError("You must specify either text or media to post.")

    response = api.post_status(
        app, user, status_text,
        visibility=args.visibility,
        media_ids=media_ids,
        sensitive=args.sensitive,
        spoiler_text=spoiler_text,
        in_reply_to_id=args.reply_to,
        language=args.language,
        scheduled_at=scheduled_at,
        content_type=args.content_type,
        expires_in=args.expires_in,
        poll_options=args.poll_option,
        poll_expires_in=args.poll_expires_in,
        poll_multiple=args.poll_multiple,
        poll_hide_totals=args.poll_hide_totals,
    )

    if args.json:
        print(response.text)
    else:
        status = response.json()
        if user.optimized:
            cache_status(status)
        if "scheduled_at" in status:
            scheduled_at = parse_datetime(status["scheduled_at"])
            scheduled_at = datetime.strftime(scheduled_at, "%Y-%m-%d %H:%M:%S%z")
            print_out(f"Post scheduled for: <green>{scheduled_at}</green>")
        else:
            print_out(f"Post posted: <green>{status['url']}")
        try:
            expires_at = status["pleroma"]["expires_at"]
        except KeyError:
            pass
        else:
            if expires_at is not None:
                dt = datetime.fromisoformat(expires_at).astimezone()
                print_out(f"Post will be deleted at: {dt.strftime('%c')}")

    delete_tmp_status_file()


def _get_status_text(text, editor, media, mentions=[]):
    isatty = sys.stdin.isatty()

    if not text and not isatty:
        text = sys.stdin.read().rstrip()

    if isatty:
        if editor:
            text = editor_input(editor, text, mentions)
        elif not text and not media:
            print_out("Write or paste your post."
                      "Press <yellow>{}</yellow> to post it.".format(EOF_KEY))
            if len(mentions) > 0:
                print_out("Other people in thread will be automatically prepended.")
            text = multiline_input()
            text = ' '.join(mentions) + ' ' + text

    return text


def _get_scheduled_at(scheduled_at, scheduled_in):
    if scheduled_at:
        return scheduled_at

    if scheduled_in:
        scheduled_at = datetime.now(timezone.utc) + timedelta(seconds=scheduled_in)
        return scheduled_at.replace(microsecond=0).isoformat()

    return None


def _upload_media(app, user, args):
    # Match media to corresponding description and thumbnail
    media = args.media or []
    descriptions = args.description or []
    thumbnails = args.thumbnail or []
    uploaded_media = []

    for idx, file in enumerate(media):
        description = descriptions[idx].strip() if idx < len(descriptions) else None
        thumbnail = thumbnails[idx] if idx < len(thumbnails) else None
        result = _do_upload(app, user, file, description, thumbnail)
        uploaded_media.append(result)

    _wait_until_all_processed(app, user, uploaded_media)

    return [m["id"] for m in uploaded_media]


def _wait_until_all_processed(app, user, uploaded_media):
    """
    Media is uploaded asynchronously, and cannot be attached until the server
    has finished processing it. This function waits for that to happen.

    Once media is processed, it will have the URL populated.
    """
    if all(m["url"] for m in uploaded_media):
        return

    # Timeout after waiting 1 minute
    start_time = time()
    timeout = 60

    print_out("<dim>Waiting for media to finish processing...</dim>")
    for media in uploaded_media:
        _wait_until_processed(app, user, media, start_time, timeout)


def _wait_until_processed(app, user, media, start_time, timeout):
    if media["url"]:
        return

    media = api.get_media(app, user, media["id"])
    while not media["url"]:
        sleep(1)
        if time() > start_time + timeout:
            raise ConsoleError(f"Media not processed by server after {timeout} seconds. Aborting.")
        media = api.get_media(app, user, media["id"])


def delete(app, user, args):
    response = api.delete_status(app, user, args.status_id)
    if args.json:
        print(response.text)
    else:
        print_out("<green>✓ Status deleted</green>")


def favourite(app, user, args):
    response = api.favourite(app, user, args.status_id)
    if args.json:
        print(response.text)
    else:
        print_out("<green>✓ Status favourited</green>")


def unfavourite(app, user, args):
    response = api.unfavourite(app, user, args.status_id)
    if args.json:
        print(response.text)
    else:
        print_out("<green>✓ Status unfavourited</green>")


def reblog(app, user, args):
    response = api.reblog(app, user, args.status_id, visibility=args.visibility)
    if args.json:
        print(response.text)
    else:
        print_out("<green>✓ Status reblogged</green>")


def unreblog(app, user, args):
    response = api.unreblog(app, user, args.status_id)
    if args.json:
        print(response.text)
    else:
        print_out("<green>✓ Status unreblogged</green>")


def pin(app, user, args):
    response = api.pin(app, user, args.status_id)
    if args.json:
        print(response.text)
    else:
        print_out("<green>✓ Status pinned</green>")


def unpin(app, user, args):
    response = api.unpin(app, user, args.status_id)
    if args.json:
        print(response.text)
    else:
        print_out("<green>✓ Status unpinned</green>")


def bookmark(app, user, args):
    response = api.bookmark(app, user, args.status_id)
    if args.json:
        print(response.text)
    else:
        print_out("<green>✓ Status bookmarked</green>")


def unbookmark(app, user, args):
    response = api.unbookmark(app, user, args.status_id)
    if args.json:
        print(response.text)
    else:
        print_out("<green>✓ Status unbookmarked</green>")


def react(app, user, args):
    response = api.react(app, user, args.status_id, args.emoji)
    if args.json:
        print(response.text)
    else:
        if response.status_code == 200:
            print_out(f"<green>✓ Reacted:</green> {args.emoji}")
        else:
            print_out("<red>Emoji invalid</red>")
        status = from_dict(Status, response.json(), user.optimized)
        print_status(status)


def unreact(app, user, args):
    response = api.unreact(app, user, args.status_id, args.emoji)
    if args.json:
        print(response.text)
    else:
        print_out(f"<green>✓ Unreacted:</green> {args.emoji}")
        status = from_dict(Status, response.json(), user.optimized)
        print_status(status)


def emojis(app, user, args):
    response = api.list_emoji(app, user)
    if args.json:
        print(response.text)
    else:
        emoji_packs = {}
        for emoji, data in response.json().items():
            if args.pack:
                is_in_pack = False
                for tag in data['tags']:
                    if tag.lstrip('pack:') == args.pack:
                        is_in_pack = True
                        break
                if not is_in_pack:
                    continue
            for tag in data['tags']:
                pack = tag.removeprefix('pack:')
                if pack not in emoji_packs:
                    emoji_packs[pack] = {}
                emoji_packs[pack][emoji] = data['image_url']
        for pack, emojis in emoji_packs.items():
            print_out('pack:', pack)
            for emoji, url in emojis.items():
                print_out(f'\t{emoji}: {url}')


def bookmarks(app, user, args):
    timeline(app, user, args, api.bookmark_timeline_generator(app, user, limit=args.count))


def reblogged_by(app, user, args):
    response = api.reblogged_by(app, user, args.status_id)

    if args.json:
        print(response.text)
    else:
        headers = ["Account", "Display name"]
        rows = [[a["acct"], a["display_name"]] for a in response.json()]
        print_table(headers, rows)


def auth(app, user, args):
    config_data = config.load_config()

    if not config_data["users"]:
        print_out("You are not logged in to any accounts")
        return

    active_user = config_data["active_user"]

    print_out("Authenticated accounts:")
    for uid, u in config_data["users"].items():
        active_label = "ACTIVE" if active_user == uid else ""
        print_out("* <green>{}</green> <yellow>{}</yellow>".format(uid, active_label))

    path = config.get_config_file_path()
    print_out("\nAuth tokens are stored in: <blue>{}</blue>".format(path))


def env(app, user, args):
    print_out(f"witchie {__version__}")
    print_out(f"Python {sys.version}")
    print_out(platform.platform())


def update_account(app, user, args):
    options = [
        args.avatar,
        args.bot,
        args.discoverable,
        args.display_name,
        args.header,
        args.language,
        args.locked,
        args.note,
        args.privacy,
        args.sensitive,
    ]

    if all(option is None for option in options):
        raise ConsoleError("Please specify at least one option to update the account")

    response = api.update_account(
        app,
        user,
        avatar=args.avatar,
        bot=args.bot,
        discoverable=args.discoverable,
        display_name=args.display_name,
        header=args.header,
        language=args.language,
        locked=args.locked,
        note=args.note,
        privacy=args.privacy,
        sensitive=args.sensitive,
    )

    if args.json:
        print(response.text)
    else:
        print_out("<green>✓ Account updated</green>")


def login_cli(app, user, args):
    base_url = args_get_instance(args.instance, args.scheme)
    app = create_app_interactive(base_url)
    login_interactive(app, args.email)

    print_out()
    print_out("<green>✓ Successfully logged in.</green>")


def login(app, user, args):
    base_url = args_get_instance(args.instance, args.scheme)
    app = create_app_interactive(base_url)
    login_browser_interactive(app)

    print_out()
    print_out("<green>✓ Successfully logged in.</green>")


def logout(app, user, args):
    user = config.load_user(args.account, throw=True)
    config.delete_user(user)
    print_out("<green>✓ User {} logged out</green>".format(config.user_id(user)))


def activate(app, user, args):
    if not args.account:
        print_out("Specify one of the following user accounts to activate:\n")
        print_user_list(config.get_user_list())
        return

    user = config.load_user(args.account, throw=True)
    config.activate_user(user)
    print_out("<green>✓ User {} active</green>".format(config.user_id(user)))


def upload(app, user, args):
    response = _do_upload(app, user, args.file, args.description, None)

    msg = "Successfully uploaded media ID <yellow>{}</yellow>, type '<yellow>{}</yellow>'"

    print_out()
    print_out(msg.format(response['id'], response['type']))
    print_out("URL: <green>{}</green>".format(response['url']))
    print_out("Preview URL:  <green>{}</green>".format(response['preview_url']))


def search(app, user, args):
    response = api.search(app, user, args.query, args.resolve)
    if args.json:
        print(response.text)
    else:
        print_search_results(response.json())


def _do_upload(app, user, file, description, thumbnail):
    print_out("Uploading media: <green>{}</green>".format(file.name))
    return api.upload_media(app, user, file, description=description, thumbnail=thumbnail)


def follow(app, user, args):
    account = api.find_account(app, user, args.account)
    response = api.follow(app, user, account["id"])
    if args.json:
        print(response.text)
    else:
        print_out(f"<green>✓ You are now following {args.account}</green>")


def unfollow(app, user, args):
    account = api.find_account(app, user, args.account)
    response = api.unfollow(app, user, account["id"])
    if args.json:
        print(response.text)
    else:
        print_out(f"<green>✓ You are no longer following {args.account}</green>")


def following(app, user, args):
    account = args.account or user.username
    account = api.find_account(app, user, account)
    accounts = api.following(app, user, account["id"])
    if args.json:
        print(json.dumps(accounts))
    else:
        print_acct_list(accounts)


def followers(app, user, args):
    account = args.account or user.username
    account = api.find_account(app, user, account)
    accounts = api.followers(app, user, account["id"])
    if args.json:
        print(json.dumps(accounts))
    else:
        print_acct_list(accounts)


def tags_follow(app, user, args):
    tn = args.tag_name if not args.tag_name.startswith("#") else args.tag_name[1:]
    api.follow_tag(app, user, tn)
    print_out("<green>✓ You are now following #{}</green>".format(tn))


def tags_unfollow(app, user, args):
    tn = args.tag_name if not args.tag_name.startswith("#") else args.tag_name[1:]
    api.unfollow_tag(app, user, tn)
    print_out("<green>✓ You are no longer following #{}</green>".format(tn))


def tags_followed(app, user, args):
    response = api.followed_tags(app, user)
    print_tag_list(response)


def lists(app, user, args):
    lists = api.get_lists(app, user)

    if lists:
        print_lists(lists)
    else:
        print_out("You have no lists defined.")


def list_accounts(app, user, args):
    list_id = _get_list_id(app, user, args)
    response = api.get_list_accounts(app, user, list_id)
    print_list_accounts(response)


def list_create(app, user, args):
    api.create_list(app, user, title=args.title, replies_policy=args.replies_policy)
    print_out(f"<green>✓ List \"{args.title}\" created.</green>")


def list_delete(app, user, args):
    list_id = _get_list_id(app, user, args)
    api.delete_list(app, user, list_id)
    print_out(f"<green>✓ List \"{args.title if args.title else args.id}\"</green>"
              " <red>deleted.</red>")


def list_add(app, user, args):
    list_id = _get_list_id(app, user, args)
    account = api.find_account(app, user, args.account)

    try:
        api.add_accounts_to_list(app, user, list_id, [account['id']])
    except Exception as ex:
        # if we failed to add the account, try to give a
        # more specific error message than "record not found"
        my_accounts = api.followers(app, user, account['id'])
        found = False
        if my_accounts:
            for my_account in my_accounts:
                if my_account['id'] == account['id']:
                    found = True
                    break
        if found is False:
            print_out(f"<red>You must follow @{account['acct']}"
                      " before adding this account to a list.</red>")
        else:
            print_out(f"<red>{ex}</red>")
        return

    print_out(f"<green>✓ Added account \"{args.account}\"</green>")


def list_remove(app, user, args):
    list_id = _get_list_id(app, user, args)
    account = api.find_account(app, user, args.account)
    api.remove_accounts_from_list(app, user, list_id, [account['id']])
    print_out(f"<green>✓ Removed account \"{args.account}\"</green>")


def _get_list_id(app, user, args):
    list_id = args.id or api.find_list_id(app, user, args.title)
    if not list_id:
        raise ConsoleError("List not found")
    return list_id


def mute(app, user, args):
    account = api.find_account(app, user, args.account)
    response = api.mute(app, user, account['id'])
    if args.json:
        print(response.text)
    else:
        print_out("<green>✓ You have muted {}</green>".format(args.account))


def unmute(app, user, args):
    account = api.find_account(app, user, args.account)
    response = api.unmute(app, user, account['id'])
    if args.json:
        print(response.text)
    else:
        print_out("<green>✓ {} is no longer muted</green>".format(args.account))


def muted(app, user, args):
    response = api.muted(app, user)
    if args.json:
        print(json.dumps(response))
    else:
        if len(response) > 0:
            print("Muted accounts:")
            print_acct_list(response)
        else:
            print("No accounts muted")


def block(app, user, args):
    account = api.find_account(app, user, args.account)
    response = api.block(app, user, account['id'])
    if args.json:
        print(response.text)
    else:
        print_out("<green>✓ You are now blocking {}</green>".format(args.account))


def unblock(app, user, args):
    account = api.find_account(app, user, args.account)
    response = api.unblock(app, user, account['id'])
    if args.json:
        print(response.text)
    else:
        print_out("<green>✓ {} is no longer blocked</green>".format(args.account))


def vote(app, user, args):
    use_cache = user.optimized
    status_response = None
    if use_cache:
        status_response = get_cached_status(args.status_id)
    if status_response is None:
        status_response = api.fetch_status(app, user, args.status_id).json()
    status = from_dict(Status, status_response, use_cache)

    if not status.poll:
        print_out("<red>This post doesn't have a poll</red>")
        return
    if status.poll.expires_at < datetime.now(timezone.utc):
        print_out("<red>The poll has expired</red>")

    poll = status.poll

    if poll.multiple:
        for i, option in enumerate(poll.options):
            print(f"[{i}] {option.title}")
        selected = input("Enter space-separated options you vote for: ")
        try:
            selected = list(filter(lambda x: x < i,
                                   (int(j) for j in selected.split())))
        except ValueError:
            print_out("<red>Invalid options</red>")
            return
        if not selected:
            print_out("<red>No valid options</red>")
            return
    else:
        for i, option in enumerate(poll.options):
            print(f"({i}) {option.title}")
        selected = input("Enter the option you vote for: ")
        try:
            selected = [int(selected)]
        except ValueError:
            print_out("<red>Invalid option</red>")
            return

    response = api.vote(app, user, poll.id, selected)
    poll = from_dict(Poll, response, use_cache)
    print_poll(poll)


def blocked(app, user, args):
    response = api.blocked(app, user)
    if args.json:
        print(json.dumps(response))
    else:
        if len(response) > 0:
            print("Blocked accounts:")
            print_acct_list(response)
        else:
            print("No accounts blocked")


def whoami(app, user, args):
    response = api.verify_credentials(app, user)
    if args.json:
        print(response.text)
    else:
        account = from_dict(Account, response.json())
        print_account(account)


def whois(app, user, args):
    account = api.find_account(app, user, args.account)
    # Here it's not possible to avoid parsing json since it's needed to find the account.
    if args.json:
        print(json.dumps(account))
    else:
        account = from_dict(Account, account)
        print_account(account)


def instance(app, user, args):
    default = app.base_url if app else None
    base_url = args_get_instance(args.instance, args.scheme, default)

    if not base_url:
        raise ConsoleError("Please specify an instance.")

    try:
        response = api.get_instance(base_url)
    except ApiError:
        raise ConsoleError(
            f"Instance not found at {base_url}.\n"
            "The given domain probably does not host a Mastodon instance."
        )

    if args.json:
        print(response.text)
    else:
        instance = from_dict(Instance, response.json())
        print_instance(instance)


def notifications(app, user, args):
    if args.clear:
        api.clear_notifications(app, user)
        print_out("<green>Cleared notifications</green>")
        return

    exclude = []
    if args.mentions:
        # Filter everything except mentions
        # https://docs.joinmastodon.org/methods/notifications/
        exclude = ["follow", "favourite", "reblog", "poll", "follow_request"]

    notifications = api.get_notifications(app, user, exclude_types=exclude)

    if not notifications:
        print_out("<yellow>No notification</yellow>")
        return
    is_pleroma = 'pleroma' in notifications[0]
    if args.read and is_pleroma:
        notifications = list(filter(lambda n: not n['pleroma']['is_seen'], notifications))
        if not notifications:
            print_out("<yellow>No new notification</yellow>")
            return
        last_id = notifications[0]['id']

    if args.reverse:
        notifications = reversed(notifications)

    notifications = [from_dict(Notification, n) for n in notifications]
    print_notifications(notifications)
    if args.read and is_pleroma:
        params = {
            'max_id': last_id
        }
        api.read_notifications(app, user, params)


def tui(app, user, args):
    try:
        import urwid  # noqa
        import beautifulsoup4  # noqa
    except ModuleNotFoundError:
        print('Please install urwid and beautifulsoup4 to use TUI.')
    from .tui.app import TUI
    TUI.create(app, user, args).run()
