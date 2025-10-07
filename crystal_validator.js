document.addEventListener('DOMContentLoaded', () => {

    // --- 1. CONFIGURATION & STATE ---
    const AppConfig = {
        GM_MARGIN_THRESHOLD: 5.0,
        UNIT_MULTIPLIERS: {
            'Hz': 1, 'kHz': 1e3, 'MHz': 1e6,
            'F': 1, 'pF': 1e-12, 'nF': 1e-9, 'uF': 1e-6,
            'Ohm': 1, 'kOhm': 1e3,
            'W': 1, 'mW': 1e-3, 'uW': 1e-6,
            'A/V': 1, 'mA/V': 1e-3,
            'V': 1, 'mV': 1e-3,
        },
        PROBE_MODELS: {
            "Manuale/Custom": 0.0,
            "Sonda Attiva (LeCroy ZS1500)": 0.9,
            "Sonda Passiva (Tek P5050B)": 12.0,
        },
        DEFAULT_PROBE_NAME: "Manuale/Custom",
        DEFAULT_XTAL_NAME: "Manuale/Custom",
        PARAM_MAP: {
            "crystal-params": [
                { key: "FREQ", name: "Frequenza (F)", defVal: "", unit: "MHz", units: ['MHz', 'kHz', 'Hz'], desc: "Frequenza operativa nominale." },
                { key: "C0", name: "Capacità Shunt (C0)", defVal: "", unit: "pF", units: ['pF', 'nF', 'F'], desc: "Capacità del contenitore e degli elettrodi." },
                { key: "ESR_MAX", name: "ESR Max", defVal: "", unit: "Ohm", units: ['Ohm', 'kOhm'], desc: "Massima Resistenza Serie Equivalente." },
                { key: "DL_MAX", name: "DL Max", defVal: "", unit: "uW", units: ['uW', 'mW', 'W'], desc: "Massima potenza dissipabile." },
            ],
            "circuit-params": [
                { key: "GM_MCU", name: "Gm MCU", defVal: "", unit: "mA/V", units: ['mA/V', 'A/V'], desc: "Transconduttanza dell'amplificatore MCU." },
                { key: "CL_SEL", name: "CL Esterna (CL_sel)", defVal: "", unit: "pF", units: ['pF', 'nF', 'F'], desc: "Valore condensatori esterni (CL1=CL2)." },
                { key: "REXT_SEL", name: "Rext Selezionata", defVal: "0", unit: "Ohm", units: ['Ohm', 'kOhm'], desc: "Resistenza in serie per limitazione corrente." },
                { key: "CS_PIN", name: "Cs PIN", defVal: "", unit: "pF", units: ['pF', 'nF', 'F'], desc: "Capacità parassita del singolo pin MCU." },
                { key: "CS_PCB", name: "Cs PCB", defVal: "", unit: "pF", units: ['pF', 'nF', 'F'], desc: "Capacità parassita della singola linea PCB." },
            ],
            "measurement-params": [
                { key: "VPP_MEASURED", name: "Vpp Misurata", defVal: "", unit: "mV", units: ['mV', 'V'], desc: "Tensione Picco-Picco misurata su OSC_IN." },
                { key: "C_PROBE", name: "Cap. Sonda (C_probe)", defVal: "", unit: "pF", units: ['pF', 'nF', 'F'], desc: "Capacità della sonda DSO utilizzata." },
            ]
        },
        OUTPUT_MAP: [
            { key: "cl_eff", label: "Capacità di Carico Effettiva (CL_eff):", unit: "pF" },
            { key: "gm_crit", label: "Transconduttanza Critica (Gm_crit):", unit: "mA/V" },
            { key: "gain_margin", label: "Margine di Guadagno (S_f):", unit: "Ratio" },
            { key: "drive_level", label: "Drive Level Calcolato (DL):", unit: "uW" },
        ],
        STATUS_MAP: [
            { key: "gm_crit_status", label: "Gm/Gm_crit (Avvio Oscillazione):" },
            { key: "gain_margin_status", label: "Margine di Guadagno (Robustezza):" },
            { key: "dl_status", label: "Drive Level (Affidabilità):" },
        ]
    };

    const model = {
        params: {},
        results: {},
        reset() {
            this.params = {};
            this.results = {};
        },
        calculate() {
            try {
                const p = this.params;
                const f = p.FREQ, c0 = p.C0, cs_pcb = p.CS_PCB, cs_pin = p.CS_PIN, cl_sel = p.CL_SEL, esr_max = p.ESR_MAX, gm = p.GM_MCU, dl_max = p.DL_MAX, rext_sel = p.REXT_SEL, vpp = p.VPP_MEASURED, c_probe = p.C_PROBE;

                const total_esr = esr_max + rext_sel;
                const c_stray = cs_pcb + cs_pin;
                const cl_eff = (cl_sel + c_stray) / 2.0;
                const gm_crit = 4.0 * total_esr * Math.pow(2 * Math.PI * f, 2) * Math.pow(c0 + cl_eff, 2);
                const gain_margin = gm_crit > 0 ? gm / gm_crit : Infinity;
                const c_leg_for_dl = cl_sel + c_stray + c_probe;
                const drive_level = (total_esr / 2.0) * Math.pow(Math.PI * f * c_leg_for_dl * vpp, 2);
                const dl_ratio = dl_max > 0 ? drive_level / dl_max : Infinity;

                this.results = { cl_eff, gm_crit, gain_margin, drive_level, dl_ratio };
                return { success: true, error: null };
            } catch (e) {
                return { success: false, error: e.message };
            }
        }
    };

    // --- 2. UI ELEMENT GENERATION ---
    function initializeUI() {
        const paramTemplate = document.getElementById('param-template');
        
        // Populate input sections
        for (const sectionId in AppConfig.PARAM_MAP) {
            const params = AppConfig.PARAM_MAP[sectionId];
            const container = document.getElementById(sectionId);
            params.forEach(param => {
                const clone = paramTemplate.content.cloneNode(true);
                clone.querySelector('.param-label').textContent = `${param.name}:`;
                clone.querySelector('.param-desc').textContent = param.desc;
                const valueInput = clone.querySelector('.param-value');
                valueInput.id = `input-${param.key}`;
                valueInput.value = param.defVal;
                const unitSelect = clone.querySelector('.param-unit');
                unitSelect.id = `unit-${param.key}`;
                param.units.forEach(unit => {
                    const option = document.createElement('option');
                    option.value = unit;
                    option.textContent = unit;
                    if (unit === param.unit) option.selected = true;
                    unitSelect.appendChild(option);
                });
                container.appendChild(clone);
            });
        }

        // Populate output sections
        const outputGrid = document.querySelector('.output-grid');
        AppConfig.OUTPUT_MAP.forEach(out => {
            outputGrid.innerHTML += `<label class="output-label">${out.label}</label><span class="output-value status-stale" id="out-${out.key}">N/A</span>`;
        });

        const statusGrid = document.querySelector('.status-grid');
        AppConfig.STATUS_MAP.forEach(stat => {
            statusGrid.innerHTML += `<label class="status-label">${stat.label}</label><span class="status-text status-stale" id="status-${stat.key}">Calcoli non eseguiti.</span>`;
        });
    }

    // --- 3. UI LOGIC & EVENT HANDLERS ---
    const statusBar = document.getElementById('status-bar');

    function setStatus(message) { statusBar.textContent = message; }

    function formatValue(value, precision = 3) {
        if (value === null || !isFinite(value)) return "N/A";
        if (value === 0) return `0.${'0'.repeat(precision)}`;
        const absVal = Math.abs(value);
        if (absVal > 0 && (absVal < 1e-3 || absVal >= 1e4)) {
            return value.toExponential(precision);
        }
        return value.toFixed(precision);
    }

    function onInputChange() {
        setStatus("I parametri sono stati modificati. Eseguire nuovamente il calcolo.");
        document.querySelectorAll('.output-value, .status-text').forEach(el => {
            el.classList.add('status-stale');
            el.classList.remove('status-ok', 'status-warn', 'status-crit');
        });
        document.getElementById('final-status-text').textContent = "---";
        document.getElementById('final-status-text').className = 'status-stale';
    }

    function runCalculation() {
        model.reset();
        document.querySelectorAll('input.invalid').forEach(el => el.classList.remove('invalid'));

        try {
            // Gather and validate inputs
            for (const sectionId in AppConfig.PARAM_MAP) {
                for (const param of AppConfig.PARAM_MAP[sectionId]) {
                    const input = document.getElementById(`input-${param.key}`);
                    const unitSelect = document.getElementById(`unit-${param.key}`);
                    const valStr = input.value.trim();
                    if (valStr === '') {
                        input.classList.add('invalid');
                        throw new Error(`Il campo ${param.name} non può essere vuoto.`);
                    }
                    const value = parseFloat(valStr);
                    if (isNaN(value)) {
                        input.classList.add('invalid');
                        throw new Error(`Valore non numerico per ${param.name}.`);
                    }
                    const multiplier = AppConfig.UNIT_MULTIPLIERS[unitSelect.value];
                    model.params[param.key] = value * multiplier;
                }
            }

            // Perform calculation
            const { success, error } = model.calculate();
            if (!success) throw new Error(error);

            updateOutputView();
            setStatus("Calcoli eseguiti con successo.");

        } catch (e) {
            setStatus(`Errore: ${e.message}`);
            alert(`Errore di Input: ${e.message}`);
        }
    }

    function updateOutputView() {
        const { cl_eff, gm_crit, gain_margin, drive_level, dl_ratio } = model.results;
        const p = model.params;

        // Update result values
        document.getElementById('out-cl_eff').textContent = formatValue(cl_eff * 1e12); // to pF
        document.getElementById('out-gm_crit').textContent = formatValue(gm_crit * 1e3); // to mA/V
        document.getElementById('out-gain_margin').textContent = formatValue(gain_margin);
        document.getElementById('out-drive_level').textContent = formatValue(drive_level * 1e6); // to uW

        // Update status labels
        let isFail = false;

        // Gm/Gm_crit Status
        const gmStatus = document.getElementById('status-gm_crit_status');
        if (gm_crit > p.GM_MCU) {
            gmStatus.textContent = `Gm (${formatValue(p.GM_MCU * 1e3, 1)} mA/V) < Gm_crit (${formatValue(gm_crit * 1e3, 1)} mA/V). CRITICO.`;
            gmStatus.className = 'status-text status-crit';
            isFail = true;
        } else {
            gmStatus.textContent = `Gm (${formatValue(p.GM_MCU * 1e3, 1)} mA/V) > Gm_crit (${formatValue(gm_crit * 1e3, 1)} mA/V). OK.`;
            gmStatus.className = 'status-text status-ok';
        }

        // Gain Margin Status
        const marginStatus = document.getElementById('status-gain_margin_status');
        if (gain_margin < 3.0) {
            marginStatus.textContent = `Gain Margin (${formatValue(gain_margin, 2)}) troppo basso. CRITICO.`;
            marginStatus.className = 'status-text status-crit';
            isFail = true;
        } else if (gain_margin < AppConfig.GM_MARGIN_THRESHOLD) {
            marginStatus.textContent = `Gain Margin (${formatValue(gain_margin, 2)}) accettabile, ma < ${AppConfig.GM_MARGIN_THRESHOLD}. OTTIMIZZARE.`;
            marginStatus.className = 'status-text status-warn';
        } else {
            marginStatus.textContent = `Gain Margin (${formatValue(gain_margin, 2)}) >= ${AppConfig.GM_MARGIN_THRESHOLD}. ECCELLENTE.`;
            marginStatus.className = 'status-text status-ok';
        }

        // Drive Level Status
        const dlStatus = document.getElementById('status-dl_status');
        if (dl_ratio > 1.0) {
            dlStatus.textContent = `DL (${formatValue(drive_level * 1e6, 1)} uW) ECCEDE DL Max (${formatValue(p.DL_MAX * 1e6, 1)} uW). CRITICO.`;
            dlStatus.className = 'status-text status-crit';
            isFail = true;
        } else if (dl_ratio > 0.8) {
            dlStatus.textContent = `DL (${formatValue(drive_level * 1e6, 1)} uW) vicino al limite (DL/DL_max = ${formatValue(dl_ratio, 2)}). ATTENZIONE.`;
            dlStatus.className = 'status-text status-warn';
        } else {
            dlStatus.textContent = `DL (${formatValue(drive_level * 1e6, 1)} uW) entro i limiti (DL/DL_max = ${formatValue(dl_ratio, 2)}). OK.`;
            dlStatus.className = 'status-text status-ok';
        }

        // Final Status
        const finalStatus = document.getElementById('final-status-text');
        if (isFail) {
            finalStatus.textContent = "VALIDATION: FAIL";
            finalStatus.className = 'status-crit';
        } else {
            finalStatus.textContent = "VALIDATION: PASS";
            finalStatus.className = 'status-ok';
        }
    }

    function resetApplication() {
        document.querySelectorAll('.param-value').forEach(input => input.value = '');
        document.getElementById('input-REXT_SEL').value = '0'; // Default Rext to 0
        onInputChange();
        // Clear results and statuses to initial state
        document.querySelectorAll('.output-value').forEach(el => el.textContent = 'N/A');
        document.querySelectorAll('.status-text').forEach(el => el.textContent = 'Calcoli non eseguiti.');
        setStatus("Pronto. I valori sono stati reimpostati.");
    }

    // --- 4. INITIALIZATION ---
    initializeUI();

    // Add event listeners
    document.getElementById('calculate-btn').addEventListener('click', runCalculation);
    document.getElementById('reset-btn').addEventListener('click', resetApplication);
    document.querySelectorAll('.param-value, .param-unit').forEach(el => {
        el.addEventListener('change', onInputChange);
        el.addEventListener('keyup', onInputChange);
    });

});
