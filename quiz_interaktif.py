import tkinter as tk
from tkinter import messagebox, ttk
import time
import os
import json

class QuizApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Quiz Interaktif - Event-Driven Programming")
        self.window.geometry("760x640")
        self.window.minsize(720, 580)
        self.window.configure(bg="#F1F5F9")  # Background abu-abu modern (Slate-100)

        # ---------------------------------------------------------
        # Data Quiz: 10 Soal mencakup seluruh materi modul Event-Driven
        # ---------------------------------------------------------
        self.questions = [
            {
                "question": "1. Apa itu konsep 'Event-Driven Programming'?",
                "options": [
                    "Program yang alur eksekusinya selalu linier dari baris pertama ke terakhir",
                    "Program yang alur eksekusinya ditentukan oleh kejadian (event) seperti input pengguna atau sensor",
                    "Program yang berjalan secara eksklusif hanya pada command line interface (CLI)",
                    "Program yang hanya dapat dieksekusi di dalam web browser"
                ],
                "correct": 1
            },
            {
                "question": "2. Apa fungsi utama dari 'Event Loop' (seperti root.mainloop()) pada Tkinter?",
                "options": [
                    "Menghentikan seluruh program saat terjadi error runtime",
                    "Mendengarkan event terus-menerus dan mendistribusikannya ke handler yang sesuai",
                    "Menghapus variabel yang tidak lagi digunakan dari RAM secara otomatis",
                    "Mengompilasi script Python menjadi berkas biner (.exe)"
                ],
                "correct": 1
            },
            {
                "question": "3. Method Tkinter apa yang digunakan untuk menghubungkan suatu event dengan fungsi handler/callback?",
                "options": [
                    "widget.connect(event, callback)",
                    "widget.listen(event, callback)",
                    "widget.bind(event, callback)",
                    "widget.attach(event, callback)"
                ],
                "correct": 2
            },
            {
                "question": "4. Penulisan string event di Tkinter untuk menangkap penekanan tombol Enter pada keyboard adalah...",
                "options": [
                    "'<Enter>' (karena enter berarti menekan tombol)",
                    "'<Return>' (karena '<Enter>' digunakan untuk event kursor mouse masuk ke widget)",
                    "'<Key-Enter>' (karena tombol enter)",
                    "'<Submit>' (karena mengirimkan form)"
                ],
                "correct": 1
            },
            {
                "question": "5. Mengapa kita menggunakan widget.after() daripada time.sleep() untuk timer dan animasi di GUI?",
                "options": [
                    "time.sleep() memblokir event loop sehingga jendela GUI menjadi freeze / Not Responding",
                    "time.sleep() memiliki konsumsi memori 10 kali lebih besar daripada after()",
                    "widget.after() secara otomatis mempercepat clock GPU komputer",
                    "time.sleep() tidak didukung oleh modul Tkinter di sistem operasi Windows"
                ],
                "correct": 0
            },
            {
                "question": "6. Method apa yang digunakan untuk membatalkan timer yang sebelumnya telah dijadwalkan dengan after()?",
                "options": [
                    "root.after_cancel(timer_id)",
                    "root.stop_timer(timer_id)",
                    "root.kill_timer(timer_id)",
                    "root.cancel_loop(timer_id)"
                ],
                "correct": 0
            },
            {
                "question": "7. Variabel kontrol Tkinter manakah yang paling tepat digunakan untuk mengelola sekumpulan Radiobutton bernilai indeks integer?",
                "options": [
                    "tk.StringVar()",
                    "tk.BooleanVar()",
                    "tk.IntVar()",
                    "tk.DoubleVar()"
                ],
                "correct": 2
            },
            {
                "question": "8. Dalam event-driven GUI, apa peran utama validasi input pengguna sebelum memproses aksi submit?",
                "options": [
                    "Mencegah pengiriman data kosong/tidak valid serta memberikan feedback visual langsung",
                    "Memaksa pengguna untuk membeli lisensi aplikasi berbayar",
                    "Mengunci ukuran layar agar resolusi monitor tidak berubah",
                    "Menghapus riwayat cache sistem operasi secara permanen"
                ],
                "correct": 0
            },
            {
                "question": "9. Method Canvas apa yang digunakan untuk memindahkan/menggeser objek grafis secara bertahap saat membuat animasi?",
                "options": [
                    "canvas.move(item_id, dx, dy)",
                    "canvas.shift(item_id, x, y)",
                    "canvas.relocate(item_id, dx, dy)",
                    "canvas.translate(item_id, dx, dy)"
                ],
                "correct": 0
            },
            {
                "question": "10. Apa yang dimaksud dengan 'State Management' dalam pengembangan aplikasi GUI?",
                "options": [
                    "Pengaturan lisensi software pada setiap negara bagian",
                    "Penyimpanan dan pelacakan status data aplikasi (skor, indeks soal, timer) sepanjang siklus hidup GUI",
                    "Pengaturan sistem pendingin CPU saat aplikasi dijalankan",
                    "Pemisahan antara sistem operasi 32-bit dan 64-bit"
                ],
                "correct": 1
            }
        ]

        # ---------------------------------------------------------
        # State Management: Menyimpan dan memantau status aplikasi
        # ---------------------------------------------------------
        self.current_question = 0
        self.score = 0
        self.time_limit_per_question = 30  # 30 detik per soal
        self.time_left = self.time_limit_per_question
        self.selected_answer = tk.IntVar(value=-1)
        self.is_feedback_active = False   # Flag untuk mencegah multi-submit saat animasi feedback
        self.is_quiz_finished = False     # Flag status apakah kuis sudah selesai
        self.timer_job = None              # ID timer countdown after()
        self.anim_jobs = []                # Daftar ID timer animasi after()
        self.history = []                  # Riwayat jawaban pengguna untuk laporan akhir

        # File lokasi penyimpanan auto-save progres kuis
        self.progress_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quiz_progress.json")

        # Konfigurasi style ttk
        self.setup_styles()

        # Bangun UI
        self.buat_interface()
        # Pasang trace pada variabel kontrol agar highlight selalu sinkron seketika saat nilai berubah
        self.selected_answer.trace_add("write", lambda *args: self.highlight_selected_option())

        # Cek apakah ada progres kuis sebelumnya yang tersimpan untuk dilanjutkan (Auto-Save)
        resumed = self.check_and_load_progress()

        # Pasang pintasan keyboard global (bind_all)
        self.bind_shortcuts()

        self.load_question()
        self.start_timer()

        # Pastikan jendela utama selalu memegang fokus keyboard aktif
        self.window.focus_force()
        self.window.focus_set()
        self.window.lift()

        if resumed:
            self.feedback_banner.config(
                text=f"📂 Progres kuis berhasil dipulihkan! Melanjutkan Soal ke-{self.current_question + 1} (Skor: {self.score} Poin).",
                fg="#1D4ED8",
                bg="#EFF6FF"
            )

        # Tangani penutupan jendela secara aman (Auto-Save saat keluar)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_styles(self):
        """Konfigurasi style ttk agar tampilan lebih modern"""
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Custom progressbar hijau segar
        self.style.configure(
            "Quiz.Horizontal.TProgressbar",
            troughcolor="#E2E8F0",
            background="#10B981",
            lightcolor="#34D399",
            darkcolor="#059669",
            bordercolor="#CBD5E1",
            thickness=14
        )

        # Custom Treeview untuk hasil akhir
        self.style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background="#0F172A",
            foreground="white"
        )
        self.style.configure(
            "Treeview",
            font=("Segoe UI", 9),
            rowheight=26
        )

    def buat_interface(self):
        """Membangun seluruh komponen antarmuka pengguna (UI)"""
        # ==================== 1. HEADER ====================
        self.header_frame = tk.Frame(self.window, bg="#0F172A", height=70)
        self.header_frame.pack(fill=tk.X, side=tk.TOP)
        self.header_frame.pack_propagate(False)

        header_content = tk.Frame(self.header_frame, bg="#0F172A")
        header_content.pack(fill=tk.BOTH, expand=True, padx=25)

        title_box = tk.Frame(header_content, bg="#0F172A")
        title_box.pack(side=tk.LEFT, pady=10)

        lbl_app_title = tk.Label(
            title_box,
            text="🎯 QUIZ INTERAKTIF",
            font=("Segoe UI", 16, "bold"),
            fg="#38BDF8",
            bg="#0F172A"
        )
        lbl_app_title.pack(anchor="w")

        lbl_app_sub = tk.Label(
            title_box,
            text="Tugas Akhir: Modul Event-Driven Programming GUI",
            font=("Segoe UI", 9),
            fg="#94A3B8",
            bg="#0F172A"
        )
        lbl_app_sub.pack(anchor="w")

        # Badge Topik di sebelah kanan header
        badge_frame = tk.Frame(header_content, bg="#1E293B", padx=12, pady=6)
        badge_frame.pack(side=tk.RIGHT, pady=15)
        lbl_badge = tk.Label(
            badge_frame,
            text="Python Tkinter 8.6",
            font=("Segoe UI", 9, "bold"),
            fg="#E2E8F0",
            bg="#1E293B"
        )
        lbl_badge.pack()

        # ==================== 2. STATUS & PROGRESS BAR ====================
        self.status_bar_frame = tk.Frame(self.window, bg="#FFFFFF", relief=tk.FLAT, bd=0)
        self.status_bar_frame.pack(fill=tk.X, padx=25, pady=(15, 0))

        status_inner = tk.Frame(self.status_bar_frame, bg="#FFFFFF", padx=18, pady=12)
        status_inner.pack(fill=tk.X)

        # Indikator Nomor Soal
        self.lbl_soal_nomor = tk.Label(
            status_inner,
            text="Soal: 1 / 10",
            font=("Segoe UI", 11, "bold"),
            fg="#334155",
            bg="#FFFFFF"
        )
        self.lbl_soal_nomor.pack(side=tk.LEFT)

        # Real-time Score Badge
        self.score_badge = tk.Label(
            status_inner,
            text="🏆 Skor: 0 Poin",
            font=("Segoe UI", 11, "bold"),
            fg="#2563EB",
            bg="#EFF6FF",
            padx=10,
            pady=3,
            relief=tk.RIDGE,
            bd=1
        )
        self.score_badge.pack(side=tk.LEFT, padx=15)

        # Countdown Timer Badge
        self.lbl_timer = tk.Label(
            status_inner,
            text="⏱️ Sisa Waktu: 30s",
            font=("Segoe UI", 11, "bold"),
            fg="#0F766E",
            bg="#CCFBF1",
            padx=12,
            pady=3,
            relief=tk.RIDGE,
            bd=1
        )
        self.lbl_timer.pack(side=tk.RIGHT)

        # Progress bar di bawah status
        self.progress_frame = tk.Frame(self.window, bg="#F1F5F9")
        self.progress_frame.pack(fill=tk.X, padx=25, pady=(4, 10))

        self.progressbar = ttk.Progressbar(
            self.progress_frame,
            orient="horizontal",
            mode="determinate",
            maximum=len(self.questions),
            style="Quiz.Horizontal.TProgressbar"
        )
        self.progressbar.pack(fill=tk.X)

        # ==================== 3. KARTU SOAL & OPSI JAWABAN ====================
        # Frame pembungkus untuk efek animasi shake
        self.card_wrapper = tk.Frame(self.window, bg="#F1F5F9")
        self.card_wrapper.pack(fill=tk.BOTH, expand=True, padx=25, pady=5)

        self.card_frame = tk.Frame(
            self.card_wrapper,
            bg="#FFFFFF",
            relief=tk.SOLID,
            bd=1,
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )
        self.card_frame.pack(fill=tk.BOTH, expand=True)

        # Teks Pertanyaan
        self.lbl_question = tk.Label(
            self.card_frame,
            text="",
            font=("Segoe UI", 13, "bold"),
            fg="#0F172A",
            bg="#FFFFFF",
            justify=tk.LEFT,
            wraplength=660,
            anchor="w"
        )
        self.lbl_question.pack(fill=tk.X, padx=24, pady=(20, 12))

        # Garis pemisah halus
        sep = tk.Frame(self.card_frame, height=1, bg="#E2E8F0")
        sep.pack(fill=tk.X, padx=24, pady=(0, 12))

        # Container Radiobutton Pilihan Jawaban
        self.options_container = tk.Frame(self.card_frame, bg="#FFFFFF")
        self.options_container.pack(fill=tk.BOTH, expand=True, padx=24)

        self.radio_buttons = []
        self.radio_frames = []

        for i in range(4):
            # Frame tiap opsi agar tampilan rapi seperti kartu tombol opsi
            opt_frame = tk.Frame(
                self.options_container,
                bg="#F8FAFC",
                relief=tk.SOLID,
                bd=1,
                highlightbackground="#E2E8F0",
                highlightthickness=1,
                cursor="hand2"
            )
            opt_frame.pack(fill=tk.X, pady=4, ipady=3)

            rb = tk.Radiobutton(
                opt_frame,
                text="",
                value=i,
                variable=self.selected_answer,
                font=("Segoe UI", 10),
                fg="#1E293B",
                bg="#F8FAFC",
                activebackground="#EFF6FF",
                selectcolor="#FFFFFF",
                anchor="w",
                justify=tk.LEFT,
                wraplength=610,
                cursor="hand2",
                command=self.highlight_selected_option
            )
            rb.pack(fill=tk.X, padx=12, pady=4)

            # Klik frame maupun radiobutton langsung memilih opsi secara instan (0 delay)
            def make_click_handler(idx=i):
                return lambda e: self.on_option_clicked(idx)

            opt_frame.bind("<Button-1>", make_click_handler(i))
            rb.bind("<Button-1>", make_click_handler(i))

            # Hover effect untuk interaktivitas responsif saat kursor mouse melintas
            def make_hover_handler(frame=opt_frame, radio=rb, idx=i, hover=True):
                return lambda e: self.on_option_hover(frame, radio, idx, hover)

            opt_frame.bind("<Enter>", make_hover_handler(opt_frame, rb, i, True))
            opt_frame.bind("<Leave>", make_hover_handler(opt_frame, rb, i, False))
            rb.bind("<Enter>", make_hover_handler(opt_frame, rb, i, True))
            rb.bind("<Leave>", make_hover_handler(opt_frame, rb, i, False))

            self.radio_buttons.append(rb)
            self.radio_frames.append(opt_frame)

        # Banner Animasi Visual untuk Feedback (Benar / Salah / Validasi Error)
        self.feedback_banner = tk.Label(
            self.card_frame,
            text="",
            font=("Segoe UI", 10, "bold"),
            fg="#334155",
            bg="#FFFFFF",
            pady=8,
            anchor="center"
        )
        self.feedback_banner.pack(fill=tk.X, padx=24, pady=(5, 12))

        # ==================== 4. TOMBOL AKSI & SHORTCUT HINTS ====================
        self.action_frame = tk.Frame(self.window, bg="#F1F5F9")
        self.action_frame.pack(fill=tk.X, padx=25, pady=(5, 15))

        # Hint shortcut di kiri bawah
        hint_label = tk.Label(
            self.action_frame,
            text="💡 Pintasan: [1-4] Pilih Opsi  |  [Enter] Submit Jawaban  |  [Esc] Lewati",
            font=("Segoe UI", 9),
            fg="#64748B",
            bg="#F1F5F9"
        )
        hint_label.pack(side=tk.LEFT, pady=6)

        # Tombol Lewati (Esc)
        self.btn_skip = tk.Button(
            self.action_frame,
            text="Lewati (Esc)",
            command=self.skip_question,
            font=("Segoe UI", 10),
            fg="#475569",
            bg="#E2E8F0",
            activebackground="#CBD5E1",
            relief=tk.FLAT,
            padx=16,
            pady=6,
            cursor="hand2"
        )
        self.btn_skip.pack(side=tk.RIGHT, padx=(8, 0))

        # Tombol Submit (Enter)
        self.btn_submit = tk.Button(
            self.action_frame,
            text="Submit Jawaban (Enter)",
            command=self.submit_answer,
            font=("Segoe UI", 10, "bold"),
            fg="#FFFFFF",
            bg="#2563EB",
            activebackground="#1D4ED8",
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            padx=20,
            pady=6,
            cursor="hand2"
        )
        self.btn_submit.pack(side=tk.RIGHT)

        # Simpan padding dasar wrapper untuk efek getar / shake
        self.base_card_padx = 25

    def bind_shortcuts(self):
        """Memasang Event Handling global untuk keyboard shortcuts sesuai materi praktikum"""
        # Keyboard Event: Enter untuk submit jawaban (berlaku global di semua widget)
        self.window.bind_all("<Return>", lambda event: self.submit_answer())
        self.window.bind_all("<KP_Enter>", lambda event: self.submit_answer())

        # Keyboard Event: Esc untuk melewati soal (berlaku global)
        self.window.bind_all("<Escape>", lambda event: self.skip_question())

        # Keyboard Event: Angka 1, 2, 3, 4 untuk memilih opsi secara cepat
        for key, idx in [("1", 0), ("2", 1), ("3", 2), ("4", 3)]:
            self.window.bind_all(key, lambda event, i=idx: self.select_option_by_key(i))
            self.window.bind_all(f"<KP_{key}>", lambda event, i=idx: self.select_option_by_key(i))

        # Pastikan klik mouse di area manapun selalu mengembalikan fokus keyboard ke jendela
        self.window.bind_all("<Button-1>", lambda event: self.window.focus_set(), add="+")

    def on_option_hover(self, frame, rb, idx, is_hovering):
        """Efek hover dinamis saat kursor mouse melintas di atas opsi"""
        if self.is_feedback_active:
            return
        # Hanya ubah background jika opsi ini tidak sedang terpilih aktif
        if self.selected_answer.get() != idx:
            if is_hovering:
                frame.config(bg="#F1F5F9", highlightbackground="#94A3B8")
                rb.config(bg="#F1F5F9")
            else:
                frame.config(bg="#F8FAFC", highlightbackground="#E2E8F0")
                rb.config(bg="#F8FAFC")

    def on_option_clicked(self, idx):
        """Event handler saat container frame atau radiobutton diklik"""
        if not self.is_feedback_active:
            self.selected_answer.set(idx)
            self.highlight_selected_option()

    def select_option_by_key(self, idx):
        """Event handler saat tombol angka keyboard ditekan untuk memilih opsi"""
        if not self.is_feedback_active and 0 <= idx < 4:
            self.selected_answer.set(idx)
            self.highlight_selected_option()

    def highlight_selected_option(self, *args):
        """Memberikan feedback visual seketika pada opsi yang sedang aktif terpilih"""
        if self.is_feedback_active:
            return
        if not hasattr(self, "radio_frames") or not self.radio_frames:
            return

        sel = self.selected_answer.get()
        for i, (frame, rb) in enumerate(zip(self.radio_frames, self.radio_buttons)):
            if i == sel and sel != -1:
                frame.config(bg="#EFF6FF", highlightbackground="#3B82F6", bd=2)
                rb.config(
                    bg="#EFF6FF",
                    fg="#1D4ED8",
                    selectcolor="#EFF6FF",
                    activebackground="#EFF6FF",
                    font=("Segoe UI", 10, "bold")
                )
            else:
                frame.config(bg="#F8FAFC", highlightbackground="#E2E8F0", bd=1)
                rb.config(
                    bg="#F8FAFC",
                    fg="#1E293B",
                    selectcolor="#FFFFFF",
                    activebackground="#EFF6FF",
                    font=("Segoe UI", 10)
                )

    def load_question(self):
        """Memuat pertanyaan dan pilihan jawaban dari dataset ke komponen interface"""
        # Batalkan animasi yang mungkin masih berjalan
        self.cancel_animations()

        # Reset flag dan pilihan jawaban
        self.is_feedback_active = False
        self.selected_answer.set(-1)

        # Aktifkan kembali tombol interaktif
        self.set_controls_state(tk.NORMAL)

        q_data = self.questions[self.current_question]

        # Update teks soal
        self.lbl_question.config(text=q_data["question"])

        # Update pilihan jawaban dengan label A, B, C, D
        labels = ["A. ", "B. ", "C. ", "D. "]
        for i, opt_text in enumerate(q_data["options"]):
            self.radio_buttons[i].config(
                text=f"{labels[i]}{opt_text}",
                fg="#1E293B",
                bg="#F8FAFC",
                selectcolor="#FFFFFF",
                activebackground="#EFF6FF",
                font=("Segoe UI", 10)
            )
            self.radio_frames[i].config(
                bg="#F8FAFC",
                highlightbackground="#E2E8F0",
                bd=1
            )

        # Update indikator nomor soal dan progress bar
        self.lbl_soal_nomor.config(
            text=f"Soal: {self.current_question + 1} / {len(self.questions)}"
        )
        self.progressbar["value"] = self.current_question

        # Reset banner feedback
        self.feedback_banner.config(
            text="",
            bg="#FFFFFF",
            fg="#334155"
        )

        # Reset dan perbarui timer label
        self.time_left = self.time_limit_per_question
        self.lbl_timer.config(
            text=f"⏱️ Sisa Waktu: {self.time_left}s",
            fg="#0F766E",
            bg="#CCFBF1"
        )

        # Pastikan jendela utama selalu memegang fokus keyboard aktif
        self.window.focus_set()
        self.window.focus_force()

    def start_timer(self):
        """Memulai timer countdown untuk soal saat ini menggunakan root.after()"""
        # Hentikan timer sebelumnya jika ada
        self.stop_timer()
        self.time_left = self.time_limit_per_question
        self.update_timer()

    def update_timer(self):
        """Looping rekursif timer menggunakan self.window.after()"""
        if self.is_feedback_active:
            return

        if self.time_left > 0:
            # Perubahan warna dinamis sesuai sisa waktu (Visual Alert)
            if self.time_left > 10:
                color_fg = "#0F766E"  # Hijau toska (Aman)
                color_bg = "#CCFBF1"
            elif self.time_left > 5:
                color_fg = "#B45309"  # Oranye (Peringatan)
                color_bg = "#FEF3C7"
            else:
                # Berkedip merah saat sisa waktu <= 5 detik
                color_fg = "#DC2626"  # Merah (Kritis)
                color_bg = "#FEE2E2" if self.time_left % 2 == 1 else "#FFFFFF"

            self.lbl_timer.config(
                text=f"⏱️ Sisa Waktu: {self.time_left}s",
                fg=color_fg,
                bg=color_bg
            )

            self.time_left -= 1
            # Jadwalkan panggilan berikutnya setelah 1000 ms (1 detik)
            self.timer_job = self.window.after(1000, self.update_timer)
        else:
            # Waktu habis!
            self.lbl_timer.config(text="⏱️ Waktu Habis!", fg="#DC2626", bg="#FEE2E2")
            self.handle_timeout()

    def stop_timer(self):
        """Membatalkan timer countdown dengan after_cancel()"""
        if self.timer_job is not None:
            self.window.after_cancel(self.timer_job)
            self.timer_job = None

    def cancel_animations(self):
        """Membatalkan seluruh animasi after() yang sedang berjalan"""
        for job in self.anim_jobs:
            try:
                self.window.after_cancel(job)
            except Exception:
                pass
        self.anim_jobs.clear()

        # Kembalikan posisi padding awal wrapper kartu
        self.card_wrapper.pack_configure(padx=self.base_card_padx)

    def set_controls_state(self, state):
        """Mengatur status aktif/nonaktif tombol dan opsi (mencegah multi-click saat animasi)"""
        for rb in self.radio_buttons:
            rb.config(state=state)
        self.btn_submit.config(state=state)
        self.btn_skip.config(state=state)

    def submit_answer(self, event=None):
        """Validasi pilihan jawaban dan proses evaluasi skor dengan animasi feedback"""
        if self.is_feedback_active or self.is_quiz_finished:
            return

        selected = self.selected_answer.get()

        # ================= VALIDASI INPUT =================
        # Konsep: Validasi input sebelum proses dilanjutkan
        if selected == -1:
            self.feedback_banner.config(
                text="⚠️ Silakan pilih salah satu jawaban terlebih dahulu! (Atau tekan 'Lewati' / [Esc])",
                fg="#B45309",
                bg="#FEF3C7"
            )
            # Animasi visual getar (Shake Animation) untuk memberi peringatan pada pengguna
            self.animate_shake(step=0)
            return

        # Kunci jawaban
        self.stop_timer()
        self.is_feedback_active = True
        self.set_controls_state(tk.DISABLED)

        q_data = self.questions[self.current_question]
        correct_idx = q_data["correct"]
        labels = ["A", "B", "C", "D"]

        # Evaluasi jawaban
        is_correct = (selected == correct_idx)

        if is_correct:
            self.score += 10
            # Update skor real-time
            self.score_badge.config(text=f"🏆 Skor: {self.score} Poin")

            # Catat riwayat
            self.history.append({
                "no": self.current_question + 1,
                "question": q_data["question"],
                "user_ans": f"{labels[selected]}. {q_data['options'][selected]}",
                "correct_ans": f"{labels[correct_idx]}. {q_data['options'][correct_idx]}",
                "status": "Benar (+10)",
                "result_type": "BENAR"
            })

            # Tampilkan pesan feedback benar
            self.feedback_banner.config(
                text="🎉 BENAR! Jawaban Anda tepat (+10 Poin)",
                fg="#15803D",
                bg="#DCFCE7"
            )

            # Highlight opsi yang benar dengan warna hijau
            self.radio_frames[selected].config(
                bg="#DCFCE7",
                highlightbackground="#22C55E",
                bd=2
            )
            self.radio_buttons[selected].config(
                bg="#DCFCE7",
                fg="#15803D",
                font=("Segoe UI", 10, "bold")
            )

            # Jalankan animasi visual pulse warna hijau
            self.animate_pulse_feedback(color_seq=["#86EFAC", "#4ADE80", "#22C55E", "#DCFCE7"], step=0)

        else:
            # Jawaban salah
            self.history.append({
                "no": self.current_question + 1,
                "question": q_data["question"],
                "user_ans": f"{labels[selected]}. {q_data['options'][selected]}",
                "correct_ans": f"{labels[correct_idx]}. {q_data['options'][correct_idx]}",
                "status": "Salah (0)",
                "result_type": "SALAH"
            })

            # Tampilkan feedback salah dan tunjukkan kunci jawaban
            self.feedback_banner.config(
                text=f"❌ SALAH! Jawaban yang benar adalah: {labels[correct_idx]}. {q_data['options'][correct_idx]}",
                fg="#B91C1C",
                bg="#FEE2E2"
            )

            # Tandai opsi salah (merah) dan opsi benar (hijau)
            self.radio_frames[selected].config(
                bg="#FEE2E2",
                highlightbackground="#EF4444",
                bd=2
            )
            self.radio_buttons[selected].config(
                bg="#FEE2E2",
                fg="#B91C1C"
            )

            self.radio_frames[correct_idx].config(
                bg="#DCFCE7",
                highlightbackground="#22C55E",
                bd=2
            )
            self.radio_buttons[correct_idx].config(
                bg="#DCFCE7",
                fg="#15803D",
                font=("Segoe UI", 10, "bold")
            )

            # Jalankan animasi visual getar (shake) untuk feedback jawaban salah
            self.animate_shake(step=0)

        # Simpan progres terkini ke disk (Auto-Save)
        self.save_progress()

        # Transisi otomatis ke soal berikutnya setelah delay 1.5 detik
        job = self.window.after(1500, self.next_question)
        self.anim_jobs.append(job)

    def skip_question(self, event=None):
        """Event handler untuk melewati soal saat ini (shortcut Esc)"""
        if self.is_feedback_active or self.is_quiz_finished:
            return

        self.stop_timer()
        self.is_feedback_active = True
        self.set_controls_state(tk.DISABLED)

        q_data = self.questions[self.current_question]
        correct_idx = q_data["correct"]
        labels = ["A", "B", "C", "D"]

        # Catat riwayat
        self.history.append({
            "no": self.current_question + 1,
            "question": q_data["question"],
            "user_ans": "(Dilewati)",
            "correct_ans": f"{labels[correct_idx]}. {q_data['options'][correct_idx]}",
            "status": "Dilewati (0)",
            "result_type": "DILEWATI"
        })

        # Feedback visual lewati
        self.feedback_banner.config(
            text=f"⏭️ Soal Dilewati! Kunci: {labels[correct_idx]}. {q_data['options'][correct_idx]}",
            fg="#475569",
            bg="#E2E8F0"
        )

        # Sorot kunci jawaban
        self.radio_frames[correct_idx].config(
            bg="#DCFCE7",
            highlightbackground="#22C55E",
            bd=2
        )
        self.radio_buttons[correct_idx].config(
            bg="#DCFCE7",
            fg="#15803D",
            font=("Segoe UI", 10, "bold")
        )

        # Simpan progres terkini ke disk (Auto-Save)
        self.save_progress()

        job = self.window.after(1200, self.next_question)
        self.anim_jobs.append(job)

    def handle_timeout(self):
        """Event handler ketika waktu habis (countdown mencapai 0)"""
        if self.is_feedback_active:
            return

        self.stop_timer()
        self.is_feedback_active = True
        self.set_controls_state(tk.DISABLED)

        q_data = self.questions[self.current_question]
        correct_idx = q_data["correct"]
        labels = ["A", "B", "C", "D"]

        # Catat riwayat
        self.history.append({
            "no": self.current_question + 1,
            "question": q_data["question"],
            "user_ans": "(Waktu Habis)",
            "correct_ans": f"{labels[correct_idx]}. {q_data['options'][correct_idx]}",
            "status": "Waktu Habis (0)",
            "result_type": "TIMEOUT"
        })

        # Feedback visual waktu habis
        self.feedback_banner.config(
            text=f"⏱️ WAKTU HABIS! Jawaban benar: {labels[correct_idx]}. {q_data['options'][correct_idx]}",
            fg="#B91C1C",
            bg="#FEE2E2"
        )

        # Sorot kunci jawaban yang benar
        self.radio_frames[correct_idx].config(
            bg="#DCFCE7",
            highlightbackground="#22C55E",
            bd=2
        )
        self.radio_buttons[correct_idx].config(
            bg="#DCFCE7",
            fg="#15803D",
            font=("Segoe UI", 10, "bold")
        )

        # Animasi getar saat waktu habis
        self.animate_shake(step=0)

        # Simpan progres terkini ke disk (Auto-Save)
        self.save_progress()

        job = self.window.after(1600, self.next_question)
        self.anim_jobs.append(job)

    def animate_shake(self, step=0):
        """Animasi visual horizontal shake menggunakan root.after() rekursif"""
        offsets = [-12, 12, -9, 9, -5, 5, -2, 2, 0]
        if step < len(offsets):
            dx = offsets[step]
            self.card_wrapper.pack_configure(padx=(self.base_card_padx + dx, self.base_card_padx - dx))
            job = self.window.after(35, lambda: self.animate_shake(step + 1))
            self.anim_jobs.append(job)
        else:
            self.card_wrapper.pack_configure(padx=self.base_card_padx)

    def animate_pulse_feedback(self, color_seq, step=0):
        """Animasi visual pulsing glow background banner menggunakan after()"""
        if step < len(color_seq):
            self.feedback_banner.config(bg=color_seq[step])
            job = self.window.after(70, lambda: self.animate_pulse_feedback(color_seq, step + 1))
            self.anim_jobs.append(job)
        else:
            self.feedback_banner.config(bg="#DCFCE7")

    def next_question(self):
        """Melanjutkan ke soal berikutnya atau menampilkan hasil akhir jika soal telah usai"""
        self.cancel_animations()
        self.current_question += 1

        if self.current_question < len(self.questions):
            self.save_progress()
            self.load_question()
            self.start_timer()
        else:
            # Seluruh soal telah selesai
            self.progressbar["value"] = len(self.questions)
            self.show_result()

    def show_result(self):
        """Menampilkan antarmuka hasil akhir kuis beserta review detail jawaban"""
        self.stop_timer()
        self.cancel_animations()
        self.is_quiz_finished = True
        self.clear_saved_progress()

        # Bersihkan container soal
        self.status_bar_frame.pack_forget()
        self.progress_frame.pack_forget()
        self.card_wrapper.pack_forget()
        self.action_frame.pack_forget()

        # Hitung statistik
        total_soal = len(self.questions)
        max_score = total_soal * 10
        percentage = (self.score / max_score) * 100 if max_score > 0 else 0

        total_benar = sum(1 for h in self.history if h["result_type"] == "BENAR")
        total_salah = sum(1 for h in self.history if h["result_type"] == "SALAH")
        total_dilewati = sum(1 for h in self.history if h["result_type"] in ["DILEWATI", "TIMEOUT"])

        # Tentukan gelar / badge performa
        if percentage >= 90:
            predikat = "LUAR BIASA! 🌟 (Sangat Menguasai Materi)"
            badge_color = "#15803D"
        elif percentage >= 75:
            predikat = "BAGUS SEKALI! 👏 (Pemahaman Konsep Sangat Baik)"
            badge_color = "#2563EB"
        elif percentage >= 60:
            predikat = "LULUS! 👍 (Pemahaman Cukup Baik)"
            badge_color = "#D97706"
        else:
            predikat = "PERLU BELAJAR LAGI! 📚 (Review Kembali Materi Modul)"
            badge_color = "#DC2626"

        # Frame Utama Hasil
        self.result_container = tk.Frame(self.window, bg="#F1F5F9")
        self.result_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=15)

        # Kartu Skor Ringkasan
        summary_card = tk.Frame(
            self.result_container,
            bg="#FFFFFF",
            relief=tk.SOLID,
            bd=1,
            highlightbackground="#E2E8F0",
            highlightthickness=1,
            padx=20,
            pady=15
        )
        summary_card.pack(fill=tk.X, pady=(0, 10))

        lbl_score_big = tk.Label(
            summary_card,
            text=f"Skor Akhir: {self.score} / {max_score} ({percentage:.0f}%)",
            font=("Segoe UI", 18, "bold"),
            fg=badge_color,
            bg="#FFFFFF"
        )
        lbl_score_big.pack()

        lbl_predikat = tk.Label(
            summary_card,
            text=predikat,
            font=("Segoe UI", 11, "bold"),
            fg=badge_color,
            bg="#FFFFFF"
        )
        lbl_predikat.pack(pady=(2, 8))

        # Baris Statistik Detail
        stats_frame = tk.Frame(summary_card, bg="#FFFFFF")
        stats_frame.pack()

        lbl_b = tk.Label(stats_frame, text=f"✅ Benar: {total_benar}", font=("Segoe UI", 10, "bold"), fg="#16A34A", bg="#FFFFFF")
        lbl_b.pack(side=tk.LEFT, padx=12)

        lbl_s = tk.Label(stats_frame, text=f"❌ Salah: {total_salah}", font=("Segoe UI", 10, "bold"), fg="#DC2626", bg="#FFFFFF")
        lbl_s.pack(side=tk.LEFT, padx=12)

        lbl_d = tk.Label(stats_frame, text=f"⏭️ Dilewati/Waktu Habis: {total_dilewati}", font=("Segoe UI", 10, "bold"), fg="#475569", bg="#FFFFFF")
        lbl_d.pack(side=tk.LEFT, padx=12)

        # Tabel Review Soal (ttk.Treeview)
        review_frame = tk.Frame(self.result_container, bg="#FFFFFF")
        review_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        tree_scroll = ttk.Scrollbar(review_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            review_frame,
            columns=("no", "status", "user_ans", "correct_ans"),
            show="headings",
            yscrollcommand=tree_scroll.set,
            height=6
        )
        tree_scroll.config(command=self.tree.yview)

        self.tree.heading("no", text="No")
        self.tree.heading("status", text="Hasil")
        self.tree.heading("user_ans", text="Jawaban Anda")
        self.tree.heading("correct_ans", text="Kunci Jawaban")

        self.tree.column("no", width=40, anchor="center")
        self.tree.column("status", width=110, anchor="center")
        self.tree.column("user_ans", width=260, anchor="w")
        self.tree.column("correct_ans", width=260, anchor="w")

        # Konfigurasi warna baris
        self.tree.tag_configure("row_benar", background="#DCFCE7", foreground="#14532D")
        self.tree.tag_configure("row_salah", background="#FEE2E2", foreground="#7F1D1D")
        self.tree.tag_configure("row_lewat", background="#F1F5F9", foreground="#334155")

        for item in self.history:
            tag = "row_lewat"
            if item["result_type"] == "BENAR":
                tag = "row_benar"
            elif item["result_type"] == "SALAH":
                tag = "row_salah"

            self.tree.insert(
                "",
                tk.END,
                values=(item["no"], item["status"], item["user_ans"], item["correct_ans"]),
                tags=(tag,)
            )

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Tombol Aksi Akhir (Ulangi Kuis & Keluar)
        bottom_btn_frame = tk.Frame(self.result_container, bg="#F1F5F9")
        bottom_btn_frame.pack(fill=tk.X, pady=(10, 0))

        btn_restart = tk.Button(
            bottom_btn_frame,
            text="🔄 Ulangi Kuis",
            command=self.restart_quiz,
            font=("Segoe UI", 11, "bold"),
            fg="#FFFFFF",
            bg="#2563EB",
            activebackground="#1D4ED8",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        btn_restart.pack(side=tk.LEFT)

        btn_exit = tk.Button(
            bottom_btn_frame,
            text="🚪 Keluar Aplikasi",
            command=self.on_closing,
            font=("Segoe UI", 11),
            fg="#334155",
            bg="#E2E8F0",
            activebackground="#CBD5E1",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        btn_exit.pack(side=tk.RIGHT)

    def save_progress(self):
        """Menyimpan progres kuis saat ini ke berkas JSON (Fitur Auto-Save)"""
        try:
            data = {
                "current_question": self.current_question,
                "score": self.score,
                "time_left": self.time_left,
                "history": self.history,
                "timestamp": time.time()
            }
            with open(self.progress_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[Auto-Save Error] Gagal menyimpan progres: {e}")

    def clear_saved_progress(self):
        """Menghapus berkas auto-save ketika kuis selesai atau diulang dari awal"""
        try:
            if os.path.exists(self.progress_file):
                os.remove(self.progress_file)
        except Exception as e:
            print(f"[Auto-Save Error] Gagal menghapus berkas progres: {e}")

    def check_and_load_progress(self):
        """Memeriksa apakah terdapat progres kuis sebelumnya yang belum selesai (Restore State)"""
        if not os.path.exists(self.progress_file):
            return False

        try:
            with open(self.progress_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            saved_q = data.get("current_question", 0)
            saved_score = data.get("score", 0)
            saved_history = data.get("history", [])
            saved_time = data.get("time_left", self.time_limit_per_question)

            # Hanya tawarkan lanjutkan jika progres masih di tengah-tengah kuis
            if 0 <= saved_q < len(self.questions) and (saved_q > 0 or len(saved_history) > 0):
                lanjutkan = messagebox.askyesno(
                    "Lanjutkan Kuis?",
                    f"Ditemukan progres pengerjaan kuis sebelumnya:\n\n"
                    f"• Sedang di Soal ke-{saved_q + 1} dari {len(self.questions)}\n"
                    f"• Skor saat ini: {saved_score} Poin\n"
                    f"• Soal terjawab: {len(saved_history)} soal\n\n"
                    f"Apakah Anda ingin melanjutkan progres tersebut?",
                    parent=self.window
                )
                # Segera kembalikan fokus keyboard ke jendela utama setelah dialog ditutup
                self.window.focus_force()
                self.window.focus_set()
                self.window.lift()
                if lanjutkan:
                    self.current_question = saved_q
                    self.score = saved_score
                    self.history = saved_history
                    # Berikan toleransi sisa waktu minimal 15 detik agar tidak langsung habis saat aplikasi dibuka
                    self.time_left = max(saved_time, 15)
                    self.score_badge.config(text=f"🏆 Skor: {self.score} Poin")
                    return True
                else:
                    self.clear_saved_progress()
            else:
                self.clear_saved_progress()
        except Exception as e:
            print(f"[Auto-Save Error] Gagal memuat berkas progres: {e}")
            self.clear_saved_progress()

        return False

    def restart_quiz(self):
        """Mereset seluruh state management kuis dan memulai dari soal pertama"""
        # Hancurkan frame hasil
        if hasattr(self, "result_container") and self.result_container.winfo_exists():
            self.result_container.destroy()

        # Reset status penyelesaian & hapus berkas auto-save
        self.is_quiz_finished = False
        self.clear_saved_progress()

        # Reset variabel state
        self.current_question = 0
        self.score = 0
        self.history.clear()
        self.score_badge.config(text="🏆 Skor: 0 Poin")

        # Tampilkan kembali komponen utama
        self.status_bar_frame.pack(fill=tk.X, padx=25, pady=(15, 0))
        self.progress_frame.pack(fill=tk.X, padx=25, pady=(4, 10))
        self.card_wrapper.pack(fill=tk.BOTH, expand=True, padx=25, pady=5)
        self.action_frame.pack(fill=tk.X, padx=25, pady=(5, 15))

        # Muat ulang soal
        self.load_question()
        self.start_timer()

    def on_closing(self):
        """Event handler saat aplikasi akan ditutup (Auto-Save & Graceful Shutdown)"""
        # Hentikan semua timer aktif agar thread mainloop berhenti bersih
        self.stop_timer()
        self.cancel_animations()

        # Simpan progres otomatis jika kuis masih berjalan dan belum selesai
        if self.current_question < len(self.questions) and not self.is_quiz_finished:
            self.save_progress()

        self.window.destroy()

    def jalankan(self):
        """Method utama untuk memulai event loop Tkinter"""
        self.window.mainloop()


if __name__ == "__main__":
    app = QuizApp()
    app.jalankan()

