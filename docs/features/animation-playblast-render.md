# Animation Playblast Render

**Kategori:** Animator Tool
**Tool:** ExToolbox → AnimPlayblast

---

## Deskripsi

Tool **Animation Playblast Render** digunakan untuk merender preview animasi (playblast) secara cepat langsung dari Blender. Tool ini otomatis menerapkan preset render, mengatur output path berdasarkan pola project yang telah dikonfigurasi di ExConfig, lalu merender menggunakan OpenGL renderer.

Fitur utama:
- Render berdasarkan **Render Marker** (`EX_START` dan `EX_END`) jika tersedia, atau menggunakan frame range scene
- Otomatis switch ke **Camera View** saat render berlangsung
- Viewport otomatis menggunakan mode **Solid + Texture** saat render
- Otomatis kembali ke mode **Solid + Material** setelah render selesai
- Output path digenerate secara otomatis dari konfigurasi ExConfig

> **Catatan:** Tool ini membutuhkan konfigurasi ExConfig (pattern Animation & Playblast) sebelum dapat digunakan.

---

## Prasyarat

Sebelum menggunakan tool ini, pastikan:

- File Blender sudah disimpan
- ExConfig sudah dikonfigurasi dengan pattern **Animation** dan **Playblast**
- Terdapat **camera** di scene
- ExToolbox sudah terpasang dan aktif di 3D Viewport

---

## Cara Penggunaan

### Langkah 1 — Buka ExToolbox & Pilih Mode

Di **3D Viewport**, buka panel **ExToolbox** (sidebar `N`). Ubah **Select Mode** menjadi `AnimPlayblast`.

![Pilih mode AnimPlayblast di ExToolbox](../images/photo_2026-04-06%2014.21.24.jpeg)

---

### Langkah 2 — Set Render Marker (Opsional)

Jika ingin merender range tertentu saja (bukan seluruh timeline), navigasi ke frame awal yang ingin dirender, lalu klik tombol **"Start"**. Kemudian navigasi ke frame akhir dan klik **"End"**.

Marker `EX_START` dan `EX_END` akan muncul di timeline.

![Set Render Marker di timeline](../images/photo_2026-04-06%2014.17.39.jpeg)

---

### Langkah 3 — Tambah Safe Area (Opsional)

Klik tombol **"Add Safe Area"** untuk menampilkan overlay safe area di camera. Ini berguna untuk mengecek batas aman frame sebelum render.

![Tambah Safe Area ke camera](../images/anim-playblast-step-03.jpeg)

---

### Langkah 4 — Render Playblast

Klik tombol **"Render Playblast"** untuk memulai proses render.

Tool akan secara otomatis:
1. Menerapkan preset render dari ExConfig
2. Menentukan frame range (dari marker `EX_START`/`EX_END` jika ada)
3. Mengatur output path sesuai pola project
4. Merender dengan OpenGL renderer
5. Membersihkan render marker setelah selesai
6. Mengembalikan viewport ke mode normal

![Klik Render Playblast](../images/anim-playblast-step-04.jpeg)

---

### Langkah 5 — Verifikasi Output

Setelah render selesai, cek folder output yang dikonfigurasi di ExConfig. File video playblast sudah tersimpan di path yang ditentukan.

![Hasil output playblast](../images/anim-playblast-step-05.jpeg)

---

## Perilaku & Batasan

| Aspek | Detail |
|---|---|
| Renderer | OpenGL (viewport render) |
| Frame range | Dari marker `EX_START`/`EX_END`, fallback ke frame_start/frame_end scene |
| Output path | Digenerate otomatis dari ExConfig (pattern Animation + Playblast) |
| Viewport shading | Otomatis SOLID + TEXTURE saat render, kembali SOLID + MATERIAL setelah selesai |
| Render marker | Dihapus otomatis setelah render selesai |
| Safe area | Menggunakan image overlay dari `/mnt/J/00_tools/cam_guide/action-safe_nowm.png` |

---

## Troubleshooting

**Error "No camera found in the scene"?**
Pastikan scene memiliki camera aktif. Tambahkan camera dan jadikan camera aktif di scene.

**Error "Blend file not saved"?**
Simpan file Blender terlebih dahulu sebelum menjalankan Render Playblast.

**Error "Animation and/or Playblast patterns not configured"?**
Buka panel **ExConfig** dan konfigurasi pattern **Animation** dan **Playblast** terlebih dahulu.

**Error "No playblast config path set"?**
Di panel ExConfig → Playblast Config, pastikan path ke file preset JSON sudah diisi.

**Output path salah atau tidak terbuat?**
Cek konfigurasi Pattern Match `animation_playblast` di ExConfig → Pattern Match panel.
