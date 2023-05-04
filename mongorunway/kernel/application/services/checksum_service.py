# Copyright (c) 2023 Animatea
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""This module contains services for working with migration file checksums."""
from __future__ import annotations

__all__: typing.Sequence[str] = (
    "calculate_migration_checksum",
)

import hashlib
import typing

if typing.TYPE_CHECKING:
    from mongorunway.kernel.domain.migration_module import MigrationModule


def calculate_migration_checksum(module: MigrationModule, /) -> str:
    """Calculates the checksum of a migration module.

    Parameters
    ----------
    module : MigrationModule
        The migration module to calculate the checksum for.

    Returns
    -------
    str
        The checksum of the migration module.

    Raises
    ------
    FileNotFoundError
        If the migration module's file location cannot be found.
    """
    with open(module.location, "r") as f:
        file_data = f.read().encode()
        return hashlib.md5(file_data).hexdigest()
