# Quick Open Graph Window

**Kategori:** Animator Tool
**Tool:** DelthλTools → GraphNewWindow

---

## Deskripsi

Tool **Quick Open Graph Window** digunakan untuk membuka **Graph Editor** di jendela baru secara cepat dengan satu klik. Sangat berguna saat bekerja dengan animasi dan ingin melihat Graph Editor secara terpisah tanpa mengubah layout workspace yang sedang aktif.

---

## Prasyarat

Sebelum menggunakan tool ini, pastikan:

- DelthλTools sudah terpasang dan aktif di 3D Viewport

---

## Cara Penggunaan

### Langkah 1 — Buka DelthλTools & Pilih Mode

Di **3D Viewport**, buka panel **DelthλTools** (sidebar `N`). Ubah **Select Mode** menjadi `GraphNewWindow`.

![Pilih mode GraphNewWindow di DelthλTools](../images/quick-graph-window-step-01.jpeg)

---

### Langkah 2 — Buka Graph Editor Window

Klik tombol **"Graph New Window"** untuk membuka jendela baru.

Blender akan membuat jendela baru dan secara otomatis mengaturnya menjadi **Graph Editor**.

![Klik Graph New Window](../images/quick-graph-window-step-02.jpeg)

---

### Langkah 3 — Gunakan Graph Editor

Jendela Graph Editor baru kini siap digunakan. Layout workspace utama tidak berubah.

![Graph Editor terbuka di jendela baru](../images/quick-graph-window-step-03.jpeg)

---

## Perilaku & Batasan

| Aspek | Detail |
|---|---|
| Jendela baru | Dibuka sebagai window Blender terpisah |
| Area type | Otomatis diset ke Graph Editor |
| Layout utama | Tidak berubah |
| Fallback | Jika tidak ada area Graph Editor di window baru, area VIEW_3D pertama akan dikonversi ke Graph Editor |

---

## Troubleshooting

**Jendela terbuka tapi bukan Graph Editor?**
Ini bisa terjadi jika sistem tidak menemukan area yang bisa dikonversi. Coba tutup jendela tersebut dan klik tombol lagi.

**Tombol tidak muncul?**
Pastikan mode yang dipilih di DelthλTools adalah `GraphNewWindow`.
