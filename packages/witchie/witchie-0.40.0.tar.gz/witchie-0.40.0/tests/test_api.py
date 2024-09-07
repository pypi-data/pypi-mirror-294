# SPDX-FileCopyrightText: 2017-2023 Ivan Habunek et al <ivan@habunek.com>
# SPDX-FileCopyrightText: 2023-2024 Ngô Ngọc Đức Huy <huyngo@disroot.org>
#
# SPDX-License-Identifier: GPL-3.0-only

from unittest import mock

import pytest

from tests.utils import MockResponse
from witchie import CLIENT_NAME, CLIENT_WEBSITE, App
from witchie.api import SCOPES, AuthenticationError, create_app, login


@mock.patch('witchie.http.anon_post')
def test_create_app(mock_post):
    mock_post.return_value = MockResponse({
        'client_id': 'foo',
        'client_secret': 'bar',
    })

    create_app('https://bigfish.software')

    mock_post.assert_called_once_with('https://bigfish.software/api/v1/apps', json={
        'website': CLIENT_WEBSITE,
        'client_name': CLIENT_NAME,
        'scopes': SCOPES,
        'redirect_uris': 'urn:ietf:wg:oauth:2.0:oob',
    })


@mock.patch('witchie.http.anon_post')
def test_login(mock_post):
    app = App('bigfish.software', 'https://bigfish.software', 'foo', 'bar')

    data = {
        'grant_type': 'password',
        'client_id': app.client_id,
        'client_secret': app.client_secret,
        'username': 'user',
        'password': 'pass',
        'scope': SCOPES,
    }

    mock_post.return_value = MockResponse({
        'token_type': 'bearer',
        'scope': 'read write follow',
        'access_token': 'xxx',
        'created_at': 1492523699
    })

    login(app, 'user', 'pass')

    mock_post.assert_called_once_with(
        'https://bigfish.software/oauth/token', data=data, allow_redirects=False)


@mock.patch('witchie.http.anon_post')
def test_login_failed(mock_post):
    app = App('bigfish.software', 'https://bigfish.software', 'foo', 'bar')

    data = {
        'grant_type': 'password',
        'client_id': app.client_id,
        'client_secret': app.client_secret,
        'username': 'user',
        'password': 'pass',
        'scope': SCOPES,
    }

    mock_post.return_value = MockResponse(is_redirect=True)

    with pytest.raises(AuthenticationError):
        login(app, 'user', 'pass')

    mock_post.assert_called_once_with(
        'https://bigfish.software/oauth/token', data=data, allow_redirects=False)
