from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION_PATH = ROOT / 'VERSION'


def run(cmd: list[str]) -> None:
    print('>', ' '.join(cmd))
    subprocess.check_call(cmd)


def main() -> None:
    if not VERSION_PATH.exists():
        print('VERSION 파일이 없습니다')
        sys.exit(2)
    version = VERSION_PATH.read_text(encoding='utf-8').strip()
    zip_name = f'package-{version}.zip'

    # git 태그 및 릴리스 초안 생성 (GitHub CLI 필요: gh)
    run(['git', 'tag', f'v{version}'])
    run(['git', 'push', '--tags'])

    # 릴리스 생성
    run(['gh', 'release', 'create', f'v{version}', zip_name, '--title', f'v{version}', '--notes', 'auto release'])

    # version.json 템플릿 출력
    owner_repo = os.environ.get('GH_REPO')  # 예: owner/repo
    if owner_repo:
        owner, repo = owner_repo.split('/', 1)
        version_json = {
            'version': version,
            'zip_url': f'https://github.com/{owner}/{repo}/releases/download/v{version}/{zip_name}',
            'sha256': '<fill-after-upload>',
            'restart_args': ['python', 'app/main.py'],
        }
        print(json.dumps(version_json, indent=2))


if __name__ == '__main__':
    main()

