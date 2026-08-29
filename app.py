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

# =====================================================================
# MÓDULO 3: VIGAS COMBINADAS, CATÁLOGOS Y PERFIL PERSONALIZADO (DXF EN MM)
# =====================================================================
elif "Módulo 3" in modulo:
    st.header("Cálculo de Módulo Resistente y Gráfico 2D Interactivo")

    # Intentamos importar dependencias de forma segura
    try:
        import ezdxf
        import matplotlib.pyplot as plt
        DXF_DISPONIBLE = True
    except ImportError:
        DXF_DISPONIBLE = False

    # CATÁLOGOS COMERCIALES (IPN / UPN)
    cat_ipn = {
        "IPN 80": {"h": 8.0, "b": 4.2, "tw": 0.39, "tf": 0.59, "area": 7.58, "ix": 77.8, "iy": 6.29, "ey": 0.0},
        "IPN 100": {"h": 10.0, "b": 5.0, "tw": 0.45, "tf": 0.68, "area": 10.6, "ix": 171.0, "iy": 12.2, "ey": 0.0},
        "IPN 120": {"h": 12.0, "b": 5.8, "tw": 0.51, "tf": 0.77, "area": 14.2, "ix": 328.0, "iy": 21.5, "ey": 0.0},
        "IPN 140": {"h": 14.0, "b": 6.6, "tw": 0.57, "tf": 0.86, "area": 18.3, "ix": 573.0, "iy": 35.2, "ey": 0.0},
        "IPN 160": {"h": 16.0, "b": 7.4, "tw": 0.63, "tf": 0.95, "area": 22.8, "ix": 935.0, "iy": 54.7, "ey": 0.0},
        "IPN 180": {"h": 18.0, "b": 8.2, "tw": 0.69, "tf": 1.04, "area": 27.9, "ix": 1450.0, "iy": 81.3, "ey": 0.0},
        "IPN 200": {"h": 20.0, "b": 9.0, "tw": 0.75, "tf": 1.13, "area": 33.4, "ix": 2140.0, "iy": 117.0, "ey": 0.0},
        "IPN 220": {"h": 22.0, "b": 9.8, "tw": 0.81, "tf": 1.22, "area": 39.5, "ix": 3060.0, "iy": 162.0, "ey": 0.0},
        "IPN 240": {"h": 24.0, "b": 10.6, "tw": 0.87, "tf": 1.31, "area": 46.1, "ix": 4250.0, "iy": 221.0, "ey": 0.0},
        "IPN 260": {"h": 26.0, "b": 11.3, "tw": 0.94, "tf": 1.41, "area": 53.4, "ix": 5740.0, "iy": 288.0, "ey": 0.0},
        "IPN 300": {"h": 30.0, "b": 12.5, "tw": 1.08, "tf": 1.62, "area": 69.0, "ix": 9800.0, "iy": 451.0, "ey": 0.0},
        "IPN 340": {"h": 34.0, "b": 13.7, "tw": 1.22, "tf": 1.83, "area": 86.8, "ix": 15700.0, "iy": 680.0, "ey": 0.0},
        "IPN 400": {"h": 40.0, "b": 15.5, "tw": 1.44, "tf": 2.16, "area": 118.0, "ix": 29210.0, "iy": 1050.0, "ey": 0.0}
    }

    # Selector de origen de la geometría
    tipo_entrada = st.radio("Seleccione el origen de la geometría:", ["Catálogos Comerciales (IPN/UPN)", "Cargar Archivo DXF Personalizado"])

    if tipo_entrada == "Cargar Archivo DXF Personalizado":
        st.subheader("Importación de Geometría DXF")
        archivo_dxf = st.file_uploader("Sube tu archivo DXF en milímetros", type=["dxf"])
        
        if archivo_dxf is not None and DXF_DISPONIBLE:
            with open("temp_dxf.dxf", "wb") as f:
                f.write(archivo_dxf.getbuffer())
            
            try:
                doc = ezdxf.readfile("temp_dxf.dxf")
                msp = doc.modelspace()
                
                poligonos = []
                for entity in msp:
                    if entity.dxftype() == 'LWPOLYLINE':
                        puntos = [(p[0], p[1]) for p in entity.get_points()]
                        if len(puntos) >= 3:
                            if puntos[0] != puntos[-1]:
                                puntos.append(puntos[0])
                            poligonos.append(puntos)
                
                if poligonos:
                    st.success(f"¡Se detectaron {len(poligonos)} contornos cerrados en el archivo DXF!")
                    
                    area_total = 0.0
                    Qx_total = 0.0
                    Qy_total = 0.0
                    detalles_figuras = []
                    
                    for idx, poly in enumerate(poligonos):
                        n = len(poly)
                        A_i = 0.0
                        Cx_i = 0.0
                        Cy_i = 0.0
                        Ix_local = 0.0
                        Iy_local = 0.0
                        
                        for i in range(n - 1):
                            x1, y1 = poly[i]
                            x2, y2 = poly[i+1]
                            cross = (x1 * y2 - x2 * y1)
                            A_i += cross
                            Cx_i += (x1 + x2) * cross
                            Cy_i += (y1 + y2) * cross
                            
                        A_i = abs(A_i / 2.0)
                        if A_i < 1e-6:
                            continue
                        Cx_i = Cx_i / (6.0 * A_i)
                        Cy_i = Cy_i / (6.0 * A_i)
                        
                        for i in range(n - 1):
                            x1, y1 = poly[i]
                            x2, y2 = poly[i+1]
                            cross = (x1 * y2 - x2 * y1)
                            Ix_local += (y1**2 + y1*y2 + y2**2) * cross
                            Iy_local += (x1**2 + x1*x2 + x2**2) * cross
                            
                        Ix_local = abs(Ix_local) / 12.0
                        Iy_local = abs(Iy_local) / 12.0
                        
                        area_total += A_i
                        Qx_total += A_i * Cy_i
                        Qy_total += A_i * Cx_i
                        
                        detalles_figuras.append({
                            'id': idx + 1, 'area': A_i, 'cx': Cx_i, 'cy': Cy_i,
                            'ix_local': Ix_local, 'iy_local': Iy_local
                        })
                    
                    if area_total > 0:
                        XG = Qy_total / area_total
                        YG = Qx_total / area_total
                        
                        Ix_total = 0.0
                        Iy_total = 0.0
                        y_max = -float('inf')
                        y_min = float('inf')
                        
                        for fig in detalles_figuras:
                            dx = fig['cx'] - XG
                            dy = fig['cy'] - YG
                            Ix_total += fig['ix_local'] + fig['area'] * (dy ** 2)
                            Iy_total += fig['iy_local'] + fig['area'] * (dx ** 2)
                        
                        for poly in poligonos:
                            for p in poly:
                                if p[1] > y_max: y_max = p[1]
                                if p[1] < y_min: y_min = p[1]
                        
                        dist_sup = max(abs(y_max - YG), 1e-5)
                        dist_inf = max(abs(YG - y_min), 1e-5)
                        Wx_sup = Ix_total / dist_sup
                        Wx_inf = Ix_total / dist_inf
                        
                        st.markdown("### Resultados del Análisis Estructural (Steiner)")
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Área Total ($A$)", f"{area_total:.2f} mm²")
                        col2.metric("Baricentro ($X_G, Y_G$)", f"({XG:.2f}, {YG:.2f}) mm")
                        col3.metric("Inercia Global ($I_x$)", f"{Ix_total:.2e} mm⁴")
                        
                        col4, col5 = st.columns(2)
                        col4.metric("Módulo Resistente Sup ($W_{x,sup}$)", f"{Wx_sup:.2f} mm³")
                        col5.metric("Módulo Resistente Inf ($W_{x,inf}$)", f"{Wx_inf:.2f} mm³")
                        
                        st.markdown("### Visualización Gráfica 2D")
                        fig, ax = plt.subplots(figsize=(6, 6))
                        for poly in poligonos:
                            xs = [p[0] for p in poly]
                            ys = [p[1] for p in poly]
                            ax.plot(xs, ys, marker='o', markersize=2)
                            ax.fill(xs, ys, alpha=0.3)
                        ax.plot(XG, YG, 'rx', markersize=10, label='Baricentro Global ($G$)')
                        ax.set_aspect('equal')
                        ax.set_xlabel('X (mm)')
                        ax.set_ylabel('Y (mm)')
                        ax.legend()
                        st.pyplot(fig)
                    else:
                        st.error("El área total calculada es igual a cero.")
                else:
                    st.warning("No se encontraron polilíneas cerradas válidas en el DXF.")
            except Exception as e:
                st.error(f"Error al procesar el archivo DXF: {e}")
        elif archivo_dxf is not None and not DXF_DISPONIBLE:
            st.error("La librería 'ezdxf' no está instalada en el entorno.")
    else:
        st.info("Seleccione una opción en el menú superior o cargue su archivo DXF personalizado para comenzar.")
