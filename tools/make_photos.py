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


MIN_QUALITY = 62   # 이 아래로는 어두운 실내 사진에서 블록 노이즈가 눈에 띈다.


def _fit(im, edge):
    if max(im.size) <= edge:
        return im
    ratio = edge / float(max(im.size))
    return im.resize((max(1, int(im.width * ratio)), max(1, int(im.height * ratio))), Image.LANCZOS)


def encode(src, dst, target=TARGET_BYTES, max_edge=MAX_EDGE):
    """목표 용량 안에서 '품질 우선'으로 인코딩한다.

    같은 30KB라면 해상도를 낮추고 품질을 지키는 쪽이 더 깨끗하다.
    갤러리 카드는 실제로 360px 안팎으로 표시되므로 700~800px이면 2x 화면에도 충분하다.
    """
    im = Image.open(src).convert("RGB")

    # 큰 해상도부터 시도하되 품질 하한(MIN_QUALITY)을 지킬 수 있는 조합만 채택.
    for edge in (max_edge, 1000, 900, 800, 700, 600):
        cur = _fit(im, edge)
        for q in range(88, MIN_QUALITY - 1, -3):
            cur.save(dst, "WEBP", quality=q, method=6)
            if os.path.getsize(dst) <= target:
                return cur.size, q, os.path.getsize(dst)

    # 최소 해상도에서도 안 맞으면 그때만 품질을 더 낮춘다.
    cur = _fit(im, 600)
    for q in range(MIN_QUALITY, 29, -4):
        cur.save(dst, "WEBP", quality=q, method=6)
        if os.path.getsize(dst) <= target:
            break
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
