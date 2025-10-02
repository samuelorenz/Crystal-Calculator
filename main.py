import tkinter as tk
from tkinter import messagebox, ttk, font, filedialog
import json
import numpy as np
from enum import Enum


# --- CONFIGURATION (Centralized constants) ---

class AppConfig:
    """Centralizes all application constants and configuration."""
    APP_VERSION = "3.4"
    # Icona dell'applicazione (formato base64 per non avere file esterni)
    ICON_DATA = """
    R0lGODlhIAAgAPcAMf//////zP//mf//Zv//M///AP/MzP/Mmf/MZv/MM//MAP+ZzP+Zmf+ZZv+ZM/+Z
    AP9mM/9mmf9mZv9mM/9mAP8AzP8Amf8AZv8AM/8AAMz/zMz/mcz/Zsz/M8z/AMzMzMzMmcyZZszMM8zM
    AMyZzMyZmcyZZsyZM8yZAMyZzDNmmcyZZsxmM8yZAMxmM8xmmcxmZsxmM8xmAMwAzMwAmcwAZswAM8wA
    AJn/zJn/mZn/Zpn/M5n/AJnMzJnMmZmZZpnMM5nMAJmZzJmZmZmZZpmZM5mZAJmZzDNmmZmZZplmM5mZ
    AJlmM5lmmZlmZplmM5lmAJkAAGb/zGb/mWb/Zmb/M2b/AGbMzGbMmWaZZmbMM2bMAGaZzGaZmWaZZmaZ
    M2aZAGaZzDNmmWaZZh5mM2aZAGZmzGZmmWZmZmZmM2ZmAGYAzGYAmWYAZmYAM2YAAP//zP//mf//Zv//
    M///AADMzADMmf/MZv/MM//MAD+ZzD+Zmf+ZZv+ZM/+ZAD9mMz9mmf9mZv9mMz9mAD8AzD8Amf8AZv8A
    M/8AADD/zDD/mTD/ZzD/MzD/AACSzACSkyySWSwyMwySAACZzACZmSyZWSwyMyaZAACZzDNmkyyZWRxm
    MyaZAACSWRxmMyaSAADMkyyMWRxmMyaSAAAAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYA
    MyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYA
    MyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYA
    MyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYA
    MyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYA
    MyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYA
    MyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMyYAMiYA
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    AAAAAAAAAAAAAAAAACH5BAEAAPwALAAAAAAgACAAAAj/AP8JHEiwoMGDCBMqXMiwocOHECNKnEixosWL
    GDNq3Mixo8ePIEOKHEmypMmTKFOqXMmypcuXMGPKnEmzps2bOHPq3Mmzp8+fQIMKHUq0qNGjSJMqXcq0
    qtOnBQRKnUq1qtWrWLNq3cq1q9evYMOKHUu2rNmzaNOqXcu2rdu3cOPKnUu3rt27ePPq3cu3r9+/gAML
    Hky4sOHDiBMrXsy4sePHkCNLnky5suXLmDNr3sy5s+fPoEOLHk26tOnTqFOrXs26tevXsGPLnk27tu3b
    uHPr3s27t+/fwIMLH068uPHjyJMrX868ufPn0KNLn069uvXr2LNr3869u/fv4MOL/x9Pvrz58+jTq1/P
    vr379/Djy59Pv779+/jz69/Pv7///wAGKOCABBZo4IEIJqjgggw26OCDEEYo4YQUVmjhhRhmqOGGHHbo
    4YcghijiiCSWaOKJKKao4oostujiizDGKOOMNNZo44045qjjjjz26OOPQA5JZJBEFmnkkUgmqeSSTDY5
    pJE86mQlk1BGKeWUVFZp5ZVYZqnlllx26eWXYIYp5phklmnmmWimqeaabLbp5ptwxinnnHTWaeedeOap
    55589unnn4AGKuighBZq6KGIJqrooow26uijkEYq6aSUtgIAAQAh+QQBAAD8ACwAAAAAIAAgAAAI/wD/
    CRxIsKDBgwgTKlzIsKHDhxAjSpxIsaLFixgzatzIsaPHjyBDihxJsqTJkyhTqlzJsqXLlzBjypxJs6bN
    mzhz6tzJs6fPn0CDCh1LdGjRgwgTKl3KtKnTp1CjSj0qCADVq1izat3KtavXr2DDih1LtqzZs2jTql3L
    tq3bt3Djyp1Lt67du3jz6t3Lt6/fv4ADCx5MuLDhw4gTK17MuLHjx5AjS55MubLly5gza97MubPnz6BD
    ix5NurTp06hTq17NurXr17Bjy55Nu7bt27hz697Nu7fv38CDCx9OvLjx48iTK1/OvLnz59CjS59Ovbr1
    69iza9/Ovbv37+DDi/8fT768+fPo06tfz769+/fw48ufT7++/fv48+vfz7+///8ABijggAQWaOCBCCao
    4IIMNujggxBGKOGEFFZo4YUYZqjhhhx26OGHIIYo4ogklmjiiSimqOKKLLbo4oswxijjjDTWaOONOOao
    44489ujjj0AOSeSQRBZp5JFIJqnkkkw26eSTUEYp5ZRUVmnllVhmqeWWXHbp5ZdghinmmGSWaeaZaKap
    5ppstunmm3DGKeecdNZp55145qnnnnz26eefgAYq6KCEFmrooYgmquiijDbq6KOQRirppJRWaumlmGaq
    6aacdurpp6CGKuqopJZq6qmopqrqqqy26uqrsMYq66y01mrrrbjmquuuvPbq66/ABissAAA7
    """
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
    FONT_ITALIC = ('Segoe UI', 9, 'italic')
    FONT_BOLD = ('Segoe UI', 10, 'bold')
    FONT_TITLE = ('Segoe UI', 11, 'bold')
    FONT_GROUP_TITLE = ('Segoe UI', 12, 'bold')
    FONT_HEADER = ('Segoe UI', 12, 'bold')
    FONT_MAIN_TITLE = ('Segoe UI', 16, 'bold')
    FONT_VALUE = ('Consolas', 12, 'bold')
    FONT_VALUE_STALE = ('Consolas', 12, 'normal')
    FONT_STATUS = ('Segoe UI', 11, 'bold')

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
    DEFAULT_PROBE_NAME = "Sonda Attiva (LeCroy ZS1500)"

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

    # GUI Layout Definitions: (key, name, default_val, default_unit, unit_list, description)
    PARAM_MAP = {
        "Parametri del Cristallo (XTAL Datasheet)": [
            ("FREQ", "Frequenza (F)", "30", "MHz", ['MHz', 'kHz', 'Hz'], "Frequenza operativa nominale."),
            ("C0", "Capacità Shunt (C0)", "7.0", "pF", ['pF', 'nF', 'F'],
             "Capacità del contenitore e degli elettrodi."),
            ("ESR_MAX", "ESR Max", "30.0", "Ohm", ['Ohm', 'kOhm'], "Massima Resistenza Serie Equivalente."),
            ("DL_MAX", "DL Max", "500", "uW", ['uW', 'mW', 'W'], "Massima potenza dissipabile."),
        ],
        "Parametri Circuito e MCU": [
            ("GM_MCU", "Gm MCU", "9.7", "mA/V", ['mA/V', 'A/V'], "Transconduttanza dell'amplificatore MCU."),
            ("CL_SEL", "CL Esterna (CL_sel)", "22.0", "pF", ['pF', 'nF', 'F'],
             "Valore condensatori esterni (CL1=CL2)."),
            ("REXT_SEL", "Rext Selezionata", "0.0", "Ohm", ['Ohm', 'kOhm'],
             "Resistenza in serie per limitazione corrente."),
            ("CS_PIN", "Cs PIN", "4.2", "pF", ['pF', 'nF', 'F'], "Capacità parassita del pin XTAL (per ramo)."),
            ("CS_PCB", "Cs PCB", "3.6", "pF", ['pF', 'nF', 'F'], "Capacità parassita del layout PCB (per ramo)."),
        ],
        "Misurazioni (Per calcolo DL effettivo)": [
            ("VPP_MEASURED", "Vpp Misurata", "125", "mV", ['mV', 'V'],
             "Tensione Picco-Picco misurata su OSC_IN (pin CL1)."),
            ("C_PROBE", "Cap. Sonda (C_probe)", f"{PROBE_MODELS[DEFAULT_PROBE_NAME]}", "pF", ['pF', 'nF', 'F'],
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
            # Get all params from the stored dictionary
            p = self.params
            f, c0, cs_pcb, cs_pin, cl_sel, esr_max, gm, dl_max, rext_sel, vpp_measured, c_probe = (
                p[Param.FREQ], p[Param.C0], p[Param.CS_PCB], p[Param.CS_PIN], p[Param.CL_SEL],
                p[Param.ESR_MAX], p[Param.GM_MCU], p[Param.DL_MAX], p[Param.REXT_SEL],
                p[Param.VPP_MEASURED], p[Param.C_PROBE]
            )

            total_esr = esr_max + rext_sel

            # Stray capacitance for a single leg of the circuit
            c_stray_single_leg = cs_pcb + cs_pin

            # Effective Load Capacitance (CL_eff) calculation based on AN2867.
            # It's the series combination of the two legs (CL_sel + C_stray_single_leg).
            cl_eff = (cl_sel + c_stray_single_leg) / 2.0

            # Critical Transconductance (Gm_crit)
            gm_crit = 4.0 * total_esr * (2 * np.pi * f) ** 2 * (c0 + cl_eff) ** 2

            # Gain Margin
            gain_margin = gm / gm_crit if gm_crit > 0 else float('inf')

            # Reactance of one load capacitor
            rext_est = 1.0 / (2 * np.pi * f * cl_sel) if cl_sel > 0 else 0.0

            # Drive Level calculation uses the total capacitance on the measured leg
            c_leg_for_dl = cl_sel + c_stray_single_leg + c_probe
            # Standard formula for Drive Level based on Vpp measured on one leg
            drive_level = (total_esr / 2.0) * (np.pi * f * c_leg_for_dl * vpp_measured) ** 2

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
        super().__init__(master)
        self.controller = controller

        self.vars = {}
        self.entries = {}
        self.unit_combos = {}
        self.output_labels = {}
        self.probe_combo = None
        self.xtal_combo = None

        self._configure_styles()
        self._create_widgets()

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        cfg = AppConfig
        style.configure("TFrame", background=cfg.COLOR_BACKGROUND)
        style.configure("Input.TFrame", background=cfg.COLOR_FRAME_BG)
        style.configure("TLabel", font=cfg.FONT_DEFAULT, background=cfg.COLOR_BACKGROUND)
        style.configure("Input.TLabel", background=cfg.COLOR_FRAME_BG)
        style.configure("Header.TLabel", font=cfg.FONT_MAIN_TITLE, background=cfg.COLOR_BACKGROUND,
                        foreground=cfg.COLOR_ACCENT_DARK)
        style.configure("Group.TLabel", font=cfg.FONT_GROUP_TITLE, background=cfg.COLOR_BACKGROUND,
                        foreground=cfg.COLOR_ACCENT_DARK)
        style.configure("TEntry", fieldbackground=cfg.COLOR_FRAME_BG, font=('Courier New', 10))
        style.map("Invalid.TEntry", fieldbackground=[("!disabled", cfg.COLOR_INVALID_ENTRY)])
        style.configure("Readonly.TEntry", fieldbackground=cfg.COLOR_DISABLED_ENTRY)
        style.configure("Calc.TButton", font=cfg.FONT_HEADER, padding=10, background=cfg.COLOR_ACCENT,
                        foreground='white')
        style.map("Calc.TButton", background=[('active', cfg.COLOR_ACCENT_DARK)])
        style.configure("Reset.TButton", font=cfg.FONT_DEFAULT, padding=5)
        style.configure("Output.TLabelframe", background=cfg.COLOR_FRAME_BG, borderwidth=1, relief='solid',
                        font=cfg.FONT_TITLE)

    def _create_widgets(self):
        self.pack(fill="both", expand=True, padx=10, pady=10)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)

        self._create_header(self)
        self._create_preset_selector(self)
        self._create_input_frame(self)
        self._create_control_frame(self)
        self._create_output_frame(self)

    def _create_header(self, parent):
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        ttk.Label(header_frame, text="Crystal Oscillator Validator", style="Header.TLabel").pack()

    def _create_preset_selector(self, parent):
        frame = ttk.Frame(parent, padding=(0, 0, 0, 15))
        frame.grid(row=1, column=0, sticky="ew")

        ttk.Label(frame, text="Preset Quarzo:", font=AppConfig.FONT_BOLD).pack(side="left", padx=(0, 10))

        self.xtal_combo = ttk.Combobox(frame, values=list(AppConfig.XTAL_PRESETS.keys()), state='readonly', width=30)
        self.xtal_combo.set(AppConfig.DEFAULT_XTAL_NAME)
        self.xtal_combo.bind("<<ComboboxSelected>>", self.controller.update_from_xtal_preset)
        self.xtal_combo.pack(side="left")

    def _create_input_frame(self, parent):
        frame = ttk.Frame(parent)
        frame.grid(row=2, column=0, sticky="ew")
        frame.columnconfigure(0, weight=1)
        self._populate_input_fields(frame)

    def _populate_input_fields(self, parent_frame):
        input_container = ttk.Frame(parent_frame, style="TFrame")
        input_container.pack(fill=tk.BOTH, expand=True)

        row_idx = 0
        for group_idx, (group_title, params) in enumerate(AppConfig.PARAM_MAP.items()):
            if group_idx > 0:
                ttk.Separator(input_container).grid(row=row_idx, column=0, sticky='ew', pady=(15, 10))
                row_idx += 1

            title = ttk.Label(input_container, text=group_title, style="Group.TLabel")
            title.grid(row=row_idx, column=0, sticky='w', pady=(0, 5))
            row_idx += 1

            for _, (key_str, name, default_val, default_unit, units, desc) in enumerate(params):
                key = Param[key_str]
                var = tk.StringVar(value=default_val)
                var.trace_add("write", lambda *args, k=key: self.controller.on_input_change(k))
                self.vars[key] = var

                bg_frame = tk.Frame(input_container, background=AppConfig.COLOR_FRAME_BG)
                bg_frame.grid(row=row_idx, column=0, sticky='nsew', ipady=2)

                bg_frame.columnconfigure(0, minsize=320, weight=0)  # Label
                bg_frame.columnconfigure(1, weight=1)  # Input Field Frame
                bg_frame.columnconfigure(2, weight=2)  # Description

                label = ttk.Label(bg_frame, text=f"{name}:", font=AppConfig.FONT_BOLD, style="Input.TLabel")
                label.grid(row=0, column=0, sticky="e", padx=(0, 10))

                input_field_frame = ttk.Frame(bg_frame, style="Input.TFrame")
                input_field_frame.grid(row=0, column=1, sticky='ew')
                input_field_frame.columnconfigure(0, weight=1)

                entry = ttk.Entry(input_field_frame, textvariable=var, width=15, justify='right')
                entry.grid(row=0, column=0, sticky='ew')
                self.entries[key] = entry

                unit_combo = ttk.Combobox(input_field_frame, values=units, width=6, state='readonly')
                unit_combo.set(default_unit)
                unit_combo.bind("<<ComboboxSelected>>", lambda e, k=key: self.controller.on_input_change(k))
                unit_combo.grid(row=0, column=1, sticky='w', padx=5)
                self.unit_combos[key] = unit_combo

                desc_label = ttk.Label(bg_frame, text=desc, foreground='gray', wraplength=400,
                                       font=AppConfig.FONT_ITALIC, style="Input.TLabel")
                desc_label.grid(row=0, column=2, sticky="w", padx=10)

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
        frame.grid(row=3, column=0, pady=20)

        frame.columnconfigure(0, weight=1)

        button_container = ttk.Frame(frame)
        button_container.grid(row=0, column=0)

        calc_button = ttk.Button(button_container, text="Esegui Calcoli", command=self.controller.run_calculation,
                                 style="Calc.TButton")
        calc_button.pack(side='left', padx=(0, 5))

        reset_button = ttk.Button(button_container, text="Reset Valori", command=self.controller.reset_application,
                                  style="Reset.TButton")
        reset_button.pack(side='left', padx=(5, 0))

    def _create_output_frame(self, parent):
        frame = ttk.LabelFrame(parent, text="REPORT TECNICO: PARAMETRI DERIVATI", style="Output.TLabelframe",
                               padding="15")
        frame.grid(row=4, column=0, sticky="nsew")

        frame.columnconfigure(0, minsize=320, weight=0)
        frame.columnconfigure(1, minsize=120, weight=0)
        frame.columnconfigure(2, minsize=50, weight=0)
        frame.columnconfigure(3, weight=1)

        output_defs = [
            ("cl_eff", "Capacità di Carico Effettiva (CL_eff):", "pF"),
            ("gm_crit", "Transconduttanza Critica (Gm_crit):", "mA/V"),
            ("gain_margin", "Margine di Guadagno (S_f = Gm/Gm_crit):", "Ratio"),
            ("rext_est", "Reattanza di Carico (X_CL):", "Ohm"),
            ("drive_level", "Drive Level Calcolato (DL):", "uW"),
        ]
        status_defs = [
            ("gm_crit_status", "Gm/Gm_crit (Avvio Oscillazione):"),
            ("gain_margin_status", "Margine di Guadagno (Robustezza):"),
            ("dl_status", "Drive Level (Affidabilità):"),
        ]

        row_idx = 0
        for key, text, unit in output_defs:
            ttk.Label(frame, text=text, font=AppConfig.FONT_BOLD, style="Input.TLabel").grid(row=row_idx, column=0,
                                                                                             sticky="e", padx=5, pady=6)
            self.output_labels[key] = ttk.Label(frame, text="N/A", font=AppConfig.FONT_VALUE, anchor='e',
                                                foreground='#333', style="Input.TLabel")
            self.output_labels[key].grid(row=row_idx, column=1, sticky="e", padx=5)
            ttk.Label(frame, text=f"[{unit}]", foreground='darkgray', style="Input.TLabel").grid(row=row_idx, column=2,
                                                                                                 sticky="w")
            row_idx += 1

        ttk.Separator(frame, orient='horizontal').grid(row=row_idx, column=0, columnspan=4, sticky="ew", pady=15)
        row_idx += 1

        ttk.Label(frame, text="STATO DI VALIDAZIONE FINALE", font=AppConfig.FONT_HEADER,
                  foreground=AppConfig.COLOR_ACCENT, style="Input.TLabel").grid(row=row_idx, column=0, columnspan=4,
                                                                                sticky="w", pady=(5, 10))
        row_idx += 1

        for key, text in status_defs:
            ttk.Label(frame, text=text, font=AppConfig.FONT_BOLD, style="Input.TLabel").grid(row=row_idx, column=0,
                                                                                             sticky="e", padx=5, pady=8)
            self.output_labels[key] = ttk.Label(frame, text="Eseguire Calcoli", font=AppConfig.FONT_STATUS,
                                                style="Input.TLabel")
            self.output_labels[key].grid(row=row_idx, column=1, columnspan=3, sticky="w", padx=10)
            row_idx += 1


# --- CONTROLLER (Application Logic) ---

class AppController:
    """Orchestrates the Model and the View."""

    def __init__(self, master):
        self.master = master
        self.model = CrystalCircuitModel()

        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        self._create_menu()

        # --- Main Scrolling Canvas Setup ---
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

        def on_view_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def on_canvas_configure(event):
            canvas.itemconfig(canvas_frame_id, width=event.width)

        self.view.bind("<Configure>", on_view_configure)
        canvas.bind("<Configure>", on_canvas_configure)

        self._create_status_bar()

    def _create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Salva Lavoro", command=self.save_work)
        file_menu.add_command(label="Carica Lavoro", command=self.load_work)
        file_menu.add_separator()
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

    def update_from_xtal_preset(self, event=None):
        """Updates input fields based on the selected crystal preset."""
        selected_xtal = self.view.xtal_combo.get()
        preset = AppConfig.XTAL_PRESETS.get(selected_xtal, {})

        # Define which parameters are controlled by the preset
        preset_params = [Param.FREQ, Param.C0, Param.ESR_MAX, Param.DL_MAX]

        is_custom = selected_xtal == AppConfig.DEFAULT_XTAL_NAME

        # Update values and states for preset-controlled fields
        for key in preset_params:
            if key.name in preset:
                val, unit = preset[key.name]
                self.view.vars[key].set(val)
                self.view.unit_combos[key].set(unit)

            entry_style = 'TEntry' if is_custom else 'Readonly.TEntry'
            self.view.entries[key].config(state='normal' if is_custom else 'readonly', style=entry_style)
            self.view.unit_combos[key].config(state='readonly' if is_custom else 'disabled')

        self.on_input_change(None)  # Mark results as stale

    def update_probe_capacitance(self, event=None):
        """Updates the C_probe entry based on combobox selection."""
        selected_name = self.view.probe_combo.get()

        if selected_name == "Manuale/Custom":
            self.view.entries[Param.C_PROBE].config(state='normal', style='TEntry')
        elif selected_name in AppConfig.PROBE_MODELS:
            probe_cap_val = AppConfig.PROBE_MODELS[selected_name]
            self.view.vars[Param.C_PROBE].set(f"{probe_cap_val}")
            self.view.unit_combos[Param.C_PROBE].set("pF")
            self.view.entries[Param.C_PROBE].config(state='readonly', style='Readonly.TEntry')
        self.on_input_change(Param.C_PROBE)

    def _format_value(self, value, precision=3):
        """Formats a number for display, using scientific notation for large/small values."""
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
        """Gathers data, triggers model calculation, and updates the view."""
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
        self.view.output_labels["rext_est"].config(text=self._format_value(results['rext_est']))
        self.view.output_labels["drive_level"].config(text=self._format_value(results['drive_level'] * 1e6))

        for key in ["cl_eff", "gm_crit", "gain_margin", "rext_est", "drive_level"]:
            self.view.output_labels[key].config(font=AppConfig.FONT_VALUE, foreground='#333')

        self._update_status_labels()

    def _update_status_labels(self):
        results = self.model.results
        gm_mcu = self.model.params[Param.GM_MCU]
        dl_max = self.model.params[Param.DL_MAX]
        gain_margin = results['gain_margin']
        gm_crit = results['gm_crit']
        drive_level = results['drive_level']
        dl_ratio = results['dl_ratio']

        # --- Gm/Gm_crit Status ---
        gm_label = self.view.output_labels["gm_crit_status"]
        gm_f = self._format_value(gm_mcu * 1e3, 1)
        gmc_f = self._format_value(gm_crit * 1e3, 1)
        if gm_crit > gm_mcu:
            gm_text = f"Gm ({gm_f} mA/V) < Gm_crit ({gmc_f} mA/V). Avvio non garantito. CRITICO."
            gm_color = AppConfig.COLOR_ERROR
        else:
            gm_text = f"Gm ({gm_f} mA/V) > Gm_crit ({gmc_f} mA/V). OK."
            gm_color = AppConfig.COLOR_OK
        gm_label.config(text=gm_text, foreground=gm_color)

        # --- Gain Margin Status ---
        margin_label = self.view.output_labels["gain_margin_status"]
        threshold = self.model.GM_MARGIN_THRESHOLD
        gm_margin_f = self._format_value(gain_margin, 2)
        if gain_margin >= threshold:
            margin_text = f"Gain Margin ({gm_margin_f}) >= {threshold:.1f}. ECCELLENTE."
            margin_color = AppConfig.COLOR_OK
        elif gain_margin >= 3.0:
            margin_text = f"Gain Margin ({gm_margin_f}) accettabile, ma < {threshold:.1f}. OTTIMIZZARE."
            margin_color = AppConfig.COLOR_WARN
        else:
            margin_text = f"Gain Margin ({gm_margin_f}) troppo basso. Rischio instabilità. CRITICO."
            margin_color = AppConfig.COLOR_ERROR
        margin_label.config(text=margin_text, foreground=margin_color)

        # --- Drive Level Status ---
        dl_label = self.view.output_labels["dl_status"]
        dl_f = self._format_value(drive_level * 1e6, 1)
        dl_max_f = self._format_value(dl_max * 1e6, 1)
        dl_ratio_f = self._format_value(dl_ratio, 2)
        if dl_ratio > 1.0:
            dl_text = f"DL ({dl_f} uW) ECCEDE DL Max ({dl_max_f} uW). Rext obbligatoria. CRITICO."
            dl_color = AppConfig.COLOR_ERROR
        elif dl_ratio > 0.8:
            dl_text = f"DL ({dl_f} uW) vicino al limite (DL/DL_max = {dl_ratio_f}). ATTENZIONE."
            dl_color = AppConfig.COLOR_WARN
        else:
            dl_text = f"DL ({dl_f} uW) entro i limiti di sicurezza (DL/DL_max = {dl_ratio_f}). OK."
            dl_color = AppConfig.COLOR_OK
        dl_label.config(text=dl_text, foreground=dl_color)

    def reset_application(self):
        """Resets all input fields to their default values."""
        self.model.reset()
        # Reset to manual mode
        self.view.xtal_combo.set(AppConfig.DEFAULT_XTAL_NAME)
        self.update_from_xtal_preset()

        # Set default values for manual mode
        for _, params in AppConfig.PARAM_MAP.items():
            for key_str, _, default_val, default_unit, _, _ in params:
                key = Param[key_str]
                if key in self.view.vars:
                    self.view.vars[key].set(default_val)
                    self.view.unit_combos[key].set(default_unit)

        self.view.probe_combo.set(AppConfig.DEFAULT_PROBE_NAME)
        self.update_probe_capacitance()
        self.status_var.set("Pronto. I valori sono stati reimpostati.")

    def save_work(self):
        """Saves all input parameters to a JSON file."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".xtal",
            filetypes=[("Crystal Oscillator Validator Files", "*.xtal"), ("All Files", "*.*")]
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
        """Loads input parameters from a JSON file."""
        filepath = filedialog.askopenfilename(
            filetypes=[("Crystal Oscillator Validator Files", "*.xtal"), ("All Files", "*.*")]
        )
        if not filepath:
            return

        try:
            with open(filepath, 'r') as f:
                data = json.load(f)

            for key in Param:
                if key.name in data:
                    self.view.vars[key].set(data[key.name].get("value", ""))
                    self.view.unit_combos[key].set(data[key.name].get("unit", ""))

            if "__presets__" in data:
                self.view.xtal_combo.set(data["__presets__"].get("xtal", AppConfig.DEFAULT_XTAL_NAME))
                self.view.probe_combo.set(data["__presets__"].get("probe", AppConfig.DEFAULT_PROBE_NAME))

            # Refresh UI state based on loaded presets
            self.update_from_xtal_preset()
            self.update_probe_capacitance()

            self.status_var.set(f"Lavoro caricato da: {filepath}")

        except Exception as e:
            messagebox.showerror("Errore di Caricamento",
                                 f"Impossibile caricare il file. Potrebbe essere corrotto o non valido.\nErrore: {e}")
            self.status_var.set("Caricamento fallito.")

    def show_about_dialog(self):
        messagebox.showinfo(
            "About Crystal Oscillator Validator",
            f"Crystal Oscillator Validator\nVersione: {AppConfig.APP_VERSION}\n\n"
            f"Creato da: Samuele Lorenzoni\n\n"
            "Questo strumento aiuta a validare il design di un circuito oscillatore a cristallo "
            "basato sui parametri del datasheet e sulle misurazioni del circuito."
        )

    def exit_application(self):
        self.master.quit()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Crystal Oscillator Validator")
    root.geometry("1200x900")
    root.minsize(1000, 800)
    root.configure(background=AppConfig.COLOR_BACKGROUND)

    try:
        icon = tk.PhotoImage(data=AppConfig.ICON_DATA)
        root.iconphoto(True, icon)
    except tk.TclError:
        print("Non è stato possibile caricare l'icona dell'applicazione.")

    app = AppController(root)

    root.mainloop()

