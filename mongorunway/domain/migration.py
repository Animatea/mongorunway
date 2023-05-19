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
"""The main interface for managing migrations is the `Migration` class.
It represents a single migration that can be applied or reverted in a database.
"""
from __future__ import annotations

__all__: typing.Sequence[str] = (
    "Migration",
    "MigrationReadModel",
)

import dataclasses
import typing

if typing.TYPE_CHECKING:
    from mongorunway.domain import migration_business_rule as domain_rule
    from mongorunway.domain import migration_command as domain_command


class Migration:
    """This class provides methods for upgrading and downgrading a database schema using
    a sequence of MigrationCommand instances.

    Parameters
    ----------
    name : str
        The name of the migration.
    version : int
        The version number of the migration.
    checksum : str
        A hash checksum of the migration contents.
    description : str
        A description of the migration.
    upgrade_commands : sequence of MigrationCommand
        A sequence of commands to upgrade the database schema.
    downgrade_commands : sequence of MigrationCommand
        A sequence of commands to downgrade the database schema.
    """

    __slots__: typing.Sequence[str] = (
        "_name",
        "_version",
        "_checksum",
        "_is_applied",
        "_description",
        "_upgrade_process",
        "_downgrade_process",
    )

    def __init__(
        self,
        *,
        name: str,
        version: int,
        checksum: str,
        is_applied: bool,
        description: str,
        upgrade_process: MigrationProcess,
        downgrade_process: MigrationProcess,
    ) -> None:
        self._name = name
        self._version = version
        self._checksum = checksum
        self._is_applied = is_applied
        self._description = description
        self._upgrade_process = upgrade_process
        self._downgrade_process = downgrade_process

    @property
    def name(self) -> str:
        """Returns the name of the migration.

        Returns
        -------
        str
            The name of the migration.
        """
        return self._name

    @property
    def version(self) -> int:
        """Get the version of the migration.

        Returns
        -------
        int
            The version of the migration.
        """
        return self._version

    @property
    def checksum(self) -> str:
        """Get the checksum of the migration.

        Returns
        -------
        str
            The checksum of the migration.
        """
        return self._checksum

    @property
    def description(self) -> str:
        """Get the description of the migration.

        Returns
        -------
        str
            The description of the migration.
        """
        return self._description

    @property
    def is_applied(self) -> bool:
        return self._is_applied

    @property
    def upgrade_process(self) -> MigrationProcess:
        """Get the upgrade commands for the migration.

        Returns
        -------
        Sequence[MigrationCommand]
            A sequence of MigrationCommand objects representing the upgrade commands
            for the migration.
        """
        return self._upgrade_process

    @property
    def downgrade_process(self) -> MigrationProcess:
        """Get the downgrade commands for the object.

        Returns
        -------
        Sequence[MigrationCommand]
            A sequence of MigrationCommand objects representing the downgrade commands
            for the migration.
        """
        return self._downgrade_process

    def set_is_applied(self, value: bool, /) -> None:
        self._is_applied = value

    def to_dict(self, *, unique: bool = False) -> typing.Dict[str, typing.Any]:
        """Convert the object to a dictionary representation for MongoDB.

        Parameters
        ----------
        unique : bool, optional
            If True, will add a unique _id key to the dictionary, which will be
            equal to the version of the current migration. Defaults to False.

        Returns
        -------
        Dict[str, Any]
            A dictionary representation of the object suitable for storing in a
            MongoDB collection.
        """
        mapping = {
            "name": self.name,
            "version": self.version,
            "checksum": self.checksum,
            "is_applied": self.is_applied,
            "description": self.description,
        }

        if unique:
            mapping["_id"] = self.version

        return mapping


@dataclasses.dataclass
class MigrationReadModel:
    """Represents a read model of a migration that provides information about the migration.

    Attributes
    ----------
    name : str
        The name of the migration.
    version : int
        The version of the migration.
    checksum : str
        The checksum of the migration.
    description : str
        The description of the migration.
    """

    name: str
    """The name of the migration."""

    version: int
    """The version of the migration."""

    checksum: str
    """The checksum of the migration."""

    description: str
    """The description of the migration."""

    is_applied: bool
    """"""

    @classmethod
    def from_dict(cls, mapping: typing.MutableMapping[str, typing.Any], /) -> MigrationReadModel:
        """Create a MigrationReadModel instance from a dictionary.

        Parameters
        ----------
        mapping : typing.MutableMapping[str, typing.Any]
            A dictionary containing the attributes of the migration.

        Returns
        -------
        MigrationReadModel
            An instance of MigrationReadModel initialized with the attributes
            from the dictionary.
        """
        mapping.pop("_id", None)  # For mongo records
        return cls(**mapping)

    @classmethod
    def from_migration(cls, migration: Migration, /) -> MigrationReadModel:
        """Create a MigrationReadModel instance from a Migration instance.

        Parameters
        ----------
        migration : Migration
            A Migration instance to create the MigrationReadModel instance from.

        Returns
        -------
        MigrationReadModel
            An instance of MigrationReadModel initialized with the attributes
            from the Migration instance.
        """
        return cls(
            name=migration.name,
            version=migration.version,
            checksum=migration.checksum,
            description=migration.description,
            is_applied=migration.is_applied,
        )


class MigrationProcess:
    def __init__(
        self,
        commands: domain_command.CommandSequence,
        migration_version: int,
        name: str,
    ) -> None:
        self._rules: domain_rule.RuleSequence = []
        self._name = name
        self._commands = commands
        self._migration_version = migration_version

    @property
    def name(self) -> str:
        return self._name

    @property
    def commands(self) -> domain_command.CommandSequence:
        return self._commands

    @property
    def migration_version(self) -> int:
        return self._migration_version

    @property
    def rules(self) -> domain_rule.RuleSequence:
        return self._rules

    def has_rules(self) -> bool:
        return bool(self._rules)

    def add_rule(self, rule: domain_rule.MigrationBusinessRule, /):
        self._rules.append(rule)
        return self