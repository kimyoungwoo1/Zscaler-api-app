import os
import sys
import runpy


def main() -> None:
    base_dir = os.path.abspath(os.path.dirname(__file__))
    # app/ 하위 모듈들이 절대 import 가능하도록 경로 추가
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)
    ui_dir = os.path.join(base_dir, "ui")
    if os.path.isdir(ui_dir) and ui_dir not in sys.path:
        sys.path.insert(0, ui_dir)

    # 기존 스크립트 실행 흐름을 그대로 사용
    target = os.path.join(ui_dir, "main.py")
    if not os.path.exists(target):
        raise SystemExit(f"ui/main.py 를 찾을 수 없습니다: {target}")

    runpy.run_path(target, run_name="__main__")


if __name__ == "__main__":
    main()

