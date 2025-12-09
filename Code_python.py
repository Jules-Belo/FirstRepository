#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog, scrolledtext
import os
import time
import serial
from serial import SerialException

# ========= CONFIG ==========
PORT = '/dev/cu.usbmodem34B7DA6494902'
BAUDRATE = 1000000
TRIAL_DURATION = 10.0      # durée d'un essai (s)
DT = 0.01                  # période d'envoi des 'g' (100 Hz)

# ✅ Dossier cible FIXE
FOLDER_BASE = "/Users/julesbelo/Desktop/Cours/Master/M2/Github/GIT/FirstRepository/data"
os.makedirs(FOLDER_BASE, exist_ok=True)
# ===========================


class GaugeApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("IHM jauge de contrainte (UNO R4)")

        # État interne
        self.running = False
        self.ser = None
        self.file = None
        self.start_time_pc = None

        # --- Ligne 1 : info mode ---
        row = 0
        tk.Label(
            root,
            text=f"Port Arduino : {PORT} - Essai : {TRIAL_DURATION:.0f} s"
        ).grid(row=row, column=0, columnspan=4, sticky="w", padx=5, pady=5)

        # --- Ligne 2 : préfixe et numéro d'essai ---
        row += 1
        tk.Label(root, text="Préfixe fichier :").grid(
            row=row, column=0, sticky="e", padx=5, pady=5
        )
        self.prefix_var = tk.StringVar(value="Sujet01")
        tk.Entry(root, textvariable=self.prefix_var, width=20).grid(
            row=row, column=1, sticky="w", padx=5, pady=5
        )

        tk.Label(root, text="Essai n° :").grid(
            row=row, column=2, sticky="e", padx=5, pady=5
        )
        self.trial_var = tk.StringVar(value="1")
        tk.Entry(root, textvariable=self.trial_var, width=6).grid(
            row=row, column=3, sticky="w", padx=5, pady=5
        )

        # --- Ligne 3 : dossier cible ---
        row += 1
        tk.Label(root, text="Dossier :").grid(
            row=row, column=0, sticky="e", padx=5, pady=5
        )
        self.folder_var = tk.StringVar(value=os.path.abspath(FOLDER_BASE))
        tk.Entry(root, textvariable=self.folder_var, width=40).grid(
            row=row, column=1, columnspan=2, sticky="w", padx=5, pady=5
        )
        tk.Button(root, text="Parcourir", command=self.choose_folder).grid(
            row=row, column=3, sticky="w", padx=5, pady=5
        )

        # --- Ligne 4 : statut ---
        row += 1
        tk.Label(root, text="État :").grid(
            row=row, column=0, sticky="e", padx=5, pady=5
        )
        self.status_var = tk.StringVar(value="En attente")
        self.status_label = tk.Label(root, textvariable=self.status_var, fg="orange")
        self.status_label.grid(
            row=row, column=1, columnspan=3, sticky="w", padx=5, pady=5
        )

        # --- Ligne 5 : boutons ---
        row += 1
        tk.Button(
            root, text="Start (10 s)",
            command=self.start_trial,
            bg="#2e7d32", fg="white", width=12
        ).grid(row=row, column=0, padx=5, pady=5)

        tk.Button(
            root, text="Stop",
            command=self.stop_trial,
            bg="#c62828", fg="white", width=12
        ).grid(row=row, column=1, padx=5, pady=5)

        tk.Button(
            root, text="Quitter",
            command=self.quit_app, width=10
        ).grid(row=row, column=3, padx=5, pady=5, sticky="e")

        # --- Ligne 6 : log série ---
        row += 1
        self.log = scrolledtext.ScrolledText(root, width=90, height=20, state="disabled")
        self.log.grid(row=row, column=0, columnspan=4, padx=5, pady=5)

    # ---------- Utils UI ----------

    def choose_folder(self):
        folder = filedialog.askdirectory(initialdir=self.folder_var.get())
        if folder:
            self.folder_var.set(folder)

    def set_status(self, text: str, color: str = "orange"):
        self.status_var.set(text)
        self.status_label.config(fg=color)

    def log_print(self, text: str):
        self.log.config(state="normal")
        self.log.insert(tk.END, text + "\n")
        self.log.see(tk.END)
        self.log.config(state="disabled")

    # ---------- Gestion essai ----------

    def start_trial(self):
        if self.running:
            return

        prefix = self.prefix_var.get().strip()
        folder = self.folder_var.get().strip()
        trial_str = self.trial_var.get().strip()

        if not prefix or not folder or not trial_str.isdigit():
            self.set_status("Erreur : préfixe / essai / dossier", "red")
            return

        trial = int(trial_str)

        # Préparation fichier
        os.makedirs(folder, exist_ok=True)
        filename = f"{prefix}_T{trial:02d}.csv"
        filepath = os.path.join(folder, filename)

        try:
            self.file = open(filepath, "w")
            self.file.write("time_s,value\n")
        except Exception as e:
            self.set_status("Erreur ouverture fichier", "red")
            self.log_print(f"Erreur fichier : {e}")
            self.file = None
            return

        # Ouverture série
        try:
            self.ser = serial.Serial(PORT, BAUDRATE, timeout=0.05)
        except SerialException as e:
            self.set_status("Erreur port série", "red")
            self.log_print(f"Erreur série : {e}")
            self.file.close()
            self.file = None
            return

        time.sleep(2.0)
        self.ser.reset_input_buffer()

        # Envoi 'r'
        try:
            self.ser.write(b'r')
            self.ser.flush()
        except SerialException as e:
            self.set_status("Erreur envoi 'r'", "red")
            self.log_print(f"Erreur série : {e}")
            self.cleanup_serial_file()
            return

        self.running = True
        self.start_time_pc = time.time()

        self.set_status(f"Essai T{trial:02d} en cours ({TRIAL_DURATION:.0f} s)", "green")
        self.log_print(f">>> Start T{trial:02d}, fichier : {filepath}")

        self.schedule_read()

    def schedule_read(self):
        if not self.running:
            return

        elapsed = time.time() - self.start_time_pc
        if elapsed >= TRIAL_DURATION:
            self.stop_trial(auto=True)
            return

        # Envoi 'g'
        try:
            self.ser.write(b'g')
            self.ser.flush()
        except SerialException as e:
            self.log_print(f"Erreur envoi 'g' : {e}")
            self.stop_trial(auto=True)
            return

        # Lecture
        try:
            line = self.ser.readline().decode(errors='ignore').strip()
        except SerialException as e:
            self.log_print(f"Erreur lecture série : {e}")
            self.stop_trial(auto=True)
            return

        if line and ',' in line:
            try:
                t_str, v_str = line.split(',', 1)
                t_ms = int(t_str)
                val = float(v_str)

                t_s = t_ms / 1000.0
                val_cal = val

                if self.file:
                    self.file.write(f"{t_s:.6f},{val_cal:.6f}\n")

                self.log_print(f"{t_s:.3f} s -> {val_cal:.3f}")

            except ValueError:
                self.log_print(f"Ligne non valide : {line}")

        self.root.after(int(DT * 1000), self.schedule_read)

    def stop_trial(self, auto: bool = False):
        if not self.running:
            return

        self.running = False

        # Reset Arduino
        if self.ser:
            try:
                self.ser.write(b'x')
                self.ser.flush()
                time.sleep(0.05)
            except SerialException:
                pass

        self.cleanup_serial_file()

        try:
            trial = int(self.trial_var.get())
        except ValueError:
            trial = 1
        self.trial_var.set(str(trial + 1))

        if auto:
            self.set_status("Essai terminé automatiquement", "orange")
            self.log_print(">>> Essai terminé (auto).")
        else:
            self.set_status("Essai stoppé manuellement", "red")
            self.log_print(">>> Essai stoppé manuellement.")

    def cleanup_serial_file(self):
        if self.ser:
            try:
                self.ser.close()
            except Exception:
                pass
            self.ser = None

        if self.file:
            try:
                self.file.close()
            except Exception:
                pass
            self.file = None

        self.start_time_pc = None

    def quit_app(self):
        self.running = False

        if self.ser:
            try:
                self.ser.write(b'x')
                self.ser.flush()
            except SerialException:
                pass

        self.cleanup_serial_file()
        self.root.after(50, self.root.destroy)


if __name__ == "__main__":
    root = tk.Tk()
    app = GaugeApp(root)
    root.mainloop()