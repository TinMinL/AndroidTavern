#!/usr/bin/env python3
"""Fetch the pinned upstream runtime, verifying every file before copying."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = 'https://github.com/doomedskull1011/SillyTavernAndroid.git'
COMMIT = 'c6e0689e539935bd5dd89d7a569adeaf6317583b'

def verify(root):
    manifest = json.loads((ROOT / 'runtime/binaries.lock.json').read_text())
    for name, expected in manifest.items():
        path = root / name
        if not path.is_file() or path.stat().st_size != expected['size']:
            raise RuntimeError('Missing or incorrect size (Git LFS required): ' + name)
        with path.open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        if digest != expected['sha256']:
            raise RuntimeError('SHA-256 mismatch: ' + name)
    return manifest

def copy_runtime(source):
    actual = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    if actual != COMMIT:
        raise RuntimeError('Source checkout must be at ' + COMMIT)
    manifest = verify(source)
    for name in manifest:
        destination = ROOT / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / name, destination)
    verify(ROOT)
    print('Verified and prepared', len(manifest), 'runtime files.')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, help='Existing pinned checkout with Git LFS files hydrated')
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    if args.verify_only:
        print('Verified', len(verify(ROOT)), 'runtime files.')
    elif args.source:
        copy_runtime(args.source.resolve())
    else:
        with tempfile.TemporaryDirectory(prefix='androidtavern-runtime-') as temporary:
            source = Path(temporary) / 'upstream'
            env = os.environ.copy()
            env['GIT_LFS_SKIP_SMUDGE'] = '1'
            def run(*command):
                subprocess.run(command, check=True, env=env)
            run('git', 'init', str(source))
            run('git', '-C', str(source), 'remote', 'add', 'origin', UPSTREAM)
            run('git', '-C', str(source), 'fetch', '--depth', '1', 'origin', COMMIT)
            run('git', '-C', str(source), 'checkout', '--detach', 'FETCH_HEAD')
            run('git', '-C', str(source), 'lfs', 'pull', '--include=app/src/main/assets/**,app/src/main/jniLibs/**')
            copy_runtime(source)

if __name__ == '__main__':
    main()
