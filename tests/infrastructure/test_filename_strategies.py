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
from __future__ import annotations

import pytest

from mongorunway.infrastructure.filename_strategies import MissingFilenameStrategy
from mongorunway.infrastructure.filename_strategies import NumericalFilenameStrategy
from mongorunway.infrastructure.filename_strategies import UnixFilenameStrategy


@pytest.fixture(scope="function")
def missing_strategy() -> MissingFilenameStrategy:
    return MissingFilenameStrategy()


@pytest.fixture(scope="function")
def numerical_strategy() -> NumericalFilenameStrategy:
    return NumericalFilenameStrategy()


@pytest.fixture(scope="function")
def unix_strategy() -> UnixFilenameStrategy:
    return UnixFilenameStrategy()


class TestMissingFilenameStrategy:
    @pytest.mark.parametrize(
        "filename, expected_result",
        [
            ("file1.txt", True),
            ("file2.txt", True),
            ("file3.txt", True),
        ],
    )
    def test_is_valid_filename(
        self,
        missing_strategy: MissingFilenameStrategy,
        filename: str,
        expected_result: bool,
    ) -> None:
        assert missing_strategy.is_valid_filename(filename) == expected_result

    @pytest.mark.parametrize(
        "filename, position, expected_result",
        [
            ("file1.txt", 1, "file1.txt"),
            ("file2.txt", 2, "file2.txt"),
            ("file3.txt", 3, "file3.txt"),
        ],
    )
    def test_transform_migration_filename(
        self,
        missing_strategy: MissingFilenameStrategy,
        filename: str,
        position: int,
        expected_result: str,
    ) -> None:
        assert missing_strategy.transform_migration_filename(filename, position) == expected_result


class TestNumericalFilenameStrategy:
    @pytest.mark.parametrize(
        "filename, expected_result",
        [
            ("001_file.txt", True),
            ("002_file.txt", True),
            ("003_file.txt", True),
            ("file.txt", False),
            ("abc_file.txt", False),
        ],
    )
    def test_is_valid_filename(
        self,
        numerical_strategy: NumericalFilenameStrategy,
        filename: str,
        expected_result: bool,
    ) -> None:
        assert numerical_strategy.is_valid_filename(filename) == expected_result

    @pytest.mark.parametrize(
        "filename, position, expected_result",
        [
            ("001_file.txt", 1, "001_file.txt"),
            ("002_file.txt", 2, "002_file.txt"),
            ("file.txt", 1, "001_file.txt"),
            ("abc_file.txt", 2, "002_abc_file.txt"),
        ],
    )
    def test_transform_migration_filename(
        self,
        numerical_strategy: NumericalFilenameStrategy,
        filename: str,
        position: int,
        expected_result: str,
    ) -> None:
        assert (
            numerical_strategy.transform_migration_filename(
                filename,
                position,
            )
            == expected_result
        )


class TestUnixFilenameStrategy:
    @pytest.mark.parametrize(
        "filename, expected_result",
        [
            ("1234567890_file.txt", True),
            ("12345678901234567890_file.txt", True),
            ("file.txt", False),
            ("12345_file.txt", False),
        ],
    )
    def test_is_valid_filename(
        self,
        unix_strategy: UnixFilenameStrategy,
        filename: str,
        expected_result: bool,
    ) -> None:
        assert unix_strategy.is_valid_filename(filename) == expected_result

    @pytest.mark.parametrize(
        "filename, position, expected_result",
        [
            ("1234567890_file.txt", 1, "1234567890_file.txt"),
            ("12345678901234567890_file.txt", 2, "12345678901234567890_file.txt"),
        ],
    )
    def test_transform_migration_filename(
        self,
        unix_strategy: UnixFilenameStrategy,
        filename: str,
        position: int,
        expected_result: str,
    ) -> None:
        assert unix_strategy.transform_migration_filename(filename, position) == expected_result
