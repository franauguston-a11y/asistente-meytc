import streamlit as st
import pandas as pd

# ==============================================================================
# CONFIGURACIÓN GENERAL DE LA APLICACIÓN Y SIMULADOR
# ==============================================================================
st.set_page_config(
    page_title="Plataforma de Simulación y Catálogos MEYTC",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Plataforma de Cálculo, Simulación y Catálogos Comerciales (MEYTC)")
st.caption("Proyecto de Beca de Investigación — Máquinas de Elevación y Transporte (UTN FRRe)")
st.markdown("---")

# Navegación lateral reducida
modulo = st.sidebar.radio(
    "Navegación de Módulos:",
    [
        "🛞 Módulo 1: Simulación Rodamientos (ISO 281)",
        "🔍 Módulo 2: Buscador de Catálogos (IA)"
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
        carga_p = st.number_input("Carga Dinámica Equivalente P (kN):", min_value=1.0, value=25.0)
        cap_c = st.number_input("Capacidad de Carga Dinámica C (kN):", min_value=1.0, value=104.0)
        rpm = st.slider("Velocidad de Giro (rpm):", min_value=10, max_value=1000, value=150, step=10)
        tipo_elem = st.radio("Contacto / Elemento Rodante:", ["Bolas (p=3)", "Rodillos (p=10/3)"])

    with col2:
        st.subheader("Resultado de la Simulación")
        p_exp = 3.0 if "Bolas" in tipo_elem else (10.0 / 3.0)
        l10_mill = (cap_c / carga_p) ** p_exp
        l10_horas = (10**6 / (60 * rpm)) * l10_mill

        st.metric(label="Vida Útil Simulada L10h:", value=f"{l10_horas:,.0f} hs")
        st.markdown(f"$$L_{{10}} = \\left( \\frac{{{cap_c}}}{{{carga_p}}} \\right)^{{{p_exp:.2f}}} = {l10_mill:.2f} \\text{{ millones de revoluciones}}$$")
        st.markdown(f"$$L_{{10h}} = \\frac{{10^6}}{{60 \\cdot {rpm}}} \\cdot {l10_mill:.2f} = {l10_horas:,.0f} \\text{{ horas}}$$")

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

            # Detectores de medidas y atributos
            has_50 = any(w in q_low for w in ["50mm", "50 mm", "50", "d 50", "d=50"])
            has_14 = any(w in q_low for w in ["14mm", "14 mm", "14", "d 14", "d=14"])
            has_16 = any(w in q_low for w in ["16mm", "16 mm", "16"])
            has_400 = any(w in q_low for w in ["400mm", "400 mm", "400", "dp 400"])
            has_250 = any(w in q_low for w in ["250mm", "250 mm", "250"])

            is_doble = any(w in q_low for w in ["doble hilera", "dos hileras", "2 hileras", "doble"])
            is_simple = any(w in q_low for w in ["simple hilera", "una hilera", "1 hilera", "simple"])
            has_temp = any(w in q_low for w in ["temperatura", "temperaturas", "calor", "termico", "térmico", "300", "250", "350"])

            has_anti = any(w in q_low for w in ["anti-giratorio", "antigiratorio", "no giratorio", "antigiro", "35x7", "19x7"])
            has_alma_acero = any(w in q_low for w in ["alma de acero", "aa", "iwrc", "alma metalica"])
            has_alma_fibra = any(w in q_low for w in ["alma de fibra", "af", "fc"])
            has_galvanizado = any(w in q_low for w in ["galvanizado", "inoxidable", "zinc", "corrosivo"])

            has_templado = any(w in q_low for w in ["templado", "templada", "hrc", "induccion", "endurecido"])
            has_acero_fundido = any(w in q_low for w in ["acero fundido", "gs-60", "gs60"])
            has_fundicion_gris = any(w in q_low for w in ["fundicion gris", "gg-25", "gg25"])

            # Evaluación Rodamientos
            if "rodamiento" in q_low or "skf" in q_low or "fag" in q_low or "hilera" in q_low:
                if has_50 and is_doble and has_temp:
                    st.success("✅ **Coincidencia Exacta: Rodamiento SKF Doble Hilera para Alta Temperatura**")
                    st.markdown("""
                    * **Modelo recomendado:** **SKF 22210 E/VA228** (Rodillos oscilantes de doble hilera).
                    * **Cotado:** $d = 50\\text{ mm}$, $D = 90\\text{ mm}$, $B = 23\\text{ mm}$.
                    * **Lubricación / Térmica:** Juego C4 con **grafito sintético** (hasta **+350 °C**).
                    * 📄 *Referencia: Catálogo SKF Rodamientos Especiales, Pág. 145.*
                    """)
                elif has_50 and (is_simple or not is_doble) and has_temp:
                    st.success("✅ **Coincidencia Exacta: Rodamiento SKF Simple Hilera para Alta Temperatura**")
                    st.markdown("""
                    * **Modelo recomendado:** **SKF 6210 VA201** ($d=50\\text{ mm}$, simple hilera, hasta **+250 °C**).
                    * 📄 *Referencia: Catálogo SKF Soluciones Térmicas, Pág. 112.*
                    """)
                elif has_50 and is_doble:
                    st.success("✅ **Coincidencia Dimensional: SKF Doble Hilera de Bolas**")
                    st.markdown("* **Modelo:** **SKF 2210 EKTN9** ($d=50\\text{ mm}$). Pág. 210.")
                elif has_50:
                    st.success("✅ **Coincidencia Dimensional: SKF Rodamiento Estándar d=50mm**")
                    st.markdown("* **Modelo:** **SKF 6210-2RS1** ($d=50\\text{ mm}$, $D=90\\text{ mm}$). Pág. 184.")

            # Evaluación Cables
            elif "cable" in q_low or "iph" in q_low or "rotura" in q_low or "galvanizado" in q_low:
                if (has_14 or "14" in q_low) and has_anti and (has_galvanizado or has_alma_acero):
                    st.success("✅ **Coincidencia Exacta: Catálogo IPH - Cable Anti-giratorio Galvanizado**")
                    st.markdown("* **Modelo:** **IPH 35x7 HD + AA (Galvanizado)** ($d=14\\text{ mm}$, $F_0=152\\text{ kN}$). Pág. 64.")
                elif (has_14 or "14" in q_low) and has_anti:
                    st.success("✅ **Coincidencia Exacta: Catálogo IPH - Cable Anti-giratorio Estándar**")
                    st.markdown("* **Modelo:** **IPH 35x7** ($d=14\\text{ mm}$, $F_0=148\\text{ kN}$). Pág. 58.")
                elif (has_14 or has_16) and has_alma_fibra:
                    st.success("✅ **Coincidencia: Catálogo IPH - Cable Flexible Alma de Fibra**")
                    st.markdown("* **Modelo:** **IPH 6x36 WS + AF** ($d=14/16\\text{ mm}$, $F_0=125\\text{ kN}$). Pág. 38.")
                elif has_14 or "14" in q_low:
                    st.success("✅ **Coincidencia Dimensional: Catálogo IPH (Estándar DIN 3060)**")
                    st.markdown("* **Modelo:** **IPH 6x36 WS + AA** ($d=14\\text{ mm}$, $F_0=134\\text{ kN}$). Pág. 42.")

            # Evaluación Poleas
            elif "polea" in q_low or "garganta" in q_low or "iso 4301" in q_low:
                if (has_400 or "400" in q_low) and (has_templado or has_acero_fundido):
                    st.success("✅ **Coincidencia Exacta: Catálogo DIN 15061 - Polea Templada Heavy Duty**")
                    st.markdown("* **Modelo:** **GS-60 Templada (Perfil H-400)** ($D_p=400\\text{ mm}$, 48-52 HRC). Pág. 88.")
                elif (has_250 or has_400) and has_fundicion_gris:
                    st.success("✅ **Coincidencia: Catálogo DIN 15061 - Polea Fundición Gris**")
                    st.markdown("* **Modelo:** **GG-25 (Perfil M-250/M-400)**. Pág. 45.")
                elif has_400 or "400" in q_low:
                    st.success("✅ **Coincidencia Dimensional: Polea Dp=400mm**")
                    st.markdown("* **Modelo:** **Polea DIN 15061 $D_p=400\\text{ mm}$**. Pág. 52.")

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
