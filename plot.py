import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as mcolors
import time

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Physics Lab · Graph Studio",
    page_icon="⚗️",
    layout="centered"
)

# =========================================================
# CUSTOM CSS — Dark Glassmorphism Theme
# =========================================================

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">

<style>

/* ── ROOT VARIABLES ── */
:root {
  --bg-deep:     #020408;
  --bg-panel:    rgba(8, 16, 28, 0.85);
  --bg-card:     rgba(12, 24, 42, 0.75);
  --accent-cyan: #00f5ff;
  --accent-blue: #0080ff;
  --accent-violet: #7c3aed;
  --accent-pink:  #f472b6;
  --text-primary: #e2f0ff;
  --text-muted:   #6b8aa8;
  --border:       rgba(0, 245, 255, 0.15);
  --glow-cyan:    0 0 20px rgba(0,245,255,0.4), 0 0 60px rgba(0,245,255,0.15);
  --glow-blue:    0 0 20px rgba(0,128,255,0.4), 0 0 60px rgba(0,128,255,0.15);
}

/* ── GLOBAL BACKGROUND ── */
.stApp {
  background: var(--bg-deep);
  background-image:
    radial-gradient(ellipse 80% 60% at 50% -10%, rgba(0,128,255,0.12) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 90% 80%, rgba(124,58,237,0.08) 0%, transparent 50%),
    repeating-linear-gradient(
      0deg,
      transparent,
      transparent 40px,
      rgba(0,245,255,0.015) 40px,
      rgba(0,245,255,0.015) 41px
    ),
    repeating-linear-gradient(
      90deg,
      transparent,
      transparent 40px,
      rgba(0,245,255,0.015) 40px,
      rgba(0,245,255,0.015) 41px
    );
  font-family: 'Rajdhani', sans-serif;
  color: var(--text-primary);
}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 3rem; }

/* ── HERO HEADER ── */
.hero-header {
  text-align: center;
  padding: 2.5rem 1rem 1.5rem;
  position: relative;
}
.hero-title {
  font-family: 'Orbitron', monospace;
  font-size: 2.6rem;
  font-weight: 900;
  letter-spacing: 0.12em;
  background: linear-gradient(135deg, #00f5ff 0%, #0080ff 50%, #7c3aed 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-transform: uppercase;
  margin: 0;
  line-height: 1.2;
  filter: drop-shadow(0 0 30px rgba(0,245,255,0.5));
}
.hero-sub {
  font-family: 'Share Tech Mono', monospace;
  font-size: 0.85rem;
  color: var(--text-muted);
  letter-spacing: 0.25em;
  margin-top: 0.5rem;
  text-transform: uppercase;
}
.hero-line {
  width: 120px;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
  margin: 1rem auto 0;
}

/* ── SECTION CARDS ── */
.section-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1.5rem 1.8rem;
  margin: 1.2rem 0;
  backdrop-filter: blur(20px);
  box-shadow: 0 4px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
  position: relative;
  overflow: hidden;
}
.section-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
  opacity: 0.6;
}
.section-title {
  font-family: 'Orbitron', monospace;
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--accent-cyan);
  margin: 0 0 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

/* ── RESULT CARD ── */
.result-card {
  background: linear-gradient(135deg, rgba(0,245,255,0.04), rgba(0,128,255,0.06));
  border: 1px solid rgba(0,245,255,0.25);
  border-radius: 14px;
  padding: 1.5rem 1.8rem;
  margin: 1.2rem 0;
  backdrop-filter: blur(20px);
  box-shadow: 0 0 40px rgba(0,245,255,0.08), inset 0 1px 0 rgba(0,245,255,0.1);
}
.result-card h3 {
  font-family: 'Orbitron', monospace;
  font-size: 0.9rem;
  letter-spacing: 0.2em;
  color: var(--accent-cyan);
  text-transform: uppercase;
  margin: 0 0 1rem;
}
.result-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.6rem 0;
  border-bottom: 1px solid rgba(0,245,255,0.07);
  font-size: 1rem;
}
.result-row:last-child { border-bottom: none; }
.result-label {
  font-family: 'Share Tech Mono', monospace;
  color: var(--text-muted);
  font-size: 0.85rem;
  letter-spacing: 0.05em;
}
.result-value {
  font-family: 'Orbitron', monospace;
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--accent-cyan);
  text-shadow: 0 0 15px rgba(0,245,255,0.6);
}

/* ── SELECTBOX ── */
.stSelectbox > div > div {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  color: var(--text-primary) !important;
  font-family: 'Rajdhani', sans-serif !important;
  font-size: 1.05rem !important;
  font-weight: 600 !important;
}
.stSelectbox > div > div:focus-within {
  border-color: var(--accent-cyan) !important;
  box-shadow: 0 0 0 2px rgba(0,245,255,0.2) !important;
}

/* ── TEXT INPUTS ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
  background: rgba(8,20,36,0.9) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  color: var(--accent-cyan) !important;
  font-family: 'Share Tech Mono', monospace !important;
  font-size: 0.9rem !important;
  padding: 0.7rem 1rem !important;
  caret-color: var(--accent-cyan);
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
  border-color: var(--accent-cyan) !important;
  box-shadow: 0 0 0 2px rgba(0,245,255,0.15), var(--glow-cyan) !important;
}
.stTextInput > label,
.stNumberInput > label,
.stSelectbox > label {
  font-family: 'Share Tech Mono', monospace !important;
  font-size: 0.82rem !important;
  letter-spacing: 0.12em !important;
  color: var(--text-muted) !important;
  text-transform: uppercase !important;
}

/* ── BUTTON ── */
.stButton > button {
  width: 100%;
  background: linear-gradient(135deg, rgba(0,245,255,0.1), rgba(0,128,255,0.15)) !important;
  border: 1px solid var(--accent-cyan) !important;
  border-radius: 10px !important;
  color: var(--accent-cyan) !important;
  font-family: 'Orbitron', monospace !important;
  font-size: 0.85rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.2em !important;
  text-transform: uppercase !important;
  padding: 0.75rem 2rem !important;
  cursor: pointer !important;
  transition: all 0.3s ease !important;
  position: relative !important;
  overflow: hidden !important;
  box-shadow: 0 0 20px rgba(0,245,255,0.15) !important;
}
.stButton > button:hover {
  background: linear-gradient(135deg, rgba(0,245,255,0.2), rgba(0,128,255,0.25)) !important;
  box-shadow: var(--glow-cyan) !important;
  transform: translateY(-1px) !important;
}
.stButton > button:active {
  transform: translateY(0) !important;
}

/* ── DATAFRAME ── */
.stDataFrame {
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  overflow: hidden !important;
}
[data-testid="stDataFrameResizable"] {
  background: var(--bg-card) !important;
}

/* ── ERROR ── */
.stAlert {
  background: rgba(239,68,68,0.1) !important;
  border: 1px solid rgba(239,68,68,0.4) !important;
  border-radius: 10px !important;
  color: #fca5a5 !important;
}

/* ── DIVIDER ── */
hr {
  border: none !important;
  height: 1px !important;
  background: linear-gradient(90deg, transparent, var(--border), transparent) !important;
  margin: 1.5rem 0 !important;
}

/* ── PLOTLY / PYPLOT CONTAINER ── */
.element-container iframe,
[data-testid="stImage"] img {
  border-radius: 12px;
  border: 1px solid var(--border);
}

/* ── SCAN LINE ANIMATION OVERLAY (decorative) ── */
@keyframes scanline {
  0%   { transform: translateY(-100%); }
  100% { transform: translateY(100vh); }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HERO HEADER
# =========================================================

st.markdown("""
<div class="hero-header">
  <h1 class="hero-title">⚗ Physics Lab</h1>
  <p class="hero-sub">Graph Studio · Experiment Analysis Platform</p>
  <div class="hero-line"></div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# GRAPH STYLING HELPER
# =========================================================

def style_figure(fig, ax):
    """Apply dark neon theme to any matplotlib figure."""
    fig.patch.set_facecolor('#020810')
    ax.set_facecolor('#040d1a')

    # Grid
    ax.grid(True, color='#0a2040', linewidth=0.8, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)

    # Spines
    for spine in ax.spines.values():
        spine.set_edgecolor('#0d2d50')
        spine.set_linewidth(1)

    # Tick labels
    ax.tick_params(colors='#4a8aaa', labelsize=10, length=4)
    ax.xaxis.label.set_color('#6ba8c8')
    ax.yaxis.label.set_color('#6ba8c8')
    ax.title.set_color('#00f5ff')
    ax.title.set_fontsize(13)
    ax.title.set_fontweight('bold')

    # Legend
    legend = ax.get_legend()
    if legend:
        legend.get_frame().set_facecolor('#040d1a')
        legend.get_frame().set_edgecolor('#0d2d50')
        for text in legend.get_texts():
            text.set_color('#8ab8d0')

    fig.tight_layout(pad=2.0)


def glow_line(ax, x, y, color_hex='#00f5ff', label=None, linewidth=2.2):
    """Plot a glowing line with multi-layer halo effect."""
    x = list(x)
    y = list(y)

    # Outer glow layers
    for alpha, lw in [(0.04, 18), (0.08, 12), (0.15, 7), (0.3, 4)]:
        ax.plot(x, y, color=color_hex, linewidth=lw, alpha=alpha, solid_capstyle='round')

    # Core bright line
    ax.plot(x, y, color=color_hex, linewidth=linewidth, alpha=1.0,
            solid_capstyle='round', label=label,
            path_effects=[pe.withStroke(linewidth=linewidth+0.5, foreground=color_hex)])


def animated_glow_plot(x_data, y_data, xlabel, ylabel, title,
                        color_main='#00f5ff', color_fit='#ff6ec7',
                        do_fit=False, fit_deg=1,
                        scatter_x=None, scatter_y=None,
                        scatter_color='#ffd700',
                        extra_lines=None):
    """
    Build a dark glowing matplotlib figure.
    Returns (fig, slope, intercept) if do_fit else (fig, None, None)
    """
    fig, ax = plt.subplots(figsize=(9, 5.5))
    style_figure(fig, ax)

    x_np = np.array(x_data, dtype=float)
    y_np = np.array(y_data, dtype=float)

    # Sort
    idx = np.argsort(x_np)
    xs, ys = x_np[idx], y_np[idx]

    # Fill under curve
    ax.fill_between(xs, ys, alpha=0.06, color=color_main, interpolate=True)

    # Main glowing line
    glow_line(ax, xs, ys, color_main, label='Experimental Data')

    # Scatter overlay
    if scatter_x is not None and scatter_y is not None:
        sx = np.array(scatter_x, dtype=float)
        sy = np.array(scatter_y, dtype=float)
        ax.scatter(sx, sy, color=scatter_color, s=70, zorder=6,
                   edgecolors='#020810', linewidths=0.8,
                   label='Data Points',
                   path_effects=[pe.withStroke(linewidth=4, foreground=scatter_color + '55')])
    else:
        # Dot markers on the line itself
        ax.scatter(xs, ys, color='#ffffff', s=45, zorder=6,
                   edgecolors=color_main, linewidths=1.5,
                   path_effects=[pe.withStroke(linewidth=4, foreground=color_main + '55')])

    slope, intercept = None, None

    if do_fit:
        slope, intercept = np.polyfit(xs, ys, fit_deg) if fit_deg == 1 else (None, None)
        if fit_deg == 1:
            fit_y = slope * xs + intercept
        else:
            poly = np.polyfit(xs, ys, fit_deg)
            curve = np.poly1d(poly)
            x_smooth = np.linspace(xs.min(), xs.max(), 300)
            fit_y_smooth = curve(x_smooth)
            glow_line(ax, x_smooth, fit_y_smooth, color_fit, label='Fitted Curve', linewidth=2)
            slope, intercept = np.polyfit(xs, ys, 1)

        if fit_deg == 1:
            glow_line(ax, xs, fit_y, color_fit, label='Best Fit Line', linewidth=1.8)

    if extra_lines:
        for ex in extra_lines:
            glow_line(ax, ex['x'], ex['y'], ex.get('color', '#ffaa00'),
                      ex.get('label'), ex.get('lw', 1.8))

    ax.set_xlabel(xlabel, fontsize=11, labelpad=8)
    ax.set_ylabel(ylabel, fontsize=11, labelpad=8)
    ax.set_title(title, fontsize=13, pad=14)
    ax.legend(loc='best', fontsize=9)

    return fig, slope, intercept


# =========================================================
# EXPERIMENT SELECTOR
# =========================================================

st.markdown('<div style="margin: 0.5rem 0 1rem;">', unsafe_allow_html=True)

experiment = st.selectbox(
    "SELECT EXPERIMENT",
    [
        "— Choose an Experiment —",
        "Newton's Rings",
        "Characteristics of Solar Cell",
        "Malus Law",
        "Band Gap of Semiconductor",
        "General Graphs"
    ]
)
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# NEWTON'S RINGS
# =========================================================

if experiment == "Newton's Rings":

    st.markdown("""
    <div class="section-card">
      <div class="section-title">🔬 Newton's Rings — Observation Table</div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        n_input = st.text_input("Order of dark rings (n)",
            placeholder="18, 16, 14, 12, 10, 8, 6, 4, 2")
        x1_input = st.text_input("Left readings x₁ (cm)",
            placeholder="1.607, 1.575, 1.508 …")
    with col2:
        x2_input = st.text_input("Right readings x₂ (cm)",
            placeholder="0.942, 0.957, 0.984 …")
        wavelength_nm = st.number_input("Wavelength λ (nm)", min_value=1.0, value=589.0, step=1.0)

    if st.button("⚡ GENERATE GRAPH & RESULTS", key="nr"):
        try:
            n   = [float(i.strip()) for i in n_input.split(",") if i.strip()]
            x1  = [float(i.strip()) for i in x1_input.split(",") if i.strip()]
            x2  = [float(i.strip()) for i in x2_input.split(",") if i.strip()]

            if not (len(n) == len(x1) == len(x2)):
                st.error("All columns must contain the same number of values.")
            else:
                Dn  = [abs(a - b) for a, b in zip(x1, x2)]
                Dn2 = [round(d**2, 4) for d in Dn]

                df = pd.DataFrame({
                    "n": n, "x₁ (cm)": x1, "x₂ (cm)": x2,
                    "Dₙ = x₁−x₂": [round(i,4) for i in Dn],
                    "Dₙ² (cm²)": Dn2
                })
                st.dataframe(df, use_container_width=True)

                fig, slope, intercept = animated_glow_plot(
                    n, Dn2,
                    xlabel="Order of dark ring (n)",
                    ylabel="Dₙ² (cm²)",
                    title="Newton's Rings — Dₙ² vs n",
                    color_main='#00f5ff',
                    color_fit='#ff6ec7',
                    do_fit=True, fit_deg=1
                )
                st.pyplot(fig)

                wavelength_cm = wavelength_nm * 1e-7
                R = slope / (4 * wavelength_cm)

                st.markdown(f"""
                <div class="result-card">
                  <h3>📌 Final Results</h3>
                  <div class="result-row">
                    <span class="result-label">Slope of Graph</span>
                    <span class="result-value">{slope:.6f} cm²/ring</span>
                  </div>
                  <div class="result-row">
                    <span class="result-label">Wavelength (λ)</span>
                    <span class="result-value">{wavelength_nm:.1f} nm</span>
                  </div>
                  <div class="result-row">
                    <span class="result-label">Radius of Curvature (R)</span>
                    <span class="result-value">{R:.4f} cm</span>
                  </div>
                </div>""", unsafe_allow_html=True)

        except ValueError:
            st.error("Please enter valid numeric values only.")

# =========================================================
# SOLAR CELL
# =========================================================

elif experiment == "Characteristics of Solar Cell":

    st.markdown("""
    <div class="section-card">
      <div class="section-title">☀️ Solar Cell I-V Characteristics</div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        voltage_input = st.text_input("Voltage (V)", placeholder="2.6, 2.4, 2.2, 2.0, 1.8 …")
    with col2:
        current_input = st.text_input("Current (µA)", placeholder="18.3, 23.3, 28.6, 32.1 …")

    if st.button("⚡ GENERATE SOLAR CELL GRAPH", key="sc"):
        try:
            voltage = [float(i.strip()) for i in voltage_input.split(",") if i.strip()]
            current = [float(i.strip()) for i in current_input.split(",") if i.strip()]

            if len(voltage) != len(current):
                st.error("Voltage and Current must have the same number of values.")
            else:
                df = pd.DataFrame({"Voltage (V)": voltage, "Current (µA)": current})
                st.dataframe(df, use_container_width=True)

                v_np = np.array(voltage); i_np = np.array(current)
                idx  = np.argsort(v_np)
                vs, cs = v_np[idx], i_np[idx]

                poly   = np.polyfit(vs, cs, 3)
                curve  = np.poly1d(poly)
                x_sm   = np.linspace(vs.min(), vs.max(), 300)
                y_sm   = curve(x_sm)

                fig, ax = plt.subplots(figsize=(9, 5.5))
                style_figure(fig, ax)
                ax.fill_between(x_sm, y_sm, alpha=0.06, color='#00ff88')
                glow_line(ax, x_sm, y_sm, '#00ff88', label='I-V Curve', linewidth=2.2)
                ax.scatter(vs, cs, color='#ffd700', s=70, zorder=6,
                           edgecolors='#020810', linewidths=0.8,
                           label='Experimental Points',
                           path_effects=[pe.withStroke(linewidth=4, foreground='#ffd70055')])
                ax.set_xlabel("Voltage (V)", fontsize=11, labelpad=8)
                ax.set_ylabel("Current (µA)", fontsize=11, labelpad=8)
                ax.set_title("Solar Cell I-V Characteristics", fontsize=13, pad=14)
                ax.legend(fontsize=9)
                st.pyplot(fig)

                Isc   = max(current); Voc = max(voltage)
                power = [v*i for v,i in zip(voltage,current)]
                Pmax  = max(power); midx = power.index(Pmax)
                Vm, Im = voltage[midx], current[midx]
                FF     = Pmax / (Voc * Isc)

                st.markdown(f"""
                <div class="result-card">
                  <h3>📌 Final Results</h3>
                  <div class="result-row"><span class="result-label">Open Circuit Voltage (V_oc)</span><span class="result-value">{Voc:.2f} V</span></div>
                  <div class="result-row"><span class="result-label">Short Circuit Current (I_sc)</span><span class="result-value">{Isc:.2f} µA</span></div>
                  <div class="result-row"><span class="result-label">Max Power Voltage (Vm)</span><span class="result-value">{Vm:.2f} V</span></div>
                  <div class="result-row"><span class="result-label">Max Power Current (Im)</span><span class="result-value">{Im:.2f} µA</span></div>
                  <div class="result-row"><span class="result-label">Maximum Power (Pmax)</span><span class="result-value">{Pmax:.2f} µW</span></div>
                  <div class="result-row"><span class="result-label">Fill Factor (FF)</span><span class="result-value">{FF:.4f}</span></div>
                </div>""", unsafe_allow_html=True)

        except ValueError:
            st.error("Please enter valid numeric values only.")

# =========================================================
# MALUS LAW
# =========================================================

elif experiment == "Malus Law":

    st.markdown("""
    <div class="section-card">
      <div class="section-title">🌗 Malus Law — Polarisation Experiment</div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        theta_input   = st.text_input("Angular Position θ (degrees)", placeholder="0, 10, 20, 30 …")
    with col2:
        current_input = st.text_input("Current I (µA)", placeholder="13.8, 16.2, 28.0, 43.6 …")

    if st.button("⚡ GENERATE MALUS LAW GRAPH", key="ml"):
        try:
            theta   = [float(i.strip()) for i in theta_input.split(",") if i.strip()]
            current = [float(i.strip()) for i in current_input.split(",") if i.strip()]

            if len(theta) != len(current):
                st.error("Theta and Current must have the same number of values.")
            else:
                Imax       = max(current)
                theta_rad  = np.radians(theta)
                cos2       = list(np.cos(theta_rad)**2)
                P          = [i/Imax for i in current]

                df = pd.DataFrame({
                    "θ (°)": theta, "I (µA)": current,
                    "I/I_max": [round(p,3) for p in P],
                    "cos²θ":  [round(c,3) for c in cos2]
                })
                st.dataframe(df, use_container_width=True)

                fig, slope, intercept = animated_glow_plot(
                    cos2, P,
                    xlabel="cos²θ", ylabel="I / I_max",
                    title="Malus Law Verification — I/I_max vs cos²θ",
                    color_main='#bf7fff',
                    color_fit='#00f5ff',
                    do_fit=True, fit_deg=1,
                    scatter_x=cos2, scatter_y=P,
                    scatter_color='#ffd700'
                )
                st.pyplot(fig)

                st.markdown(f"""
                <div class="result-card">
                  <h3>📌 Final Results</h3>
                  <div class="result-row"><span class="result-label">Maximum Current (I_max)</span><span class="result-value">{Imax:.2f} µA</span></div>
                  <div class="result-row"><span class="result-label">Slope of Graph</span><span class="result-value">{slope:.4f}</span></div>
                  <div class="result-row"><span class="result-label">Intercept</span><span class="result-value">{intercept:.4f}</span></div>
                  <div class="result-row"><span class="result-label">Conclusion</span><span class="result-value" style="font-size:0.85rem;color:#00ff88;">Malus Law Verified ✓</span></div>
                </div>""", unsafe_allow_html=True)

        except ValueError:
            st.error("Please enter valid numeric values only.")

# =========================================================
# BAND GAP
# =========================================================

elif experiment == "Band Gap of Semiconductor":

    st.markdown("""
    <div class="section-card">
      <div class="section-title">💎 Band Gap of Semiconductor</div>
    </div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        temp_input    = st.text_input("Temperature t (°C)", placeholder="30, 35, 40 …")
    with col2:
        voltage_input = st.text_input("Voltage (V)", placeholder="3, 3, 3 …")
    with col3:
        current_input = st.text_input("Current I (mA)", placeholder="0.004, 0.006 …")

    if st.button("⚡ GENERATE BAND GAP GRAPH", key="bg"):
        try:
            temp    = [float(i.strip()) for i in temp_input.split(",") if i.strip()]
            voltage = [float(i.strip()) for i in voltage_input.split(",") if i.strip()]
            current = [float(i.strip()) for i in current_input.split(",") if i.strip()]

            if not (len(temp) == len(voltage) == len(current)):
                st.error("All inputs must have the same number of values.")
            else:
                T          = [t+273 for t in temp]
                resistance = [v/i for v,i in zip(voltage,current)]
                logR       = [float(np.log10(r)) for r in resistance]
                invT       = [1/t for t in T]

                df = pd.DataFrame({
                    "Temp (°C)": temp, "V (V)": voltage, "I (mA)": current,
                    "R = V/I (Ω)": [round(r,2) for r in resistance],
                    "log₁₀R":      [round(l,3) for l in logR],
                    "T (K)": T,
                    "1/T (K⁻¹)":  [round(i,6) for i in invT]
                })
                st.dataframe(df, use_container_width=True)

                fig, slope, intercept = animated_glow_plot(
                    invT, logR,
                    xlabel="1/T  (K⁻¹)", ylabel="log₁₀ R",
                    title="Band Gap — log₁₀R vs 1/T",
                    color_main='#ff6ec7',
                    color_fit='#00f5ff',
                    do_fit=True, fit_deg=1,
                    scatter_x=invT, scatter_y=logR,
                    scatter_color='#ffd700'
                )
                st.pyplot(fig)

                k  = 8.617e-5
                Eg = abs(2.3026 * 1000 * k * slope)

                st.markdown(f"""
                <div class="result-card">
                  <h3>📌 Final Results</h3>
                  <div class="result-row"><span class="result-label">Slope of Graph</span><span class="result-value">{slope:.4f}</span></div>
                  <div class="result-row"><span class="result-label">Intercept</span><span class="result-value">{intercept:.4f}</span></div>
                  <div class="result-row"><span class="result-label">Energy Band Gap (Eg)</span><span class="result-value">{Eg:.4f} eV</span></div>
                  <div class="result-row"><span class="result-label">Conclusion</span><span class="result-value" style="font-size:0.85rem;color:#00ff88;">log R vs 1/T is linear ✓</span></div>
                </div>""", unsafe_allow_html=True)

        except ValueError:
            st.error("Please enter valid numeric values only.")

# =========================================================
# GENERAL GRAPHS
# =========================================================

elif experiment == "General Graphs":

    st.markdown("""
    <div class="section-card">
      <div class="section-title">📊 Custom Graph Plotter</div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        x_input = st.text_input("X Values", placeholder="1, 2, 3, 4, 5")
        x_label = st.text_input("X-axis Label", placeholder="Time (s)")
    with col2:
        y_input = st.text_input("Y Values", placeholder="2, 4, 6, 8, 10")
        y_label = st.text_input("Y-axis Label", placeholder="Distance (m)")

    col3, col4 = st.columns(2)
    with col3:
        glow_color = st.selectbox("Curve Color", [
            "Cyan (#00f5ff)", "Green (#00ff88)", "Pink (#ff6ec7)",
            "Violet (#bf7fff)", "Gold (#ffd700)", "Orange (#ff8c00)"
        ])
    with col4:
        show_fit = st.selectbox("Show Best Fit Line?", ["Yes", "No"])

    color_map = {
        "Cyan (#00f5ff)":   "#00f5ff",
        "Green (#00ff88)":  "#00ff88",
        "Pink (#ff6ec7)":   "#ff6ec7",
        "Violet (#bf7fff)": "#bf7fff",
        "Gold (#ffd700)":   "#ffd700",
        "Orange (#ff8c00)": "#ff8c00",
    }

    if st.button("⚡ GENERATE GRAPH", key="gg"):
        try:
            x = [float(i.strip()) for i in x_input.split(",") if i.strip()]
            y = [float(i.strip()) for i in y_input.split(",") if i.strip()]

            if len(x) != len(y):
                st.error("X and Y must contain the same number of values.")
            else:
                df = pd.DataFrame({
                    x_label or "X": x,
                    y_label or "Y": y
                })
                st.dataframe(df, use_container_width=True)

                chosen_color = color_map[glow_color]
                fit_color = '#ff6ec7' if chosen_color != '#ff6ec7' else '#00f5ff'

                fig, slope, intercept = animated_glow_plot(
                    x, y,
                    xlabel=x_label or "X-axis",
                    ylabel=y_label or "Y-axis",
                    title=f"{y_label} vs {x_label}" if x_label and y_label else "Custom Graph",
                    color_main=chosen_color,
                    color_fit=fit_color,
                    do_fit=(show_fit == "Yes"), fit_deg=1
                )
                st.pyplot(fig)

                if show_fit == "Yes" and slope is not None:
                    st.markdown(f"""
                    <div class="result-card">
                      <h3>📌 Linear Fit Results</h3>
                      <div class="result-row"><span class="result-label">Slope</span><span class="result-value">{slope:.4f}</span></div>
                      <div class="result-row"><span class="result-label">Intercept</span><span class="result-value">{intercept:.4f}</span></div>
                    </div>""", unsafe_allow_html=True)

        except ValueError:
            st.error("Please enter valid numeric values only.")

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div style="text-align:center; padding: 2rem 0 1rem; opacity:0.35;">
  <p style="font-family:'Share Tech Mono',monospace; font-size:0.75rem; letter-spacing:0.2em; color:#4a8aaa;">
    PHYSICS LAB GRAPH STUDIO · BUILT WITH STREAMLIT
  </p>
</div>
""", unsafe_allow_html=True)