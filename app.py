import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

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

# ==============================================================================
# ESTADO GLOBAL DE LA SESIÓN (st.session_state)
# ==============================================================================
if "cable_seleccionado" not in st.session_state:
    st.session_state.cable_seleccionado = {
        "guardado": False,
        "diametro_dc": 10.0,
        "s_ramal": 2500.0,
        "grupo_detectado": "III",
        "ct_min": 7.0,
        "cp_min": 8.0,
        "cpc_min": 5.0,
        "carga_total_p": 10000.0
    }

modulo = st.sidebar.radio(
    "Navegación de Módulos:",
    [
        "🏗️ Módulo 1: Selección de Cables (Norma DIN 655)",
        "🛞 Módulo 2: Simulación Rodamientos (ISO 281)",
        "📐 Módulo 3: Vigas Combinadas, Gráfico y Módulo Resistente (Steiner)"
    ]
)

# ==============================================================================
# MÓDULO 1: SELECCIÓN DE CABLES DE ACERO (NORMA DIN 655) Y PREDIMENSIONADO
# ==============================================================================
if modulo == "🏗️ Módulo 1: Selección de Cables (Norma DIN 655)":
    st.header("🏗️ Selección y Dimensionado de Cables de Acero (Norma DIN 655)")
    st.markdown("Cálculo de solicitación en ramales, diámetro de cable, coeficientes de seguridad y dimensionado de tambor y poleas.")

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

    tab_cable_m3, tab_tambor_m3, tab_polea_m3 = st.tabs([
        "🪢 1. Selección del Cable",
        "🥁 2. Dimensionamiento de Tambor",
        "🔘 3. Dimensionamiento de Poleas"
    ])

    with tab_cable_m3:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("1. Solicitación y Clasificación")
            p_kgf = st.number_input("Carga total P (kgf):", min_value=100.0, value=10000.0, step=500.0)
            num_ramales = st.number_input("Número de Ramales:", min_value=1, value=4, step=1)
            s_ram = p_kgf / num_ramales

            st.metric("Solicitación por Ramal (Sram):", f"{s_ram:,.1f} kgf")

            frecuencia = st.selectbox("Frecuencia de los movimientos:", ["Movimiento de precisión", "Movimiento poco frecuente", "Movimiento frecuente"])
            
            opciones_importancia = []
            if frecuencia == "Movimiento de precisión":
                opciones_importancia = ["Sin precisar"]
            elif frecuencia == "Movimiento poco frecuente":
                opciones_importancia = ["Raramente a plena carga", "Plena carga"]
            else:
                opciones_importancia = ["Raramente a plena carga", "Plena carga", "Todas las cargas en la industria siderúrgica"]

            importancia = st.selectbox("Importancia de la carga:", opciones_importancia)

            grupo_detectado = tabla5.get((frecuencia, importancia), "III")
            st.success(f"📌 **Grupo de Mecanismo Obtenido:** Grupo **{grupo_detectado}**")
            st.caption("📖 *Fuente: Clasificación del grupo según Tabla N° 5 — Norma DIN 655.*")

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
            st.caption("📖 *Fuente: Coeficientes para dimensionado según Tabla N° 7 — Norma DIN 655.*")

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

            cables_disponibles = tabla3_din655[construccion]
            d_mas_cercano = min(cables_disponibles.keys(), key=lambda x: abs(x - dc_adoptado))
            f0_rotura = cables_disponibles[d_mas_cercano][resistencia_mat]
            coef_seguridad_real = f0_rotura / s_ram

            mnu_min, mnu_max = p_group["mnu_130_160"]
            if resistencia_mat == 180:
                mnu_min *= 1.125
                mnu_max *= 1.125

            st.markdown(f"""
            * **Carga de Rotura Nominal ($F_0$):** **{f0_rotura:,.0f} kgf**
            * **Coeficiente de Seguridad Real ($\mu$):** **{coef_seguridad_real:.2f}**
            * **Coeficiente Exigido:** Mínimo **{mnu_min:.2f}**
            """)

            if coef_seguridad_real >= mnu_min:
                st.success("✅ **El cable ADOPTADO CUMPLE con el coeficiente de seguridad requerido.**")
            else:
                st.error("❌ **VERIFICACIÓN FALLIDA:** El coeficiente de seguridad es menor al exigido.")

            if st.button("💾 Confirmar Selección de Cable para la App", type="primary"):
                st.session_state.cable_seleccionado = {
                    "guardado": True,
                    "diametro_dc": dc_adoptado,
                    "s_ramal": s_ram,
                    "grupo_detectado": grupo_detectado,
                    "ct_min": ct_min,
                    "cp_min": cp_min,
                    "cpc_min": cpc_min,
                    "carga_total_p": p_kgf
                }
                st.success("✅ Datos transferidos automáticamente.")

    c_data = st.session_state.cable_seleccionado

    with tab_tambor_m3:
        st.subheader("2. Dimensionamiento de Tambor de Arrollamiento")
        st.info(f"📌 **Cable Heredado:** $D_c = \\mathbf{{{c_data['diametro_dc']:.1f}\\text{{ mm}}}}$ | Solicitación $S_{{ram}} = \\mathbf{{{c_data['s_ramal']:,.1f}\\text{{ kgf}}}}$ | Grupo: **{c_data['grupo_detectado']}**")

        dt_teorico = c_data["ct_min"] * math.sqrt(c_data["s_ramal"])

        col_t1, col_t2 = st.columns(2)
        with col_t1:
            ct_adoptado = st.number_input("Adopto Coeficiente de Tambor ($c_t$):", min_value=1.0, value=float(c_data["ct_min"]), step=1.0)
            st.write(f"- **Diámetro teóricamente necesario:** `{dt_teorico:.1f} mm`")
            dt_adoptado = st.number_input("Adopto Diámetro Primitivo del Tambor $D_t$ (mm):", min_value=10.0, value=float(round(dt_teorico, -1)), step=10.0)

        with col_t2:
            altura_h = st.number_input("Altura de elevación $h$ (m):", min_value=1.0, value=6.0, step=0.5)
            separacion_sep = st.number_input("Separación central entre ranuras $s_{ep}$ (mm):", min_value=0.0, value=250.0, step=10.0)
            espiras_seg = st.number_input("Espiras adicionales de seguridad:", min_value=1, value=3, step=1)

            geo = min(tabla13, key=lambda x: abs(x["dc"] - c_data["diametro_dc"]))
            s_paso, r_ranura, a_juego = geo["s"], geo["r"], geo["a"]

            cant_espiras = (((c_data["carga_total_p"] / 2) * altura_h * 1000) / (dt_adoptado * math.pi)) + 2 * espiras_seg if dt_adoptado > 0 else 0
            cant_espiras_adop = math.ceil(cant_espiras)

            lt_calc = 2 * cant_espiras_adop * s_paso + separacion_sep
            det_calc = dt_adoptado - (2 * a_juego)

            st.markdown(f"""
            * **Longitud Mínima del Tambor ($L_t$):** **{lt_calc:.1f} mm**
            * **Diámetro Exterior del Tambor ($D_{{et}}$):** **{det_calc:.1f} mm**
            """)

    with tab_polea_m3:
        st.subheader("3. Dimensionamiento de Poleas")
        dp_teorico = c_data["cp_min"] * math.sqrt(c_data["s_ramal"])
        dpc_teorico = c_data["cpc_min"] * math.sqrt(c_data["s_ramal"])

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown("#### Polea de Reenvío (Principal)")
            dp_adoptado = st.number_input("Adopto Diámetro Polea $D_p$ (mm):", min_value=10.0, value=float(round(dp_teorico, -1)), step=10.0)
        with col_p2:
            st.markdown("#### Polea Compensadora")
            dpc_adoptado = st.number_input("Adopto Diámetro Polea Comp. $D_{{pc}}$ (mm):", min_value=10.0, value=float(round(dpc_teorico, -1)), step=10.0)

# ==============================================================================
# MÓDULO 2: SIMULACIÓN DE RODAMIENTOS
# ==============================================================================
elif modulo == "🛞 Módulo 2: Simulación Rodamientos (ISO 281)":
    st.header("🛞 Simulación de Vida Útil de Rodamientos ($L_{10h}$)")
    col1, col2 = st.columns(2)
    with col1:
        carga_p = st.number_input("Carga Dinámica Equivalente P (kN):", min_value=1.0, value=25.0, step=2.5)
        cap_c = st.number_input("Capacidad de Carga Dinámica C (kN):", min_value=1.0, value=104.0, step=5.0)
        rpm = st.slider("Velocidad de Giro (rpm):", min_value=10, max_value=1000, value=150, step=10)
        tipo_elem = st.radio("Contacto / Elemento Rodante:", ["Bolas (p=3)", "Rodillos (p=10/3)"])
        horas_dia = st.number_input("Horas de uso por día (h/día):", min_value=1.0, max_value=24.0, value=8.0, step=1.0)
        dias_ano = st.number_input("Días de uso por año (días/año):", min_value=1, max_value=365, value=250, step=5)

    with col2:
        p_exp = 3.0 if "Bolas" in tipo_elem else (10.0 / 3.0)
        l10_mill = (cap_c / carga_p) ** p_exp
        l10_horas = (10**6 / (60 * rpm)) * l10_mill
        horas_anuales = horas_dia * dias_ano
        anos_util = l10_horas / horas_anuales if horas_anuales > 0 else 0

        st.metric(label="Vida Útil Simulada L10h:", value=f"{l10_horas:,.0f} hs")
        st.metric(label="Vida Útil Estimativa (Años):", value=f"{anos_util:,.1f} años")

# ==============================================================================
# MÓDULO 3: VIGAS COMBINADAS, CATÁLOGOS Y PERFIL PERSONALIZADO (DXF EN MM)
# ==============================================================================
elif modulo == "📐 Módulo 3: Vigas Combinadas, Gráfico y Módulo Resistente (Steiner)":
    st.header("📐 Cálculo de Módulo Resistente y Gráfico 2D Interactivo")

    # Intentamos importar ezdxf de forma segura para la lectura de archivos DXF
    try:
        import ezdxf
        DXF_DISPONIBLE = True
    except ImportError:
        DXF_DISPONIBLE = False

    # CATÁLOGOS COMERCIALES (IPN / UPN)
    cat_ipn = {
        "IPN 80":  {"h": 8.0,  "b": 4.2,  "tw": 0.39, "tf": 0.59, "area": 7.58,  "ix": 77.8,   "iy": 6.29,  "ey": 0.0},
        "IPN 100": {"h": 10.0, "b": 5.0,  "tw": 0.45, "tf": 0.68, "area": 10.6,  "ix": 171.0,  "iy": 12.2,  "ey": 0.0},
        "IPN 120": {"h": 12.0, "b": 5.8,  "tw": 0.51, "tf": 0.77, "area": 14.2,  "ix": 328.0,  "iy": 21.5,  "ey": 0.0},
        "IPN 140": {"h": 14.0, "b": 6.6,  "tw": 0.57, "tf": 0.86, "area": 18.3,  "ix": 573.0,  "iy": 35.2,  "ey": 0.0},
        "IPN 160": {"h": 16.0, "b": 7.4,  "tw": 0.63, "tf": 0.95, "area": 22.8,  "ix": 935.0,  "iy": 54.7,  "ey": 0.0},
        "IPN 180": {"h": 18.0, "b": 8.2,  "tw": 0.69, "tf": 1.04, "area": 27.9,  "ix": 1450.0, "iy": 81.3,  "ey": 0.0},
        "IPN 200": {"h": 20.0, "b": 9.0,  "tw": 0.75, "tf": 1.13, "area": 33.4,  "ix": 2140.0, "iy": 117.0,  "ey": 0.0},
        "IPN 220": {"h": 22.0, "b": 9.8,  "tw": 0.81, "tf": 1.22, "area": 39.5,  "ix": 3060.0, "iy": 162.0,  "ey": 0.0},
        "IPN 240": {"h": 24.0, "b": 10.6, "tw": 0.87, "tf": 1.31, "area": 46.1,  "ix": 4250.0, "iy": 221.0,  "ey": 0.0},
        "IPN 260": {"h": 26.0, "b": 11.3, "tw": 0.94, "tf": 1.41, "area": 53.4,  "ix": 5740.0, "iy": 288.0,  "ey": 0.0},
        "IPN 300": {"h": 30.0, "b": 12.5, "tw": 1.08, "tf": 1.62, "area": 69.0,  "ix": 9800.0, "iy": 451.0,  "ey": 0.0},
        "IPN 340": {"h": 34.0, "b": 13.7, "tw": 1.22, "tf": 1.83, "area": 86.8,  "ix": 15700.0, "iy": 680.0,  "ey": 0.0},
        "IPN 400": {"h": 40.0, "b": 15.5, "tw": 1.44, "tf": 2.16, "area": 118.0, "ix": 29210.0, "iy": 1050.0, "ey": 0.0},
        "IPN 450": {"h": 45.0, "b": 17.0, "tw": 1.62, "tf": 2.43, "area": 147.0, "ix": 44900.0, "iy": 1510.0, "ey": 0.0},
        "IPN 500": {"h": 50.0, "b": 18.5, "tw": 1.80, "tf": 2.70, "area": 179.0, "ix": 66700.0, "iy": 2140.0, "ey": 0.0}
    }

    cat_upn = {
        "UPN 80":  {"h": 8.0,  "b": 4.5,  "tw": 0.50, "tf": 0.80, "area": 11.0,  "ix": 106.0,  "iy": 19.4,  "ey": 1.35},
        "UPN 100": {"h": 10.0, "b": 5.0,  "tw": 0.55, "tf": 0.85, "area": 13.5,  "ix": 206.0,  "iy": 29.3,  "ey": 1.45},
        "UPN 120": {"h": 12.0, "b": 5.5,  "tw": 0.60, "tf": 0.90, "area": 17.0,  "ix": 364.0,  "iy": 43.2,  "ey": 1.57},
        "UPN 140": {"h": 14.0, "b": 6.0,  "tw": 0.70, "tf": 1.00, "area": 21.5,  "ix": 605.0,  "iy": 62.7,  "ey": 1.71},
        "UPN 160": {"h": 16.0, "b": 6.5,  "tw": 0.75, "tf": 1.05, "area": 24.0,  "ix": 925.0,  "iy": 85.3,  "ey": 1.84},
        "UPN 180": {"h": 18.0, "b": 7.0,  "tw": 0.80, "tf": 1.10, "area": 28.0,  "ix": 1350.0, "iy": 114.0, "ey": 1.93},
        "UPN 200": {"h": 20.0, "b": 7.5,  "tw": 0.85, "tf": 1.15, "area": 32.2,  "ix": 1910.0, "iy": 148.0, "ey": 2.01},
        "UPN 220": {"h": 22.0, "b": 8.0,  "tw": 0.90, "tf": 1.20, "area": 37.4,  "ix": 2690.0, "iy": 197.0, "ey": 2.13},
        "UPN 240": {"h": 24.0, "b": 8.5, "tw": 0.95, "tf": 1.30, "area": 42.3,  "ix": 3600.0, "iy": 248.0, "ey": 2.23},
        "UPN 260": {"h": 26.0, "b": 9.0,  "tw": 1.00, "tf": 1.40, "area": 48.3,  "ix": 4820.0, "iy": 317.0, "ey": 2.35},
        "UPN 300": {"h": 30.0, "b": 10.0, "tw": 1.00, "tf": 1.60, "area": 58.8,  "ix": 8030.0, "iy": 495.0, "ey": 2.70},
        "UPN 350": {"h": 35.0, "b": 10.5, "tw": 1.15, "tf": 1.60, "area": 77.3,  "ix": 12840.0, "iy": 606.0, "ey": 2.82},
        "UPN 400": {"h": 40.0, "b": 11.0, "tw": 1.22, "tf": 1.80, "area": 99.7,  "ix": 20260.0, "iy": 796.0, "ey": 2.94}
    }

    # FUNCIONES DE CÁLCULO GEOMÉTRICO (Shoelace)
    def calcular_propiedades_poligono(verts):
        n = len(verts)
        if n < 3:
            return None, 0, 0, 0, 0, 0

        if verts[0] != verts[-1]:
            verts = verts + [verts[0]]
            n = len(verts)

        area = 0.0
        cx = 0.0
        cy = 0.0
        ix = 0.0
        iy = 0.0

        for i in range(n - 1):
            xi, yi = verts[i]
            xi1, yi1 = verts[i+1]
            cross = (xi * yi1 - xi1 * yi)
            area += cross
            cx += (xi + xi1) * cross
            cy += (yi + yi1) * cross

        area = area / 2.0
        if abs(area) < 1e-6:
            return None, 0, 0, 0, 0, 0

        area = abs(area)
        cx = cx / (6.0 * area)
        cy = cy / (6.0 * area)

        for i in range(n - 1):
            xi, yi = verts[i]
            xi1, yi1 = verts[i+1]
            cross = (xi * yi1 - xi1 * yi)
            x_i, y_i = xi - cx, yi - cy
            x_ip1, y_ip1 = xi1 - cx, yi1 - cy

            ix += (y_i**2 + y_i*y_ip1 + y_ip1**2) * cross
            iy += (x_i**2 + x_i*x_ip1 + x_ip1*y_ip1) * cross

        ix = abs(ix / 12.0)
        iy = abs(iy / 12.0)
        
        return verts[:-1], area, cx, cy, ix, iy

    def obtener_poligono_perfil(p_type, p_data, x_center, y_center, rot_deg):
        h, b, tw, tf = p_data["h"], p_data["b"], p_data["tw"], p_data["tf"]
        ey = p_data.get("ey", 0.0)

        if p_type == "IPN":
            verts = [
                (-b/2, h/2), (b/2, h/2), (b/2, h/2 - tf), (tw/2, h/2 - tf),
                (tw/2, -h/2 + tf), (b/2, -h/2 + tf), (b/2, -h/2), (-b/2, -h/2),
                (-b/2, -h/2 + tf), (-tw/2, -h/2 + tf), (-tw/2, h/2 - tf), (-b/2, h/2 - tf)
            ]
        else:
            x_back = -ey
            x_web_in = -ey + tw
            x_tip = b - ey
            verts = [
                (x_back, h/2), (x_tip, h/2), (x_tip, h/2 - tf), (x_web_in, h/2 - tf),
                (x_web_in, -h/2 + tf), (x_tip, -h/2 + tf), (x_tip, -h/2), (x_back, -h/2)
            ]

        rad = math.radians(rot_deg)
        cos_r, sin_r = math.cos(rad), math.sin(rad)
        return [(vx * cos_r - vy * sin_r + x_center, vx * sin_r + vy * cos_r + y_center) for vx, vy in verts]

    # SELECCIÓN DE FUENTE DE DATOS
    modo_fuente = st.radio(
        "Seleccione el origen de la sección:",
        ["Catálogo Comercial (IPN / UPN)", "📂 Perfil Personalizado (Subir DXF de AutoCAD en mm)"],
        horizontal=True
    )

    col_pantalla_izq, col_pantalla_der = st.columns([1.4, 1.0])

    if modo_fuente == "📂 Perfil Personalizado (Subir DXF de AutoCAD en mm)":
        with col_pantalla_izq:
            st.markdown("### 1. Carga de Geometría CAD (DXF en mm)")
            
            archivo_subido = st.file_uploader("Suba el archivo del perfil diseñado:", type=["dxf"])
            
            with st.expander("ℹ️ Instrucciones para preparar y subir tu archivo DXF en milímetros"):
                st.markdown("""
                Para que el programa lea tu diseño mecánico correctamente:
                1. **Polilínea Cerrada:** Dibuja el contorno de tu perfil usando el comando **`PLINE`**. Al terminar, escribe **`C`** (Cerrar) y presiona *Enter*. No uses líneas sueltas.
                2. **Unidad Madre (mm):** Dibuja la pieza directamente en **milímetros** (por ejemplo, si el perfil tiene 200 mm de altura, dibújalo de 200 unidades).
                3. **Sin elementos extraños:** Guarda el archivo DXF conteniendo **únicamente la polilínea del perfil**. Evita incluir cotas, ejes de referencia o textos flotantes.
                4. **Versión de guardado:** Ve a *File > Save As* y selecciona **AutoCAD 2018 DXF** (o versiones 2013/2010).
                """)
            
            verts_p1 = []
            a1, ix1, iy1 = 0, 0, 0
            x1_c, y1_c = 0, 0
            
            if archivo_subido is not None:
                try:
                    if DXF_DISPONIBLE:
                        import tempfile
                        import os

                        # Creamos un archivo temporal en disco para evitar el error de bytes-like object
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.dxf') as tmp_file:
                            tmp_file.write(archivo_subido.getvalue())
                            tmp_path = tmp_file.name

                        try:
                            doc = ezdxf.readfile(tmp_path)
                            msp = doc.modelspace()
                            for entity in msp.query('LWPOLYLINE POLYLINE'):
                                verts_p1 = [(v[0], v[1]) for v in entity.get_points('xy')]
                                break 
                        finally:
                            if os.path.exists(tmp_path):
                                os.unlink(tmp_path)

                        if not verts_p1:
                            st.error("No se encontró una polilínea válida en el archivo DXF.")
                    else:
                        st.error("La librería 'ezdxf' no está instalada en el entorno.")

                    if len(verts_p1) >= 3:
                        _, a1, x1_bar, y1_bar, ix1, iy1 = calcular_propiedades_poligono(verts_p1)
                        verts_p1 = [(v[0] - x1_bar, v[1] - y1_bar) for v in verts_p1]
                        x1_c, y1_c = 0.0, 0.0
                        st.success(f"¡Archivo leído con éxito! Área detectada: {a1:,.2f} mm²")
                except Exception as e:
                    st.error(f"Error al procesar el archivo DXF: {e}")

            agregar_p2 = False

        with col_pantalla_der:
            st.markdown("### 👁️ Visualizador de Control (mm)")
            fig, ax = plt.subplots(figsize=(5, 5))
            if len(verts_p1) >= 3:
                poly_custom = patches.Polygon(verts_p1, closed=True, color='darkorange', alpha=0.8, edgecolor='black', lw=1.5, label="Perfil Custom (mm)")
                ax.add_patch(poly_custom)
                ax.plot(0, 0, 'ro', markersize=6, label="Baricentro (0,0)")
                
                all_x = [v[0] for v in verts_p1]
                all_y = [v[1] for v in verts_p1]
                margin = max(max(all_x)-min(all_x), max(all_y)-min(all_y)) * 0.4 + 5
                ax.set_xlim(-margin, margin)
                ax.set_ylim(-margin, margin)
            else:
                ax.text(0, 0, "Esperando archivo DXF en mm...", ha='center', va='center', fontsize=11, color='gray')
                ax.set_xlim(-50, 50)
                ax.set_ylim(-50, 50)

            ax.set_aspect('equal', adjustable='box')
            ax.set_xlabel("X [mm]")
            ax.set_ylabel("Y [mm]")
            ax.grid(True, linestyle='--', alpha=0.5)
            ax.legend(loc='upper right', fontsize=8)
            st.pyplot(fig)

        area_tot = a1
        yg_comp, xg_comp = 0.0, 0.0
        ix_tot, iy_tot = ix1, iy1
        
        if len(verts_p1) >= 3:
            all_y = [v[1] for v in verts_p1]
            all_x = [v[0] for v in verts_p1]
            d_sup = max(all_y)
            d_inf = abs(min(all_y))
            d_der = max(all_x)
            d_izq = abs(min(all_x))

            wx_sup = ix_tot / d_sup if d_sup > 0 else 0
            wx_inf = ix_tot / d_inf if d_inf > 0 else 0
            wy_der = iy_tot / d_der if d_der > 0 else 0
            wy_izq = iy_tot / d_izq if d_izq > 0 else 0
        else:
            wx_sup, wx_inf, wy_der, wy_izq = 0, 0, 0, 0

        # PANEL DE RESULTADOS EN MM PARA PERFIL PERSONALIZADO
        st.markdown("---")
        st.subheader("📊 Módulos Resistentes y Propiedades Mecánicas Resultantes")

        c_r1, c_r2, c_r3, c_r4 = st.columns(4)
        with c_r1:
            st.metric("Área Total (A):", f"{area_tot:,.1f} mm²")
            st.metric("Baricentro Y_G:", f"{yg_comp:.1f} mm")
        with c_r2:
            st.metric("Inercia Ix Total:", f"{ix_tot:,.0f} mm⁴")
            st.metric("Inercia Iy Total:", f"{iy_tot:,.0f} mm⁴")
        with c_r3:
            st.metric("Wx Superior:", f"{wx_sup:,.0f} mm³")
            st.metric("Wx Inferior:", f"{wx_inf:,.0f} mm³")
        with c_r4:
            st.metric("Wy Derecho:", f"{wy_der:,.0f} mm³")
            st.metric("Wy Izquierdo:", f"{wy_izq:,.0f} mm³")

    else:
        # MODO CATÁLOGO COMERCIAL (P1 + P2)
        with col_pantalla_izq:
            col_p1, col_p2 = st.columns(2)

            with col_p1:
                st.markdown("### 1. Perfil Base (P1)")
                tipo_p1 = st.selectbox("Tipo Perfil Base:", ["IPN", "UPN"], index=0, key="tipo_p1")
                prof1_name = st.selectbox("Designación Perfil 1:", list(cat_ipn.keys()) if tipo_p1 == "IPN" else list(cat_upn.keys()), index=4, key="prof1_name")
                p1 = cat_ipn[prof1_name] if tipo_p1 == "IPN" else cat_upn[prof1_name]

                x1_c, y1_c = 0.0, p1["h"] / 2.0
                rot_p1 = 0
                ix1, iy1, a1 = p1["ix"], p1["iy"], p1["area"]

            with col_p2:
                st.markdown("### 2. Refuerzo (P2)")
                agregar_p2 = st.checkbox("¿Agregar perfil 2?", value=True, key="agregar_p2")

                if agregar_p2:
                    tipo_p2 = st.selectbox("Tipo Perfil Refuerzo:", ["UPN", "IPN"], index=0, key="tipo_p2")
                    lista_cat_p2 = cat_upn if tipo_p2 == "UPN" else cat_ipn
                    prof2_name = st.selectbox("Designación Perfil 2:", list(lista_cat_p2.keys()), index=0, key="prof2_name")
                    p2 = lista_cat_p2[prof2_name]
                else:
                    p2 = None

            if agregar_p2:
                st.markdown("#### 🔗 Posición de Soldadura / Contacto")
                rot_p2 = st.slider("Rotación P2 (°):", min_value=0, max_value=360, value=90, step=15, key="rot_p2_slider")
                ubicacion_contacto = st.selectbox(
                    "Ubicación del Perfil 2 respecto al Base:",
                    [
                        "Sobre el ala superior (Al ras)",
                        "Debajo del ala inferior (Al ras)",
                        "Lateral derecho (Contra el ala)",
                        "Lateral izquierdo (Contra el ala)"
                    ],
                    key="ubicacion_contacto_select"
                )

                h1, b1 = p1["h"], p1["b"]
                rad_p2 = math.radians(rot_p2)
                cos_r, sin_r = math.cos(rad_p2), math.sin(rad_p2)
                
                verts_p2_local = obtener_poligono_perfil(tipo_p2, p2, 0.0, 0.0, rot_p2)
                min_y_p2 = min(v[1] for v in verts_p2_local)
                max_y_p2 = max(v[1] for v in verts_p2_local)
                min_x_p2 = min(v[0] for v in verts_p2_local)
                max_x_p2 = max(v[0] for v in verts_p2_local)

                if ubicacion_contacto == "Sobre el ala superior (Al ras)":
                    x2_c, y2_c = 0.0, h1 - min_y_p2
                elif ubicacion_contacto == "Debajo del ala inferior (Al ras)":
                    x2_c, y2_c = 0.0, -max_y_p2
                elif ubicacion_contacto == "Lateral derecho (Contra el ala)":
                    x2_c, y2_c = (b1 / 2.0) - min_x_p2, (h1 / 2.0) - ((min_y_p2 + max_y_p2) / 2.0)
                else:
                    x2_c, y2_c = (-b1 / 2.0) - max_x_p2, (h1 / 2.0) - ((min_y_p2 + max_y_p2) / 2.0)

                a2 = p2["area"]
                cos_a2, sin_a2 = cos_r ** 2, sin_r ** 2
                ix2_local = p2["ix"] * cos_a2 + p2["iy"] * sin_a2
                iy2_local = p2["ix"] * sin_a2 + p2["iy"] * cos_a2
            else:
                a2, x2_c, y2_c, ix2_local, iy2_local, rot_p2 = 0.0, 0.0, 0.0, 0.0, 0.0, 0

        area_tot = a1 + a2
        xg_comp = ((a1 * x1_c) + (a2 * x2_c)) / area_tot
        yg_comp = ((a1 * y1_c) + (a2 * y2_c)) / area_tot

        ix_tot = (ix1 + a1 * (y1_c - yg_comp)**2) + (ix2_local + a2 * (y2_c - yg_comp)**2) if agregar_p2 else ix1
        iy_tot = (iy1 + a1 * (x1_c - xg_comp)**2) + (iy2_local + a2 * (x2_c - xg_comp)**2) if agregar_p2 else iy1

        with col_pantalla_der:
            st.markdown("### 🖼️ Sección Compuesta Real (Soldada)")
            fig, ax = plt.subplots(figsize=(5, 5))

            verts_p1_draw = obtener_poligono_perfil(tipo_p1, p1, x1_c, y1_c, rot_p1)
            poly1 = patches.Polygon(verts_p1_draw, closed=True, color='navy', alpha=0.75, edgecolor='black', lw=1.2, label=f"P1: {prof1_name}")
            ax.add_patch(poly1)

            if agregar_p2:
                verts_p2_draw = obtener_poligono_perfil(tipo_p2, p2, x2_c, y2_c, rot_p2)
                poly2 = patches.Polygon(verts_p2_draw, closed=True, color='firebrick', alpha=0.75, edgecolor='black', lw=1.2, label=f"P2: {prof2_name} ({rot_p2}°)")
                ax.add_patch(poly2)

            ax.axhline(yg_comp, color='crimson', linestyle='--', linewidth=1.5, label=f'Eje Neutro X_G ({yg_comp:.2f} cm)')
            ax.axvline(xg_comp, color='darkgreen', linestyle=':', linewidth=1.5, label=f'Eje Neutro Y_G ({xg_comp:.2f} cm)')
            ax.plot(xg_comp, yg_comp, 'ro', markersize=8)

            all_x = [v[0] for v in verts_p1_draw] + ([v[0] for v in verts_p2_draw] if agregar_p2 else [])
            all_y = [v[1] for v in verts_p1_draw] + ([v[1] for v in verts_p2_draw] if agregar_p2 else [])
            
            margin = 6.0
            ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
            ax.set_ylim(min(all_y) - margin, max(all_y) + margin)
            ax.set_aspect('equal', adjustable='box')
            ax.set_xlabel("X [cm]")
            ax.set_ylabel("Y [cm]")
            ax.grid(True, linestyle='--', alpha=0.5)
            ax.legend(loc='upper right', fontsize=8)
            st.pyplot(fig)

        d_sup = max(all_y) - yg_comp
        d_inf = yg_comp - min(all_y)
        d_der = max(all_x) - xg_comp
        d_izq = xg_comp - min(all_x)

        wx_sup = ix_tot / d_sup if d_sup > 0 else 0
        wx_inf = ix_tot / d_inf if d_inf > 0 else 0
        wy_der = iy_tot / d_der if d_der > 0 else 0
        wy_izq = iy_tot / d_izq if d_izq > 0 else 0

        # PANEL DE RESULTADOS EN CM PARA CATÁLOGO
        st.markdown("---")
        st.subheader("📊 Módulos Resistentes y Propiedades Mecánicas Resultantes")

        c_r1, c_r2, c_r3, c_r4 = st.columns(4)
        with c_r1:
            st.metric("Área Total (A):", f"{area_tot:.2f} cm²")
            st.metric("Baricentro Y_G:", f"{yg_comp:.2f} cm")
        with c_r2:
            st.metric("Inercia Ix Total:", f"{ix_tot:,.1f} cm⁴")
            st.metric("Inercia Iy Total:", f"{iy_tot:,.1f} cm⁴")
        with c_r3:
            st.metric("Wx Superior:", f"{wx_sup:,.1f} cm³")
            st.metric("Wx Inferior:", f"{wx_inf:,.1f} cm³")
        with c_r4:
            st.metric("Wy Derecho:", f"{wy_der:,.1f} cm³")
            st.metric("Wy Izquierdo:", f"{wy_izq:,.1f} cm³")
