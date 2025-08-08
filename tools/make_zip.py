import os
import zipfile
import hashlib

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
APP_DIR = os.path.join(ROOT, 'app')
OUT_DIR = ROOT
VERSION_PATH = os.path.join(ROOT, 'VERSION')

# 패키징 대상 디렉터리(루트 기준) → zip 내부 경로는 app/<dir>/...
SOURCE_DIRS = [
    'ui',
    'ZIdentity',
    'Zscaler_Internet_Access',
    'Zscaler_Private_access',
]

# 패키징 대상 개별 파일(루트 기준) → zip 내부 경로는 app/<file>
SOURCE_FILES = [
    os.path.join('app', 'main.py'),
    os.path.join('app', 'ssl_verify.py'),
    # 루트 인증서가 있으면 app/로 포함
    'zscaler_root_ca.cer',
]


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def make_zip(version: str) -> str:
    zip_name = f'package-{version}.zip'
    zip_path = os.path.join(OUT_DIR, zip_name)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # 디렉터리들 포함 (ui, ZIdentity, Zscaler_*) → zip 내부는 app/<dir>/...
        for d in SOURCE_DIRS:
            src_dir = os.path.join(ROOT, d)
            if not os.path.isdir(src_dir):
                continue
            for base, _, files in os.walk(src_dir):
                for fn in files:
                    p = os.path.join(base, fn)
                    rel_from_root = os.path.relpath(p, ROOT)
                    rel_in_zip = os.path.join('app', rel_from_root)
                    zf.write(p, rel_in_zip)

        # 개별 파일 포함 (app/main.py, app/ssl_verify.py, 루트 인증서 등)
        for f in SOURCE_FILES:
            src = os.path.join(ROOT, f)
            if os.path.exists(src):
                # app/main.py 등은 이미 app/ 경로를 포함한 상대경로이므로 그대로 사용
                rel_in_zip = f if f.startswith('app' + os.sep) else os.path.join('app', os.path.basename(f))
                zf.write(src, rel_in_zip)

        # VERSION 포함
        if os.path.exists(VERSION_PATH):
            zf.write(VERSION_PATH, 'VERSION')

    print('ZIP:', zip_path)
    print('SHA256:', sha256_file(zip_path))
    return zip_path


if __name__ == '__main__':
    version = (open(VERSION_PATH, 'r', encoding='utf-8').read().strip()
               if os.path.exists(VERSION_PATH) else '0.0.0')
    make_zip(version)

