# ==============================================================================
# MÓDULO 3: VIGAS COMBINADAS (CON RESTRICCIÓN DE CONTACTO FÍSICO / SOLDADURA)
# ==============================================================================
elif modulo == "📐 Módulo 3: Vigas Combinadas, Gráfico y Módulo Resistente (Steiner)":
    st.header("📐 Cálculo de Módulo Resistente y Gráfico 2D Real de Perfiles")
    st.markdown("Visualización geométrica exacta de perfiles **IPN** y **UPN** soldados con verificación de contacto físico.")

    # Catálogos de Perfiles
    cat_ipn = {
        "IPN 160": {"h": 16.0, "b": 7.4, "tw": 0.63, "tf": 0.95, "area": 22.8, "ix": 935.0, "iy": 54.7, "ey": 0.0},
        "IPN 200": {"h": 20.0, "b": 9.0, "tw": 0.75, "tf": 1.13, "area": 33.4, "ix": 2140.0, "iy": 117.0, "ey": 0.0},
        "IPN 240": {"h": 24.0, "b": 10.6, "tw": 0.87, "tf": 1.31, "area": 46.1, "ix": 4250.0, "iy": 221.0, "ey": 0.0},
        "IPN 300": {"h": 30.0, "b": 12.5, "tw": 1.08, "tf": 1.62, "area": 69.0, "ix": 9800.0, "iy": 451.0, "ey": 0.0},
        "IPN 400": {"h": 40.0, "b": 15.5, "tw": 1.44, "tf": 2.16, "area": 118.0, "ix": 29210.0, "iy": 1050.0, "ey": 0.0}
    }

    cat_upn = {
        "UPN 160": {"h": 16.0, "b": 6.5, "tw": 0.75, "tf": 1.05, "area": 24.0, "ix": 925.0, "iy": 85.3, "ey": 1.84},
        "UPN 200": {"h": 20.0, "b": 7.5, "tw": 0.85, "tf": 1.15, "area": 32.2, "ix": 1910.0, "iy": 148.0, "ey": 2.01},
        "UPN 240": {"h": 24.0, "b": 8.5, "tw": 0.95, "tf": 1.30, "area": 42.3, "ix": 3600.0, "iy": 248.0, "ey": 2.23},
        "UPN 300": {"h": 30.0, "b": 10.0, "tw": 1.00, "tf": 1.60, "area": 58.8, "ix": 8030.0, "iy": 495.0, "ey": 2.70}
    }

    col_ctrl, col_vis = st.columns([1.1, 1.2])

    with col_ctrl:
        st.subheader("1. Viga Base (Perfil Principal 1)")
        tipo_p1 = st.selectbox("Tipo Perfil Base:", ["IPN", "UPN"], index=0)
        prof1_name = st.selectbox("Designación Perfil 1:", list(cat_ipn.keys()) if tipo_p1 == "IPN" else list(cat_upn.keys()), index=2)
        p1 = cat_ipn[prof1_name] if tipo_p1 == "IPN" else cat_upn[prof1_name]

        x1_c, y1_c = 0.0, p1["h"] / 2.0
        rot_p1 = 0
        ix1, iy1, a1 = p1["ix"], p1["iy"], p1["area"]

        st.divider()
        st.subheader("2. Perfil de Refuerzo Soldado (Perfil 2)")
        agregar_p2 = st.checkbox("¿Agregar segundo perfil soldado?", value=True)

        if agregar_p2:
            tipo_p2 = st.selectbox("Tipo Perfil Refuerzo:", ["UPN", "IPN"], index=0)
            prof2_name = st.selectbox("Designación Perfil 2:", list(cat_upn.keys()) if tipo_p2 == "UPN" else list(cat_ipn.keys()), index=1)
            p2 = cat_upn[prof2_name] if tipo_p2 == "UPN" else cat_ipn[prof2_name]

            posicion_soldadura = st.radio(
                "Ubicación de Soldadura (Restringida a Contacto Físico):",
                [
                    "Ala Superior (Viga Carril - UPN Acostado C invertida)",
                    "Ala Superior (UPN o IPN derecho / centrado)",
                    "Ala Inferior (Refuerzo inferior centrado)",
                    "Alma Lateral Derecha (Apoyado sobre el ala P1)",
                    "Desplazamiento a lo largo del Ala Superior (Ajuste X limitado)"
                ]
            )

            # Cálculo automático de coordenadas según geometrías en contacto exacto
            if posicion_soldadura == "Ala Superior (Viga Carril - UPN Acostado C invertida)":
                rot_p2 = 270 if tipo_p2 == "UPN" else 90
                x2_c = 0.0
                # El dorso del alma de P2 apoya en el ala superior de P1 (y = p1['h'])
                ey2 = p2["ey"] if tipo_p2 == "UPN" else p2["b"] / 2.0
                y2_c = p1["h"] + ey2

            elif posicion_soldadura == "Ala Superior (UPN o IPN derecho / centrado)":
                rot_p2 = 0
                x2_c = 0.0
                # La base de P2 apoya en la superficie superior de P1
                y2_c = p1["h"] + (p2["h"] / 2.0)

            elif posicion_soldadura == "Ala Inferior (Refuerzo inferior centrado)":
                rot_p2 = 0
                x2_c = 0.0
                # La superficie superior de P2 apoya en el ala inferior de P1 (y = 0)
                y2_c = -p2["h"] / 2.0

            elif posicion_soldadura == "Alma Lateral Derecha (Apoyado sobre el ala P1)":
                rot_p2 = 0
                # Contacto entre ala derecha de P1 y dorso/ala izquierda de P2
                ey2 = p2["ey"] if tipo_p2 == "UPN" else p2["b"] / 2.0
                x2_c = (p1["b"] / 2.0) + ey2
                y2_c = p1["h"] / 2.0

            elif posicion_soldadura == "Desplazamiento a lo largo del Ala Superior (Ajuste X limitado)":
                rot_p2 = 270 if tipo_p2 == "UPN" else 90
                ey2 = p2["ey"] if tipo_p2 == "UPN" else p2["b"] / 2.0
                y2_c = p1["h"] + ey2
                
                # El solape X máximo está limitado al ancho del ala de P1
                max_x = max(0.0, (p1["b"] / 2.0) - (p2["h"] / 2.0 if rot_p2 in [90, 270] else p2["b"] / 2.0))
                x2_c = st.slider("Desplazamiento Lateral X (cm):", min_value=-float(max_x), max_value=float(max_x), value=0.0, step=0.1)

            a2 = p2["area"]

            # Momento de inercia según orientación
            if rot_p2 in [90, 270]:
                ix2_local, iy2_local = p2["iy"], p2["ix"]
            else:
                ix2_local, iy2_local = p2["ix"], p2["iy"]
        else:
            a2, x2_c, y2_c, ix2_local, iy2_local = 0.0, 0.0, 0.0, 0.0, 0.0

    # ==========================================================================
    # CÁLCULOS DE STEINER
    # ==========================================================================
    area_tot = a1 + a2
    xg_comp = ((a1 * x1_c) + (a2 * x2_c)) / area_tot
    yg_comp = ((a1 * y1_c) + (a2 * y2_c)) / area_tot

    ix_tot = (ix1 + a1 * (y1_c - yg_comp)**2) + (ix2_local + a2 * (y2_c - yg_comp)**2) if agregar_p2 else ix1
    iy_tot = (iy1 + a1 * (x1_c - xg_comp)**2) + (iy2_local + a2 * (x2_c - xg_comp)**2) if agregar_p2 else iy1

    # ==========================================================================
    # GEOMETRÍA REAL (POLÍGONOS) Y DIBUJO
    # ==========================================================================
    def obtener_poligono_perfil(p_type, p_data, x_center, y_center, rot_deg):
        h, b, tw, tf = p_data["h"], p_data["b"], p_data["tw"], p_data["tf"]
        ey = p_data.get("ey", 0.0)

        if p_type == "IPN":
            verts = [
                (-b/2, h/2), (b/2, h/2), (b/2, h/2 - tf), (tw/2, h/2 - tf),
                (tw/2, -h/2 + tf), (b/2, -h/2 + tf), (b/2, -h/2), (-b/2, -h/2),
                (-b/2, -h/2 + tf), (-tw/2, -h/2 + tf), (-tw/2, h/2 - tf), (-b/2, h/2 - tf)
            ]
        else: # UPN
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

    with col_vis:
        st.subheader("🖼️ Sección Compuesta Real (Acoplamiento Físico Garantizado)")

        fig, ax = plt.subplots(figsize=(6, 6))

        verts_p1 = obtener_poligono_perfil(tipo_p1, p1, x1_c, y1_c, rot_p1)
        poly1 = patches.Polygon(verts_p1, closed=True, color='navy', alpha=0.75, edgecolor='black', lw=1.2, label=f"P1: {prof1_name}")
        ax.add_patch(poly1)

        if agregar_p2:
            verts_p2 = obtener_poligono_perfil(tipo_p2, p2, x2_c, y2_c, rot_p2)
            poly2 = patches.Polygon(verts_p2, closed=True, color='firebrick', alpha=0.75, edgecolor='black', lw=1.2, label=f"P2: {prof2_name} ({rot_p2}°)")
            ax.add_patch(poly2)

        ax.axhline(yg_comp, color='crimson', linestyle='--', linewidth=1.5, label=f'Eje Neutro X_G ({yg_comp:.2f} cm)')
        ax.axvline(xg_comp, color='darkgreen', linestyle=':', linewidth=1.5, label=f'Eje Neutro Y_G ({xg_comp:.2f} cm)')
        ax.plot(xg_comp, yg_comp, 'ro', markersize=8)

        all_x = [v[0] for v in verts_p1] + ([v[0] for v in verts_p2] if agregar_p2 else [])
        all_y = [v[1] for v in verts_p1] + ([v[1] for v in verts_p2] if agregar_p2 else [])
        
        margin = 5.0
        ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
        ax.set_ylim(min(all_y) - margin, max(all_y) + margin)
        ax.set_aspect('equal', adjustable='box')
        ax.set_xlabel("X [cm]")
        ax.set_ylabel("Y [cm]")
        ax.set_title("Corte Transversal y Soldadura en Contacto Directo", fontsize=11, fontweight='bold')
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend(loc='upper right', fontsize=8)

        st.pyplot(fig)

    # Módulos Resistentes
    d_sup = max(all_y) - yg_comp
    d_inf = yg_comp - min(all_y)
    d_der = max(all_x) - xg_comp
    d_izq = xg_comp - min(all_x)

    wx_sup = ix_tot / d_sup if d_sup > 0 else 0
    wx_inf = ix_tot / d_inf if d_inf > 0 else 0
    wy_der = iy_tot / d_der if d_der > 0 else 0
    wy_izq = iy_tot / d_izq if d_izq > 0 else 0

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
