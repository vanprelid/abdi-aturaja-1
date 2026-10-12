#!/usr/bin/env python3
"""Buat gambar infografis lewat Gemini API (Nano Banana) dan simpan sebagai PNG.

Pemakaian:
    GEMINI_API_KEY=... python3 gambar_ai.py prompt.txt keluaran.png [--model gemini-3-pro-image] [--rasio 16:9]

Kunci dibaca dari variabel lingkungan GEMINI_API_KEY (atau dari berkas yang ditunjuk
GEMINI_API_KEY_FILE). Jangan pernah menulis kunci ke dalam skill, repo, atau prompt.
Setiap panggilan berbayar sesuai tarif Google; buat satu gambar dulu, lihat, baru ulangi.
"""
import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request

API = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def kunci():
    k = os.environ.get("GEMINI_API_KEY", "").strip()
    if not k and os.environ.get("GEMINI_API_KEY_FILE"):
        k = open(os.environ["GEMINI_API_KEY_FILE"]).read().strip()
    if not k:
        sys.exit("GEMINI_API_KEY belum diset.")
    return k


def main():
    p = argparse.ArgumentParser()
    p.add_argument("prompt_file")
    p.add_argument("out_png")
    p.add_argument("--model", default="gemini-3-pro-image")
    p.add_argument("--rasio", default="16:9")
    p.add_argument("--ukuran", default="2K", help="1K, 2K, atau 4K (bila model mendukung)")
    a = p.parse_args()

    body = {
        "contents": [{"parts": [{"text": open(a.prompt_file, encoding="utf-8").read()}]}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "imageConfig": {"aspectRatio": a.rasio, "imageSize": a.ukuran},
        },
    }
    req = urllib.request.Request(
        API.format(model=a.model),
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "X-goog-api-key": kunci()},
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode()[:600]}")

    saved = False
    for cand in data.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            if "inlineData" in part:
                open(a.out_png, "wb").write(base64.b64decode(part["inlineData"]["data"]))
                saved = True
            elif part.get("text"):
                print("Catatan model:", part["text"][:400])
    if not saved:
        sys.exit("Tidak ada gambar di respons: " + json.dumps(data)[:600])
    print("Disimpan:", a.out_png)
    print("Ingat: cocokkan setiap label dan angka di gambar dengan sumbernya.")


if __name__ == "__main__":
    main()
