import tkinter as tk
from tkinter import ttk

# ============================================================
# 2. CARA KERJA root.after() (DEMO PERULANGAN SEDERHANA)
# ============================================================
class LoopingDemoFrame(tk.Frame):
    """
    Fungsi after(delay_ms, callback) menerima parameter waktu dalam milidetik.
    Fungsi memanggil dirinya sendiri secara rekursif melalui after() untuk perulangan.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.count = 0
        self.is_running = False
        self.timer_id = None

        tk.Label(
            self,
            text="Demo Looping root.after()",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        tk.Label(
            self,
            text="Fungsi dipanggil berulang setiap 1 detik (1000 ms).\nLihat perubahan angka dan cek output Terminal/Console!",
            font=("Arial", 10),
            justify=tk.CENTER
        ).pack(pady=5)

        self.lbl_counter = tk.Label(
            self,
            text="Detik: 0",
            font=("Arial", 20, "bold"),
            fg="#1976D2"
        )
        self.lbl_counter.pack(pady=15)

        btn_box = tk.Frame(self)
        btn_box.pack(pady=5)

        self.btn_mulai = tk.Button(
            btn_box,
            text="Mulai Loop",
            command=self.mulai_loop,
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            width=12
        )
        self.btn_mulai.pack(side=tk.LEFT, padx=5)

        self.btn_stop = tk.Button(
            btn_box,
            text="Stop Loop",
            command=self.stop_loop,
            font=("Arial", 10, "bold"),
            bg="#f44336",
            fg="white",
            width=12
        )
        self.btn_stop.pack(side=tk.LEFT, padx=5)

    def mulai_loop(self):
        if not self.is_running:
            self.is_running = True
            self.jalankan_terus()

    def jalankan_terus(self):
        if self.is_running:
            self.count += 1
            print(f"[Console] Fungsi dipanggil ke-{self.count} (setiap 1 detik)")
            self.lbl_counter.config(text=f"Detik: {self.count}")
            # Panggil ulang fungsi ini setelah 1000 milidetik (1 detik)
            self.timer_id = self.after(1000, self.jalankan_terus)

    def stop_loop(self):
        if self.is_running:
            self.is_running = False
            if self.timer_id:
                self.after_cancel(self.timer_id)
                self.timer_id = None
            print("[Console] Perulangan after() dihentikan.")


# ============================================================
# 3. IMPLEMENTASI COUNTDOWN TIMER (PENGHITUNG MUNDUR)
# ============================================================
class TimerApp(tk.Frame):
    """
    Penghitung waktu mundur yang dilengkapi tombol Mulai, Stop, dan Reset.
    Menggunakan self.after() untuk countdown dan self.after_cancel() untuk membatalkan timer.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.durasi_default = 10  # 10 detik
        self.sisa_waktu = self.durasi_default
        self.timer_id = None
        self.is_running = False

        tk.Label(
            self,
            text="Aplikasi Countdown Timer",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        # Label Tampilan Waktu
        self.lbl_waktu = tk.Label(
            self,
            text=f"00:{self.sisa_waktu:02d}",
            font=("Arial", 36, "bold"),
            fg="#333333"
        )
        self.lbl_waktu.pack(pady=15)

        # Tombol Kontrol
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        self.btn_mulai = tk.Button(
            btn_frame,
            text="Mulai",
            command=self.mulai_timer,
            font=("Arial", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            width=8
        )
        self.btn_mulai.pack(side=tk.LEFT, padx=5)

        self.btn_stop = tk.Button(
            btn_frame,
            text="Stop",
            command=self.stop_timer,
            font=("Arial", 11, "bold"),
            bg="#f44336",
            fg="white",
            width=8
        )
        self.btn_stop.pack(side=tk.LEFT, padx=5)

        self.btn_reset = tk.Button(
            btn_frame,
            text="Reset",
            command=self.reset_timer,
            font=("Arial", 11),
            width=8
        )
        self.btn_reset.pack(side=tk.LEFT, padx=5)

    def mulai_timer(self):
        if not self.is_running:
            if self.sisa_waktu <= 0:
                self.sisa_waktu = self.durasi_default
                self.lbl_waktu.config(text=f"00:{self.sisa_waktu:02d}", fg="#333333")
            self.is_running = True
            self.hitung_mundur()

    def hitung_mundur(self):
        if self.sisa_waktu > 0 and self.is_running:
            self.sisa_waktu -= 1
            self.lbl_waktu.config(text=f"00:{self.sisa_waktu:02d}", fg="#333333")
            # Simpan ID timer agar bisa dibatalkan nanti dengan after_cancel
            self.timer_id = self.after(1000, self.hitung_mundur)
        elif self.sisa_waktu == 0:
            self.is_running = False
            self.lbl_waktu.config(text="Waktu Habis!", fg="red")

    def stop_timer(self):
        if self.is_running:
            self.is_running = False
            if self.timer_id:
                self.after_cancel(self.timer_id)
                self.timer_id = None

    def reset_timer(self):
        self.stop_timer()
        self.sisa_waktu = self.durasi_default
        self.lbl_waktu.config(text=f"00:{self.sisa_waktu:02d}", fg="#333333")


# ============================================================
# 4. IMPLEMENTASI ANIMASI SEDERHANA PADA CANVAS
# ============================================================
class AnimasiApp(tk.Frame):
    """
    Animasi bola memantul pada widget Canvas.
    Menggunakan canvas.move() dan pembaruan frame setiap 20 ms menggunakan self.after().
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas_width = 400
        self.canvas_height = 200

        tk.Label(
            self,
            text="Animasi Bola Memantul",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        # Buat Canvas
        self.canvas = tk.Canvas(
            self,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="white",
            relief=tk.SUNKEN,
            bd=2
        )
        self.canvas.pack(padx=10, pady=5)

        # Buat objek lingkaran (oval) pada koordinat awal: (x1, y1, x2, y2)
        self.bola = self.canvas.create_oval(10, 80, 40, 110, fill="blue", outline="black")
        self.dx = 3  # Kecepatan gerak sumbu X (horizontal)
        self.anim_id = None
        self.is_animating = False

        # Tombol Kontrol Animasi
        btn_box = tk.Frame(self)
        btn_box.pack(pady=8)

        self.btn_toggle = tk.Button(
            btn_box,
            text="Mulai Animasi",
            command=self.toggle_animasi,
            font=("Arial", 10, "bold"),
            bg="#2196F3",
            fg="white",
            width=15
        )
        self.btn_toggle.pack(side=tk.LEFT, padx=5)

        self.btn_reset = tk.Button(
            btn_box,
            text="Reset Posisi",
            command=self.reset_posisi,
            font=("Arial", 10),
            width=12
        )
        self.btn_reset.pack(side=tk.LEFT, padx=5)

    def toggle_animasi(self):
        if not self.is_animating:
            self.is_animating = True
            self.btn_toggle.config(text="Jeda Animasi", bg="#FF9800")
            self.gerakkan_bola()
        else:
            self.is_animating = False
            self.btn_toggle.config(text="Lanjutkan Animasi", bg="#2196F3")
            if self.anim_id:
                self.after_cancel(self.anim_id)
                self.anim_id = None

    def gerakkan_bola(self):
        if not self.is_animating:
            return

        # Geser objek sejauh dx
        self.canvas.move(self.bola, self.dx, 0)

        # Ambil koordinat posisi bola saat ini: [x1, y1, x2, y2]
        posisi = self.canvas.coords(self.bola)

        # Memantul jika menabrak dinding kanan (posisi[2] >= lebar) atau kiri (posisi[0] <= 0)
        if posisi[2] >= self.canvas_width or posisi[0] <= 0:
            self.dx = -self.dx

        # Perbarui frame setiap 20 milidetik (sekitar 50 FPS)
        self.anim_id = self.after(20, self.gerakkan_bola)

    def reset_posisi(self):
        if self.is_animating:
            self.toggle_animasi()
        self.canvas.coords(self.bola, 10, 80, 40, 110)
        self.dx = abs(self.dx)


# ============================================================
# APLIKASI UTAMA (TABBED NOTEBOOK UNTUK MENGGABUNGKAN SEMUA DEMO)
# ============================================================
class TimerAnimasiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Praktikum Event-Driven: Timer dan Animasi")
        self.root.geometry("460x420")
        self.root.resizable(False, False)

        # Notebook Tab untuk navigasi antar materi
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tab 1: Countdown Timer
        tab_timer = TimerApp(notebook)
        notebook.add(tab_timer, text="1. Countdown Timer")

        # Tab 2: Animasi Canvas
        tab_animasi = AnimasiApp(notebook)
        notebook.add(tab_animasi, text="2. Animasi Canvas")

        # Tab 3: Demo Looping after()
        tab_loop = LoopingDemoFrame(notebook)
        notebook.add(tab_loop, text="3. Looping after()")


# Menjalankan aplikasi GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = TimerAnimasiApp(root)
    root.mainloop()

