import pathlib
import sys

files = sys.argv[1].split()
valid = False

for f in files:
    p = pathlib.Path(f)

    if p.exists():
        content = p.read_bytes()
        if b'assert' in content or b'test_' in content:
            valid = True
            break

if not valid:
    print('No valid test assertions found!')
    sys.exit(1)
