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

from Crypto.Cipher import AES

KEY = "9265471A9CBF3D568A13D3C481532C18".decode("hex")
IV = "4E0341DEE6BBAA416419B3EAE8F53BD9".decode("hex")


def decrypt(data):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    return cipher.decrypt(data)


def encrypt(data):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    return cipher.encrypt(data)


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--decrypt",
                        type=str, nargs="+",
                        help="decrypt SSBB DLS1 files")
    parser.add_argument("-e", "--encrypt",
                        type=str, nargs="+",
                        help="encrypt SSBB DLS1 files")

    args = parser.parse_args()
    if args.decrypt:
        for path in args.decrypt:
            fname, fext = os.path.splitext(path)
            with open(fname + ".dec" + fext, "wb") as f:
                f.write(decrypt(open(path, "rb").read()))
    if args.encrypt:
        for path in args.encrypt:
            fname, fext = os.path.splitext(path)
            with open(fname + ".enc" + fext, "wb") as f:
               f.write(encrypt(open(path, "rb").read()))
