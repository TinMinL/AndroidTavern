#!/usr/bin/env python3
"""Build this dependency-free Android wrapper with official SDK tools, no Gradle.

Requires JDK 17, Android SDK platform 34 and build-tools 34.0.0, and Git LFS
assets. Produces a TEST-SIGNED APK. Keep the keystore to install later previews
as updates; never use this development key for a public release.
"""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import xml.etree.ElementTree as ET
import zipfile
from prepare_runtime import verify


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sdk', required=True, type=Path)
    parser.add_argument('--jdk', required=True, type=Path)
    parser.add_argument('--keystore', required=True, type=Path)
    parser.add_argument('--ci', action='store_true', help='Use a separate application ID and launcher labels')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    out = root / 'build' / 'pilot'
    if out.exists():
        shutil.rmtree(out)  # Only this script's reproducible build directory.
    out.mkdir(parents=True)
    sdk = args.sdk.resolve()
    jdk = args.jdk.resolve()
    bt = sdk / 'build-tools' / '34.0.0'
    android = sdk / 'platforms' / 'android-34' / 'android.jar'
    env = os.environ.copy()
    env['JAVA_HOME'] = str(jdk)
    env['PATH'] = str(jdk / 'bin') + os.pathsep + env.get('PATH', '')

    def run(command):
        subprocess.run([str(x) for x in command], check=True, env=env, cwd=root)

    assets = root / 'app/src/main/assets'
    native = root / 'app/src/main/jniLibs'
    verify(root)
    for p in [*assets.glob('*.zip'), *native.rglob('*.so')]:
        with p.open('rb') as stream:
            magic = stream.read(4)
        if magic != (b'PK\x03\x04' if p.suffix == '.zip' else b'\x7fELF'):
            raise RuntimeError('Missing/corrupt binary or LFS pointer: ' + str(p))

    # AGP normally expands namespace-relative class names. Do it explicitly.
    ns = 'http://schemas.android.com/apk/res/android'
    ET.register_namespace('android', ns)
    manifest = ET.parse(root / 'app/src/main/AndroidManifest.xml')
    manifest.getroot().set('package', 'com.sillytavern.localpilot' + ('.ci' if args.ci else ''))
    for element in manifest.iter():
        for attr in ['name', 'targetActivity']:
            key = '{' + ns + '}' + attr
            value = element.get(key, '')
            if value.startswith('.'):
                element.set(key, 'com.sillytavern.app' + value)
    if args.ci:
        manifest.find('application').set('{' + ns + '}label', '酒馆 CI·管理')
        for alias in manifest.findall('application/activity-alias'):
            alias.set('{' + ns + '}label', '酒馆 CI ' + alias.get('{' + ns + '}name').split('Inst')[-1].replace('Alias', ''))
    manifest.write(out / 'AndroidManifest.xml', encoding='utf-8', xml_declaration=True)
    gen = out / 'generated'; gen.mkdir()
    classes = out / 'classes'; classes.mkdir()
    dex = out / 'dex'; dex.mkdir()
    run([bt / 'aapt2', 'compile', '--dir', root / 'app/src/main/res', '-o', out / 'resources.zip'])
    run([bt / 'aapt2', 'link', '-o', out / 'base.apk', '-I', android,
         '--manifest', out / 'AndroidManifest.xml', '--java', gen,
         '--custom-package', 'com.sillytavern.app', '--min-sdk-version', '24',
         '--target-sdk-version', '34', '--version-code', '1',
         '--version-name', '0.1.0-preview.1', out / 'resources.zip'])
    java_files = sorted((root / 'app/src/main/java').rglob('*.java')) + list(gen.rglob('*.java'))
    run([jdk / 'bin/javac', '-encoding', 'UTF-8', '-source', '8', '-target', '8',
         '-bootclasspath', android, '-classpath', bt / 'core-lambda-stubs.jar',
         '-d', classes, *java_files])
    run([jdk / 'bin/jar', 'cf', out / 'classes.jar', '-C', classes, '.'])
    run([bt / 'd8', '--release', '--min-api', '24', '--lib', android,
         '--output', dex, out / 'classes.jar'])
    with zipfile.ZipFile(out / 'base.apk', 'a') as apk:
        for p in sorted(dex.glob('*.dex')):
            apk.write(p, p.name, compress_type=zipfile.ZIP_DEFLATED)
        for p in sorted(assets.rglob('*')):
            if p.is_file():
                apk.write(p, 'assets/' + p.relative_to(assets).as_posix(),
                          compress_type=zipfile.ZIP_STORED)
        for p in sorted(native.rglob('*.so')):
            apk.write(p, 'lib/' + p.relative_to(native).as_posix(),
                      compress_type=zipfile.ZIP_DEFLATED)
    run([bt / 'zipalign', '-f', '4', out / 'base.apk', out / 'aligned.apk'])
    key = args.keystore.resolve()
    if not key.exists():
        key.parent.mkdir(parents=True, exist_ok=True)
        run([jdk / 'bin/keytool', '-genkeypair', '-keystore', key, '-storepass', 'android',
             '-keypass', 'android', '-alias', 'pilot-test', '-keyalg', 'RSA', '-keysize', '2048',
             '-validity', '10000', '-dname', 'CN=SillyTavern Local Pilot Test, O=Private Development, C=ZZ'])
        key.chmod(0o600)
    target = out / ('SillyTavern-Pilot-0.1.0-preview.1' + ('-ci' if args.ci else '') + '-arm64.apk')
    run([bt / 'apksigner', 'sign', '--ks', key, '--ks-key-alias', 'pilot-test',
         '--ks-pass', 'pass:android', '--key-pass', 'pass:android', '--out', target, out / 'aligned.apk'])
    run([bt / 'apksigner', 'verify', '--verbose', '--print-certs', target])
    run([bt / 'zipalign', '-c', '4', target])
    print('APK:', target)


if __name__ == '__main__':
    main()
