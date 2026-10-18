#!/usr/bin/env python3
"""Test the bundled payload on the host. This is NOT an Android acceptance test.

Routes verified against upstream 1.18.0 at 51ad27fb86d39a3daca3adaa970375c9670c12df:
src/server-main.js, src/endpoints/characters.js, src/endpoints/worldinfo.js.
No model endpoint or private user data is used.
"""
import argparse
import http.cookiejar
import json
from pathlib import Path
import socket
import subprocess
import time
import urllib.error
import urllib.request
import uuid


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--payload', type=Path, required=True)
    p.add_argument('--work', type=Path, required=True)
    args = p.parse_args()
    work = args.work.resolve(); work.mkdir(parents=True, exist_ok=True)
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0)); port = sock.getsockname()[1]
    base = f'http://127.0.0.1:{port}'
    op = urllib.request.build_opener(urllib.request.ProxyHandler({}),
            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    headers = {}

    def call(path, data=None, files=None):
        h = headers.copy()
        if files:
            boundary = 'pilot-' + uuid.uuid4().hex; parts = []
            for k, v in (data or {}).items():
                parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
            for k, (name, body) in files.items():
                parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"; filename="{name}"\r\nContent-Type: application/json\r\n\r\n'.encode() + body + b'\r\n')
            parts.append(f'--{boundary}--\r\n'.encode()); payload = b''.join(parts)
            h['Content-Type'] = 'multipart/form-data; boundary=' + boundary
        elif data is not None:
            payload = json.dumps(data).encode(); h['Content-Type'] = 'application/json'
        else:
            payload = None
        with op.open(urllib.request.Request(base + path, data=payload, headers=h), timeout=30) as r:
            return r.status, r.read()

    with (work / 'server.log').open('w') as log:
        proc = subprocess.Popen(['node', 'server.js', '--port', str(port), '--listen', 'false',
                '--browserLaunchEnabled', 'false', '--dataRoot', str(work / 'data'),
                '--configPath', str(work / 'config.yaml')], cwd=args.payload.resolve(),
                stdout=log, stderr=subprocess.STDOUT)
        try:
            deadline = time.monotonic() + 50
            while True:
                try:
                    status, _ = call('/'); assert status == 200; break
                except urllib.error.URLError:
                    if proc.poll() is not None or time.monotonic() > deadline:
                        raise RuntimeError('Server startup failed; inspect ' + str(work / 'server.log'))
                    time.sleep(0.25)
            checks = {'frontend_http': 200}
            headers['X-CSRF-Token'] = json.loads(call('/csrf-token')[1])['token']
            assert call('/api/ping', {})[0] == 204; checks['session_ping'] = 204
            world = {'entries': {'0': {'uid': 0, 'key': ['test'], 'content': '本地兼容测试', 'constant': False, 'disable': False}}}
            name = json.loads(call('/api/worldinfo/import', {}, {'avatar': ('pilot-world.json', json.dumps(world).encode())})[1])['name']
            assert json.loads(call('/api/worldinfo/get', {'name': name})[1]) == world
            checks['worldbook_roundtrip'] = 'pass'
            card = {'spec': 'chara_card_v2', 'spec_version': '2.0', 'data': {
                'name': 'Pilot test', 'description': 'Local smoke test', 'personality': '',
                'scenario': '', 'first_mes': '你好', 'mes_example': '', 'creator_notes': '',
                'system_prompt': '', 'post_history_instructions': '', 'alternate_greetings': [],
                'tags': [], 'creator': 'Local test', 'character_version': '1',
                'extensions': {'pilot_test': {'keep': True}},
                'character_book': {'name': 'Embedded test', 'entries': []}}}
            avatar = json.loads(call('/api/characters/import', {'file_type': 'json'},
                    {'avatar': ('pilot-card.json', json.dumps(card).encode())})[1])['file_name'] + '.png'
            out = json.loads(call('/api/characters/export', {'avatar_url': avatar, 'format': 'json'})[1])
            assert out['data']['name'] == 'Pilot test'
            assert out['data']['extensions']['pilot_test']['keep'] is True
            assert out['data']['character_book']['name'] == 'Embedded test'
            checks['card_json_and_custom_fields'] = 'pass'
            assert call('/api/characters/export', {'avatar_url': avatar, 'format': 'png'})[1].startswith(b'\x89PNG')
            checks['card_png_export'] = 'pass'
            checks['scope'] = 'Host test only; Android, background generation and extensions remain unverified'
            (work / 'result.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2))
            print(json.dumps(checks, ensure_ascii=False))
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill(); proc.wait()


if __name__ == '__main__':
    main()
