#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""매장 원본 사진을 메인페이지 갤러리용 webp로 변환한다.

사용법:
    python3 tools/make_photos.py <원본1> <원본2> <원본3> ...

- 출력: assets/photos/<GALLERY에 정의된 파일명> (순서대로 매칭)
- 목표 용량 30KB 이하를 만족하도록 품질을 자동으로 낮춰가며 인코딩
- 세로 사진 기준 긴 변 1200px로 축소 (갤러리는 3/4 비율로 크롭 표시)

의존성: Pillow (pip install Pillow)
"""
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "assets", "photos")
TARGET_BYTES = 30 * 1024
MAX_EDGE = 1200
NAMES = ["exterior-sign.webp", "room-interior.webp", "room-styler.webp"]


def encode(src, dst, target=TARGET_BYTES, max_edge=MAX_EDGE):
    im = Image.open(src)
    im = im.convert("RGB")
    if max(im.size) > max_edge:
        ratio = max_edge / float(max(im.size))
        im = im.resize((max(1, int(im.width * ratio)), max(1, int(im.height * ratio))), Image.LANCZOS)

    # 품질을 낮춰가며 목표 용량을 맞추고, 그래도 크면 해상도를 단계적으로 줄인다.
    for edge in (max_edge, int(max_edge * 0.85), int(max_edge * 0.7)):
        cur = im
        if max(cur.size) > edge:
            ratio = edge / float(max(cur.size))
            cur = im.resize((max(1, int(im.width * ratio)), max(1, int(im.height * ratio))), Image.LANCZOS)
        for q in range(82, 29, -4):
            cur.save(dst, "WEBP", quality=q, method=6)
            if os.path.getsize(dst) <= target:
                return cur.size, q, os.path.getsize(dst)
    return cur.size, q, os.path.getsize(dst)


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    os.makedirs(OUT_DIR, exist_ok=True)
    for i, src in enumerate(argv):
        if i >= len(NAMES):
            print("건너뜀(정의된 슬롯 초과): {}".format(src))
            continue
        dst = os.path.join(OUT_DIR, NAMES[i])
        size, q, nbytes = encode(src, dst)
        print("{} -> assets/photos/{}  {}x{}  q={}  {:.1f}KB".format(
            os.path.basename(src), NAMES[i], size[0], size[1], q, nbytes / 1024.0))
    print("변환 완료. 이어서 `python3 generate.py` 를 실행하세요.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
