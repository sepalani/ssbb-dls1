#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""SSBB crypto module.

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

WIFI_KEY = "9265471A9CBF3D568A13D3C481532C18".decode("hex")
WIFI_IV = "4E0341DEE6BBAA416419B3EAE8F53BD9".decode("hex")

SD_KEY = "AB01B9D8E1622B08AFBAD84DBFC2A55D".decode("hex")
SD_IV = "4E0341DEE6BBAA416419B3EAE8F53BD9".decode("hex")

KEY_IV_MAP = {
    "WIFI": (WIFI_KEY, WIFI_IV),
    "SD": (SD_KEY, SD_IV)
}


def decrypt(data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(data)


def encrypt(data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
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
    parser.add_argument("-s", "--sd",
                        action="store_true",
                        help="use SD key for encryption/decryption")

    args = parser.parse_args()
    if args.sd:
        key, iv = KEY_IV_MAP["SD"]
    else:
        key, iv = KEY_IV_MAP["WIFI"]
    if args.decrypt:
        for path in args.decrypt:
            fname, fext = os.path.splitext(path)
            with open(fname + ".dec" + fext, "wb") as f:
                f.write(decrypt(open(path, "rb").read(), key, iv))
    if args.encrypt:
        for path in args.encrypt:
            fname, fext = os.path.splitext(path)
            with open(fname + ".enc" + fext, "wb") as f:
                f.write(encrypt(open(path, "rb").read(), key, iv))
