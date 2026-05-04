# Character Three Point Light Properties

**Kategori:** Lighting, Compositing & Render Tool
**Tool:** DelthλTools → LightingProperties

---

## Deskripsi

Tool **Character Three Point Light Properties** menyediakan tiga fungsi untuk manajemen properti lighting karakter:

1. **Export Lighting Preset** — Menyimpan nilai properti light (warna, energy, exposure, shadow jitter overblur) ke file JSON
2. **Import Lighting Preset** — Memuat dan menerapkan nilai properti light dari file JSON yang telah di-export sebelumnya
3. **Make Override Lights Local** — Mengonversi light object yang berstatus library override menjadi data lokal agar dapat diedit secara bebas
4. **Override Fog Materials** — Membuat override pada object `Fog` dari library link dan melokalisasi materialnya agar bisa diedit

---

## Prasyarat

Sebelum menggunakan tool ini, pastikan:

- Lighting setup sudah ter-append di scene (lihat [Character Three Point Light Setup](./character-three-point-light-setup.md))
- Light objects sudah memiliki custom property key yang sesuai (dikonfigurasi di panel LightingProperties)
- DelthλTools sudah terpasang dan aktif

---

## Cara Penggunaan

### Export Lighting Preset

#### Langkah 1 — Buka DelthλTools & Pilih Mode

Di **3D Viewport**, buka panel **DelthλTools** (sidebar `N`). Ubah **Select Mode** menjadi `LightingProperties`.

![Pilih mode LightingProperties di DelthλTools](../images/light-props-step-01.jpeg)

---

#### Langkah 2 — Set Custom Property Key

Pastikan field **Key** di panel LightingProperties sudah diisi dengan nama custom property yang digunakan pada light objects (contoh: `lighting_preset`).

![Set custom property key](../images/light-props-step-02.jpeg)

---

#### Langkah 3 — Export Preset

Klik tombol **"Export Lighting Preset"**. File browser akan terbuka. Pilih lokasi dan nama file, lalu klik **Export**.

Data yang diekspor mencakup: nama light, collection, warna (color), energy, exposure, dan shadow jitter overblur.

![Export Lighting Preset](../images/light-props-step-03.jpeg)

---

### Import Lighting Preset

#### Langkah 1 — Import Preset

Klik tombol **"Import Lighting Preset"**. File browser akan terbuka. Pilih file `.json` yang sebelumnya di-export.

Tool akan menerapkan nilai properti ke light objects yang sesuai berdasarkan nama dan collection.

![Import Lighting Preset](../images/light-props-step-04.jpeg)

---

### Make Override Lights Local

#### Langkah 1 — Jalankan Make Override Lights Local

Klik tombol **"Make Override Lights Local"** untuk mengonversi light data dari library override menjadi lokal.

Gunakan opsi **Only Selected** jika hanya ingin memproses light yang sedang terpilih. Gunakan opsi **Purge Unreferenced** untuk menghapus linked light data yang tidak lagi terpakai.

![Make Override Lights Local](../images/light-props-step-05.jpeg)

---

### Override Fog Materials

#### Langkah 1 — Jalankan Override Fog Materials

Klik tombol **"Override Fog Materials"** untuk membuat override pada hierarchy collection yang mengandung object `Fog` dan melokalisasi materialnya.

> Setelah proses selesai, material Fog dapat diedit secara bebas tanpa mempengaruhi file library asalnya.

![Override Fog Materials](../images/light-props-step-06.jpeg)

---

## Perilaku & Batasan

| Aspek | Detail |
|---|---|
| Format export | JSON |
| Data yang diekspor | color, energy, exposure, shadow_jitter_overblur |
| Pengelompokan export | Berdasarkan nama collection |
| Import | Mencocokkan berdasarkan nama light dan nama collection |
| Make Override Local | Memproses semua light atau hanya yang selected (sesuai opsi) |
| Override Fog | Target default: object bernama `Fog` |
| Fog material | Node groups linked juga dilokalisasi jika opsi Localize Node Groups aktif |

---

## Troubleshooting

**Import tidak menerapkan nilai ke light?**
Pastikan nama collection dan nama light di file JSON cocok dengan yang ada di scene. Nama bersifat case-sensitive.

**Tombol Export/Import tidak muncul?**
Pastikan mode yang dipilih di DelthλTools adalah `LightingProperties`.

**Make Override Lights Local tidak memproses light?**
Pastikan light objects adalah library override (bukan local murni). Jika tidak ada override light, tool tidak akan mengubah apa pun.

**Override Fog gagal dengan error "No collections under the scene contain object 'Fog'"?**
Pastikan object bernama `Fog` ada di scene dan berada di dalam collection yang ter-link dari library.
