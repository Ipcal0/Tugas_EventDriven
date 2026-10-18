# Modul 6: Validasi dan Error Handling pada Aplikasi Registrasi

## 6.1 Jenis-Jenis Validasi
Validasi adalah proses memastikan bahwa data yang diinput pengguna sesuai dengan format dan kriteria yang diharapkan. Ada beberapa jenis validasi:
1. **Validasi Format**: Memastikan input sesuai format yang diharapkan (email dengan simbol `@` dan domain, format nomor telepon Indonesia `08xxxxxxxxxx`, tanggal, dll).
2. **Validasi Range**: Memastikan nilai numerik berada dalam rentang yang valid (contoh: umur minimal 13 tahun dan maksimal 100 tahun).
3. **Validasi Required**: Memastikan field wajib tidak dibiarkan kosong atau hanya berisi spasi.
4. **Validasi Custom**: Validasi khusus sesuai aturan bisnis aplikasi (contoh: password minimal 8 karakter dengan kombinasi huruf dan angka, konfirmasi password harus identik).

---

## 6.2 Real-time vs Submit-time Validation
- **Real-time Validation**: Validasi yang terjadi secara reaktif seketika saat pengguna mengetik (`trace_add` pada Tkinter Variable), memberikan feedback visual langsung (ikon warna hijau/merah, pesan hint).
- **Submit-time Validation**: Validasi menyeluruh yang dipicu saat tombol submit ditekan (`final_validation`), memastikan seluruh syarat terpenuhi sebelum data diproses lebih lanjut atau dikirim ke sistem.

---

## 6.3 Cara Menjalankan Aplikasi
Buka terminal/PowerShell di folder ini, lalu jalankan perintah:
```bash
python registrasi_app.py
```

---

## Checklist Pengujian Output (Apa Saja yang Dicek)

| Komponen / Field | Kasus Uji Salah (Negatif) | Kasus Uji Benar (Positif) | Yang Harus Dicek pada UI |
| :--- | :--- | :--- | :--- |
| **1. Nama Lengkap** | • Kurang dari 3 huruf (cth: `Ab`)<br>• Mengandung angka/simbol (cth: `Budi123`, `Ani!`)<br>• Hanya spasi | • Ketik minimal 3 huruf (cth: `Budi Santoso`) | • Indikator berubah dari merah (●) ke hijau (●)<br>• Teks hint berubah menjadi `✓ Nama valid`<br>• Progress bertambah |
| **2. Email** | • Tidak ada `@` (cth: `userdomain.com`)<br>• Tidak ada domain (cth: `user@`)<br>• Format salah (cth: `user@com`) | • Format valid (cth: `user@example.com`) | • Indikator berubah dari merah ke hijau<br>• Teks hint berubah menjadi `✓ Email valid`<br>• Progress bertambah |
| **3. Nomor Telepon** | • Tidak berawalan `08` (cth: `021998877`)<br>• Kurang dari 10 digit (cth: `08123`)<br>• Lebih dari 13 digit<br>• Ada huruf/simbol | • Berawalan `08` dengan 10-13 digit angka (cth: `081234567890`) | • Indikator berubah hijau<br>• Teks hint berubah menjadi `✓ Nomor telepon valid`<br>• Progress bertambah |
| **4. Password** | • Kurang dari 8 karakter (cth: `pass1`)<br>• Hanya huruf tanpa angka (cth: `rahasiaa`)<br>• Hanya angka tanpa huruf (cth: `12345678`) | • Minimal 8 karakter kombinasi huruf dan angka (cth: `rahasia123`) | • Indikator password berubah hijau<br>• Input disamarkan dengan tanda bintang (`*`) |
| **5. Konfirmasi Password** | • Berbeda dengan password utama (cth: password: `rahasia123`, konfirmasi: `rahasia321`) | • Sama persis dengan password (cth: `rahasia123`) | • Indikator berubah hijau<br>• Teks hint menjadi `✓ Password cocok` |
| **6. Umur (Spinbox)** | • Angka di bawah 13 (cth: `12`)<br>• Angka di atas 100 (cth: `105`)<br>• Diisi bukan angka | • Angka 13 s.d. 100 (cth: `20`) | • Indikator umur berubah hijau<br>• Teks hint menjadi `✓ Umur valid` |
| **7. Persetujuan (Checkbox)** | • Dibiarkan tidak dicentang (unchecked) | • Dicentang (checked) | • Progress bar bertambah |
| **8. Progress Bar & Label** | Form belum lengkap | Semua 7 kriteria valid | • Progress bar naik bertahap: 0%, 14%, 29%, 43%, 57%, 71%, 86%, hingga `100% Complete (7/7 fields)` |
| **9. Tombol Submit** | Masih ada field merah / tidak valid / belum centang persetujuan | Semua 7 kriteria telah valid | • Awalnya disabled (warna abu-abu).<br>• Otomatis menjadi enabled (warna hijau) saat 100% lengkap. |
| **10. Proses Loading (Simulasi)** | - | Klik tombol "DAFTAR SEKARANG" | • Tombol berubah teks menjadi `"MEMPROSES..."` dengan warna oranye.<br>• Seluruh field input terkunci (disabled) selama 2 detik. |
| **11. Pop-up Sukses** | - | Selesai proses loading (2 detik) | • Muncul MessageBox `"Registrasi Berhasil"` berisi ringkasan data pendaftar & tanggal registrasi.<br>• Muncul MessageBox konfirmasi `"Ingin mendaftarkan pengguna lain?"` |
| **12. Fitur Reset Form** | - | Pilih `"Yes"` pada konfirmasi reset form | • Semua field kosong kembali.<br>• Indikator kembali merah (●).<br>• Hint text kembali ke teks panduan awal.<br>• Progress bar kembali ke `0% Complete (0/7 fields)`.<br>• Tombol submit kembali disabled (abu-abu). |

