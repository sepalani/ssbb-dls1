#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""SSBB archive module.

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


class Archive(object):
    """SSBB DLS1 archive format.

    Example:
    0000  52 53 42 4a 02 00 00 00  00 00 00 20 00 01 90 5c  |RSBJ....... ...\|
    0010  07 39 94 cd 00 01 90 7c  00 00 16 1e 72 49 fd 31  |.9.....|....rI.1|
    0020  SECTION 1 DATA
    ...   SECTION 1 SIZE
    1907c SECTION 2 DATA
    ...   SECTION 2 SIZE

    52 53 42 4a - "RSBJ" FourCC
    02 00 00 00 - Section count
    --- Repeat for each section
    00 00 00 20 - Section address
    00 01 90 5c - Section size
    07 39 94 cd - Section CRC32
    ---
    00 01 90 7c - Section address
    00 00 16 1e - Section size
    72 49 fd 31 - Section CRC32
    """

    Section = namedtuple("ArchiveSection", ["data", "size", "crc32"])

    class Assertion(AssertionError):
        def __init__(self, section, message):
            AssertionError.__init__(
                self, "[{}] {}".format(
                    "Section {}".format(section)
                    if section is not None
                    else "Header",
                    message
                )
            )

        @staticmethod
        def do(condition, section, message):
            if not condition:
                raise Archive.Assertion(section, message)

    def __init__(self):
        """Create empty Archive."""
        self._sections = []

    def __len__(self):
        """Return Archive section count."""
        return len(self._sections)

    def __iter__(self):
        """Iterate over Archive sections."""
        return iter(self._sections)

    def __getitem__(self, index):
        """Get Archive section."""
        return self._sections[index]

    def __setitem__(self, index, data):
        """Set Archive section."""
        if isinstance(data, Archive.Section):
            self._sections[index] = data
            return
        data = bytearray(data)
        self._sections[index] = Archive.Section(
            data, len(data), binascii.crc32(data) & 0xFFFFFFFF
        )

    def __delitem__(self, index):
        """Delete Archive section."""
        del self._sections[index]

    def add_section(self, data):
        """Add Archive section."""
        if isinstance(data, Archive.Section):
            self._sections.append(data)
            return
        data = bytearray(data)
        self._sections.append(
            Archive.Section(data, len(data), binascii.crc32(data) & 0xFFFFFFFF)
        )

    def get_section(self, index):
        """Get Archive section."""
        return self[index]

    def set_section(self, index, data):
        """Set Archive section."""
        self[index] = data

    def delete_section(self, index):
        """Delete Archive section."""
        del self[index]

    def pack(self, padding=16):
        """Pack Archive into bytearray."""
        header = bytearray(b"RSBJ")
        section_count = len(self._sections)
        header.extend(struct.pack("<I", section_count))
        section_address = 8 + 12 * section_count

        data = bytearray()
        for section in self._sections:
            header.extend(struct.pack(
                ">III",
                section_address, section.size, section.crc32
            ))
            data.extend(section.data)
            section_address += section.size

        archive = header + data
        if padding:
            archive.extend(bytearray(
                (padding - len(archive) % padding) % padding
            ))

        return archive

    def unpack(self, data, ignore_errors=False):
        """Unpack Archive from bytes."""
        self._sections = []
        data = bytearray(data)
        fourcc = data[:4]
        if not ignore_errors:
            Archive.Assertion.do(
                fourcc == bytearray(b"RSBJ"),
                None, "invalid four-character code"
            )

        section_count, = struct.unpack_from("<I", data, 4)
        index = 8
        for i in range(section_count):
            address, size, crc32 = struct.unpack_from(">III", data, index)
            if not ignore_errors:
                Archive.Assertion.do(
                    address < len(data),
                    i, "address ({}) out of range ({})".format(
                        address, len(data)
                    )
                )
                Archive.Assertion.do(
                    address+size < len(data),
                    i, "size ({}) out of range {}".format(
                        size, len(data)
                    )
                )
            section = data[address:address+size]
            if not ignore_errors:
                expected_crc32 = binascii.crc32(section) & 0xFFFFFFFF
                Archive.Assertion.do(
                    crc32 == expected_crc32,
                    i, "bad crc32 (0x{:08x}), 0x{:08x} expected".format(
                        crc32, expected_crc32
                    )
                )
            self._sections.append(Archive.Section(
                section, len(section), crc32
            ))
            index += 12

        return self


def pack(archive):
    return archive.pack()


def pack_into(archive, buffer, offset):
    data = archive.pack()
    buffer[offset:offset+len(data)] = data


def unpack(data, ignore_errors=False):
    return Archive().unpack(data, ignore_errors)


def unpack_from(buffer, offset=0, ignore_errors=False):
    data = buffer[offset:]
    return Archive().unpack(data, ignore_errors)


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-u", "--unpack",
                       type=str, metavar="FILE",
                       help="unpack files from SSBB archive file")
    group.add_argument("-p", "--pack",
                       type=str, nargs="+", metavar="FILE",
                       help="pack files into SSBB archive file")
    parser.add_argument("-i", "--ignore-errors", dest="ignore",
                        action="store_true",
                        help="ignore unpacking errors")
    parser.add_argument("-o", "--offset",
                        type=int, default=0,
                        help="specify the offset to read from/write to")
    parser.add_argument("-d", "--dest",
                        type=str,
                        help="destination file(s) name")

    args = parser.parse_args()
    if not args.unpack and not args.pack:
        parser.print_help()
    if args.unpack:
        archive = unpack_from(
            open(args.unpack, "rb").read(), args.offset, args.ignore
        )
        name, ext = os.path.splitext(args.dest if args.dest else args.unpack)
        for i, section in enumerate(archive):
            with open("{}.{:03d}{}".format(name, i, ext), "wb") as f:
                f.write(section.data)
    if args.pack:
        archive = Archive()
        for path in args.pack:
            archive.add_section(open(path, "rb").read())
        name = args.dest if args.dest else "{}.rsbj".format(args.pack[0])
        flags = "rb+" if os.path.exists(name) else "wb"
        with open(name, flags) as f:
            f.seek(args.offset)
            f.write(archive.pack())
