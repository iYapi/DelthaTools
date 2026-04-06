# Character Three Point Light Setup

**Kategori:** Lighting, Compositing & Render Tool
**Tool:** ExToolbox → LightingSetup

---

## Deskripsi

Tool **Character Three Point Light Setup** digunakan untuk secara otomatis meng-append setup pencahayaan tiga titik (key, fill, rim) untuk karakter langsung dari file preset blend.

Proses yang dilakukan tool ini secara otomatis:
1. Mendeteksi rig (Armature) di dalam collection karakter yang aktif
2. Meng-append collection `LightingSetup` dari file preset blend
3. Menempatkan collection lighting di bawah collection `RIMFILL`
4. Merename collection dan objek lighting sesuai suffix nama karakter
5. Menambahkan constraint **Child Of** pada `light_root` agar lighting mengikuti pergerakan karakter (target: bone `c_traj` atau `body`)
6. Mengatur **Light Linking** untuk fill dan rim light agar hanya menerangi karakter yang bersangkutan

> **Catatan:** Collection karakter harus diawali dengan prefix `c-` (contoh: `c-hero`, `c-napo`). Terdapat penanganan khusus untuk karakter `c-napo` yang menggunakan bone `c_body` sebagai target Child Of.

---

## Prasyarat

Sebelum menggunakan tool ini, pastikan:

- Project sudah dibuka di Blender
- Collection karakter sudah tersedia dan namanya **diawali dengan `c-`**
- Collection karakter memiliki **rig (Armature)** di dalamnya
- File preset blend (lighting setup) sudah dikonfigurasi di panel ExToolbox
- ExToolbox sudah terpasang dan aktif di 3D Viewport

---

## Cara Penggunaan

### Langkah 1 — Pilih Collection Karakter di Outliner

Di **Outliner**, klik collection karakter yang ingin diberi lighting. Pastikan collection tersebut menjadi **Active Collection** (highlighted).

Collection harus diawali dengan prefix `c-`, contoh: `c-hero`.

![Pilih collection karakter di Outliner](../images/light-setup-step-01.jpeg)

---

### Langkah 2 — Buka ExToolbox & Pilih Mode

Di **3D Viewport**, buka panel **ExToolbox** (sidebar `N`). Ubah **Select Mode** menjadi `LightingSetup`.

![Pilih mode LightingSetup di ExToolbox](../images/light-setup-step-02.jpeg)

---

### Langkah 3 — Set Path File Preset

Pada panel LightingSetup, isi field **Filepath** dengan path menuju file preset blend yang berisi collection `LightingSetup`.

![Isi filepath preset blend](../images/light-setup-step-03.jpeg)

---

### Langkah 4 — Append Lighting Setup

Klik tombol **"Append Lighting Setup"** untuk memulai proses.

Tool akan secara otomatis mendeteksi rig, meng-append lighting, merename, menambahkan constraint, dan mengatur light linking.

![Klik Append Lighting Setup](../images/light-setup-step-04.jpeg)

---

### Langkah 5 — Verifikasi Hasil

Setelah proses selesai, periksa di Outliner:
- Collection `RIMFILL` sudah terbuat (jika belum ada)
- Di dalam `RIMFILL` terdapat collection baru bernama `rf-<nama_karakter>`
- Objek lighting sudah mendapat suffix nama karakter
- Rig karakter kembali ke mode **POSE**

![Verifikasi hasil di Outliner](../images/light-setup-step-05.jpeg)

---

## Perilaku & Batasan

| Aspek | Detail |
|---|---|
| Prefix collection | Wajib diawali `c-` (contoh: `c-hero`) |
| Nama collection lighting | Format: `rf-<suffix>` di dalam `RIMFILL` |
| Nama objek lighting | Ditambahkan suffix `_<nama_karakter>` |
| Constraint | Child Of pada `light_root` → bone `c_traj` atau `body` di rig |
| Napo special case | Jika collection `c-napo`, bone target adalah `c_body` |
| Light Linking | Fill & Rim light hanya menerangi collection karakter aktif (via collection `LL_<suffix>`) |
| Rig pose | Diset REST saat append, dikembalikan POSE setelah selesai |

---

## Troubleshooting

**Warning "No rig (Armature) found under collection"?**
Pastikan collection karakter memiliki Armature di dalamnya. Tool tidak dapat melanjutkan tanpa rig.

**Warning "Active collection doesn't start with 'c-'"?**
Pastikan nama collection diawali dengan `c-`. Rename collection jika perlu.

**Warning "No root light found in collection"?**
File preset blend harus memiliki objek bernama `light_root` (atau `light_root_<suffix>`). Periksa file preset blend.

**Popup "Select Bone" muncul?**
Rig tidak memiliki bone `c_traj` atau `body`. Pilih bone yang sesuai dari daftar yang muncul.

**Error "No presets file path specified"?**
Isi terlebih dahulu field **Filepath** di panel LightingSetup dengan path file preset blend.
