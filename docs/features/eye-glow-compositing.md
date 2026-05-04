# Eye Glow Compositing

**Kategori:** Lighting, Compositing & Render Tool
**Tool:** DelthλTools → EyeGlowCompositing

---

## Deskripsi

Tool **Eye Glow Compositing** digunakan untuk secara otomatis meng-append dan mengatur node compositing untuk efek eye glow pada karakter. Tool ini membuat setup Compositing Node yang sudah terhubung antara **Cryptomatte** (untuk masking mata) dan node group **Eye_Glow_Setup** (untuk efek glow).

Proses yang dilakukan otomatis:
1. Mengaktifkan compositor node tree di scene
2. Meng-append node group `Eye_Glow_Setup` dari file preset blend
3. Membuat node **Cryptomatte V2** dengan matte ID untuk material mata (`eyes`, `eyes.001`, dst. hingga `eyes.030`)
4. Menghubungkan output Cryptomatte ke input Eye_Glow_Setup

---

## Prasyarat

Sebelum menggunakan tool ini, pastikan:

- Scene sudah memiliki render layer dengan **CryptoMaterial** pass aktif (layer: `Comp.CryptoMaterial`)
- Material mata pada karakter menggunakan nama yang diawali dengan `eyes` (sesuai matte ID)
- File preset blend yang berisi node group `Eye_Glow_Setup` sudah dikonfigurasi di panel DelthλTools
- DelthλTools sudah terpasang dan aktif

---

## Cara Penggunaan

### Langkah 1 — Aktifkan CryptoMaterial Pass

Sebelum menggunakan tool ini, pastikan pass **CryptoMaterial** sudah aktif di render layer yang digunakan (`Comp`).

Di **Properties → View Layer → Passes → Cryptomatte**, aktifkan **Cryptomatte Material**.

![Aktifkan CryptoMaterial Pass](../images/eye-glow-step-01.jpeg)

---

### Langkah 2 — Buka DelthλTools & Pilih Mode

Di **3D Viewport**, buka panel **DelthλTools** (sidebar `N`). Ubah **Select Mode** menjadi `EyeGlowCompositing`.

![Pilih mode EyeGlowCompositing di DelthλTools](../images/eye-glow-step-02.jpeg)

---

### Langkah 3 — Set Path File Preset

Pada panel EyeGlowCompositing, pastikan field **Filepath** sudah diisi dengan path menuju file preset blend yang berisi node group `Eye_Glow_Setup`.

![Isi filepath preset blend](../images/eye-glow-step-03.jpeg)

---

### Langkah 4 — Append Eye Glow Setup

Klik tombol **"Append compositing node Setup"** untuk memulai proses.

Tool akan membuka Compositor, meng-append node group, membuat Cryptomatte node, lalu menghubungkan keduanya secara otomatis.

![Klik Append compositing node Setup](../images/eye-glow-step-04.jpeg)

---

### Langkah 5 — Verifikasi di Compositor

Buka **Compositor** (Workspace Compositing atau ubah area ke Compositor). Pastikan node **Cryptomatte_Eye_Glow** dan **Eye_Glow_Setup** sudah muncul dan terhubung.

Hubungkan input/output node ini ke node tree compositor yang ada sesuai kebutuhan.

![Verifikasi node di Compositor](../images/eye-glow-step-05.jpeg)

---

## Perilaku & Batasan

| Aspek | Detail |
|---|---|
| Node group | `Eye_Glow_Setup` (di-append dari preset blend jika belum ada) |
| Cryptomatte layer | `Comp.CryptoMaterial` |
| Matte ID | `eyes`, `eyes.001` hingga `eyes.030` |
| Posisi node | Cryptomatte di koordinat (-200, 0), Eye_Glow_Setup di (200, 0) |
| Koneksi otomatis | Cryptomatte output[0] → Eye_Glow_Setup input[1] |
| Compositor | Otomatis diaktifkan (`use_nodes` dan `use_compositing`) |

---

## Troubleshooting

**Error "Failed to append node group 'Eye_Glow_Setup'"?**
Pastikan file preset blend yang dikonfigurasi benar-benar mengandung NodeTree bernama `Eye_Glow_Setup`.

**Error "No presets file path specified"?**
Isi field **Filepath** di panel EyeGlowCompositing dengan path file preset blend.

**Efek glow tidak terlihat saat render?**
Pastikan pass **CryptoMaterial** sudah aktif di render layer `Comp` dan material mata bernama `eyes` (atau `eyes.001`, dst.).

**Node sudah muncul tapi tidak terhubung?**
Error koneksi akan muncul di notifikasi Blender. Periksa apakah output Cryptomatte dan input Eye_Glow_Setup tersedia (tidak kosong).
