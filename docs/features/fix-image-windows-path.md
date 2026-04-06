# Fix Image Windows Path

**Kategori:** Asset Tool
**Tool:** ExToolbox → ImgWinPath

---

## Deskripsi

Tool **Fix Image Windows Path** digunakan untuk mendeteksi image yang pathnya hilang (missing) di dalam project Blender, lalu secara otomatis mencoba memperbaiki path tersebut.

Tool ini khusus menangani path yang berasal dari sistem Windows (format `A:\` atau `A:/`) dan mengonversinya ke format path Linux/network mount (`/mnt/A/`).

> **Catatan:** Tool ini hanya memperbaiki image yang sedang digunakan (users > 0). Image yang tidak terpakai akan dilewati.

---

## Prasyarat

Sebelum menggunakan tool ini, pastikan:

- Project sudah dibuka dan **disimpan** di Blender
- Terdapat image yang pathnya putus (missing) akibat perpindahan sistem operasi atau drive
- ExToolbox sudah terpasang dan aktif di 3D Viewport

---

## Cara Penggunaan

### Langkah 1 — Buka ExToolbox & Pilih Mode

Di **3D Viewport**, buka panel **ExToolbox** (sidebar `N`). Ubah **Select Mode** menjadi `ImgWinPath`.

![Pilih mode ImgWinPath di ExToolbox](../images/fix-image-windows-path-step-01.jpeg)

---

### Langkah 2 — Jalankan Check Missing Images

Klik tombol **"Check Missing Images"** untuk memulai proses pengecekan.

![Klik Check Missing Images](../images/fix-image-windows-path-step-02.jpeg)

---

### Langkah 3 — Verifikasi Hasil

Setelah proses selesai, lihat notifikasi di bagian bawah Blender. Tool akan melaporkan jumlah image yang missing dan berapa yang berhasil diperbaiki.

Buka **Image Editor** atau cek di **Outliner → Blender File → Images** untuk memverifikasi path sudah kembali valid.

![Hasil verifikasi image path](../images/fix-image-windows-path-step-03.jpeg)

---

## Perilaku & Batasan

| Aspek | Detail |
|---|---|
| Target | Semua image yang sedang digunakan (users > 0) |
| Image packed | Dilewati (tidak perlu diperbaiki) |
| UDIM / Tiled | Didukung — dicek berdasarkan tile number |
| Konversi path | `A:\\` dan `A:/` → `/mnt/A/` |
| Syarat | File Blender harus sudah disimpan sebelum dijalankan |

---

## Troubleshooting

**Tidak ada yang diperbaiki padahal image masih missing?**
Path mungkin bukan format `A:\`. Tool ini khusus mengonversi path drive `A:`. Untuk drive lain, perlu penyesuaian manual atau menggunakan fitur *Find Missing Files* bawaan Blender.

**Error "Please save the blend file first"?**
Simpan file Blender terlebih dahulu sebelum menjalankan tool ini.

**Tombol tidak muncul?**
Pastikan mode yang dipilih di ExToolbox adalah `ImgWinPath`.
