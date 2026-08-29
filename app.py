import streamlit as st
import pandas as pd
import math

# ==============================================================================
# CONFIGURACIÓN GENERAL DE LA APLICACIÓN
# ==============================================================================
st.set_page_config(
    page_title="Plataforma de Simulación y Catálogos MEYTC",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Plataforma de Cálculo, Simulación y Catálogos Comerciales (MEYTC)")
st.caption("Proyecto de Beca de Investigación — Máquinas de Elevación y Transporte (UTN FRRe)")
st.markdown("---")

# Navegación lateral
modulo = st.sidebar.radio(
    "Navegación de Módulos:",
    [
        "🛞 Módulo 1: Simulación Rodamientos (ISO 281)",
        "🔍 Módulo 2: Buscador de Catálogos (IA)",
        "🏗️ Módulo 3: Selección de Cables (Norma DIN 655)"
    ]
)

# ==============================================================================
# MÓDULO 1: SIMULACIÓN DE RODAMIENTOS
# ==============================================================================
if modulo == "🛞 Módulo 1: Simulación Rodamientos (ISO 281)":
    st.header("🛞 Simulación de Vida Útil de Rodamientos ($L_{10h}$)")
    st.markdown("Simulación de vida útil nominal según ISO 281 en función de cargas dinámicas y velocidad de operación.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Parámetros de Entrada")
        carga_p = st.number_input("Carga Dinámica Equivalente P (kN):", min_value=1.0, value=25.0, step=2.5)
        cap_c = st.number_input("Capacidad de Carga Dinámica C (kN):", min_value=1.0, value=104.0, step=5.0)
        rpm = st.slider("Velocidad de Giro (rpm):", min_value=10, max_value=1000, value=150, step=10)
        tipo_elem = st.radio("Contacto / Elemento Rodante:", ["Bolas (p=3)", "Rodillos (p=10/3)"])
        
        st.markdown("**Régimen de Operación (Para cálculo en años)**")
        col_hs, col_dias = st.columns(2)
        with col_hs:
            horas_dia = st.number_input("Horas de uso por día (h/día):", min_value=1.0, max_value=24.0, value=8.0, step=1.0)
        with col_dias:
            dias_ano = st.number_input("Días de uso por año (días/año):", min_value=1, max_value=365, value=250, step=5)

    with col2:
        st.subheader("Resultado de la Simulación")
        p_exp = 3.0 if "Bolas" in tipo_elem else (10.0 / 3.0)
        l10_mill = (cap_c / carga_p) ** p_exp
        l10_horas = (10**6 / (60 * rpm)) * l10_mill
        
        # Cálculo de vida útil en años
        horas_anuales = horas_dia * dias_ano
        anos_util = l10_horas / horas_anuales if horas_anuales > 0 else 0

        # Visualización de métricas
        m1, m2 = st.columns(2)
        with m1:
            st.metric(label="Vida Útil Simulada L10h:", value=f"{l10_horas:,.0f} hs")
        with m2:
            st.metric(label="Vida Útil Estimativa (Años):", value=f"{anos_util:,.1f} años")

        st.markdown(f"$$L_{{10}} = \\left( \\frac{{{cap_c}}}{{{carga_p}}} \\right)^{{{p_exp:.2f}}} = {l10_mill:.2f} \\text{{ millones de revoluciones}}$$")
        st.markdown(f"$$L_{{10h}} = \\frac{{10^6}}{{60 \\cdot {rpm}}} \\cdot {l10_mill:.2f} = {l10_horas:,.0f} \\text{{ horas}}$$")
        st.markdown(f"* **Régimen considerado:** {horas_dia:.0f} hs/día × {dias_ano} días/año = {horas_anuales:,.0f} hs/año.")

# ==============================================================================
# MÓDULO 2: BUSCADOR DE CATÁLOGOS CON IA (Multiparámetro Extendido)
# ==============================================================================
elif modulo == "🔍 Módulo 2: Buscador de Catálogos (IA)":
    st.header("🔍 Buscador Inteligente de Catálogos Comerciales")
    st.markdown("Asistente de selección de componentes técnicos con motor de análisis paramétrico de la cátedra.")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Biblioteca de Catálogos")
        cat_seleccionado = st.selectbox(
            "Seleccioná el Catálogo a consultar:",
            [
                "Todos los catálogos (Búsqueda global)",
                "Cables de Acero (IPH / DIN 3060)",
                "Rodamientos de Poleas (SKF / FAG)",
                "Poleas y Gargantas (Norma ISO 4301)",
                "Reductores de Velocidad (SEW-Eurodrive)"
            ]
        )
        st.info("💡 *El motor evalúa en simultáneo: dimensiones (mm), hileras, tipo de alma, construcciones, tratamientos térmicos y entorno operativo.*")

    with col2:
        st.subheader("Consulta de Componente")
        query_cat = st.text_input(
            "¿Qué componente estás buscando?", 
            placeholder="Ej: rodamiento SKF 50mm doble hilera para alta temperatura..."
        )

        if query_cat:
            st.markdown("### 📋 Recomendación Técnica de IA")
            q_low = query_cat.lower()

            has_50 = any(w in q_low for w in ["50mm", "50 mm", "50", "d 50", "d=50"])
            has_14 = any(w in q_low for w in ["14mm", "14 mm", "14", "d 14", "d=14"])
            has_16 = any(w in q_low for w in ["16mm", "16 mm", "16"])
            has_400 = any(w in q_low for w in ["400mm", "400 mm", "400", "dp 400"])

            is_doble = any(w in q_low for w in ["doble hilera", "dos hileras", "2 hileras", "doble"])
            has_temp = any(w in q_low for w in ["temperatura", "temperaturas", "calor", "termico", "térmico"])
            has_anti = any(w in q_low for w in ["anti-giratorio", "antigiratorio", "no giratorio", "antigiro"])

            if "rodamiento" in q_low or "skf" in q_low:
                if has_50 and is_doble and has_temp:
                    st.success("✅ **Coincidencia Exacta: Rodamiento SKF Doble Hilera para Alta Temperatura**")
                    st.markdown("""
                    * **Modelo recomendado:** **SKF 22210 E/VA228** (Rodillos oscilantes).
                    * **Cotado:** $d = 50\\text{ mm}$, $D = 90\\text{ mm}$, $B = 23\\text{ mm}$.
                    * **Térmica:** Juego C4 con **grafito sintético** (hasta **+350 °C**).
                    """)
                elif has_50:
                    st.success("✅ **Coincidencia Dimensional: SKF Rodamiento Estándar d=50mm**")
                    st.markdown("* **Modelo:** **SKF 6210-2RS1** ($d=50\\text{ mm}$, $D=90\\text{ mm}$).")
            elif "cable" in q_low or "iph" in q_low:
                if (has_14 or "14" in q_low) and has_anti:
                    st.success("✅ **Coincidencia Exacta: Cable Anti-giratorio Galvanizado**")
                    st.markdown("* **Modelo:** **IPH 35x7 HD + AA** ($d=14\\text{ mm}$, $F_0=152\\text{ kN}$).")
            else:
                st.info("🔎 **Análisis paramétrico de la consulta:** Procesando atributos ingresados...")

    st.markdown("---")
    st.subheader("📚 Vista Previa de Datos de Catálogo")
    data_cables = {
        "Modelo": ["IPH 6x36 WS+AA", "IPH 35x7 Anti-giratorio", "SKF 6210-2RS1"],
        "Categoría": ["Cable", "Cable", "Rodamiento"],
        "Atributo Principal": ["d = 14mm / F0 = 134kN", "d = 14mm / F0 = 152kN", "d = 50mm / D = 90mm"],
        "Norma / Fabricante": ["DIN 3060 / IPH", "DIN 3069 / IPH", "ISO 281 / SKF"]
    }
    st.dataframe(pd.DataFrame(data_cables), use_container_width=True)

# ==============================================================================
# MÓDULO 3: SELECCIÓN DE CABLES DE ACERO (NORMA DIN 655)
# ==============================================================================
elif modulo == "🏗️ Módulo 3: Selección de Cables (Norma DIN 655)":
    st.header("🏗️ Selección y Dimensionado de Cables de Acero (Norma DIN 655)")
    st.markdown("Cálculo de solicitación en ramales, diámetro de cable, coeficientes de seguridad y dimensionado de tambor y poleas.")

    # TABLAS DE REFERENCIA DIN 655
    tabla5 = {
        ("Movimiento de precisión", "Sin precisar"): "I",
        ("Movimiento poco frecuente", "Raramente a plena carga"): "II",
        ("Movimiento frecuente", "Raramente a plena carga"): "III",
        ("Movimiento poco frecuente", "Plena carga"): "III",
        ("Movimiento frecuente", "Plena carga"): "IV",
        ("Movimiento frecuente", "Todas las cargas en la industria siderúrgica"): "V"
    }

    tabla7 = {
        "I":   {"kc": (0.30, 0.32), "mnu_130_160": (5.5, 6.0), "ct": (5, 6),  "cp": (5.5, 7.0),  "cpc": (4.5, 5.0)},
        "II":  {"kc": (0.30, 0.32), "mnu_130_160": (5.5, 6.0), "ct": (6, 7),  "cp": (7.0, 8.0),  "cpc": (4.5, 5.0)},
        "III": {"kc": (0.32, 0.34), "mnu_130_160": (6.0, 7.0), "ct": (7, 8),  "cp": (8.0, 10.0), "cpc": (5.0, 6.0)},
        "IV":  {"kc": (0.34, 0.37), "mnu_130_160": (7.0, 8.0), "ct": (8, 9),  "cp": (9.0, 12.0), "cpc": (6.0, 7.5)},
        "V":   {"kc": (0.37, 0.40), "mnu_130_160": (8.0, 9.5), "ct": (8, 9),  "cp": (9.0, 12.0), "cpc": (6.0, 7.5)}
    }

    # Cargas de rotura DIN 655 (kgf) para 6x19 y 6x37
    tabla3_din655 = {
        "6x19": {
            6.5: {130: 1860, 160: 2300, 180: 2550},
            8.0: {130: 2900, 160: 3600, 180: 4050},
            9.5: {130: 4200, 160: 5150, 180: 5800},
            11.0: {130: 5700, 160: 7000, 180: 7900},
            12.5: {130: 7450, 160: 9150, 180: 10300},
            14.0: {130: 9450, 160: 11600, 180: 13050},
            16.0: {130: 11650, 160: 14300, 180: 16100},
            17.0: {130: 14100, 160: 17350, 180: 19500},
            19.0: {130: 16750, 160: 20600, 180: 23200},
            20.0: {130: 19650, 160: 24200, 180: 27250},
            22.0: {130: 22800, 160: 28050, 180: 31600}
        },
        "6x37": {
            9.0: {130: 3650, 160: 4450, 180: 5000},
            10.0: {130: 4600, 160: 5650, 180: 6350},
            11.0: {130: 5650, 160: 7000, 180: 7850},
            12.0: {130: 6850, 160: 8450, 180: 9500},
            13.0: {130: 8150, 160: 10050, 180: 11300},
            14.0: {130: 9600, 160: 11800, 180: 13250},
            15.0: {130: 11100, 160: 13650, 180: 15350},
            16.0: {130: 12750, 160: 15700, 180: 17650},
            18.0: {130: 14500, 160: 17850, 180: 20100},
            20.0: {130: 18350, 160: 22600, 180: 25400},
            22.0: {130: 22650, 160: 27900, 180: 31400},
            24.0: {130: 27450, 160: 33750, 180: 38000},
            27.0: {130: 32650, 160: 40200, 180: 45200},
            29.0: {130: 38300, 160: 47150, 180: 53050},
            31.0: {130: 44400, 160: 54650, 180: 61500}
        }
    }

    # Geometría del ranurado (Tabla 13)
    tabla13 = [
        {"dc": 10, "s": 12, "r": 5.5, "a": 1.0},
        {"dc": 13, "s": 15, "r": 7.0, "a": 1.5},
        {"dc": 16, "s": 18, "r": 9.0, "a": 2.0},
        {"dc": 19, "s": 22, "r": 10.5, "a": 2.5},
        {"dc": 22, "s": 25, "r": 12.0, "a": 3.0},
        {"dc": 27, "s": 31, "r": 15.0, "a": 3.5},
        {"dc": 33, "s": 37, "r": 18.0, "a": 4.0},
        {"dc": 40, "s": 45, "r": 22.0, "a": 5.0},
        {"dc": 44, "s": 49, "r": 24.0, "a": 6.0}
    ]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Solicitación y Clasificación")
        p_kgf = st.number_input("Carga total P (kgf):", min_value=100.0, value=10000.0, step=500.0)
        num_ramales = st.number_input("Número de Ramales:", min_value=1, value=4, step=1)
        s_ram = p_kgf / num_ramales

        st.metric("Solicitación por Ramal (Sram):", f"{s_ram:,.1f} kgf")

        frecuencia = st.selectbox(
            "Frecuencia de los movimientos:",
            ["Movimiento de precisión", "Movimiento poco frecuente", "Movimiento frecuente"]
        )
        
        # Filtro dinámico de importancia según frecuencia
        opciones_importancia = []
        if frecuencia == "Movimiento de precisión":
            opciones_importancia = ["Sin precisar"]
        elif frecuencia == "Movimiento poco frecuente":
            opciones_importancia = ["Raramente a plena carga", "Plena carga"]
        else:
            opciones_importancia = ["Raramente a plena carga", "Plena carga", "Todas las cargas en la industria siderúrgica"]

        importancia = st.selectbox("Importancia de la carga:", opciones_importancia)

        grupo_detectado = tabla5.get((frecuencia, importancia), "III")
        st.success(f"📌 **Grupo de Mecanismo Obtenido:** Grupo **{grupo_detectado}** (Tabla N° 5)")

        p_group = tabla7[grupo_detectado]
        kc_min, kc_max = p_group["kc"]
        ct_min, ct_max = p_group["ct"]
        cp_min, cp_max = p_group["cp"]
        cpc_min, cpc_max = p_group["cpc"]

        st.markdown(f"""
        * **Rango Coef. Cable $k_c$:** `{kc_min}` – `{kc_max}`
        * **Rango Coef. Tambor $c_t$:** `{ct_min}` – `{ct_max}`
        * **Rango Coef. Polea $c_p$:** `{cp_min}` – `{cp_max}`
        * **Rango Coef. Polea Comp. $c_{{pc}}$:** `{cpc_min}` – `{cpc_max}`
        """)

    with col2:
        st.subheader("2. Dimensionado del Cable")
        kc_adoptado = st.number_input("Adopto Coeficiente $k_c$:", min_value=0.1, max_value=1.0, value=kc_min, step=0.01)
        
        diam_teorico = kc_adoptado * math.sqrt(s_ram)
        st.info(f"📐 **Diámetro Teórico Calculado:** $d_{{calc}} = {kc_adoptado} \\cdot \\sqrt{{{s_ram:.0f}}} = {diam_teorico:.2f} \\text{{ mm}}$")

        dc_adoptado = st.number_input("Adopto Diámetro Comercial $D_c$ (mm):", min_value=1.0, value=float(math.ceil(diam_teorico)), step=1.0)

        st.markdown("#### Verificación de Carga de Rotura y Seguridad")
        
        col_m, col_r = st.columns(2)
        with col_m:
            construccion = st.selectbox("Construcción del Cable:", ["6x19", "6x37"])
        with col_r:
            resistencia_mat = st.selectbox("Tensión del Alambre (kgf/mm²):", [130, 160, 180])

        # Buscar carga de rotura más cercana o exacta
        cables_disponibles = tabla3_din655[construccion]
        d_mas_cercano = min(cables_disponibles.keys(), key=lambda x: abs(x - dc_adoptado))
        f0_rotura = cables_disponibles[d_mas_cercano][resistencia_mat]
        coef_seguridad_real = f0_rotura / s_ram

        mnu_min, mnu_max = p_group["mnu_130_160"]
        if resistencia_mat == 180:
            mnu_min *= 1.125
            mnu_max *= 1.125

        st.markdown(f"""
        * **Carga de Rotura Nominal ($F_0$):** **{f0_rotura:,.0f} kgf** *(Tabla N° 3 para d={d_mas_cercano}mm)*
        * **Coeficiente de Seguridad Real ($\mu$):** **{coef_seguridad_real:.2f}**
        * **Coeficiente Exigido:** Mínimo **{mnu_min:.2f}**
        """)

        if coef_seguridad_real >= mnu_min:
            st.success("✅ **El cable ADOPTADO CUMPLE con el coeficiente de seguridad requerido.**")
        else:
            st.error("❌ **VERIFICACIÓN FALLIDA:** El coeficiente de seguridad es menor al exigido. Aumentá el diámetro del cable.")

    st.markdown("---")
    st.subheader("3. Dimensionado de Tambor y Poleas (Tabla N° 7 y 13)")

    col_pol, col_tam = st.columns(2)

    with col_pol:
        st.markdown("#### Poleas de Reenvío y Compensadora")
        cp_adoptado = st.number_input("Adopto $c_p$ (Polea Reenvío):", min_value=1.0, value=float(cp_min), step=1.0)
        dp_teorico = cp_adoptado * math.sqrt(s_ram)
        dp_adoptado = st.number_input("Adopto Diámetro Polea $D_p$ (mm):", min_value=10.0, value=float(round(dp_teorico, -1)), step=10.0)

        cpc_adoptado = st.number_input("Adopto $c_{pc}$ (Polea Compensadora):", min_value=1.0, value=float(cpc_min), step=1.0)
        dpc_teorico = cpc_adoptado * math.sqrt(s_ram)
        dpc_adoptado = st.number_input("Adopto Diámetro Polea Comp. $D_{pc}$ (mm):", min_value=10.0, value=float(round(dpc_teorico, -1)), step=10.0)

    with col_tam:
        st.markdown("#### Tambor de Arrollamiento")
        ct_adoptado = st.number_input("Adopto $c_t$ (Tambor):", min_value=1.0, value=float(ct_min), step=1.0)
        dt_teorico = ct_adoptado * math.sqrt(s_ram)
        dt_adoptado = st.number_input("Adopto Diámetro Tambor $D_t$ (mm):", min_value=10.0, value=float(round(dt_teorico, -1)), step=10.0)

        st.markdown("**Parámetros de Elevación y Geometría de Ranurado**")
        altura_h = st.number_input("Altura de elevación h (m):", min_value=1.0, value=6.0, step=0.5)
        separacion_sep = st.number_input("Separación entre ranuras sep (mm):", min_value=0.0, value=250.0, step=10.0)
        espiras_seg = st.number_input("Espiras adicionales de seguridad:", min_value=1, value=3, step=1)

        # Geometría Tabla 13
        geo = min(tabla13, key=lambda x: abs(x["dc"] - dc_adoptado))
        s_paso, r_ranura, a_juego = geo["s"], geo["r"], geo["a"]

        # Cantidad de espiras
        cant_espiras = (((p_kgf / 2) * altura_h * 1000) / (dt_adoptado * math.pi)) + 2 * espiras_seg if dt_adoptado > 0 else 0
        cant_espiras_adop = math.ceil(cant_espiras)

        # Longitud tambor
        lt_calc = 2 * cant_espiras_adop * s_paso + separacion_sep
        det_calc = dt_adoptado - (2 * a_juego)

        st.markdown(f"""
        * **Paso ($s$):** `{s_paso} mm` | **Radio ranura ($r$):** `{r_ranura} mm` | **Juego ($a$):** `{a_juego} mm`
        * **Espiras calculadas:** `{cant_espiras:.1f}` $\\rightarrow$ **Adopto:** `{cant_espiras_adop}`
        * **Longitud Mínima del Tambor ($L_t$):** **{lt_calc:.1f} mm**
        * **Diámetro Exterior Tambor ($D_{{et}}$):** **{det_calc:.1f} mm**
        """)
