#!/usr/bin/env python3
"""QRコード生成スクリプト

Usage:
    python generate_qr.py https://your-domain.com
    python generate_qr.py https://your-domain.com -o my_qr.png
"""
import argparse

import qrcode


def generate_qr(url: str, output: str = "survey_qr.png") -> None:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output)
    print(f"QRコードを生成しました: {output}")
    print(f"URL: {url}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="アンケートURL用QRコード生成")
    parser.add_argument("url", help="アンケートページのURL")
    parser.add_argument("-o", "--output", default="survey_qr.png", help="出力ファイル名")
    args = parser.parse_args()
    generate_qr(args.url, args.output)
