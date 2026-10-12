# Prompt untuk gambar AI (Nano Banana Pro, GPT Image)

Claude tidak membuat gambar raster sendiri. Bila pengguna butuh infografis padat bergaya poster untuk media sosial, tuliskan prompt siap tempel untuk Gemini (Nano Banana Pro) atau ChatGPT (GPT Image), lalu ingatkan risikonya.

## Kapan cocok

- Infografis ringkas untuk unggahan, sampul, atau poster.
- Isi sudah final dan pendek; tidak perlu disunting nanti.

## Kapan tidak cocok

- Dokumen kerja, arsitektur yang akan berubah, atau isi dengan banyak angka. Model gambar masih bisa salah menulis label, menghilangkan nomor, atau mengarang teks. Pakai HTML/SVG atau draw.io.

## Kerangka prompt

```
Buat infografis [rasio, mis. 4:5 atau 16:9] berjudul "[JUDUL]".
Gaya: bersih dan modern, latar [putih/abu sangat muda], kartu putih dengan sudut membulat dan bayangan halus,
warna aksen tegas hanya di header bagian dan ikon: [warna 1], [warna 2], [warna 3]. Font sans-serif modern.
Tata letak: [jenis bagan, mis. swimlane 4 jalur kiri→kanan / 6 panel bernomor dalam grid 3×2].
Isi, tulis PERSIS seperti ini tanpa menambah teks lain:
- Bagian 1 "[judul]": [poin], [poin]
- Bagian 2 "[judul]": ...
Panah: [dari] → [ke] → [ke].
Jangan menambahkan logo, angka, atau teks yang tidak tercantum di atas.
```

## Setelah gambar jadi

Minta pengguna mencocokkan setiap label dan angka dengan sumbernya. Kesalahan umum: nomor urut melompat, huruf tertukar, kata terpotong, dan teks tambahan yang tidak diminta.

## Menjalankan langsung lewat API

Bila pengguna memberi kunci Gemini API, simpan di berkas privat di luar repo (izin 600) atau di variabel lingkungan, lalu:

```bash
GEMINI_API_KEY_FILE=/path/ke/berkas-kunci python3 scripts/gambar_ai.py prompt.txt hasil.png --model gemini-3-pro-image --rasio 16:9
```

- Jangan menulis kunci ke skill, repo, prompt, atau balasan.
- Model gambar di Gemini API tidak punya kuota gratis. Teruji 12 Okt 2026: `gemini-3-pro-image`, `gemini-3.1-flash-image`, dan `gemini-3.1-flash-lite-image` semuanya berbatas 0 di tier gratis. Untuk trial gratis, arahkan pengguna ke aplikasi Gemini (gemini.google.com) dengan prompt siap tempel. Respons `429 ... free_tier_requests, limit: 0` berarti penagihan (billing) belum aktif di proyek Google AI Studio itu, bukan kuncinya salah. Jangan mencoba berulang; sampaikan ke pengguna.
- Daftar model yang tersedia bisa dicek dengan `GET https://generativelanguage.googleapis.com/v1beta/models` memakai header `X-goog-api-key`.
- Buat satu gambar, periksa, baru ulangi. Setiap panggilan berbayar.
