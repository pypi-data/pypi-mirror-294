[![build](https://github.com/falk-werner/ascii-archive/actions/workflows/build.yaml/badge.svg)](https://github.com/falk-werner/ascii-archive/actions/workflows/build.yaml)
[![GitHub License](https://img.shields.io/github/license/falk-werner/ascii-archive)](https://github.com/falk-werner/ascii-archive/blob/main/LICENSE)
[![PyPI - Version](https://img.shields.io/pypi/v/ascii-archive)](https://pypi.org/project/ascii-archive/)
[!![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/falk-werner/ascii-archive)](https://github.com/falk-werner/ascii-archive/issues)

# ASCII-Archive

## Usage

### Create an archive

    ./ascii_archive.py create some.file > my-archive.txt

### Lists contents of an archive

    ./ascii_archive.py list < my-archive.txt

### Extract file of an archive

    ./ascii_archive.py extract < my-archive.txt

## File format

- archive files only contains ASCII characters
- a single line must be exceed 64 characters
- the archive is a collection of entries
- each entry begins with a single line `----- Begin ENTRYNAME -----`
- each entry ends with a single line `----- End ENTRYNAME -----`
- a client should support multiple end of line markers (\n, \r\n, \r)
- the very first entry must be `ASCII-Archive`
- the `ASCII-Archive` entry contains meta information of the file
  - each meta information is described in a single line of the following format: `KEY: VALUE`
  - clients should silently ignore fields they don't understand
  - currently, only one field is defined: `Version`, which must be set to `1`
- there is an entry type `File` containing a file
  - a file entry consists of two sections: file meta information and file contents
  - both sections are separated by an empty line
  - the file meta information is a list of fields of the following format: `KEY: VALUE`
  - clients should silently ignore fields they don't understand
  - currently, only one field is defines: `Filename`, which contains the name of the file
  - to support long filenames and respect the 64 characters per line limit, multiple occurances  
    of the `Filename` field may be present; they will be concatenated
  - the contents of the file ist base64 encoded
  - non-ASCII filenames are not supported yet
- clients should silently ignore entries, they don't know

### Grammar

```
ARCHIVE := ARCHIVE_ENTRY ENTRY*

ARCHIVE_ENTRY := ARCHIVE_ENTRY_BEGIN FIELD* ARCHIVE_ENTRY_END
ARCHIVE_ENTRY_BEGIN := '---- Begin ASCII-Archive -----' EOL
ARCHIVE_ENTRY_END := '---- END ASCII-Archive -----' EOL

ENTRY := FILE_ENTRY | GENERIC_ENTRY

FILE_ENTRY := FILE_ENTRY_BEGIN FILE_HEADER EMPTY_LINE FILE_CONTENTS FILE_ENTRY_END
FILE_ENTRY_BEGIN := '---- Begin File -----' EOL
FILE_ENTRY_END := '---- END File -----' EOL
FILE_HEADER := FIELD*
FILE_CONTENTS := B64_LINE*

GENERIC_ENTRY := GENERIC_ENTRY_BEGIN .* GENERIC_ENTRY_END
GENERIC_ENTRY_BEGIN := '---- Begin ' KEY ' -----' EOL
GENERIC_ENTRY_END := '---- END ' KEY ' -----' EOL

FIELD := KEY ':' SPACE* VALUE SPACE* EOL

B64_LINE := B64_CHAR{0-64} EOL
B64_CHAR := [a-zA-Z0-9+/=]

KEY := [a-zA-Z0-9_-]
VALUE := [^\r\n]*
EOL := '\n' | '\r\n' | '\r'
SPACE := ' ' | '\t'
```

### Example

The following example shows an archive containg two files:
- foo: with the contents "42"
- bar: with the contents "23"

```
----- Begin ASCII-Archive -----
Version: 1
----- End ASCII-Archive -----
----- Begin File -----
Filename: foo

NDI=
----- End File -----
----- Begin File -----
Filename: bar

MjM=
----- End File -----
```
