#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""SSBB DLS1 utils.

    SSBB DLS1 Project
    Copyright (C) 2018  Sepalani

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import binascii
import struct

from collections import namedtuple


def bitfield(cls):
    """Bitfield helper."""
    # Define bitfield's bits
    bits = cls.BITS
    for i, name in enumerate(cls.BITS):
        setattr(cls, name, 1 << i)
    # Define bitfield's methods
    cls.enabled = staticmethod(
        lambda value: [
            name
            for i, name in enumerate(bits)
            if value & (1 << i)
        ]
    )
    cls.disabled = staticmethod(
        lambda value: [
            name
            for i, name in enumerate(bits)
            if not (value & (1 << i))
        ]
    )
    return cls


class Setting(object):
    """SSBB Setting."""

    Date = namedtuple("SettingDate", ["year", "month", "day"])

    class Contribute:
        """Contribute flags."""
        REPLAYS = 0x01
        ALBUM = 0x02
        STAGES = 0x04
        SPECTATOR = 0x08
        ALL = 0x7F

    @bitfield
    class Character:
        """Character flags (to be confirmed...).

        >>> # Character IDs
        >>> "{:064b}".format(0x00000FFABFF9FFFF)
        '0000000000000000000011111111101010111111111110011111111111111111'
        >>> Setting.Character.disabled(0x00000FFABFF9FFFF)
        ['POPO', 'NANA', 'CHARIZARD_TRAINER_INDEPENDANT',
        'VENASAUR_TRAINER_INDEPENDANT', 'SQUIRTLE_TRAINER_INDEPENDANT',
        'GIGA_BOWSER', 'WARIOMAN', 'ZAKO_RED', 'ZAKO_BLUE', 'ZAKO_YELLOW',
        'ZAKO_GREEN', 'MARIO_DEBUG']
        """
        BITS = [
            "MARIO", "DONKEY_KONG", "LINK", "SAMUS", "ZERO_SUIT_SAMUS",
            "YOSHI", "KIRBY", "FOX", "PIKACHU", "LUIGI", "CAPTAIN_FALCON",
            "NESS", "BOWSER", "PEACH", "ZELDA", "SHEIK", "ICE_CLIMBERS",
            "POPO",  # DEBUG
            "NANA",  # DEBUG
            "MARTH", "MR_GAME_AND_WATCH", "FALCO", "GANONDORF", "WARIO",
            "METAKNIGHT", "PIT", "OLIMAR", "LUCAS", "DIDDY_KONG", "CHARIZARD",
            "CHARIZARD_TRAINER_INDEPENDANT",  # DEBUG
            "VENASAUR",
            "VENASAUR_TRAINER_INDEPENDANT",  # DEBUG
            "SQUIRTLE",
            "SQUIRTLE_TRAINER_INDEPENDANT",  # DEBUG
            "DEDEDE", "LUCARIO", "IKE", "ROBOT", "JIGGLYPUFF", "TOON_LINK",
            "WOLF", "SNAKE", "SONIC",
            # DEBUG
            "GIGA_BOWSER", "WARIOMAN",
            "ZAKO_RED", "ZAKO_BLUE", "ZAKO_YELLOW", "ZAKO_GREEN",
            "MARIO_DEBUG"
        ]
        ALL = 0x00000FFABFF9FFFF
        ALL_DEBUG = 0xFFFFFFFFFFFFFFFF

    @bitfield
    class Stage:
        """Stage flags (to be confirmed...).

        >>> # Stage ID
        >>> "{:064b}".format(0x000FFE3FF3F87BFE)
        '0000000000001111111111100011111111110011111110000111101111111110'
        >> Setting.Stage.disabled(0x000FFE3FF3F87BFE)
        ['BATTLE', 'BRIDGE_OF_ELDIN_2', 'TEST_HALBERD_00', 'TEST_HALBERD_01',
        'TEST_HALBERD_02', 'KARBY2', 'TEST_EMBLEM_00', 'TEST_EMBLEM_01',
        'CONFIGTEST', 'VIEWER', 'RESULT', 'HOMERUN', 'STAGE_BUILDER',
        'ALLSTAR_HALL', 'ONLINE_TRAINING', 'BREAK_THE_TARGET',
        'CHARACTER_ROLL', 'GENERAL', 'ADVENTURE', 'ADVENTURE0', 'ADVENTURE2',
        'ADVENTURE_MELEE_TEST', 'ADVENTURE_MELEE', 'BATTLE_S', 'BATTLEFIELD_S',
        'MAX', 'UNKNOWN']
        """
        BITS = [
            "BATTLE",  # DEBUG
            "BATTLEFIELD", "FINAL_DESTINATION", "DELFINO_PLAZA",
            "LUIGI_MANSION", "MUSHROOMY_KINGDOM", "MARIO_CIRCUIT", "75M",
            "RUMBLE_FALLS", "PIRATE_SHIP",
            "BRIDGE_OF_ELDIN_2",  # DEBUG
            "NORFAIR", "FRIGATE_ORPHEON", "YOSHI_ISLAND", "HALBERD",
            "TEST_HALBERD_00",  # DEBUG
            "TEST_HALBERD_01",  # DEBUG
            "TEST_HALBERD_02",  # DEBUG
            "KARBY2",  # DEBUG
            "LYLAT_CRUISE", "POKEMON_STADIUM_2", "SPEAR_PILLAR", "PORT_TOWN",
            "SUMMIT", "FLAT_ZONE_2", "CASTLE_SIEGE",
            "TEST_EMBLEM_00",  # DEBUG
            "TEST_EMBLEM_01",  # DEBUG
            "WARIOWARE", "DISTANT_PLANET", "SKYWORLD", "MARIO_BROS",
            "NEW_PORK_CITY", "SMASHVILLE", "SHADOW_MOSES_ISLAND",
            "GREEN_HILL_ZONE", "PICTOCHAT", "HANENBOW",
            "CONFIGTEST",  # DEBUG
            "VIEWER",  # DEBUG
            "RESULT",  # DEBUG
            "MELEE_TEMPLE", "MELEE_YOSHI_ISLAND", "MELEE_JUNGLE_JAPES",
            "MELEE_ONETT", "MELEE_GREEN_GREENS", "MELEE_POKEMON_STADIUM",
            "MELEE_RAINBOW_CRUISE", "MELEE_CORNERIA", "MELEE_BIG_BLUE",
            "MELEE_BRINSTAR",
            # DEBUG
            "BRIDGE_OF_ELDIN",
            "HOMERUN",
            "STAGE_BUILDER",
            "ALLSTAR_HALL",
            "ONLINE_TRAINING",
            "BREAK_THE_TARGET",
            "CHARACTER_ROLL",
            "GENERAL",
            "ADVENTURE", "ADVENTURE0", "ADVENTURE2",
            "ADVENTURE_MELEE_TEST",
            "ADVENTURE_MELEE",
            # Can't be masked (don't fit in 64-bit mask)
            "BATTLE_S", "BATTLEFIELD_S",
            "MAX", "UNKNOWN"
        ]
        ALL = 0x000FFE3FF3F87BFE
        ALL_DEBUG = 0xFFFFFFFFFFFFFFFF

    def __init__(self):
        self.padding = bytearray(0x10)
        self.header = [
            0x00, 0x00, 0x00, 0xdb,
            0x00, 0x00, 0x00, 0x63,
            0x00, 0x00, 0x00, 0x63
        ]
        self.crc32 = bytearray.fromhex("DEADBEEF")
        self.contribute = 0
        self.is_infinity_contribute = 0
        self.collection_lifetime = 0
        self.unknown_0x03 = 0
        self.contribute_start = Setting.Date(2000, 1, 1)
        self.contribute_end = Setting.Date(2123, 12, 31)
        self.watch_start = Setting.Date(2000, 1, 1)
        self.watch_end = Setting.Date(2123, 12, 31)
        self.deliv_start = Setting.Date(2000, 1, 1)
        self.deliv_end = Setting.Date(2123, 12, 31)
        self.upload_size_limit = 0
        self.enable_upload_character = 0
        self.enable_upload_stage = 0
        self.spectator_misc = b""

    def __repr__(self):
        repr = """# Setting class
contribute: {}
is_infinity_contribute: {}
collection_lifetime: {}
unknown_0x03: {}
contribute_start: {!r}
contribute_end: {!r}
watch_start: {!r}
watch_end: {!r}
deliv_start: {!r}
deliv_end: {!r}
upload_size_limit: {}
enable_upload_character: {}
enable_upload_stage: {}
spectator_misc: {!r}""".format(
            self.contribute,
            self.is_infinity_contribute,
            self.collection_lifetime,
            self.unknown_0x03,
            self.contribute_start,
            self.contribute_end,
            self.watch_start,
            self.watch_end,
            self.deliv_start,
            self.deliv_end,
            self.upload_size_limit,
            ", ".join(Setting.Character.enabled(self.enable_upload_character)),
            ", ".join(Setting.Stage.enabled(self.enable_upload_stage)),
            self.spectator_misc
        )
        return repr

    def pack(self):
        # Header
        setting = bytearray(self.padding)
        setting.extend(bytearray.fromhex("DEADBEEF"))  # CRC32
        setting.extend(self.header)

        # Setting
        setting.extend(struct.pack(
            ">BBBB",
            self.contribute,
            self.is_infinity_contribute,
            self.collection_lifetime,
            self.unknown_0x03,
        ))
        setting.extend(struct.pack(">HBB", *self.contribute_start))
        setting.extend(struct.pack(">HBB", *self.contribute_end))
        setting.extend(struct.pack(">HBB", *self.watch_start))
        setting.extend(struct.pack(">HBB", *self.watch_end))
        setting.extend(struct.pack(">HBB", *self.deliv_start))
        setting.extend(struct.pack(">HBB", *self.deliv_end))
        setting.extend(struct.pack(
            ">QQ",
            self.enable_upload_character,
            self.enable_upload_stage
        ))
        setting.extend(self.spectator_misc)

        # CRC32
        self.crc32 = binascii.crc32(setting) & 0xFFFFFFFF
        setting[0x10:0x14] = struct.pack(">I", self.crc32)

        return setting

    def unpack(self, data, ignore_errors=False):
        self.crc32 = struct.unpack_from(">I", data, 0x10)[0]
        data[0x10:0x14] = bytearray.fromhex("DEADBEEF")
        crc32 = binascii.crc32(data) & 0xFFFFFFFF
        if not ignore_errors:
            assert crc32 == self.crc32, "CRC32 mismatch"
        data[0x10:0x14] = struct.pack(">I", crc32)

        self.padding = data[:0x10]
        self.header = data[0x14:0x20]
        self.contribute = struct.unpack_from(">B", data, 0x20)[0]
        self.is_infinity_contribute = struct.unpack_from(">B", data, 0x21)[0]
        self.collection_lifetime = struct.unpack_from(">B", data, 0x22)[0]
        self.unknown_0x03 = struct.unpack_from(">B", data, 0x23)[0]
        self.contribute_start = Setting.Date(
            *struct.unpack_from(">HBB", data, 0x24)
        )
        self.contribute_end = Setting.Date(
            *struct.unpack_from(">HBB", data, 0x28)
        )
        self.watch_start = Setting.Date(
            *struct.unpack_from(">HBB", data, 0x2C)
        )
        self.watch_end = Setting.Date(
            *struct.unpack_from(">HBB", data, 0x30)
        )
        self.deliv_start = Setting.Date(
            *struct.unpack_from(">HBB", data, 0x34)
        )
        self.deliv_end = Setting.Date(
            *struct.unpack_from(">HBB", data, 0x38)
        )
        self.enable_upload_character = struct.unpack_from(">Q", data, 0x3C)[0]
        self.enable_upload_stage = struct.unpack_from(">Q", data, 0x44)[0]
        self.spectator_misc = data[0x4C:]

        return self


def _test():
    """Recreate s20130702_1.bin."""
    MISC = bytearray.fromhex(
        "00 01 64 14"
        "0a 28 64 64"
        "00 00 00 0a"
        "00 00 1e 00"
        "83 83 83 83"
        "83 00 00 0a"
        "0f 14 19 82"
        "7d 78 73 00"
        "01 01 02 03"
        "03 02 01 00"
        "00 03 04 04"
        "03 03 02 00"
        "00 00 00 00"
        "0a 00 50"
    )
    s = Setting()
    s.contribute = Setting.Contribute.SPECTATOR
    s.is_infinity_contribute = 0x00
    s.collection_lifetime = 0x18
    s.upload_size_limit = s.collection_lifetime
    s.unknown_0x03 = 0x03
    s.contribute_start = Setting.Date(2008, 1, 29)
    s.contribute_end = Setting.Date(2009, 6, 30)
    s.watch_start = Setting.Date(2008, 1, 29)
    s.watch_end = Setting.Date(2018, 7, 1)
    s.deliv_start = Setting.Date(2008, 1, 29)
    s.deliv_end = Setting.Date(2015, 7, 1)
    s.enable_upload_character = Setting.Character.ALL
    s.enable_upload_stage = Setting.Stage.ALL
    s.spectator_misc = MISC

    with open("s20130702_test.bin", "wb") as f:
        from archive import Archive
        archive = Archive()
        archive.add_section(s.pack())
        f.write(archive.pack())


def _new():
    """New SSBB setting update."""
    MISC = bytearray.fromhex(
        "01 01 7F 7F"
        "7F 7F 7F 7F"
        "7F 7F 7F 7F"
        "7F 7F 7F 7F"
        "7F 7F 7F 7F"
        "7F 7F 7F 7F"
        "7F 7F 7F 7F"
        "7F 00 7F 7F"
        "7F 7F 7F 7F"
        "7F 7F 7F 7F"
        "7F 7F 7F 7F"
        "7F 7F 7F 7F"
        "7F 7F 7F 7F"
        "7F 7F 7F"
    )
    s = Setting()
    s.contribute = Setting.Contribute.ALL
    s.is_infinity_contribute = 0x01
    s.collection_lifetime = 0x18
    s.upload_size_limit = 0x18
    s.unknown_0x03 = 0x03
    s.contribute_start = Setting.Date(2018, 1, 1)
    s.contribute_end = Setting.Date(2123, 12, 31)
    s.watch_start = Setting.Date(2018, 1, 1)
    s.watch_end = Setting.Date(2123, 12, 31)
    s.deliv_start = Setting.Date(2018, 1, 1)
    s.deliv_end = Setting.Date(2123, 12, 11)
    s.enable_upload_character = Setting.Character.ALL
    s.enable_upload_stage = Setting.Stage.ALL
    s.spectator_misc = MISC

    with open("s20180301_test.bin", "wb") as f:
        from archive import Archive
        archive = Archive()
        archive.add_section(s.pack())
        f.write(archive.pack())


if __name__ == "__main__":
    example = r"""
# Run it with: python -i
from archive import Archive

# Load decrypted setting
with open("s20130702_1.dec.bin", "rb") as f:
    data = bytearray(f.read())

a = Archive().unpack(data)

# Print setting data
from dls1 import Setting
s = Setting().unpack(a[0].data)
print(s)
"""
    print(example)
