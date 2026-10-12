# Sistem visual

Dipakai untuk diagram yang ditulis tangan (SVG/HTML), dan sebagai acuan saat memakai alat lain (draw.io, FigJam): pilih warna dan ukuran yang paling mendekati.

## Token warna

```css
:root{
  /* netral */
  --bg:#EEF1F6;      /* latar halaman */
  --paper:#FFFFFF;   /* panel bagan */
  --lane:#F5F7FA;    /* pita jalur / zona: netral, BUKAN berwarna tipis */
  --card:#FFFFFF;    /* kartu */
  --ink:#0F172A;     /* teks utama */
  --muted:#64748B;   /* teks keterangan */
  --shadow:rgba(15,23,42,.10);

  /* kategori: dipakai PENUH di tab jalur dan lingkaran ikon saja */
  --ink-cat:#0F172A; --violet:#7C3AED; --blue:#2563EB; --teal:#0D9488; --amber:#B45309; --orange:#C2410C;

  /* makna tetap */
  --flow:#334155;    /* garis alur */
  --rel:#16A34A;     /* rilis / hasil akhir / sukses */
  --bad:#E11D48;     /* masalah, risiko, langkah manual bermasalah */
}
/* gelap */
--bg:#080C16; --paper:#0F1522; --lane:#161E2E; --card:#1C2638; --ink:#EEF2F8; --muted:#94A3B8;
--flow:#CBD5E1; --rel:#4ADE80; --bad:#FB7185; --shadow:rgba(0,0,0,.45);
--violet:#8B5CF6; --blue:#3B82F6; --teal:#14B8A6; --amber:#D97706; --ink-cat:#475569;
```

Kenapa begini: kesan "kusam" muncul ketika setiap area diberi warna setengah hati (latar 4–8% plus garis abu). Mata tidak menemukan titik tegas. Dengan latar netral, kartu putih, dan warna penuh di tempat sempit, warnanya terasa hidup tanpa membuat ramai.

## Tipografi

- Font: **Plus Jakarta Sans** (Google Fonts), cadangan `"Segoe UI", system-ui, sans-serif`. Monospace **JetBrains Mono** untuk nomor, kode, dan label huruf kapital kecil.
- Ukuran di dalam SVG. Bagan selebar ± 1900 unit tampil mengecil ke ± 0,7× di layar 1440 px, jadi angka di SVG sengaja lebih besar:
  - judul kartu 18,5 tebal 700 (tampil ± 13 px)
  - keterangan kartu 15 tebal 500, warna `--muted` (tampil ± 11 px)
  - label garis 13,5 tebal 600
  - nomor/penanda 11–13 monospace
- Judul halaman 26–44 px tebal 800, jarak huruf −0,02em.

## Bentuk

- Kartu: sudut 12 px, bayangan `0 2px 6px var(--shadow)`, tanpa garis tepi.
- Tab jalur/zona: sudut 14 px, isi warna penuh, teks putih.
- Ikon: lingkaran r 17 px berwarna kategori, ikon garis putih tebal 1,7 px di tengahnya.
- Penanda masalah: pil merah, teks putih monospace. Di atas tab berwarna, pil putih dengan teks merah.
- Garis: alur 2 px, rilis 3 px, sudut belok dibulatkan 8 px, kepala panah segitiga kecil.

## Ritme dan ruang

- Semua kartu dalam satu bagan sama ukuran (bawaan 150 × 120).
- Jarak antar-kolom seragam (bawaan pitch 166 → celah 16 px untuk jalur garis).
- Tinggi jalur seragam (150) dengan jarak 10 px.
- Legenda, daftar penanda, sumber: di bawah bagan dalam HTML biasa, dua kolom.

## Bila memakai alat lain

- **draw.io**: pakai kotak bulat putih dengan bayangan, kontainer jalur (`swimlane`) dengan warna header penuh, konektor `orthogonalEdgeStyle` dengan `rounded=1`. Hindari isian berwarna pucat di setiap kotak.
- **FigJam/Figma**: kartu putih, section berwarna hanya di judulnya.
- **Mermaid**: tampilannya terbatas. Pakai `flowchart LR`, `subgraph` per jalur, dan `classDef` dengan isian putih plus garis berwarna. Jangan harapkan hasil setara SVG tulis tangan.
