# SPDX-FileCopyrightText: 2017-2023 Ivan Habunek et al <ivan@habunek.com>
#
# SPDX-License-Identifier: GPL-3.0-only

class ApiError(Exception):
    """Raised when an API request fails for whatever reason."""


class NotFoundError(ApiError):
    """Raised when an API requests returns a 404."""


class AuthenticationError(ApiError):
    """Raised when login fails."""


class ConsoleError(Exception):
    """Raised when an error occurs which needs to be show to the user."""
