---
name: gaya-diagram
description: Cara membuat diagram, bagan alur, arsitektur sistem, swimlane, peta proses, flowchart, peta pikiran, tangga kematangan, atau infografis yang rapi, lega, tegas warnanya, dan enak dilihat — bukan penuh, pudar, dan bertumpuk. Pakai skill ini setiap kali diminta memvisualisasikan sesuatu sebagai bagan atau diagram (system design, alur kerja, alur klien, pemetaan dokumen, "gambarkan", "visualisasikan", "bikin bagan", "buat alurnya", "petakan"), juga saat memilih alat (HTML/SVG, draw.io, Excalidraw, FigJam, Mermaid, gambar AI) atau saat memperbaiki diagram yang dinilai jelek, ramai, atau kusam. Use for any diagram, flowchart, architecture, swimlane, or infographic request, even if the user only says "visualize this".
---

# Gaya Diagram

Skill ini lahir dari satu pelajaran nyata. Versi pertama sebuah bagan arsitektur ditolak karena "penuh, bertumpukan, warna pudar dan kusam, tidak rapi". Isinya benar, tapi semua hal dimasukkan: 35 kotak, kode di tiap kotak, 11 lencana, garis memutar keliling bagan, dan latar berwarna tipis di mana-mana. Versi kedua dibuat ulang sebagai swimlane dengan 10 kartu, garis siku pendek, dan warna tegas hanya di dua tempat, lalu diterima. Selisih keduanya bukan alat, melainkan keputusan desain. Skill ini menuliskan keputusan-keputusan itu supaya percobaan pertama sudah mendekati versi kedua.

Contoh versi yang diterima ada di `assets/contoh-swimlane-arsitektur.html`. Buka bila perlu acuan rasa.

## Alur kerja

### 1. Tentukan pertanyaan yang dijawab diagram

Tulis satu kalimat: "Setelah melihat bagan ini, pembaca paham ___." Lalu tentukan pembacanya (Owner non-teknis, engineer, klien). Diagram yang mencoba menjawab semua pertanyaan sekaligus berakhir penuh. Bila sumbernya panjang (brief, dokumen), pilih satu sudut pandang dan katakan sudut yang tidak diambil, jangan menjejalkan semuanya.

Bila sumber tidak memuat sesuatu (misalnya "arsitektur ideal" yang belum diriset), jangan mengarangnya diam-diam. Gambar yang ada, dan sebut batasnya di halaman.

### 2. Pilih jenis bagan dari bentuk pertanyaannya

| Pertanyaan pembaca | Jenis bagan | Catatan |
|---|---|---|
| Siapa mengerjakan apa, urutannya bagaimana, lintas pihak/tempat | **Swimlane** | Pilihan utama untuk alur kerja ujung ke ujung dan arsitektur "as-is". Ada generatornya. |
| Komponen apa ada di lapisan mana | **Diagram lapisan** (layered) | Tumpukan horizontal: pengguna → antarmuka → layanan → data. |
| Siapa memanggil siapa, dalam urutan waktu | **Sequence diagram** | Untuk interaksi antar-sistem yang detail. |
| Sesuatu berpindah status apa saja | **State diagram** | Status sebagai kotak, transisi sebagai panah berlabel. |
| Apa beda sekarang dan nanti | **Sebelum / sesudah** berdampingan | Tandai satu-dua perubahan yang menentukan. |
| Dari mana ke mana bertahap | **Tangga / timeline** | Gambaran ideal di atas tetap utuh, tangga terpisah. |
| Bagaimana topik bercabang | **Peta pikiran / pohon** | Maksimal 3 tingkat. |
| Satu pusat dengan banyak sambungan | **Hub and spoke** | Untuk integrasi, alat, kanal. |

Jenis bagan yang tepat sudah menyelesaikan separuh masalah kerapian, karena setiap elemen punya tempat yang pasti.

### 3. Pilih medium

- **HTML + SVG tulis tangan** (bawaan): kendali penuh atas tampilan, mendukung mode gelap, bisa dianimasikan. Pakai generator swimlane bila jenisnya swimlane.
- **draw.io** (bila MCP-nya tersambung): saat pengguna perlu menyunting dan merawat diagram sendiri.
- **Excalidraw**: sketsa diskusi bergaya coret tangan. Bukan untuk dokumen resmi.
- **FigJam / Figma**: saat hasil akan dipoles manual atau dikomentari tim.
- **Mermaid**: diagram yang hidup di repo atau dokumen Markdown. Tampilan terbatas, jangan dipakai untuk hasil yang harus memukau.
- **Gambar AI** (Nano Banana Pro, GPT Image): infografis media sosial yang padat. Claude tidak membuat gambar sendiri. Bila kunci Gemini API tersedia di variabel lingkungan, `scripts/gambar_ai.py` bisa memanggilnya; bila tidak, tuliskan prompt siap tempel. Lihat `references/prompt-gambar-ai.md`, dan ingatkan bahwa setiap label dan angka harus dicek.
- **Animasi**: HTML dengan animasi CSS/SVG, direkam ke video dengan Playwright bila diminta video.

### 4. Pasang anggaran isi sebelum menggambar

Ini aturan yang paling sering dilanggar, jadi tetapkan angkanya di awal:

- **Kartu utama ≤ 12** per bagan. Lebih dari itu, pecah menjadi dua bagan atau kelompokkan.
- **Tiap kartu: judul ≤ 2 kata + maksimal 2 baris keterangan pendek** (± 16 huruf per baris). Penjelasan panjang pindah ke keterangan di bawah bagan.
- **Lencana/penanda ≤ 1 per kartu**, hanya di kartu yang memang bermasalah. Penanda yang berlaku untuk satu wilayah ditempel di label wilayahnya, bukan diulang di tiap kartu.
- **Satu bagan, satu sistem kode.** Bila ada dua lapisan informasi (misal masalah dan kode aspek), pilih satu untuk bagan, satu lagi untuk daftar di bawah.
- **Daftar rinci, legenda, dan sumber** ditaruh di bawah bagan dalam HTML biasa, bukan di dalam gambar.

Tanyakan pada setiap elemen: "Kalau ini dihapus, apakah pembaca kehilangan sesuatu yang penting untuk pertanyaan langkah 1?" Bila tidak, hapus.

### 5. Terapkan sistem visual

Token lengkap ada di `references/sistem-visual.md`. Prinsipnya:

- **Latar netral bersih, kartu putih.** Kartu dibedakan dari latar dengan bayangan halus, bukan garis tepi abu-abu tebal.
- **Warna tegas hanya di dua tempat:** tab/label wilayah (isi penuh, teks putih) dan lingkaran ikon di kartu. Jangan memberi semua area latar berwarna tipis 4–8%; itulah sumber kesan "pudar dan kusam".
- **Maksimal 4 warna kategori** + satu warna bahaya (merah) + satu warna sukses/rilis (hijau). Garis alur memakai warna gelap netral.
- **Satu keluarga huruf** (Plus Jakarta Sans) dengan tiga ukuran saja: judul kartu, keterangan, label kecil. Monospace hanya untuk nomor dan kode.
- **Ikon sederhana garis putih** di lingkaran berwarna. Ikon memberi kesan profesional jauh melebihi biayanya.
- **Mode terang dan gelap** didefinisikan sebagai token; warna kategori tetap jenuh di keduanya.

### 6. Atur tata letak dan garis

- **Grid ketat.** Semua kartu sama ukuran dalam satu bagan; jarak antar-kolom dan antar-jalur seragam.
- **Garis siku hanya lewat celah antar-kolom**, sudutnya dibulatkan. Tidak ada garis yang melintasi kartu dan sebisa mungkin tidak ada persilangan.
- **Jangan tarik garis panjang memutar.** Bila satu aktor muncul di dua tahap (misalnya Owner memberi arahan di awal dan restu di akhir), gambar dia dua kali sebagai dua langkah. Itu jauh lebih rapi daripada garis yang mengelilingi bagan.
- **Garis berlabel singkat** (1–3 kata) bila maknanya tidak jelas dari kartu. Bedakan jenis garis hanya bila maknanya berulang: alur biasa, jalur rilis (lebih tebal, hijau), langkah manual bermasalah (merah putus-putus).
- **Nomor langkah** hanya bila urutan memang informasi (01–10 di alur kerja), bukan hiasan.
- **Biarkan ruang kosong.** Bagan swimlane yang berzigzag memang menyisakan ruang; itu yang membuatnya terasa lega.

### 7. Render, lihat, perbaiki — sebelum diserahkan

Jangan menyerahkan diagram yang belum pernah dilihat. Render dengan:

```bash
node scripts/render_check.js halaman.html folder-output/
```

Script membuat screenshot terang, gelap, dan lebar ponsel, serta melaporkan bila halaman meluber ke samping. Lalu lihat gambarnya dan periksa dengan daftar di bawah, bukan hanya "ada yang bertumpuk atau tidak":

- Apakah dalam 5 detik mata langsung menemukan awal alur dan arahnya?
- Apakah ada area yang terasa penuh? Hitung kartu dan penanda terhadap anggaran langkah 4.
- Apakah warnanya tegas di tab dan ikon, sementara sisanya bersih? Atau semuanya setengah berwarna?
- Adakah teks meluber, terpotong, atau terlalu kecil (di bawah ± 11 px pada layar 1440 px)? Bagan lebar mengecil saat ditampilkan, jadi ukuran huruf di SVG harus lebih besar dari ukuran yang terlihat.
- Adakah garis yang bersilangan, menembus kartu, atau memutar jauh?
- Apakah mode gelap tetap terbaca?
- Di ponsel, bagan lebar memang digeser ke samping. Pastikan ada petunjuk "geser ke samping" dan halamannya sendiri tidak meluber.

Perbaiki satu putaran, render ulang, baru serahkan. Bila pengguna masih menilai kurang, minta mereka menyebut rasa yang salah (penuh, pudar, berantakan, kaku) dan perbaiki pada akar keputusannya, bukan menambal elemen satu per satu.

### 8. Serahkan dengan jujur

Sebutkan dalam satu-dua kalimat: jenis bagan yang dipilih dan alasannya, apa yang sengaja tidak digambar, dan bagian mana yang tafsiran (misalnya penempatan penanda masalah). Jangan menjelaskan kode warna dan font kecuali ditanya.

## Generator swimlane

Untuk swimlane, jangan menulis koordinat SVG dengan tangan. Tulis spesifikasi JSON dan jalankan:

```bash
python3 scripts/swimlane.py spesifikasi.json halaman.html
```

Generator menghitung posisi kartu, merutekan garis siku lewat celah, menambahkan ikon, lencana, legenda, dan token tema, lalu memperingatkan bila teks terlalu panjang untuk kartunya. Format JSON dan contoh lengkap ada di `references/format-swimlane.md`. Setelah itu tetap jalankan langkah 7.

## Anti-pola yang sudah terbukti ditolak

- Memasukkan semua isi sumber ke satu gambar.
- Latar berwarna tipis di setiap zona ditambah garis tepi abu-abu: kusam.
- Kode kecil abu-abu di pojok setiap kotak.
- Catatan miring di dalam gambar.
- Garis dari ujung kiri ke ujung kanan lewat atas atau bawah bagan.
- Mengecek hanya tumpang tindih, tanpa menilai rasa visual.
