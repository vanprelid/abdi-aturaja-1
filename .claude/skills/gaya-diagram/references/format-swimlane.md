# Format spesifikasi swimlane

`scripts/swimlane.py` membaca satu berkas JSON dan menulis satu halaman HTML siap terbit (Artifact) atau siap dibuka di browser. Contoh lengkap yang sudah diterima pengguna: `assets/contoh-swimlane-arsitektur.json`.

## Kunci tingkat atas

| Kunci | Wajib | Isi |
|---|---|---|
| `judul` | ya | Nama halaman dan judul besar. Nama, bukan kalimat. |
| `eyebrow` | tidak | Label kecil di atas judul, misalnya konteks dan tanggal. |
| `deskripsi` | tidak | Satu kalimat: apa yang ditunjukkan dan cara membacanya. |
| `aria` | tidak | Kalimat untuk pembaca layar; sebaiknya meringkas alurnya. |
| `lingkup` | tidak | `{ "judul": "...", "isi": "..." }`, kotak kecil di kanan atas untuk batas gambar (apa yang tidak digambar). |
| `jalur` | ya | Daftar jalur dari atas ke bawah. |
| `langkah` | ya | Kartu utama. |
| `garis` | tidak | Sambungan antar-kartu. Bila dihilangkan, kartu disambung urut kolom dengan garis alur. |
| `sampingan` | tidak | Kartu bergaris putus-putus untuk jalur samping (misalnya cara lama yang bermasalah). |
| `legenda` | tidak | Ganti teks legenda per jenis: `alur`, `rilis`, `manual`, `info`, `penanda`. |
| `daftar_penanda` | tidak | `{ "judul": "...", "isi": [{ "kode": "P1", "teks": "..." }] }`, daftar penjelasan penanda di bawah bagan. |
| `siklus` | tidak | `{ "pengantar": "...", "langkah": ["a", "b"], "sorot_terakhir": true }`, pita kecil di bawah bagan. |
| `sumber` | tidak | Baris sumber di kaki halaman, termasuk bagian yang tafsiran. |

## Jalur

```json
{"id": "srv", "nama": "Server ANS-1A", "sub": "1 VPS · 1 user", "warna": "blue", "ikon": "server", "penanda": ["P6"]}
```

- `warna`: `ink`, `violet`, `blue`, `teal`, `amber`, `rose`, `green`, `orange`. Pakai maksimal 4 jalur berbeda warna; hindari `rose` untuk jalur karena merah dipakai penanda masalah, dan `green` karena dipakai jalur rilis.
- `sub`: ± 22 huruf maksimal.
- `penanda`: penanda yang berlaku untuk seluruh jalur.

## Langkah (kartu utama)

```json
{"id": "agent", "kolom": 4, "jalur": "srv", "ikon": "hub", "judul": "Agent utama", "ket": ["sesi Claude Code,", "membagi tugas"], "penanda": ["P1"], "nomor": true}
```

- `kolom` dimulai dari 1. Satu kolom = satu langkah waktu. Satu jalur+kolom hanya boleh berisi satu kartu.
- `judul` ± 12 huruf, `ket` maksimal 2 baris, ± 16 huruf per baris. Generator memperkirakan lebar huruf dan memberi PERINGATAN bila kemungkinan meluber.
- `nomor`: tampilkan nomor kolom (bawaan `true`). Matikan bila urutan bukan informasi.
- Aktor yang muncul lagi di tahap belakang dibuat sebagai kartu baru di kolom baru, bukan ditarik garis mundur.

Ikon yang tersedia: `person`, `users`, `crown`, `chat`, `mail`, `hub`, `tool`, `branch`, `check`, `rocket`, `store`, `laptop`, `server`, `cloud`, `doc`, `database`, `lock`, `chart`, `phone`, `globe`, `flag`, `search`, `bell`, `gear`, `spark`.

## Garis

```json
{"dari": "restu", "ke": "rilis", "jenis": "rilis", "label": "setelah Merge"}
```

- `jenis`: `alur` (bawaan, gelap netral), `rilis` (hijau tebal), `manual` (merah putus-putus, bergerak), `info` (titik-titik abu).
- Garis hanya merutekan ke kanan (`kolom` tujuan > asal). Garis beda jalur berbelok di celah tepat sebelum kolom tujuan.
- Label opsional, 1–3 kata.
- Generator memperingatkan bila garis berisiko menembus kartu di jalur asal. Jalan keluarnya: pindahkan kartu ke kolom bersebelahan, atau pecah alurnya.
- Putaran berulang (misalnya permintaan perubahan yang kembali ke tahap sebelumnya) tidak digambar sebagai garis mundur. Tuliskan sebagai pita `siklus` di bawah bagan.

## Sampingan

```json
{"jalur": "lap", "kolom": 3, "lebar_kolom": 1.4, "dari": "cowork", "judul": "Claude Code lokal", "ket": ["...", "..."], "penanda": ["P10"], "jenis": "manual"}
```

Kartu tanpa isi warna, bergaris putus-putus, disambung mendatar dari kartu `dari` yang sejalur. Cocok untuk cara kerja lama, jalan pintas, atau sistem pendamping yang bukan bagian alur utama. Pakai paling banyak satu atau dua per bagan.

## Setelah menghasilkan

1. Baca semua PERINGATAN dan perbaiki spesifikasinya, bukan HTML-nya.
2. Jalankan `node scripts/render_check.js halaman.html folder/` dan lihat screenshot-nya.
3. Terbitkan halaman HTML itu sebagai Artifact (atau kirim berkasnya).
