import tkinter as tk
from tkinter import messagebox, ttk, font, filedialog, simpledialog
import json
import os
import numpy as np
from enum import Enum


# --- CONFIGURATION (Centralized constants) ---

class AppConfig:
    """Centralizes all application constants and configuration."""
    APP_VERSION = "3.4"  # Versione aggiornata
    LIBRARY_FILENAME = "xtal_library.json"

    # Colors (Scientific Paper Theme)
    COLOR_OK = "#006400"                # Dark Green
    COLOR_WARN = "#E69500"              # Amber/Ochre
    COLOR_ERROR = "#C00000"             # Dark Red
    COLOR_BACKGROUND = "#FFFFFF"        # White
    COLOR_FRAME_BG = "#FDFDFD"          # Off-white
    COLOR_ACCENT = "#A00000"             # Dark, academic red
    COLOR_ACCENT_DARK = "#700000"        # Darker red for active states
    COLOR_TEXT_PRIMARY = "#000000"       # Black
    COLOR_TEXT_SECONDARY = "#555555"     # Dark Gray
    COLOR_SEPARATOR = "#DDDDDD"         # Light Gray
    COLOR_STALE_RESULT = "#777777"       # Gray
    COLOR_INVALID_ENTRY = "#FFEEEE"     # Light pink
    COLOR_DISABLED_ENTRY = "#F5F5F5"    # Very light gray

    # Fonts (Scientific Paper Theme)
    FONT_DEFAULT = ('Times New Roman', 11)
    FONT_ITALIC = ('Times New Roman', 10, 'italic')
    FONT_BOLD = ('Times New Roman', 11, 'bold')
    FONT_TITLE = ('Times New Roman', 12, 'bold')
    FONT_GROUP_TITLE = ('Times New Roman', 13, 'bold')
    FONT_HEADER = ('Times New Roman', 14, 'bold')
    FONT_MAIN_TITLE = ('Times New Roman', 18, 'bold')
    FONT_VALUE = ('Times New Roman', 12, 'bold')
    FONT_VALUE_STALE = ('Times New Roman', 12, 'normal')
    FONT_STATUS = ('Times New Roman', 11, 'bold')
    FONT_FINAL_STATUS = ('Times New Roman', 16, 'bold')
    # Font for the formulas window
    FONT_FORMULA_TITLE = ('Times New Roman', 13, 'bold')
    FONT_FORMULA = ('Courier New', 11, 'bold') # Monospaced for formulas
    FONT_FORMULA_DESC = ('Times New Roman', 11)

    # Unit Multipliers
    UNIT_MULTIPLIERS = {
        'Hz': 1, 'kHz': 1e3, 'MHz': 1e6,
        'F': 1, 'pF': 1e-12, 'nF': 1e-9, 'uF': 1e-6,
        'Ohm': 1, 'kOhm': 1e3,
        'W': 1, 'mW': 1e-3, 'uW': 1e-6,
        'A/V': 1, 'mA/V': 1e-3,
        'V': 1, 'mV': 1e-3,
    }

    # Probe Data
    PROBE_MODELS = {
        "Manuale/Custom": 0.0,
        "Sonda Attiva (LeCroy ZS1500)": 0.9,  # Valore in pF
        "Sonda Passiva (Tek P5050B)": 12.0,  # Valore in pF
    }
    DEFAULT_PROBE_NAME = "Manuale/Custom"

    # Crystal Presets
    XTAL_PRESETS = {
        "Manuale/Custom": {},
        "ECS-250-10-36Q-AES-TR": {
            "FREQ": ("25", "MHz"),
            "C0": ("5", "pF"),
            "ESR_MAX": ("60", "Ohm"),
            "DL_MAX": ("100", "uW"),
        },
        "Abracon IXA20 (24MHz)": {
            "FREQ": ("24", "MHz"),
            "C0": ("5", "pF"),
            "ESR_MAX": ("40", "Ohm"),
            "DL_MAX": ("300", "uW"),
        },
        "MicroCrystal CM7V-T1A (32.768kHz)": {
            "FREQ": ("32.768", "kHz"),
            "C0": ("1.3", "pF"),
            "ESR_MAX": ("70", "kOhm"),
            "DL_MAX": ("1.0", "uW"),
        }
    }
    DEFAULT_XTAL_NAME = "Manuale/Custom"

    # GUI Layout Definitions
    PARAM_MAP = {
        "Parametri del Cristallo (XTAL Datasheet)": [
            ("FREQ", "Frequenza (F)", "", "MHz", ['MHz', 'kHz', 'Hz'], "Frequenza operativa nominale."),
            ("C0", "Capacità Shunt (C0)", "", "pF", ['pF', 'nF', 'F'],
             "Capacità del contenitore e degli elettrodi."),
            ("ESR_MAX", "ESR Max", "", "Ohm", ['Ohm', 'kOhm'], "Massima Resistenza Serie Equivalente."),
            ("DL_MAX", "DL Max", "", "uW", ['uW', 'mW', 'W'], "Massima potenza dissipabile."),
        ],
        "Parametri Circuito e MCU": [
            ("GM_MCU", "Gm MCU", "", "mA/V", ['mA/V', 'A/V'], "Transconduttanza dell'amplificatore MCU."),
            ("CL_SEL", "CL Esterna (CL_sel)", "", "pF", ['pF', 'nF', 'F'],
             "Valore condensatori esterni (CL1=CL2)."),
            ("REXT_SEL", "Rext Selezionata", "", "Ohm", ['Ohm', 'kOhm'],
             "Resistenza in serie per limitazione corrente."),
            ("CS_PIN", "Cs PIN", "", "pF", ['pF', 'nF', 'F'], "Capacità parassita del singolo pin MCU (un ramo)."),
            ("CS_PCB", "Cs PCB", "", "pF", ['pF', 'nF', 'F'], "Capacità parassita della singola linea PCB (un ramo)."),
        ],
        "Misurazioni (Per calcolo DL effettivo)": [
            ("VPP_MEASURED", "Vpp Misurata", "", "mV", ['mV', 'V'],
             "Tensione Picco-Picco misurata su OSC_IN (pin CL1)."),
            ("C_PROBE", "Cap. Sonda (C_probe)", "", "pF", ['pF', 'nF', 'F'],
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
            'x_cl': 0.0, 'drive_level': 0.0, 'dl_ratio': 0.0,
            'c_tot_dl': 0.0
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
            p = self.params
            f, c0, cs_pcb, cs_pin, cl_sel, esr_max, gm, dl_max, rext_sel, vpp_measured, c_probe = (
                p[Param.FREQ], p[Param.C0], p[Param.CS_PCB], p[Param.CS_PIN], p[Param.CL_SEL],
                p[Param.ESR_MAX], p[Param.GM_MCU], p[Param.DL_MAX], p[Param.REXT_SEL],
                p[Param.VPP_MEASURED], p[Param.C_PROBE]
            )

            total_esr = esr_max + rext_sel

            c_stray_single_leg = cs_pcb + cs_pin
            cl_eff = (cl_sel + c_stray_single_leg) / 2.0
            gm_crit = 4.0 * total_esr * (2 * np.pi * f) ** 2 * (c0 + cl_eff) ** 2
            gain_margin = gm / gm_crit if gm_crit > 0 else float('inf')
            x_cl = 1.0 / (2 * np.pi * f * cl_sel) if cl_sel > 0 else 0.0
            c_tot_dl = cl_sel + c_stray_single_leg + c_probe
            drive_level = (total_esr / 2.0) * (np.pi * f * c_tot_dl * vpp_measured) ** 2
            dl_ratio = drive_level / dl_max if dl_max > 0 else float('inf')

            self.results.update({
                'cl_eff': cl_eff, 'gm_crit': gm_crit, 'gain_margin': gain_margin,
                'x_cl': x_cl, 'drive_level': drive_level, 'dl_ratio': dl_ratio,
                'c_tot_dl': c_tot_dl
            })
            return True, None
        except (ZeroDivisionError, ValueError) as e:
            error_message = f"Errore di calcolo nel modello: {e}"
            print(error_message)
            return False, error_message


# --- VIEW (GUI Rendering) ---

class FormulasView(tk.Toplevel):
    """Finestra che mostra le formule di calcolo utilizzate."""

    def __init__(self, master):
        super().__init__(master)
        self.title("Formule di Calcolo")
        self.geometry("750x650")
        self.configure(background=AppConfig.COLOR_BACKGROUND)

        # Frame principale con scrollbar
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = tk.Canvas(main_frame, borderwidth=0, background=AppConfig.COLOR_FRAME_BG)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="Input.TFrame")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Contenuto della finestra
        self._populate_formulas(scrollable_frame)

    def _add_formula_block(self, parent, title, formula, description):
        """Helper per aggiungere un blocco formattato di formula."""
        frame = ttk.Frame(parent, padding=15, style="Input.TFrame")
        frame.pack(fill="x", pady=(0, 10))

        ttk.Label(frame, text=title, font=AppConfig.FONT_FORMULA_TITLE, style="Input.TLabel",
                  foreground=AppConfig.COLOR_ACCENT_DARK).pack(anchor="w")
        ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=5)

        ttk.Label(frame, text=formula, font=AppConfig.FONT_FORMULA, style="Input.TLabel", background="#E8F4FD").pack(
            anchor="w", pady=5, padx=5)

        desc_label = ttk.Label(frame, text=description, font=AppConfig.FONT_FORMULA_DESC, style="Input.TLabel",
                               wraplength=650, justify="left")
        desc_label.pack(anchor="w", pady=(10, 0))

    def _populate_formulas(self, parent):
        """Aggiunge tutte le formule alla finestra."""

        title_1 = "1. Capacità di Carico Effettiva (CL,eff)"
        formula_1 = "CL,eff = (CL,sel + Cs,pin + Cs,pcb) / 2"
        desc_1 = (
            "Rappresenta la capacità di carico totale vista dal quarzo. È calcolata come la serie delle capacità totali presenti su ciascuno dei due rami dell'oscillatore. "
            "Questo valore è cruciale perché determina la frequenza di oscillazione finale.")
        self._add_formula_block(parent, title_1, formula_1, desc_1)

        title_2 = "2. Transconduttanza Critica (gm,crit)"
        formula_2 = "gm,crit = 4 × Rtot × (2π × F)² × (C0 + CL,eff)²"
        desc_2 = (
            "È la minima transconduttanza (guadagno) che l'amplificatore dell'MCU deve possedere per avviare e sostenere l'oscillazione. "
            "Rtot è la somma di ESR e Rext.")
        self._add_formula_block(parent, title_2, formula_2, desc_2)

        title_3 = "3. Margine di Guadagno (Gain Margin)"
        formula_3 = "Gain Margin = gm,MCU / gm,crit"
        desc_3 = (
            "Indica la robustezza dell'oscillatore. È il rapporto tra il guadagno fornito dall'MCU e quello minimo richiesto per oscillare. Un valore ≥ 5 è considerato sicuro (come da AN2867).")
        self._add_formula_block(parent, title_3, formula_3, desc_3)

        title_4 = "4. Capacità Totale per Drive Level (Ctot)"
        formula_4 = "Ctot = CL,sel + Cs,pin + Cs,pcb + Cprobe"
        desc_4 = (
            "È la somma di tutte le capacità parallelo presenti su un singolo ramo del circuito durante la misurazione con una sonda. "
            "Questo valore è usato per calcolare la corrente che scorre nel ramo e, di conseguenza, la potenza dissipata dal quarzo.")
        self._add_formula_block(parent, title_4, formula_4, desc_4)

        title_5 = "5. Drive Level (DL)"
        formula_5 = "DL = (Rtot / 2) × (π × F × Ctot × Vpp)²"
        desc_5 = (
            "Rappresenta la potenza dissipata dal quarzo. Questo valore deve essere inferiore al massimo specificato dal costruttore del quarzo per evitarne il danneggiamento. "
            "Rtot è (ESR + Rext) e Vpp è la tensione picco-picco misurata sul ramo.")
        self._add_formula_block(parent, title_5, formula_5, desc_5)


class MainView(ttk.Frame):
    """Manages all GUI widgets and layout."""

    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.vars = {}
        self.entries = {}
        self.unit_combos = {}
        self.output_labels = {}
        self.probe_combo = None
        self.xtal_combo = None
        self.delete_xtal_button = None

        self._configure_styles()
        self._create_widgets()

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use('classic')

        cfg = AppConfig

        # General widget configurations
        style.configure("TFrame", background=cfg.COLOR_BACKGROUND)
        style.configure("Input.TFrame", background=cfg.COLOR_FRAME_BG)
        style.configure("TLabel", font=cfg.FONT_DEFAULT, background=cfg.COLOR_BACKGROUND,
                        foreground=cfg.COLOR_TEXT_PRIMARY)
        style.configure("Input.TLabel", background=cfg.COLOR_FRAME_BG, foreground=cfg.COLOR_TEXT_PRIMARY)
        style.configure("Header.TLabel", font=cfg.FONT_MAIN_TITLE, background=cfg.COLOR_BACKGROUND,
                        foreground=cfg.COLOR_TEXT_PRIMARY)
        style.configure("Group.TLabel", font=cfg.FONT_GROUP_TITLE, background=cfg.COLOR_BACKGROUND,
                        foreground=cfg.COLOR_TEXT_PRIMARY)
        style.configure('TSeparator', background=cfg.COLOR_SEPARATOR)

        # Entry fields
        style.configure("TEntry",
                        font=('Times New Roman', 11),
                        padding=5)
        style.map("TEntry",
                  fieldbackground=[('readonly', cfg.COLOR_DISABLED_ENTRY)],
                  foreground=[('readonly', cfg.COLOR_TEXT_SECONDARY)])
        style.configure("Invalid.TEntry", fieldbackground=cfg.COLOR_INVALID_ENTRY)

        # Buttons
        style.configure("TButton",
                        font=cfg.FONT_DEFAULT,
                        padding=(10, 5),
                        relief='raised')
        style.map("TButton",
                  background=[('active', cfg.COLOR_DISABLED_ENTRY)])

        style.configure("Calc.TButton",
                        font=cfg.FONT_HEADER,
                        padding=(20, 10),
                        background=cfg.COLOR_ACCENT,
                        foreground='white')
        style.map("Calc.TButton",
                  background=[('active', cfg.COLOR_ACCENT_DARK)])

        style.configure("Secondary.TButton",
                        font=cfg.FONT_DEFAULT,
                        padding=(10, 5))

        style.configure("Delete.TButton", foreground=cfg.COLOR_ERROR)

        # Combobox
        style.configure("TCombobox",
                        font=('Times New Roman', 11),
                        padding=5)

    def _create_widgets(self):
        self.pack(fill="both", expand=True)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)

        self._create_header(self)
        self._create_library_controls(self)
        self._create_input_frame(self)
        self._create_control_frame(self)
        self._create_output_frame(self)

    def _create_header(self, parent):
        header_frame = ttk.Frame(parent, padding=(10, 10, 10, 20))
        header_frame.grid(row=0, column=0, sticky="ew")
        ttk.Label(header_frame, text="Crystal Oscillator Validator", style="Header.TLabel").pack()

    def _create_library_controls(self, parent):
        frame = ttk.Frame(parent, padding=(10, 0, 10, 20))
        frame.grid(row=1, column=0, sticky="ew")

        ttk.Label(frame, text="Libreria Quarzi:", font=AppConfig.FONT_BOLD).pack(side="left", padx=(0, 10))

        self.xtal_combo = ttk.Combobox(frame, state='readonly', width=30)
        self.xtal_combo.set(AppConfig.DEFAULT_XTAL_NAME)
        self.xtal_combo.bind("<<ComboboxSelected>>", self.controller.load_from_library)
        self.xtal_combo.pack(side="left")

        save_button = ttk.Button(frame, text="Salva Quarzo", style="Secondary.TButton",
                                 command=self.controller.save_to_library)
        save_button.pack(side="left", padx=(10, 0))

        self.delete_xtal_button = ttk.Button(frame, text="Elimina", style="Delete.TButton",
                                             command=self.controller.delete_from_library, state="disabled")
        self.delete_xtal_button.pack(side="left", padx=(5, 0))

    def update_xtal_library_list(self, library_keys):
        self.xtal_combo['values'] = library_keys

    def _create_input_frame(self, parent):
        frame = ttk.Frame(parent, padding=(10, 0))
        frame.grid(row=2, column=0, sticky="ew")
        frame.columnconfigure(0, weight=1)
        self._populate_input_fields(frame)

    def _populate_input_fields(self, parent_frame):
        input_container = ttk.Frame(parent_frame)
        input_container.pack(fill=tk.BOTH, expand=True)

        row_idx = 0
        for group_idx, (group_title, params) in enumerate(AppConfig.PARAM_MAP.items()):
            if group_idx > 0:
                ttk.Separator(input_container).grid(row=row_idx, column=0, sticky='ew', pady=(15, 10))
                row_idx += 1

            title = ttk.Label(input_container, text=group_title, style="Group.TLabel")
            title.grid(row=row_idx, column=0, sticky='w', pady=(0, 10))
            row_idx += 1

            for _, (key_str, name, default_val, default_unit, units, desc) in enumerate(params):
                key = Param[key_str]
                var = tk.StringVar(value=default_val)
                var.trace_add("write", lambda *args, k=key: self.controller.on_input_change(k))
                self.vars[key] = var

                bg_frame = ttk.Frame(input_container, style="Input.TFrame")
                bg_frame.grid(row=row_idx, column=0, sticky='nsew')

                bg_frame.columnconfigure(0, minsize=320, weight=0)
                bg_frame.columnconfigure(1, weight=1)
                bg_frame.columnconfigure(2, weight=2)

                label = ttk.Label(bg_frame, text=f"{name}:", font=AppConfig.FONT_BOLD, style="Input.TLabel")
                label.grid(row=0, column=0, sticky="e", padx=(0, 10), pady=5)

                input_field_frame = ttk.Frame(bg_frame, style="Input.TFrame")
                input_field_frame.grid(row=0, column=1, sticky='ew', pady=5)
                input_field_frame.columnconfigure(0, weight=1)

                entry = ttk.Entry(input_field_frame, textvariable=var, width=15, justify='right')
                entry.grid(row=0, column=0, sticky='ew')
                self.entries[key] = entry

                unit_combo = ttk.Combobox(input_field_frame, values=units, width=6, state='readonly')
                unit_combo.set(default_unit)
                unit_combo.bind("<<ComboboxSelected>>", lambda e, k=key: self.controller.on_input_change(k))
                unit_combo.grid(row=0, column=1, sticky='w', padx=5)
                self.unit_combos[key] = unit_combo

                desc_label = ttk.Label(bg_frame, text=desc, foreground=AppConfig.COLOR_TEXT_SECONDARY, wraplength=400,
                                       font=AppConfig.FONT_ITALIC, style="Input.TLabel")
                desc_label.grid(row=0, column=2, sticky="w", padx=10, pady=5)

                if key == Param.C_PROBE:
                    self._create_probe_selector(bg_frame, row=0, column=3)

                row_idx += 1

    def _create_probe_selector(self, parent, row, column):
        parent.columnconfigure(column, weight=0)
        probe_selector_frame = ttk.Frame(parent, style="Input.TFrame")
        probe_selector_frame.grid(row=row, column=column, sticky='e', padx=10)

        ttk.Label(probe_selector_frame, text="Preset Sonda:", style="Input.TLabel").pack(side='left')
        self.probe_combo = ttk.Combobox(probe_selector_frame, values=list(AppConfig.PROBE_MODELS.keys()),
                                        state='readonly', width=28)
        self.probe_combo.set(AppConfig.DEFAULT_PROBE_NAME)
        self.probe_combo.bind("<<ComboboxSelected>>", self.controller.update_probe_capacitance)
        self.probe_combo.pack(side='left', padx=5)

    def _create_control_frame(self, parent):
        frame = ttk.Frame(parent, padding="10 0 10 0")
        frame.grid(row=3, column=0, pady=25)

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=0)
        frame.columnconfigure(2, weight=1)

        button_container = ttk.Frame(frame)
        button_container.grid(row=0, column=1)

        calc_button = ttk.Button(button_container, text="Esegui Calcoli", command=self.controller.run_calculation,
                                 style="Calc.TButton")
        calc_button.pack(side='left', padx=(0, 5))

        reset_button = ttk.Button(button_container, text="Reset Valori", command=self.controller.reset_application,
                                  style="Secondary.TButton")
        reset_button.pack(side='left', padx=(5, 0))

    def _create_output_frame(self, parent):
        frame = ttk.Frame(parent, padding=(10, 0))
        frame.grid(row=4, column=0, sticky="nsew")
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        bg_frame = ttk.Frame(frame, style='Input.TFrame', padding=20)
        bg_frame.grid(sticky='nsew')
        bg_frame.columnconfigure(0, minsize=320, weight=0)
        bg_frame.columnconfigure(1, minsize=120, weight=0)
        bg_frame.columnconfigure(2, minsize=50, weight=0)
        bg_frame.columnconfigure(3, weight=1)

        title_label = ttk.Label(bg_frame, text="REPORT TECNICO: PARAMETRI DERIVATI", font=AppConfig.FONT_GROUP_TITLE,
                                foreground=AppConfig.COLOR_TEXT_PRIMARY, style='Input.TLabel')
        title_label.grid(row=0, column=0, columnspan=4, sticky='w', pady=(0, 20))

        output_defs = [
            ("cl_eff", "Capacità di Carico Effettiva (CL_eff):", "pF"),
            ("gm_crit", "Transconduttanza Critica (Gm_crit):", "mA/V"),
            ("gain_margin", "Margine di Guadagno (S_f = Gm/Gm_crit):", "Ratio"),
            ("x_cl", "Reattanza di Carico (X_CL):", "Ohm"),
            ("c_tot_dl", "Capacità Totale per DL (Ctot):", "pF"),
            ("drive_level", "Drive Level Calcolato (DL):", "uW"),
        ]
        status_defs = [
            ("gm_crit_status", "Gm/Gm_crit (Avvio Oscillazione):"),
            ("gain_margin_status", "Margine di Guadagno (Robustezza):"),
            ("dl_status", "Drive Level (Affidabilità):"),
        ]

        row_idx = 1
        for key, text, unit in output_defs:
            ttk.Label(bg_frame, text=text, font=AppConfig.FONT_BOLD, style="Input.TLabel").grid(row=row_idx, column=0,
                                                                                                sticky="e", padx=5,
                                                                                                pady=6)
            self.output_labels[key] = ttk.Label(bg_frame, text="N/A", font=AppConfig.FONT_VALUE, anchor='e',
                                                foreground=AppConfig.COLOR_TEXT_SECONDARY, style="Input.TLabel")
            self.output_labels[key].grid(row=row_idx, column=1, sticky="e", padx=5)
            ttk.Label(bg_frame, text=f"[{unit}]", foreground=AppConfig.COLOR_TEXT_SECONDARY, style="Input.TLabel").grid(
                row=row_idx, column=2, sticky="w")
            row_idx += 1

        ttk.Separator(bg_frame).grid(row=row_idx, column=0, columnspan=4, sticky="ew", pady=15)
        row_idx += 1

        ttk.Label(bg_frame, text="STATO DI VALIDAZIONE", font=AppConfig.FONT_HEADER,
                  foreground=AppConfig.COLOR_ACCENT_DARK, style="Input.TLabel").grid(row=row_idx, column=0,
                                                                                     columnspan=4, sticky="w",
                                                                                     pady=(5, 10))
        row_idx += 1

        for key, text in status_defs:
            ttk.Label(bg_frame, text=text, font=AppConfig.FONT_BOLD, style="Input.TLabel").grid(row=row_idx, column=0,
                                                                                                sticky="e", padx=5,
                                                                                                pady=8)
            self.output_labels[key] = ttk.Label(bg_frame, text="Inserire i dati e calcolare",
                                                font=AppConfig.FONT_STATUS,
                                                style="Input.TLabel", foreground=AppConfig.COLOR_TEXT_SECONDARY)
            self.output_labels[key].grid(row=row_idx, column=1, columnspan=3, sticky="w", padx=10)
            row_idx += 1

        # --- MODIFICA: Aggiunta etichetta stato finale ---
        ttk.Separator(bg_frame).grid(row=row_idx, column=0, columnspan=4, sticky="ew", pady=(20, 10))
        row_idx += 1

        final_status_label_title = ttk.Label(bg_frame, text="RISULTATO FINALE:", font=AppConfig.FONT_HEADER, style="Input.TLabel")
        final_status_label_title.grid(row=row_idx, column=0, sticky="e", padx=5, pady=10)

        self.output_labels["final_status"] = ttk.Label(bg_frame, text="---", font=AppConfig.FONT_FINAL_STATUS, style="Input.TLabel")
        self.output_labels["final_status"].grid(row=row_idx, column=1, columnspan=3, sticky="w", padx=10)
        row_idx += 1


# --- CONTROLLER (Application Logic) ---

class AppController:
    """Orchestrates the Model and the View."""

    def __init__(self, master):
        self.master = master
        self.model = CrystalCircuitModel()
        self.xtal_library = {}
        self._formulas_window = None

        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        self._create_menu()

        main_frame = ttk.Frame(master)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        canvas = tk.Canvas(main_frame, borderwidth=0, background=AppConfig.COLOR_BACKGROUND, highlightthickness=0)
        v_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=v_scrollbar.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")

        self.view = MainView(canvas, self)
        canvas_frame_id = canvas.create_window((0, 0), window=self.view, anchor="nw")

        self.view.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_frame_id, width=e.width))

        self._create_status_bar()
        self._load_xtal_library()

        self.status_var.set("Pronto. Inserire i valori per iniziare.")

    def _create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Salva Lavoro", command=self.save_work)
        file_menu.add_command(label="Carica Lavoro", command=self.load_work)
        file_menu.add_separator()
        file_menu.add_command(label="Esci", command=self.exit_application)
        menubar.add_cascade(label="File", menu=file_menu)

        formulas_menu = tk.Menu(menubar, tearoff=0)
        formulas_menu.add_command(label="Mostra Formule di Calcolo", command=self.show_formulas_window)
        menubar.add_cascade(label="Formule", menu=formulas_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about_dialog)
        menubar.add_cascade(label="Help", menu=help_menu)

    def show_formulas_window(self):
        """Crea e mostra la finestra con le formule."""
        if self._formulas_window is None or not self._formulas_window.winfo_exists():
            self._formulas_window = FormulasView(self.master)
        self._formulas_window.lift()
        self._formulas_window.focus()

    def _create_status_bar(self):
        self.status_var = tk.StringVar()
        status_bar_frame = ttk.Frame(self.master, relief="sunken", style="TFrame")
        status_bar_frame.grid(row=1, column=0, sticky="ew")
        status_bar = ttk.Label(status_bar_frame, textvariable=self.status_var, anchor=tk.W, padding=5)
        status_bar.pack(fill=tk.X)

    def on_input_change(self, param_key=None):
        """Called when any input StringVar changes."""
        self.status_var.set("I parametri sono stati modificati. Eseguire nuovamente il calcolo.")
        for key in self.view.output_labels:
            if '_status' not in key:
                self.view.output_labels[key].config(text="...", foreground=AppConfig.COLOR_TEXT_SECONDARY,
                                                    font=AppConfig.FONT_VALUE_STALE)
            else:
                default_text = "Dati modificati, ricalcolare."
                if key == 'final_status':
                    default_text = "---"
                self.view.output_labels[key].config(text=default_text,
                                                    foreground=AppConfig.COLOR_TEXT_SECONDARY,
                                                    font=AppConfig.FONT_STATUS)

    def _load_xtal_library(self):
        try:
            if os.path.exists(AppConfig.LIBRARY_FILENAME):
                with open(AppConfig.LIBRARY_FILENAME, 'r') as f:
                    self.xtal_library = json.load(f)
            else:
                self.xtal_library = {AppConfig.DEFAULT_XTAL_NAME: {}}
        except (json.JSONDecodeError, IOError) as e:
            messagebox.showerror("Errore Libreria", f"Impossibile caricare la libreria dei quarzi.\n{e}")
            self.xtal_library = {AppConfig.DEFAULT_XTAL_NAME: {}}

        if AppConfig.DEFAULT_XTAL_NAME not in self.xtal_library:
            self.xtal_library[AppConfig.DEFAULT_XTAL_NAME] = {}

        self.view.update_xtal_library_list(list(self.xtal_library.keys()))

    def _save_xtal_library(self):
        try:
            with open(AppConfig.LIBRARY_FILENAME, 'w') as f:
                json.dump(self.xtal_library, f, indent=4)
        except IOError as e:
            messagebox.showerror("Errore Libreria", f"Impossibile salvare la libreria dei quarzi.\n{e}")

    def save_to_library(self):
        try:
            if not self.view.vars[Param.FREQ].get().strip():
                messagebox.showwarning("Dati Mancanti",
                                       "Inserire almeno la frequenza del quarzo prima di salvare un preset.")
                return
        except (ValueError, TypeError):
            messagebox.showwarning("Dati non validi", "I dati inseriti per il quarzo non sono validi.")
            return

        new_name = simpledialog.askstring("Salva Preset Quarzo", "Inserisci un nome per il preset:", parent=self.master)
        if not new_name or not new_name.strip():
            return

        if new_name in self.xtal_library and new_name != AppConfig.DEFAULT_XTAL_NAME:
            if not messagebox.askyesno("Sovrascrivi Preset",
                                       f"Un preset con il nome '{new_name}' esiste già. Vuoi sovrascriverlo?"):
                return

        preset_data = {}
        preset_params = [Param.FREQ, Param.C0, Param.ESR_MAX, Param.DL_MAX]
        for key in preset_params:
            preset_data[key.name] = (self.view.vars[key].get(), self.view.unit_combos[key].get())

        self.xtal_library[new_name] = preset_data
        self._save_xtal_library()
        self.view.update_xtal_library_list(list(self.xtal_library.keys()))
        self.view.xtal_combo.set(new_name)
        self.load_from_library()
        messagebox.showinfo("Libreria Aggiornata", f"Il preset '{new_name}' è stato salvato con successo.")

    def delete_from_library(self):
        selected_name = self.view.xtal_combo.get()
        if selected_name == AppConfig.DEFAULT_XTAL_NAME:
            return

        if messagebox.askyesno("Conferma Eliminazione",
                               f"Sei sicuro di voler eliminare il preset '{selected_name}' dalla libreria?"):
            del self.xtal_library[selected_name]
            self._save_xtal_library()
            self._load_xtal_library()
            self.reset_application()
            self.status_var.set(f"Preset '{selected_name}' eliminato.")

    def load_from_library(self, event=None):
        selected_xtal = self.view.xtal_combo.get()
        preset = self.xtal_library.get(selected_xtal, {})

        preset_params_keys = [Param.FREQ, Param.C0, Param.ESR_MAX, Param.DL_MAX]
        for key in preset_params_keys:
            self.view.vars[key].set("")

        for key_str, (val, unit) in preset.items():
            key = Param[key_str]
            self.view.vars[key].set(val)
            self.view.unit_combos[key].set(unit)

        is_custom = selected_xtal == AppConfig.DEFAULT_XTAL_NAME
        self.view.delete_xtal_button.config(state='disabled' if is_custom else 'normal')

        for key in Param:
            is_preset_param = key in preset_params_keys
            entry_state = 'normal' if is_custom or not is_preset_param else 'readonly'
            combo_state = 'readonly' if is_custom or not is_preset_param else 'disabled'
            self.view.entries[key].config(state=entry_state)
            self.view.unit_combos[key].config(state=combo_state)

        self.on_input_change()

    def update_probe_capacitance(self, event=None):
        selected_name = self.view.probe_combo.get()

        if selected_name == "Manuale/Custom":
            self.view.entries[Param.C_PROBE].config(state='normal')
            self.view.vars[Param.C_PROBE].set("")
        elif selected_name in AppConfig.PROBE_MODELS:
            probe_cap_val = AppConfig.PROBE_MODELS[selected_name]
            self.view.vars[Param.C_PROBE].set(f"{probe_cap_val}")
            self.view.unit_combos[Param.C_PROBE].set("pF")
            self.view.entries[Param.C_PROBE].config(state='readonly')
        self.on_input_change()

    def _format_value(self, value, precision=3):
        if value is None or not np.isfinite(value):
            return "N/A"
        if value == 0:
            return f"0.{'0' * precision}"

        abs_val = abs(value)
        if abs_val > 0 and (abs_val < 1e-3 or abs_val >= 1e4):
            return f"{value:.{precision}e}"
        else:
            return f"{value:.{precision}f}"

    def run_calculation(self):
        for entry in self.view.entries.values():
            if entry.cget('state') != 'readonly':
                entry.configure(style="TEntry")

        try:
            for key, var in self.view.vars.items():
                val_str = var.get().strip()
                unit_str = self.view.unit_combos[key].get()

                if not val_str:
                    raise ValueError(f"Il campo {key.name} non può essere vuoto.")

                base_value = float(val_str) * AppConfig.UNIT_MULTIPLIERS[unit_str]
                self.model.set_param(key, base_value)

        except (ValueError, TypeError) as e:
            err_msg = str(e)
            invalid_key = None
            if "could not convert string to float" in err_msg:
                messagebox.showerror("Errore di Input", f"Valore non numerico inserito. Controllare i campi.")
                self.status_var.set(f"Errore: Valore non numerico.")
                return

            for p_key in Param:
                if p_key.name in err_msg:
                    invalid_key = p_key
                    break
            if invalid_key:
                self.view.entries[invalid_key].configure(style="Invalid.TEntry")

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

        self.view.output_labels["cl_eff"].config(text=self._format_value(results['cl_eff'] * 1e12))
        self.view.output_labels["gm_crit"].config(text=self._format_value(results['gm_crit'] * 1e3))
        self.view.output_labels["gain_margin"].config(text=self._format_value(results['gain_margin']))
        self.view.output_labels["x_cl"].config(text=self._format_value(results['x_cl']))
        self.view.output_labels["drive_level"].config(text=self._format_value(results['drive_level'] * 1e6))
        self.view.output_labels["c_tot_dl"].config(text=self._format_value(results['c_tot_dl'] * 1e12))

        keys_to_style = ["cl_eff", "gm_crit", "gain_margin", "x_cl", "drive_level", "c_tot_dl"]
        for key in keys_to_style:
            self.view.output_labels[key].config(font=AppConfig.FONT_VALUE, foreground=AppConfig.COLOR_TEXT_PRIMARY)

        self._update_status_labels()

    def _update_status_labels(self):
        results = self.model.results
        gm_mcu = self.model.params[Param.GM_MCU]
        dl_max = self.model.params[Param.DL_MAX]
        gain_margin = results['gain_margin']
        gm_crit = results['gm_crit']
        drive_level = results['drive_level']
        dl_ratio = results['dl_ratio']

        is_fail = False

        gm_label = self.view.output_labels["gm_crit_status"]
        gm_f = self._format_value(gm_mcu * 1e3, 1)
        gmc_f = self._format_value(gm_crit * 1e3, 1)
        if gm_crit > gm_mcu:
            gm_text = f"Gm ({gm_f} mA/V) < Gm_crit ({gmc_f} mA/V). Avvio non garantito. CRITICO."
            gm_color = AppConfig.COLOR_ERROR
            is_fail = True
        else:
            gm_text = f"Gm ({gm_f} mA/V) > Gm_crit ({gmc_f} mA/V). OK."
            gm_color = AppConfig.COLOR_OK
        gm_label.config(text=gm_text, foreground=gm_color)

        margin_label = self.view.output_labels["gain_margin_status"]
        threshold = self.model.GM_MARGIN_THRESHOLD
        gm_margin_f = self._format_value(gain_margin, 2)
        if gain_margin < 3.0:
            margin_text = f"Gain Margin ({gm_margin_f}) troppo basso. Rischio instabilità. CRITICO."
            margin_color = AppConfig.COLOR_ERROR
            is_fail = True
        elif gain_margin < threshold:
            margin_text = f"Gain Margin ({gm_margin_f}) accettabile, ma < {threshold:.1f}. OTTIMIZZARE."
            margin_color = AppConfig.COLOR_WARN
        else:
            margin_text = f"Gain Margin ({gm_margin_f}) >= {threshold:.1f}. ECCELLENTE."
            margin_color = AppConfig.COLOR_OK
        margin_label.config(text=margin_text, foreground=margin_color)

        dl_label = self.view.output_labels["dl_status"]
        dl_f = self._format_value(drive_level * 1e6, 1)
        dl_max_f = self._format_value(dl_max * 1e6, 1)
        dl_ratio_f = self._format_value(dl_ratio, 2)
        if dl_ratio > 1.0:
            dl_text = f"DL ({dl_f} uW) ECCEDE DL Max ({dl_max_f} uW). Rext obbligatoria. CRITICO."
            dl_color = AppConfig.COLOR_ERROR
            is_fail = True
        elif dl_ratio > 0.8:
            dl_text = f"DL ({dl_f} uW) vicino al limite (DL/DL_max = {dl_ratio_f}). ATTENZIONE."
            dl_color = AppConfig.COLOR_WARN
        else:
            dl_text = f"DL ({dl_f} uW) entro i limiti di sicurezza (DL/DL_max = {dl_ratio_f}). OK."
            dl_color = AppConfig.COLOR_OK
        dl_label.config(text=dl_text, foreground=dl_color)

        final_status_label = self.view.output_labels["final_status"]
        if is_fail:
            final_status_label.config(text="VALIDATION: FAIL", foreground=AppConfig.COLOR_ERROR, font=AppConfig.FONT_FINAL_STATUS)
        else:
            final_status_label.config(text="VALIDATION: PASS", foreground=AppConfig.COLOR_OK, font=AppConfig.FONT_FINAL_STATUS)

    def reset_application(self):
        """Resets all input fields to be empty."""
        self.model.reset()

        for key, var in self.view.vars.items():
            var.set("")

        self.view.xtal_combo.set(AppConfig.DEFAULT_XTAL_NAME)
        self.view.probe_combo.set(AppConfig.DEFAULT_PROBE_NAME)

        self.load_from_library()
        self.update_probe_capacitance()

        self.status_var.set("Pronto. I valori sono stati reimpostati.")
        self.on_input_change()
        for key, label in self.view.output_labels.items():
            if '_status' in key:
                default_text = "Inserire i dati e calcolare"
                if key == 'final_status':
                    default_text = "---"
                label.config(text=default_text)
            else:
                label.config(text="N/A")

    def save_work(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".xtal",
            filetypes=[("Crystal Validator Work Files", "*.xtal"), ("All Files", "*.*")]
        )
        if not filepath:
            return

        try:
            data_to_save = {}
            for key in Param:
                data_to_save[key.name] = {
                    "value": self.view.vars[key].get(),
                    "unit": self.view.unit_combos[key].get()
                }

            data_to_save["__presets__"] = {
                "xtal": self.view.xtal_combo.get(),
                "probe": self.view.probe_combo.get()
            }

            with open(filepath, 'w') as f:
                json.dump(data_to_save, f, indent=4)

            self.status_var.set(f"Lavoro salvato in: {filepath}")
        except Exception as e:
            messagebox.showerror("Errore di Salvataggio", f"Impossibile salvare il file.\nErrore: {e}")
            self.status_var.set("Salvataggio fallito.")

    def load_work(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Crystal Validator Work Files", "*.xtal"), ("All Files", "*.*")]
        )
        if not filepath:
            return

        try:
            with open(filepath, 'r') as f:
                data = json.load(f)

            for key in Param:
                if key.name in data:
                    self.view.vars[key].set(data[key.name].get("value", ""))
                    self.view.unit_combos[key].set(data[key.name].get("unit", "pF"))

            if "__presets__" in data:
                self.view.xtal_combo.set(data["__presets__"].get("xtal", AppConfig.DEFAULT_XTAL_NAME))
                self.view.probe_combo.set(data["__presets__"].get("probe", AppConfig.DEFAULT_PROBE_NAME))

            self.load_from_library()
            self.update_probe_capacitance()

            self.status_var.set(f"Lavoro caricato da: {filepath}")

        except Exception as e:
            messagebox.showerror("Errore di Caricamento", f"Impossibile caricare il file.\nErrore: {e}")
            self.status_var.set("Caricamento fallito.")

    def show_about_dialog(self):
        messagebox.showinfo(
            "About Crystal Oscillator Validator",
            f"Crystal Oscillator Validator\nVersione: {AppConfig.APP_VERSION}\n\n"
            f"Questo strumento aiuta a validare il design di un circuito oscillatore a cristallo "
            "basato sui parametri del datasheet e sulle misurazioni del circuito."
        )

    def exit_application(self):
        self.master.quit()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Crystal Oscillator Validator")
    root.geometry("1200x950")
    root.minsize(1000, 850)
    root.configure(background=AppConfig.COLOR_BACKGROUND)

    app = AppController(root)

    root.mainloop()