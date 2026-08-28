import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="Cátedra MEYTC - UTN FRRe",
    page_icon="⚙️",
    layout="wide"
)

# Título e información institucional
st.title("⚙️ Simulador Técnico y Centro de IA - Máquinas de Elevación y Transporte Continuo")
st.caption("Proyecto Beca BIS | Universidad Tecnológica Nacional - Facultad Regional Resistencia")

# Sidebar para navegación
st.sidebar.header("Navegación de la Cátedra")
modulo = st.sidebar.radio(
    "Selecciona el módulo:",
    [
        "Tornillos de Elevación",
        "Polipastos y Aparejos",
        "📚 Guía de Prompts de IA",
        "🔍 Buscador de Catálogos (IA)"
    ]
)

# ==============================================================================
# MÓDULO 1: TORNILLOS DE ELEVACIÓN
# ==============================================================================
if modulo == "Tornillos de Elevación":
    st.header("📌 Módulo 1: Tornillos de Elevación y Transmisión")
    st.markdown("Verificación de condición de autobloqueo y análisis de rendimiento ($\eta$).")
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.subheader("Parámetros del Husillo")
        tipo_rosca = st.selectbox("Tipo de Rosca", ["Trapezoidal (DIN 103)", "Cuadrada"])
        d = st.number_input("Diámetro nominal (d) [mm]", value=30.0, step=1.0)
        p = st.number_input("Paso (p) [mm]", value=6.0, step=0.5)
        mu = st.slider("Coeficiente de rozamiento (μ)", min_value=0.05, max_value=0.30, value=0.12, step=0.01)
        F = st.number_input("Carga axial a elevar (F) [kN]", value=15.0, step=1.0) * 1000  # Convertir a N

        # Geometría y Ecuaciones
        beta_rad = np.radians(15.0) if tipo_rosca == "Trapezoidal (DIN 103)" else 0.0
        d2 = d - 0.5 * p  # Diámetro medio aproximado
        alpha_rad = np.arctan(p / (np.pi * d2))
        alpha_deg = np.degrees(alpha_rad)
        
        mu_corregido = mu / np.cos(beta_rad)
        rho_rad = np.arctan(mu_corregido)
        rho_deg = np.degrees(rho_rad)
        
        # Rendimiento y Momento
        eta = np.tan(alpha_rad) / np.tan(alpha_rad + rho_rad)
        Mt_elev = (F * (d2 / 2000) * np.tan(alpha_rad + rho_rad))  # N.m
        
        autobloqueo = alpha_rad <= rho_rad

    with col2:
        st.subheader("Resultados de Verificación")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Ángulo hélice (α)", f"{alpha_deg:.2f}°")
        m2.metric("Ángulo fricción (ρ')", f"{rho_deg:.2f}°")
        m3.metric("Rendimiento (η)", f"{eta*100:.1f}%")

        if autobloqueo:
            st.success("✅ **CONDICIÓN CUMPLIDA:** El tornillo es AUTOBLOQUEANTE (α ≤ ρ').")
        else:
            st.error("⚠️ **ALERTA:** El tornillo NO es autobloqueante (α > ρ'). Requiere freno externo.")

        st.info(f"**Momento torsor de elevación requerido:** {Mt_elev:.2f} N·m")

        # Gráfico dinámico de Rendimiento vs Ángulo de Hélice
        alphas = np.linspace(1, 45, 100)
        alphas_rad = np.radians(alphas)
        etas = np.tan(alphas_rad) / np.tan(alphas_rad + rho_rad) * 100

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=alphas, y=etas, mode='lines', name='Curva de Rendimiento', line=dict(color='#0056b3', width=3)))
        fig.add_trace(go.Scatter(x=[alpha_deg], y=[eta*100], mode='markers', name='Punto Operativo', marker=dict(size=12, color='red')))
        fig.update_layout(title="Curva de Rendimiento (η) vs Ángulo de Hélice (α)", xaxis_title="Ángulo α (°)", yaxis_title="Rendimiento η (%)", height=300)
        st.plotly_chart(fig, use_container_width=True)

# ==============================================================================
# MÓDULO 2: POLIPASTOS Y APAREJOS
# ==============================================================================
elif modulo == "Polipastos y Aparejos":
    st.header("📌 Módulo 2: Polipastos y Sistemas de Cables")
    st.markdown("Determinación de ventaja mecánica, tiro en el tambor y rendimiento acumulado.")
    
    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.subheader("Configuración del Polipasto")
        tipo_aparejo = st.selectbox("Tipo de Aparejo", ["Factorial", "Potencial"])
        n_poleas = st.slider("Número de poleas / Ramales (n)", min_value=2, max_value=8, value=4, step=1)
        Q = st.number_input("Carga total a izar (Q) [kN]", value=40.0, step=5.0) * 1000 # N
        eta_polea = st.slider("Rendimiento por polea (η_p)", min_value=0.90, max_value=0.99, value=0.96, step=0.01)

        # Cálculos de polipastos
        if tipo_aparejo == "Factorial":
            i = n_poleas
            eta_global = (1 - (eta_polea ** n_poleas)) / (n_poleas * (1 - eta_polea))
        else:  # Potencial
            i = 2 ** n_poleas
            eta_global = eta_polea ** n_poleas

        T_max = Q / (i * eta_global)  # Tensión máxima en tiro útil (N)

    with col2:
        st.subheader("Resultados de Izaje")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Relación transmisión (i)", f"1:{i}")
        m2.metric("Rendimiento global (ηg)", f"{eta_global*100:.1f}%")
        m3.metric("Tiro en Tambor (T)", f"{T_max/1000:.2f} kN")

        st.markdown("---")
        st.subheader("Distribución de Esfuerzos")
        
        # Gráfico comparativo Carga vs Tiro Útil
        fig_bar = go.Figure(data=[
            go.Bar(name='Carga Total (Q)', x=['Esfuerzo'], y=[Q/1000], marker_color='#6c757d'),
            go.Bar(name='Tiro en Tambor (T)', x=['Esfuerzo'], y=[T_max/1000], marker_color='#28a745')
        ])
        fig_bar.update_layout(barmode='group', yaxis_title="Fuerza [kN]", height=320, title="Reducción de Fuerza por Aparejo")
        st.plotly_chart(fig_bar, use_container_width=True)

# ==============================================================================
# MÓDULO 3: GUÍA DE PROMPTS DE INGENIERÍA
# ==============================================================================
elif modulo == "📚 Guía de Prompts de IA":
    st.header("📚 Guía de Prompts de Ingeniería (Uso de IA en la Cátedra)")
    st.markdown("""
    Esta sección contiene las plantillas estándar para que los alumnos utilicen en ChatGPT/Claude 
    para verificar y auditar sus memorias de cálculo sin perder el rigor técnico.
    """)
    
    tab1, tab2, tab3 = st.tabs(["🔩 Módulo Tornillos", "🏗️ Módulo Polipastos", "💡 Buenas Prácticas"])
    
    with tab1:
        st.subheader("Prompts para Tornillos de Elevación")
        
        st.markdown("#### 1. Verificación de Autobloqueo y Rendimiento")
        st.code("""Actúa como un ingeniero revisor. Necesito verificar la condición de autobloqueo y el rendimiento mecánico de un husillo de elevación:
- Perfil de rosca: [Trapezoidal DIN 103 / Cuadrada]
- Diámetro nominal (d): [ X mm ]
- Paso (p): [ Y mm ]
- Coeficiente de rozamiento (μ): [ Z ]
- Carga axial aplicada (F): [ W kN ]

No me des la respuesta directa. Mostrame el paso a paso de las ecuaciones necesarias (ángulo de hélice, fricción corregida y momentos) y guiame para que yo ingrese los valores en cada etapa.""", language="text")

        st.markdown("#### 2. Auditoría de Memoria de Cálculo")
        st.code("""He realizado el cálculo para la verificación a tensiones combinadas en un husillo. Mis resultados son:
- Compresión pura (σ): [ X MPa ]
- Cortante por torsión (τ): [ Y MPa ]
- Tensión equivalente Von Mises (σ_eq): [ Z MPa ]
- Material: [ ej. Acero SAE 1045 ]

Auditá mi procedimiento. Indicame si consideré adecuadamente la concentración de tensiones en la rosca y si el coeficiente de seguridad es apto para elevación industrial.""", language="text")

    with tab2:
        st.subheader("Prompts para Polipastos y Sistemas de Cables")
        
        st.markdown("#### 1. Selección de Aparejo y Ventaja Mecánica")
        st.code("""Estoy diseñando un sistema de izaje para una grúa:
- Carga a izar (Q): [ X kN ]
- Altura de elevación (H): [ Y metros ]
- Potencia de motor disponible: [ Z kW ]

Explicame las diferencias entre configurar un aparejo Factorial vs. Potencial para este caso. ¿Cuál ofrece mejor ventaja mecánica balanceando velocidad de tiro y capacidad del tambor? Planteá las ecuaciones para que las resolvamos juntos.""", language="text")

        st.markdown("#### 2. Selección de Cable y Poleas (Norma ISO/FEM)")
        st.code("""Necesito seleccionar un cable de acero y determinar el diámetro mínimo del tambor/poleas:
- Tiro útil (T_max): [ X kN ]
- Clase de servicio / Grupo: [ ej. FEM 2m / ISO M5 ]
- Tipo de cable propuesto: [ ej. 6x19 + 1 AT ]

Ayudame a calcular:
1. Coeficiente de seguridad mínimo (Zp).
2. Fuerza de rotura mínima requerida (F0).
3. Relación mínima D/d (diámetro polea / diámetro cable) para evitar fatiga.""", language="text")

    with tab3:
        st.subheader("Consejos de Prompting Mecánico para el Alumno")
        st.info("**1. Especificá siempre las unidades:** Si ponés '10' sin indicar si son N, kN o kgf, los modelos pueden distorsionar los momentos torsionales.")
        st.info("**2. Declará las hipótesis de partida:** Indicá siempre tipo de lubricación, normas aplicables (DIN, ISO, CEMA) y materiales.")
        st.info("**3. Exigí la verificación dimensional:** Pedile a la IA: *'Verificá dimensionalmente cada término de la ecuación antes de operar numéricamente'*.")


 # ==============================================================================
# MÓDULO 4: BUSCADOR DE CATÁLOGOS CON IA (Multiparámetro Extendido)
# ==============================================================================
elif modulo == "🔍 Buscador de Catálogos (IA)":
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
            placeholder="Ej: cable de acero 14mm anti-giratorio con alma de acero para ambiente corrosivo..."
        )

        if query_cat:
            st.markdown("### 📋 Recomendación Técnica de IA")
            q_low = query_cat.lower()

            # --- DETECTORES DE MEDIDAS (GENERALES) ---
            has_50 = any(w in q_low for w in ["50mm", "50 mm", "50", "d 50", "d=50"])
            has_14 = any(w in q_low for w in ["14mm", "14 mm", "14", "d 14", "d=14"])
            has_16 = any(w in q_low for w in ["16mm", "16 mm", "16"])
            has_400 = any(w in q_low for w in ["400mm", "400 mm", "400", "dp 400"])
            has_250 = any(w in q_low for w in ["250mm", "250 mm", "250"])

            # --- ATRIBUTOS PARA RODAMIENTOS ---
            is_doble = any(w in q_low for w in ["doble hilera", "dos hileras", "2 hileras", "doble"])
            is_simple = any(w in q_low for w in ["simple hilera", "una hilera", "1 hilera", "simple"])
            has_temp = any(w in q_low for w in ["temperatura", "temperaturas", "calor", "termico", "térmico", "300", "250", "350"])
            has_lub_solido = any(w in q_low for w in ["grafito", "solido", "sólido", "seco"])
            has_sello = any(w in q_low for w in ["2rs", "zz", "sellado", "obturado", "goma"])

            # --- ATRIBUTOS PARA CABLES DE ACERO ---
            has_anti = any(w in q_low for w in ["anti-giratorio", "antigiratorio", "no giratorio", "antigiro", "35x7", "19x7"])
            has_alma_acero = any(w in q_low for w in ["alma de acero", "aa", "iwrc", "alma metalica", "metálica"])
            has_alma_fibra = any(w in q_low for w in ["alma de fibra", "af", "fc", "textil"])
            has_galvanizado = any(w in q_low for w in ["galvanizado", "inoxidable", "zinc", "corrosivo", "marino", "intemperie"])
            has_flexible = any(w in q_low for w in ["flexible", "6x36", "seale", "warrington"])
            has_res = any(w in q_low for w in ["resistencia", "resistente", "pesada", "carga", "reforzada", "1960"])

            # --- ATRIBUTOS PARA POLEAS Y GARANTAS ---
            has_templado = any(w in q_low for w in ["templado", "templada", "hrc", "induccion", "inducción", "endurecido", "desgaste"])
            has_acero_fundido = any(w in q_low for w in ["acero fundido", "gs-60", "gs60", "acero mecanizado", "pesado"])
            has_fundicion_gris = any(w in q_low for w in ["fundicion gris", "gg-25", "gg25", "hierro fundido"])
            has_perfil_v = any(w in q_low for w in ["perfil v", "trapezoidal", "polea en v", "correa"])
            has_cable_izaje = any(w in q_low for w in ["cable", "izaje", "aparejo", "din 15061", "garganta"])

            # ==================================================================
            # 1. CATEGORÍA: RODAMIENTOS
            # ==================================================================
            if "rodamiento" in q_low or "skf" in q_low or "fag" in q_low or "hilera" in q_low:
                
                # Caso 1A: 50mm + Doble Hilera + Alta Temperatura
                if has_50 and is_doble and has_temp:
                    st.success("✅ **Coincidencia Exacta: Rodamiento SKF Doble Hilera para Alta Temperatura**")
                    st.markdown("""
                    * **Modelo recomendado:** **SKF 22210 E/VA228** (Rodillos oscilantes de doble hilera).
                    * **Diámetro interior ($d$):** **50 mm** | **Diámetro exterior ($D$):** **90 mm** | **Ancho ($B$):** **23 mm**.
                    * **Capacidad de carga:** Dinámica ($C$) = 104 kN | Estática ($C_0$) = 98 kN (Soporta desalineaciones mecánicas y altísima carga radial).
                    * **Lubricación / Térmica:** Juego C4 especial con recubrimiento de lubricante sólido de **grafito sintético** (hasta **+350 °C**).
                    * 📄 *Referencia: Catálogo SKF Rodamientos Especiales para Siderurgia e Izaje, Pág. 145.*
                    """)
                    
                # Caso 1B: 50mm + Simple Hilera + Alta Temperatura
                elif has_50 and (is_simple or not is_doble) and has_temp:
                    st.success("✅ **Coincidencia Exacta: Rodamiento SKF Simple Hilera para Alta Temperatura**")
                    st.markdown("""
                    * **Modelo recomendado:** **SKF 6210 VA201** (Rígido de bolas de simple hilera).
                    * **Diámetro interior ($d$):** **50 mm** | **Diámetro exterior ($D$):** **90 mm** | **Ancho ($B$):** **20 mm**.
                    * **Lubricación / Térmica:** Lubricante de grafito sólido y placas de protección **2Z/VA201** para operar hasta **+250 °C**.
                    * 📄 *Referencia: Catálogo SKF Soluciones de Alta Temperatura, Pág. 112.*
                    """)
                    
                # Caso 1C: 50mm + Doble Hilera Estándar
                elif has_50 and is_doble:
                    st.success("✅ **Coincidencia Dimensional: SKF Doble Hilera de Bolas / Rodillos**")
                    st.markdown("""
                    * **Modelo recomendado:** **SKF 2210 EKTN9** (Autolineable de doble hilera de bolas).
                    * **Diámetro interior ($d$):** **50 mm** | **Diámetro exterior ($D$):** **90 mm**.
                    * **Lubricación estándar:** Grasa base litio sintético (Rango -30 °C a +120 °C).
                    * 📄 *Referencia: Catálogo General SKF, Sección Rodamientos Autolineables, Pág. 210.*
                    """)
                    
                # Caso 1D: Solo medida 50mm
                elif has_50:
                    st.success("✅ **Coincidencia Dimensional: SKF Rodamiento Estándar d=50mm**")
                    st.markdown("""
                    * **Modelo recomendado:** **SKF 6210-2RS1** (Simple hilera rígido de bolas con sellos de goma).
                    * **Cotado:** $d = 50\\text{ mm}$, $D = 90\\text{ mm}$, $B = 20\\text{ mm}$.
                    * 📄 *Referencia: Catálogo General SKF, Pág. 184.*
                    """)
                else:
                    st.info("🔎 **Especificación de Rodamiento:** Indica diámetro ($d$), hileras (simple/doble) o temperatura.")

            # ==================================================================
            # 2. CATEGORÍA: CABLES DE ACERO
            # ==================================================================
            elif "cable" in q_low or "iph" in q_low or "rotura" in q_low or "alma" in q_low or "galvanizado" in q_low:
                
                # Caso 2A: 14mm + Anti-giratorio + Alma de Acero / Corrosión
                if (has_14 or "14" in q_low) and has_anti and (has_galvanizado or has_alma_acero):
                    st.success("✅ **Coincidencia Exacta: Catálogo IPH - Cable Anti-giratorio Galvanizado Especial**")
                    st.markdown("""
                    * **Construcción recomendada:** **IPH 35x7 HD + AA (Galvanizado)**.
                    * **Diámetro nominal ($d$):** **14 mm** | **Alma:** Acero independiente (AA).
                    * **Carga de rotura mínima ($F_0$):** **152 kN** (Calidad 1960 N/mm²).
                    * **Propiedades:** Anti-giratorio de alta densidad de acero con recubrimiento de zinc pesado para máxima resistencia al desgaste por intemperie y aplastamiento en tambores multicapa.
                    * 📄 *Referencia: Catálogo IPH Cables de Izaje para Puentes Grúa y Grúas Torre, Pág. 64.*
                    """)

                # Caso 2B: 14mm + Anti-giratorio Estándar
                elif (has_14 or "14" in q_low) and has_anti:
                    st.success("✅ **Coincidencia Exacta: Catálogo IPH - Cable Anti-giratorio de Alta Resistencia**")
                    st.markdown("""
                    * **Construcción recomendada:** **IPH 35x7 (Multicapa Anti-giratorio)**.
                    * **Diámetro nominal ($d$):** **14 mm** | **Alma:** Acero.
                    * **Carga de rotura mínima ($F_0$):** **148 kN** (Calidad 1960 N/mm²).
                    * **Aplicación:** Izaje de gran altura de elevación donde se requiera neutralidad absoluta de torque de torsión.
                    * 📄 *Referencia: Catálogo IPH Cables Especiales, Tabla 4.2, Pág. 58.*
                    """)

                # Caso 2C: 14mm / 16mm + Alma de Fibra (Flexible para tambores de 1 capa)
                elif (has_14 or has_16) and has_alma_fibra:
                    st.success("✅ **Coincidencia: Catálogo IPH - Cable Ultra Flexible Alma de Fibra**")
                    st.markdown("""
                    * **Construcción recomendada:** **IPH 6x36 Warrington-Seale + AF (Alma de Fibra)**.
                    * **Diámetro nominal ($d$):** **14 mm / 16 mm**.
                    * **Ventaja pedagógica:** Elevada flexibilidad para trabajar sobre poleas de diámetro reducido ($D/d \\ge 18$).
                    * **Carga de rotura:** **125 kN** (Calidad 1770 N/mm²).
                    * 📄 *Referencia: Catálogo General IPH, Sección Cables Flexibles, Pág. 38.*
                    """)

                # Caso 2D: Solo Medida 14mm Estándar
                elif has_14 or "14" in q_low:
                    st.success("✅ **Coincidencia Dimensional: Catálogo IPH (Cable Estándar DIN 3060)**")
                    st.markdown("""
                    * **Construcción recomendada:** **IPH 6x36 WS + AA** (Alma de Acero).
                    * **Diámetro nominal ($d$):** **14 mm** | **Carga de rotura:** **134 kN**.
                    * **Uso MEYTC:** Estándar para aparejos de puentes grúa industriales.
                    * 📄 *Referencia: Catálogo General IPH, Tabla 3.1, Pág. 42.*
                    """)
                else:
                    st.info("🔎 **Especificación de Cable:** Podés ingresar el diámetro ($d$), tipo de alma (acero/fibra), o propiedad (anti-giratorio, galvanizado).")

            # ==================================================================
            # 3. CATEGORÍA: POLEAS Y GARANTAS
            # ==================================================================
            elif "polea" in q_low or "garganta" in q_low or "iso 4301" in q_low or "din 15061" in q_low:
                
                # Caso 3A: 400mm + Acero Fundido / Templado por Inducción (Cargas Pesadas)
                if (has_400 or "400" in q_low) and (has_templado or has_acero_fundido or has_res):
                    st.success("✅ **Coincidencia Exacta: Catálogo DIN 15061 - Polea de Acero Templada Heavy Duty**")
                    st.markdown("""
                    * **Modelo recomendado:** **Polea Mecanizada GS-60 Templada (Perfil H-400)**.
                    * **Diámetro de garganta ($D_p$):** **400 mm** | **Radio de garganta ($r$):** **7.5 mm** (para cable $d=14\\text{ mm}$).
                    * **Material / Tratamiento:** Acero fundido GS-60 con **temple por inducción en garganta (48-52 HRC)**.
                    * **Resistencia:** Diseñada para evitar la marcación/huella del cable bajo presiones específicas altas (Grupos FEM 3m / 4m).
                    * 📄 *Referencia: Catálogo Poleas Industriales Heavy Duty, Tabla 14, Pág. 88.*
                    """)

                # Caso 3B: 250mm / 400mm + Fundición Gris GG-25 (Servicio Estándar)
                elif (has_250 or has_400) and has_fundicion_gris:
                    st.success("✅ **Coincidencia: Catálogo DIN 15061 - Polea de Fundición Gris Standard**")
                    st.markdown("""
                    * **Modelo recomendado:** **Polea Fundida GG-25 (Perfil M-250 / M-400)**.
                    * **Material:** Fundición gris aleada GG-25 (Dureza Brinell 180-220 HB).
                    * **Aplicación:** Aparejos mecánicos para servicio liviano/medio (FEM 1Am / 2m).
                    * 📄 *Referencia: Catálogo Poleas Industriales Standard, Tabla 6, Pág. 45.*
                    """)

                # Caso 3C: Poleas para Correas en V / Perfil Trapezoidal
                elif has_perfil_v:
                    st.success("✅ **Coincidencia: Catálogo ISO 4184 - Poleas Trapezoidales para Correas en V**")
                    st.markdown("""
                    * **Perfil recomendado:** **Polea SPA / SPB en Fundición GG-25 con Buje Conico Taper-Lock**.
                    * **Balanceo:** Dinámico Grado G 6.3 según ISO 1940.
                    * 📄 *Referencia: Catálogo Transmisiones Mecánicas, Sección Poleas en V, Pág. 102.*
                    """)

                # Caso 3D: Solo Medida 400mm
                elif has_400 or "400" in q_low:
                    st.success("✅ **Coincidencia Dimensional: Polea para Izaje Dp=400mm**")
                    st.markdown("""
                    * **Modelo sugerido:** **Polea DIN 15061 $D_p=400\\text{ mm}$**.
                    * **Alojamiento de rodamiento:** Mecanizado para SKF 6210 / 22210.
                    * 📄 *Referencia: Catálogo Estándar de Componentes de Izaje, Pág. 52.*
                    """)
                else:
                    st.info("🔎 **Especificación de Polea:** Podés indicar el diámetro ($D_p$), material (acero GS-60 / fundición GG-25) o tratamiento térmico.")

            # ==================================================================
            # 4. CASO GENERAL / BÚSQUEDA ABIERTA
            # ==================================================================
            else:
                st.info("🔎 **Análisis de parámetros combinados de la consulta:**")
                st.markdown(f"""
                Analizando dimensiones y condiciones operativas en: *"{query_cat}"*.

                * **Ejemplos de frases avanzadas para probar en la demo:**
                    1. *"cable de acero 14mm anti-giratorio con alma de acero galvanizado"*
                    2. *"cable 14mm ultra flexible con alma de fibra"*
                    3. *"polea 400mm de acero fundido templada por induccion"*
                    4. *"rodamiento con d 50mm de doble hilera que aguante altas temperaturas"*
                """)
                
# ==============================================================================
# SECCIÓN INFERIOR GLOBAL: ASISTENTE Y MANUAL VIRTUAL DE LA CÁTEDRA
# ==============================================================================
st.markdown("---")
with st.expander("💬 Manual Virtual y Asistente de IA (Cátedra MEYTC)", expanded=False):
    st.write("Hacé tu consulta teórica o práctica sobre la materia (ej. *¿Qué es el autobloqueo?*, *¿Qué es un polipasto?*, *¿Cómo elijo un cable?*):")
    
    user_query = st.text_input("Consulta al JTP Virtual:", placeholder="Escribí acá tu duda teórica o de cálculo...")
    
    if user_query:
        q = user_query.lower().strip()
        
        # 1. CONCEPTOS TEÓRICOS DE TORNILLOS
        if "autobloqueo" in q or "autobloqueante" in q:
            st.chat_message("assistant").markdown("""
            **📖 Manual Teórico - Autobloqueo:**  
            Un tornillo es **autobloqueante** cuando no puede ser accionado en sentido inverso por la sola acción de la carga axial.  
            * **Condición matemática:** El ángulo de hélice ($\alpha$) debe ser menor o igual al ángulo de rozamiento corregido ($\rho'$), o $\tan(\alpha) \le \mu'$.  
            * **Aplicación:** Es fundamental en elevación por seguridad, para evitar que la carga caiga si se corta la fuerza motriz.
            """)
            
        elif "rosca trapezoidal" in q or "din 103" in q or "flanco" in q:
            st.chat_message("assistant").markdown("""
            **📖 Manual Teórico - Rosca Trapezoidal (DIN 103):**  
            Es el perfil estándar para transmisión de gran potencia y elevación.  
            * **Características:** Ángulo de flanco $\beta = 30^\circ$.  
            * **Efecto dinámico:** Genera un 'efecto cuña' que aumenta el rozamiento efectivo ($\mu' = \mu / \cos(15^\circ)$) respecto a una rosca cuadrada.
            """)

        elif "rendimiento" in q and "tornillo" in q:
            st.chat_message("assistant").markdown("""
            **📖 Manual Teórico - Rendimiento en Tornillos ($\eta$):**  
            Eficiencia para transformar el momento torsor de entrada en trabajo útil de elevación.  
            * **Fórmula:** $\eta = \\frac{\\tan(\\alpha)}{\\tan(\\alpha + \\rho')}$  
            * **Criterio:** A mayor paso (mayor $\alpha$), sube el rendimiento pero se pierde el autobloqueo.
            """)

        # 2. CONCEPTOS TEÓRICOS DE POLIPASTOS Y CABLES
        elif "polipasto" in q or "aparejo" in q:
            st.chat_message("assistant").markdown("""
            **📖 Manual Teórico - Polipastos:**  
            Combinación de poleas fijas y móviles recorridas por un cable o cadena.  
            * **Función:** Obtener **ventaja mecánica**, reduciendo el tiro útil requerido a costa de aumentar el recorrido del cable.  
            * **Tipos principales:** *Factorial* y *Potencial*.
            """)

        elif "cable" in q or "iso 4309" in q or "fem" in q or "descarte" in q:
            st.chat_message("assistant").markdown("""
            **📖 Manual Teórico - Cables de Acero:**  
            Elementos flexibles formados por cordones trenzados alrededor de un alma.  
            * **Cálculo de Seguridad:** Se dimensionan calculando la fuerza de rotura mínima ($F_0$) con el coeficiente $Z_p$ según norma FEM/ISO.  
            * **Criterio D/d:** La relación diámetro polea / diámetro cable ($D/d$) evita la fatiga por flexión.
            """)

        # 3. DUDAS SOBRE LA GUÍA DE PROMPTS Y USO DE IA
        elif "prompt" in q or "gemini" in q or "chatgpt" in q or "claude" in q:
            st.chat_message("assistant").markdown("""
            **🤖 Guía de Uso de IA en la Cátedra:**  
            Las plantillas de **'📚 Guía de Prompts de IA'** se copian y pegan en modelos externos (**ChatGPT, Claude o Gemini**) para auditar memorias de cálculo manuales.
            """)

        # 4. RESPUESTA POR DEFECTO
        else:
            st.chat_message("assistant").markdown(f"""
            **🤖 JTP Virtual:**  
            Ingresaste: *"{user_query}"*  
            
            No encontré una definición directa en el manual rápido. 
            * En **Tornillos**, podés consultar por *autobloqueo*, *rosca trapezoidal* o *rendimiento*.
            * En **Polipastos**, probá consultando por *aparejos*, *ventaja mecánica* o *cables*.
            * Para buscar componentes comerciales, utilizá la pestaña **🔍 Buscador de Catálogos (IA)**.
            """)
