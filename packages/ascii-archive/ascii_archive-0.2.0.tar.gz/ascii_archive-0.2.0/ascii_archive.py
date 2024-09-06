#!/usr/bin/env python3
"""File archiver using ASCII files."""

import argparse
import os
import base64
from textwrap import wrap
import sys
import re

from pathlib import Path

VERSION = 1

class ArchiveReader:
    stream = None
    version = 1
    key_value_pair_pattern = re.compile(r'([a-zA-Z0-9_-]+):\s*(.+)\s*')
    entry_header_pattern = re.compile(r'----- Begin ([a-zA-Z0-9_-]+) -----')

    entry_type = None
    filename = None
    data = None

    def __init__(self, stream):
        self.stream = stream
        self.__read_file_header()

    def __readline(self):
        line = self.stream.readline()
        if not line:
            raise Exception("unexpected end of stream")
        return line.strip()

    def __read_file_header(self):
        line = self.__readline()
        if line != "----- Begin ASCII-Archive -----":
            raise Exception("invalid archive")
        line = self.__readline()
        while line != "----- End ASCII-Archive -----":
            m = self.key_value_pair_pattern.fullmatch(line)
            if m:
                key = m.group(1)
                value = m.group(2)
                if key == "Version":
                    self.version = int(value)
            line = self.__readline()
        if self.version != 1:
            raise Exception("version not supported")

    def next(self):
        self.entry_type = None
        self.filename = None
        self.data = None
        while True:
            line = self.stream.readline()
            if not line:
                return False
            m = self.entry_header_pattern.match(line.strip())
            if m:
                self.entry_type = m.group(1)
                break
        if self.entry_type == "File":
            self.__read_file()
        else:
            self.__read_unknown(self.entry_type)
        return True

    def __read_file(self):
        filename = ""
        data = ""
        line = self.__readline()
        while line != "":
            m = self.key_value_pair_pattern.fullmatch(line)
            if not m:
                raise Exception("invaid file header")
            key = m.group(1)
            value = m.group(2)
            if key == "Filename":
                filename += value
            line = self.__readline()
        line = self.__readline()
        while line != "----- End File -----":
            data += line
            line = self.__readline()
        self.filename = filename
        self.data = base64.b64decode(data)

    def __read_unknown(self, name):
        line = self.__readline()
        while line != f"----- End {name} -----":
            line = self.__readline()


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    create = subparsers.add_parser('create')
    create.add_argument('filename', nargs='+')
    subparsers.add_parser('list')
    subparsers.add_parser('extract')
    args = parser.parse_args()
    if args.command == "create":
        create_archive(args.filename)
    elif args.command == "list":
        list_archive()
    elif args.command == "extract":
        extract_archive()

def create_archive(filenames):
    print("----- Begin ASCII-Archive -----")
    print("Version: 1")
    print("----- End ASCII-Archive -----")

    for filename in filenames:
        if os.path.isfile(filename):
            print("----- Begin File -----")
            print(f"Filename: {filename}")
            print("")
            with open(filename, "rb") as f:
                text = base64.b64encode(f.read()).decode()
                for line in wrap(text, 64):
                    print(line)
            print("----- End File -----")

def list_archive():
    reader = ArchiveReader(sys.stdin)
    while reader.next():
        if reader.entry_type == "File":
            print(reader.filename)

def extract_archive():
    reader = ArchiveReader(sys.stdin)
    while reader.next():
        if reader.entry_type == "File":
            parent = Path(reader.filename).parent
            if not parent.exists():
                os.makedirs(parent)
            with open(reader.filename, "wb") as f:
                f.write(reader.data)


if __name__ == "__main__":
    main()
