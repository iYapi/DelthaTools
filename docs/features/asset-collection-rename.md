# Asset Collection Rename

**Kategori:** Asset Tool  
**Tool:** DelthλTools → AssetColRename

---

## Deskripsi

Tool **Asset Collection Rename** digunakan untuk secara otomatis merename seluruh objek di dalam sebuah collection berdasarkan nama file project dan nama collection yang aktif.

Contoh hasil rename: objek di dalam collection `c-test` akan direname menjadi `c-test_001`, `c-test_002`, dst.

> **Catatan:** Tool ini **tidak** merubah nama rig. Hanya objek non-rig di dalam collection yang akan direname.

---

## Prasyarat

Sebelum menggunakan tool ini, pastikan:

- Project sudah dibuka di Blender
- **Nama file project sama dengan nama collection** yang ingin di-rename
- DelthλTools sudah terpasang dan aktif di 3D Viewport

---

## Cara Penggunaan

### Langkah 1 — Verifikasi Nama Project

Buka project dan pastikan nama file project **sama persis** dengan nama collection yang menjadi target rename.

![Verifikasi nama project](../images/photo_2026-04-06%2013.48.51.jpeg)

---

### Langkah 2 — Buka DelthλTools & Pilih Mode

Di **3D Viewport**, buka panel **DelthλTools** (biasanya di sidebar `N`). Kemudian ubah **Select Mode** menjadi `AssetColRename`.

![Memilih mode AssetColRename di DelthλTools](../images/photo_2026-04-06%2013.52.27.jpeg)

---

### Langkah 3 — Jalankan Rename

Klik tombol **"Replace Asset Name"** untuk memulai proses rename.

![Klik Replace Asset Name](../images/photo_2026-04-06%2013.59.34.jpeg)

---

### Langkah 4 — Verifikasi Hasil

Setelah proses selesai, periksa nama objek di dalam collection. Seluruh objek (kecuali rig) seharusnya telah diperbarui sesuai nama collection.

![Hasil sebelum](../images/photo_2026-04-06%2013.59.36.jpeg) ![Hasil sesudah](../images/photo_2026-04-06%2013.59.38.jpeg)

---

## Perilaku & Batasan

| Aspek | Detail |
|---|---|
| Target rename | Semua objek di dalam collection aktif |
| Konvensi nama | Mengikuti format: `<nama_collection>_<nomor>` |
| Rig | **Tidak** ikut direname |
| Sumber nama | Diambil dari nama file project dan nama collection |

---

## Troubleshooting

**Objek tidak ikut direname?**  
Pastikan nama file project dan nama collection sudah identik (case-sensitive).

**Rig ikut direname?**  
Ini tidak seharusnya terjadi. Jika ada, periksa apakah objek rig sudah diberi naming convention yang benar (misal prefix `RIG_`).

**Tombol "Replace Asset Name" tidak muncul?**  
Pastikan mode yang dipilih di DelthλTools adalah `AssetColRename`, bukan mode lainnya.