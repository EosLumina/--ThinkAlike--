import pathlib

files = [
    'backend/app/development/ai_application_developer.py',
    'backend/app/documentation/doc_parser.py',
    'backend/app/services/value_based_matcher.py'
]

for f in files:
    p = pathlib.Path(f)
    if p.exists():
        content = p.read_bytes()
        fixed = content.replace(b'\x00', b'')
        p.write_bytes(fixed)
        print(f'Fixed {f}' if content != fixed else f'No nulls in {f}')
