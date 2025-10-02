import tkinter as tk
from tkinter import messagebox, ttk, font
import numpy as np
from enum import Enum


# --- CONFIGURATION (Centralized constants) ---

class AppConfig:
    """Centralizes all application constants and configuration."""
    APP_VERSION = "2.0"
    # Colors
    COLOR_OK = "#1C8040"
    COLOR_WARN = "#D9822B"
    COLOR_ERROR = "#C93838"
    COLOR_BACKGROUND = "#F0F0F0"
    COLOR_FRAME_BG = "#FFFFFF"
    COLOR_ACCENT = "#0078D4"
    COLOR_ACCENT_DARK = "#005a9e"
    COLOR_STALE_RESULT = "#888888"
    COLOR_INVALID_ENTRY = "#FFD2D2"
    COLOR_DISABLED_ENTRY = "#F7F7F7"

    # Fonts
    FONT_DEFAULT = ('Segoe UI', 10)
    FONT_BOLD = ('Segoe UI', 10, 'bold')
    FONT_TITLE = ('Segoe UI', 11, 'bold')
    FONT_HEADER = ('Segoe UI', 12, 'bold')
    FONT_MAIN_TITLE = ('Segoe UI', 16, 'bold')
    FONT_VALUE = ('Consolas', 12, 'bold')
    FONT_VALUE_STALE = ('Consolas', 12, 'normal')
    FONT_STATUS = ('Segoe UI', 11, 'bold')

    # Probe Data
    PROBE_MODELS = {
        "Manuale/Custom": 0.0e-12,
        "Sonda Attiva (Lo-Cap, <1pF)": 0.5e-12,
        "Sonda Passiva Standard (10x)": 11.0e-12,
        "Sonda Passiva Bassa Impedienza (1x)": 100.0e-12,
    }
    DEFAULT_PROBE_NAME = "Sonda Attiva (Lo-Cap, <1pF)"

    # GUI Layout Definitions
    PARAM_MAP = {
        "Parametri del Cristallo (XTAL Datasheet)": [
            ("FREQ", "Frequenza (F)", "30e6", "Hz", "Frequenza operativa nominale."),
            ("C0", "Capacità Shunt (C0)", "7.0e-12", "F", "Capacità del contenitore e degli elettrodi."),
            ("ESR_MAX", "ESR Max", "30.0", "Ohm", "Massima Resistenza Serie Equivalente."),
            ("DL_MAX", "DL Max", "0.5e-3", "W", "Massima potenza dissipabile."),
        ],
        "Parametri Circuito e MCU": [
            ("GM_MCU", "Gm MCU", "9.7e-3", "A/V", "Transconduttanza dell'amplificatore MCU."),
            ("CL_SEL", "CL Esterna (CL_sel)", "22.0e-12", "F", "Valore condensatori esterni (CL1=CL2)."),
            ("REXT_SEL", "Rext Selezionata", "0.0", "Ohm", "Resistenza in serie per limitazione corrente."),
            ("CS_PIN", "Cs PIN", "4.2e-12", "F", "Capacità parassita del pin XTAL (da datasheet)."),
            ("CS_PCB", "Cs PCB", "3.6e-12", "F", "Capacità parassita del layout PCB (Stray)."),
        ],
        "Misurazioni (Per calcolo DL effettivo)": [
            ("VPP_MEASURED", "Vpp Misurata", "0.125", "V", "Tensione Picco-Picco misurata su OSC_IN (pin CL1)."),
            ("C_PROBE", "Cap. Sonda (C_probe)", f"{PROBE_MODELS[DEFAULT_PROBE_NAME]:.1e}", "F",
             "Capacità della sonda DSO utilizzata."),
        ]
    }


# --- MODEL (Data and Business Logic) ---

class Param(Enum):
    FREQ, C0, ESR_MAX, DL_MAX, GM_MCU, CL_SEL, REXT_SEL, CS_PIN, CS_PCB, VPP_MEASURED, C_PROBE = range(11)


class CrystalCircuitModel:
    GM_MARGIN_THRESHOLD = 5.0

    def __init__(self):
        self.params = {}
        self.results = {}
        self.reset()

    def reset(self):
        self.params = {param: 0.0 for param in Param}
        self.results = {
            'cl_eff': 0.0, 'gm_crit': 0.0, 'gain_margin': 0.0,
            'rext_est': 0.0, 'drive_level': 0.0, 'dl_ratio': 0.0,
        }

    def set_param(self, key: Param, value: float):
        if not isinstance(key, Param):
            raise TypeError("La chiave deve essere un'istanza di Param Enum.")
        if value < 0:
            raise ValueError(f"Il valore per {key.name} non può essere negativo.")
        if key in [Param.FREQ, Param.ESR_MAX, Param.DL_MAX] and value <= 0:
            raise ValueError(f"Il valore per {key.name} deve essere positivo.")
        self.params[key] = value

    def calculate(self):
        try:
            f, c0, cs_pcb, cs_pin, cl_sel, esr_max, gm, dl_max, rext_sel, vpp_measured, c_probe = (
                self.params[p] for p in Param
            )

            total_esr = esr_max + rext_sel
            cs_tot = cs_pcb + cs_pin
            cl_eff = (cl_sel / 2.0) + cs_tot
            gm_crit = 4.0 * total_esr * (2 * np.pi * f) ** 2 * (c0 + cl_eff) ** 2
            gain_margin = gm / gm_crit if gm_crit > 0 else float('inf')
            rext_est = 1.0 / (2.0 * np.pi * f * cl_sel) if cl_sel > 0 else 0.0
            c_tot_dl = cl_sel + (cs_tot / 2.0) + c_probe
            drive_level = (total_esr * (np.pi * f * c_tot_dl * vpp_measured) ** 2) / 2.0
            dl_ratio = drive_level / dl_max if dl_max > 0 else float('inf')

            self.results.update({
                'cl_eff': cl_eff, 'gm_crit': gm_crit, 'gain_margin': gain_margin,
                'rext_est': rext_est, 'drive_level': drive_level, 'dl_ratio': dl_ratio,
            })
            return True, None
        except (ZeroDivisionError, ValueError) as e:
            error_message = f"Errore di calcolo nel modello: {e}"
            print(error_message)
            return False, error_message


# --- VIEW (GUI Rendering) ---

class MainView(ttk.Frame):
    """Manages all GUI widgets and layout."""

    def __init__(self, master, controller):
        super().__init__(master, padding="10")
        self.controller = controller

        self.vars = {}
        self.entries = {}
        self.output_labels = {}
        self.probe_combo = None

        self._configure_styles()
        self._create_widgets()

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        cfg = AppConfig
        style.configure("TFrame", background=cfg.COLOR_BACKGROUND)
        style.configure("TLabelFrame", background=cfg.COLOR_FRAME_BG, borderwidth=1, relief='solid',
                        font=cfg.FONT_TITLE)
        style.configure("TLabel", font=cfg.FONT_DEFAULT, background=cfg.COLOR_FRAME_BG)
        style.configure("Header.TLabel", font=cfg.FONT_MAIN_TITLE, background=cfg.COLOR_BACKGROUND,
                        foreground=cfg.COLOR_ACCENT_DARK)
        style.configure("TEntry", fieldbackground=cfg.COLOR_FRAME_BG, font=('Courier New', 10))
        style.map("Invalid.TEntry", fieldbackground=[("!disabled", cfg.COLOR_INVALID_ENTRY)])
        style.configure("Probe.TEntry", fieldbackground=cfg.COLOR_DISABLED_ENTRY, font=('Courier New', 10))
        style.configure("Calc.TButton", font=cfg.FONT_HEADER, padding=10, background=cfg.COLOR_ACCENT,
                        foreground='white')
        style.map("Calc.TButton", background=[('active', cfg.COLOR_ACCENT_DARK)])
        style.configure("Reset.TButton", font=cfg.FONT_DEFAULT, padding=5)

    def _create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)  # Input frame row
        self.rowconfigure(3, weight=2)  # Output frame row (more space)

        self._create_header(self)
        self._create_input_frame(self)
        self._create_control_frame(self)
        self._create_output_frame(self)

    def _create_header(self, parent):
        header_frame = ttk.Frame(parent, style="TFrame")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        ttk.Label(header_frame, text="Validatore Oscillatore a Cristallo", style="Header.TLabel").pack()

    def _create_input_frame(self, parent):
        frame = ttk.Frame(parent)
        frame.grid(row=1, column=0, sticky="nsew")  # Changed to nsew
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)  # Allow canvas to expand

        canvas = tk.Canvas(frame, borderwidth=0, background=AppConfig.COLOR_BACKGROUND,
                           highlightthickness=0)  # Removed fixed height
        v_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, padding="15")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_frame_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_frame_id, width=e.width))

        canvas.configure(yscrollcommand=v_scrollbar.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")

        scrollable_frame.columnconfigure(0, weight=1)
        self._populate_input_fields(scrollable_frame)

    def _populate_input_fields(self, parent_frame):
        for group_idx, (group_title, params) in enumerate(AppConfig.PARAM_MAP.items()):
            group_frame = ttk.LabelFrame(parent_frame, text=group_title, padding="15 15 15 10")
            group_frame.grid(row=group_idx, column=0, padx=5, pady=10, sticky="ew")
            group_frame.columnconfigure(0, minsize=250, weight=0)
            group_frame.columnconfigure(1, minsize=180, weight=0)
            group_frame.columnconfigure(2, weight=2)

            for i, (key_str, name, default, unit, desc) in enumerate(params):
                key = Param[key_str]
                var = tk.StringVar(value=default)
                var.trace_add("write", lambda *args, k=key: self.controller.on_input_change(k))
                self.vars[key] = var

                label = ttk.Label(group_frame, text=f"{name} [{unit}]:", font=AppConfig.FONT_BOLD)
                label.grid(row=i, column=0, sticky="e", padx=5, pady=5)

                desc_label = ttk.Label(group_frame, text=desc, foreground='gray', wraplength=450)

                if key == Param.C_PROBE:
                    self._create_probe_widget(group_frame, i, var)
                    desc_label.grid(row=i, column=2, sticky="w", padx=10, pady=5, rowspan=2)
                else:
                    entry = ttk.Entry(group_frame, textvariable=var, width=20, justify='right')
                    entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
                    self.entries[key] = entry
                    desc_label.grid(row=i, column=2, sticky="w", padx=10, pady=5)

    def _create_probe_widget(self, parent, row_idx, var):
        self.probe_combo = ttk.Combobox(parent, values=list(AppConfig.PROBE_MODELS.keys()), state='readonly', width=20)
        self.probe_combo.set(AppConfig.DEFAULT_PROBE_NAME)
        self.probe_combo.bind("<<ComboboxSelected>>", self.controller.update_probe_capacitance)
        self.probe_combo.grid(row=row_idx, column=1, padx=10, pady=(5, 0), sticky="ew")

        entry = ttk.Entry(parent, textvariable=var, width=20, justify='right', style="Probe.TEntry")
        entry.grid(row=row_idx + 1, column=1, padx=10, pady=(2, 5), sticky="ew")
        self.entries[Param.C_PROBE] = entry

    def _create_control_frame(self, parent):
        frame = ttk.Frame(parent, padding="10 0 10 0")
        frame.grid(row=2, column=0, pady=10)

        # Center the buttons within the frame
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=0)
        frame.columnconfigure(2, weight=0)
        frame.columnconfigure(3, weight=1)

        calc_button = ttk.Button(frame, text="ESECUZIONE CALCOLI", command=self.controller.run_calculation,
                                 style="Calc.TButton")
        calc_button.grid(row=0, column=1, padx=(0, 5))

        reset_button = ttk.Button(frame, text="Reset Valori", command=self.controller.reset_application,
                                  style="Reset.TButton")
        reset_button.grid(row=0, column=2, padx=(5, 0))

    def _create_output_frame(self, parent):
        frame = ttk.LabelFrame(parent, text="REPORT TECNICO: PARAMETRI DERIVATI", padding="15")
        frame.grid(row=3, column=0, padx=10, pady=(5, 10), sticky="nsew")

        frame.columnconfigure(0, minsize=300, weight=0)
        frame.columnconfigure(1, minsize=120, weight=0)
        frame.columnconfigure(2, minsize=50, weight=0)
        frame.columnconfigure(3, weight=1)

        output_defs = [
            ("cl_eff", "Capacità di Carico Effettiva (CL_eff):", "pF"),
            ("gm_crit", "Transconduttanza Critica (Gm_crit):", "mA/V"),
            ("gain_margin", "Margine di Guadagno (S_f = Gm/Gm_crit):", "Ratio"),
            ("rext_est", "Reattanza Circuitale (X_C):", "Ohm"),
            ("drive_level", "Drive Level Calcolato (DL):", "uW"),
        ]
        status_defs = [
            ("gm_crit_status", "Gm/Gm_crit (Avvio Oscillazione):"),
            ("gain_margin_status", "Margine di Guadagno (Robustezza):"),
            ("dl_status", "Drive Level (Affidabilità):"),
        ]

        row_idx = 0
        for key, text, unit in output_defs:
            ttk.Label(frame, text=text, font=AppConfig.FONT_BOLD).grid(row=row_idx, column=0, sticky="e", padx=5,
                                                                       pady=6)
            self.output_labels[key] = ttk.Label(frame, text="N/A", font=AppConfig.FONT_VALUE, anchor='e',
                                                foreground='#333')
            self.output_labels[key].grid(row=row_idx, column=1, sticky="e", padx=5)
            ttk.Label(frame, text=f"[{unit}]", foreground='darkgray').grid(row=row_idx, column=2, sticky="w")
            row_idx += 1

        ttk.Separator(frame, orient='horizontal').grid(row=row_idx, column=0, columnspan=4, sticky="ew", pady=15)
        row_idx += 1

        ttk.Label(frame, text="STATO DI VALIDAZIONE FINALE", font=AppConfig.FONT_HEADER,
                  foreground=AppConfig.COLOR_ACCENT).grid(row=row_idx, column=0, columnspan=4, sticky="w", pady=(5, 10))
        row_idx += 1

        for key, text in status_defs:
            ttk.Label(frame, text=text, font=AppConfig.FONT_BOLD).grid(row=row_idx, column=0, sticky="e", padx=5,
                                                                       pady=8)
            self.output_labels[key] = ttk.Label(frame, text="Eseguire Calcoli", font=AppConfig.FONT_STATUS)
            self.output_labels[key].grid(row=row_idx, column=1, columnspan=3, sticky="w", padx=10)
            row_idx += 1


# --- CONTROLLER (Application Logic) ---

class AppController:
    """Orchestrates the Model and the View."""

    def __init__(self, master):
        self.master = master
        self.model = CrystalCircuitModel()

        # Configure main window grid
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        self._create_menu()

        self.view = MainView(master, self)
        self.view.grid(row=0, column=0, sticky="nsew")

        self._create_status_bar()

    def _create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Esci", command=self.exit_application)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about_dialog)
        menubar.add_cascade(label="Help", menu=help_menu)

    def _create_status_bar(self):
        self.status_var = tk.StringVar(value="Pronto. Inserire i parametri e avviare il calcolo.")
        status_bar_frame = ttk.Frame(self.master, relief="sunken")
        status_bar_frame.grid(row=1, column=0, sticky="ew")
        status_bar = ttk.Label(status_bar_frame, textvariable=self.status_var, anchor=tk.W, padding=5)
        status_bar.pack(fill=tk.X)

    def on_input_change(self, param_key):
        """Called when any input StringVar changes."""
        self.status_var.set("I parametri sono stati modificati. Eseguire nuovamente il calcolo.")
        for key in self.view.output_labels:
            if '_status' not in key:
                self.view.output_labels[key].config(text="...", foreground=AppConfig.COLOR_STALE_RESULT,
                                                    font=AppConfig.FONT_VALUE_STALE)
            else:
                self.view.output_labels[key].config(text="Dati modificati, ricalcolare.",
                                                    foreground=AppConfig.COLOR_STALE_RESULT, font=AppConfig.FONT_STATUS)

    def update_probe_capacitance(self, event=None):
        """Updates the C_probe entry based on combobox selection."""
        selected_name = self.view.probe_combo.get()
        probe_entry = self.view.entries[Param.C_PROBE]
        probe_var = self.view.vars[Param.C_PROBE]

        if selected_name == "Manuale/Custom":
            probe_entry.config(state='normal')
            if not probe_var.get():
                probe_var.set("0.0")
        elif selected_name in AppConfig.PROBE_MODELS:
            probe_cap = AppConfig.PROBE_MODELS[selected_name]
            probe_var.set(f"{probe_cap:.1e}")
            probe_entry.config(state='readonly')
        self.on_input_change(Param.C_PROBE)

    def run_calculation(self):
        """Gathers data, triggers model calculation, and updates the view."""
        for key, entry in self.view.entries.items():
            style = "Probe.TEntry" if key == Param.C_PROBE else "TEntry"
            entry.configure(style=style)

        try:
            for key, var in self.view.vars.items():
                val_str = var.get().strip()
                if not val_str:
                    raise ValueError(f"Il campo {key.name} non può essere vuoto.")
                self.model.set_param(key, float(val_str))
        except (ValueError, TypeError) as e:
            err_msg = str(e)
            for key in Param:
                if key.name in err_msg:
                    self.view.entries[key].configure(style="Invalid.TEntry")
                    break
            messagebox.showerror("Errore di Input", f"Valore non valido: {e}")
            self.status_var.set(f"Errore: {e}")
            return

        success, error = self.model.calculate()
        if success:
            self._update_output_view()
            self.status_var.set("Calcoli eseguiti con successo.")
        else:
            messagebox.showerror("Errore di Calcolo", f"Impossibile completare il calcolo.\n{error}")
            self.status_var.set("Errore durante il calcolo.")

    def _update_output_view(self):
        results = self.model.results
        gm_mcu = self.model.params[Param.GM_MCU]
        dl_max = self.model.params[Param.DL_MAX]

        self.view.output_labels["cl_eff"].config(text=f"{results['cl_eff'] * 1e12:.3f}", font=AppConfig.FONT_VALUE,
                                                 foreground='#333')
        self.view.output_labels["gm_crit"].config(text=f"{results['gm_crit'] * 1e3:.3f}", font=AppConfig.FONT_VALUE,
                                                  foreground='#333')
        self.view.output_labels["gain_margin"].config(text=f"{results['gain_margin']:.3f}", font=AppConfig.FONT_VALUE,
                                                      foreground='#333')
        self.view.output_labels["rext_est"].config(text=f"{results['rext_est']:.3f}", font=AppConfig.FONT_VALUE,
                                                   foreground='#333')
        self.view.output_labels["drive_level"].config(text=f"{results['drive_level'] * 1e6:.3f}",
                                                      font=AppConfig.FONT_VALUE, foreground='#333')

        self._update_status_gm(gm_mcu, results['gm_crit'])
        self._update_status_gain_margin(results['gain_margin'])
        self._update_status_drive_level(results['drive_level'], dl_max, results['dl_ratio'])

    def _update_status_gm(self, gm_mcu, gm_crit):
        label = self.view.output_labels["gm_crit_status"]
        if gm_crit > gm_mcu:
            text = f"Gm ({gm_mcu * 1e3:.1f} mA/V) < Gm_crit ({gm_crit * 1e3:.1f} mA/V). Avvio non garantito. CRITICO."
            color = AppConfig.COLOR_ERROR
        else:
            text = f"Gm ({gm_mcu * 1e3:.1f} mA/V) > Gm_crit ({gm_crit * 1e3:.1f} mA/V). OK."
            color = AppConfig.COLOR_OK
        label.config(text=text, foreground=color)

    def _update_status_gain_margin(self, gain_margin):
        label = self.view.output_labels["gain_margin_status"]
        threshold = self.model.GM_MARGIN_THRESHOLD
        if gain_margin >= threshold:
            text = f"Gain Margin ({gain_margin:.2f}) >= {threshold:.1f}. ECCELLENTE."
            color = AppConfig.COLOR_OK
        elif gain_margin >= 3.0:
            text = f"Gain Margin ({gain_margin:.2f}) accettabile, ma < {threshold:.1f}. OTTIMIZZARE."
            color = AppConfig.COLOR_WARN
        else:
            text = f"Gain Margin ({gain_margin:.2f}) troppo basso. Rischio instabilità. CRITICO."
            color = AppConfig.COLOR_ERROR
        label.config(text=text, foreground=color)

    def _update_status_drive_level(self, drive_level, dl_max, dl_ratio):
        label = self.view.output_labels["dl_status"]
        if dl_ratio > 1.0:
            text = f"DL ({drive_level * 1e6:.1f} uW) ECCEDE DL Max ({dl_max * 1e6:.1f} uW). Rext obbligatoria. CRITICO."
            color = AppConfig.COLOR_ERROR
        elif dl_ratio > 0.8:
            text = f"DL ({drive_level * 1e6:.1f} uW) vicino al limite (DL/DL_max = {dl_ratio:.2f}). ATTENZIONE."
            color = AppConfig.COLOR_WARN
        else:
            text = f"DL ({drive_level * 1e6:.1f} uW) entro i limiti di sicurezza (DL/DL_max = {dl_ratio:.2f}). OK."
            color = AppConfig.COLOR_OK
        label.config(text=text, foreground=color)

    def reset_application(self):
        """Resets all input fields to their default values."""
        self.model.reset()
        for _, params in AppConfig.PARAM_MAP.items():
            for key_str, _, default, _, _ in params:
                key = Param[key_str]
                if key in self.view.vars:
                    self.view.vars[key].set(default)
        self.view.probe_combo.set(AppConfig.DEFAULT_PROBE_NAME)
        self.update_probe_capacitance()  # Ensure probe entry is also reset
        self.status_var.set("Pronto. I valori sono stati reimpostati.")

    def show_about_dialog(self):
        messagebox.showinfo(
            "About XTAL Validator",
            f"Validatore Oscillatore a Cristallo\nVersione: {AppConfig.APP_VERSION}\n\n"
            "Questo strumento aiuta a validare il design di un circuito oscillatore a cristallo "
            "basato sui parametri del datasheet e sulle misurazioni del circuito."
        )

    def exit_application(self):
        self.master.quit()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("XTAL Validator - Rev. Professional UI")
    root.geometry("1100x850")
    root.minsize(900, 750)
    root.configure(background=AppConfig.COLOR_BACKGROUND)

    app = AppController(root)

    root.mainloop()

