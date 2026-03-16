import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Reward Calculator", page_icon="📚", layout="wide")

st.title("📚 Reward Calculator")


def calculate_reward(points):
    if points < 0.5:
        return 0
    elif points <= 1:
        return 5000 + 15000 * (points - 0.5) / 0.5
    elif points <= 2:
        return 20000 + 10000 * (points - 1)
    elif points <= 2.4:
        return 30000 + 10000 * (points - 2) / 0.4
    elif points <= 4:
        return 40000 + 10000 * (points - 2.4) / 1.6
    elif points <= 10:
        return 50000 + 50000 * (points - 4) / 6
    else:
        return 100000


def format_number(num):
    return f"{num:,.0f}".replace(',', ' ')


# ── JOURNAL TABLE ────────────────────────────────────────────────────────────

st.header("📋 Recommended Journals by Average Score")

journals = [
    (5.3, "Journal of Materials Science & Technology", "", 14.3, "OA Only", "Elsevier", "No"),
    (3.4, "Acta Materialia", "", 9.3, "No", "Elsevier", "No"),
    (3.1, "CORROSION SCIENCE", 19, 8.5, "No", "Elsevier", "No"),
    (3.6, "npj Computational Materials", "", 11.9, "OA Only", "Nature", "No"),
    (3.3, "Materials Science and Engineering: A", 18, 7, "No", "Elsevier", "No"),
    (3.1, "Ceramics International", 33, 5.6, "No", "Elsevier", "No"),
    (3.0, "Applied Surface Science Advances - NOT RECOMMENDED, in ESCI index, not SCIE", "", 8.7, "OA Only", "Elsevier", "No"),
    (2.8, "Journal of Materials Research & Technology", "", 6.6, "OA Only", "Nature", "No"),
    (2.8, "Scientific reports (Nature portfolio) - NOT RECOMMENDED, BAD REPUTATION RECENTLY", "", 3.9, "OA Only", "Nature", "No"),
    (2.6, "Matter and Radiation at Extremes", "", 4.73, "No", "AIP", "No"),
    (2.4, "Journal of Alloys and Compounds", 23, 6.3, "No", "Elsevier", "No"),
    (2.4, "MATERIALS & DESIGN", 27, 7.9, "OA only", "Elsevier", "No"),
    (2.4, "Applied Surface Science", 16, 6.9, "No", "Elsevier", "No"),
    (2.2, "ACS Applied Materials & Interfaces", "", 8.2, "No", "Elsevier", "No"),
    (2.2, "Surface & Coatings Technology", 16, 6.1, "No", "Elsevier", "No"),
    (2.2, "Surfaces and Interfaces", 22, 6.3, "No", "Elsevier", "No"),
    (2.1, "Journal of Chemical Theory & Computation", "", 5.5, "No", "ACS", "No"),
    (2.1, "Machine Learning: Science and Technology", 26, 4.6, "No", "IOP", "No"),
    (2.1, "Chemistry of materials", "", 7, "No", "ACS", "No"),
    (1.9, "JOURNAL OF COMPUTATIONAL PHYSICS", 28, 3.8, "No", "Elsevier", "No"),
    (1.9, "Intermetallics", 24, 4.8, "No", "Elsevier", "No"),
    (1.8, "Journal of Chemical Information and Modeling", "", 5.3, "No", "ACS", "No"),
    (1.5, "Journal of Computational Science", "", 3.7, "No", "Elsevier", "No"),
    (1.7, "Computer Physics Communications", 38, 3.4, "No", "Elsevier", "No"),
    (1.4, "Materials Chemistry and Physics", 16, 4.7, "No", "Elsevier", "No"),
    (0.0, "Computational Condensed Matter - NOT RECOMMENDED, CURRENTLY in ESCI index, not SCIE", 16, 3.9, "NO", "Elsevier", "No"),
    (1.3, "Journal of Applied Crystallography", "", 2.8, "No", "Willey", "No"),
    (1.2, "Journal of Physical Chemistry C", "", 3.2, "No", "ACS", "No"),
    (1.0, "Computational Materials Science", 21, 3.3, "No", "Elsevier", "No"),
    (0.8, "Modelling and Simulation in Materials Science and Engineering", 25, 2.4, "No", "IOP", "No"),
    (0.8, "Molecular simulation", 13, 2, "No", "Taylor and Francis", "No"),
    (0.8, "CALPHAD-COMPUTER COUPLING OF PHASE DIAGRAMS AND THERMOCHEMISTRY", "", 1.9, "No", "Elsevier", "No"),
    (0.7, "NUCLEAR INSTRUMENTS & METHODS IN PHYSICS RESEARCH SECTION B-BEAM INTERACTIONS WITH MATERIALS AND ATOMS", 52, 1.3, "No", "Elsevier", "No"),
    (1.2, "Materials", "", 3.2, "No", "MDPI", "No"),
    (2.1, "Advanced Theory and Simulations", "", 2.9, "No", "Willey", "No"),
    (1.3, "Vacuum", "", 3.9, "No", "Elsevier", "No"),
    (9.3, "Reports on Progress in Physics", 4, 20.3, "No", "IOP", "No"),
]

df = pd.DataFrame(journals, columns=["Average Score", "Journal", "Acceptance Rate (%)", "IF2024", "OpenAccess", "Publisher", "From V3S"])

df['Acceptance Rate (%)'] = df['Acceptance Rate (%)'].replace('', 'Not available')
df['Publisher'] = df['Publisher'].replace('', 'Not available')
df['OpenAccess'] = df['OpenAccess'].replace('', 'Not available')
df['IF2024'] = df['IF2024'].apply(lambda x: 'Not available' if x == '' else x)
df['Expected Reward'] = df['Average Score'].apply(lambda x: format_number(calculate_reward(x)))

search = st.text_input("🔍 Search for a journal:", "")
if search:
    df_filtered = df[df['Journal'].str.contains(search, case=False, na=False)]
else:
    df_filtered = df


def build_html_table(df):
    header_cols = ["Average Score", "Journal", "Acceptance Rate (%)", "IF2024", "OpenAccess", "Publisher", "From V3S", "Expected Reward"]

    header_html = "".join(
        f'<th onclick="sortTable(this, {i})">{col} <span class="sort-icon">&#x21C5;</span></th>'
        for i, col in enumerate(header_cols)
    )

    rows_html = ""
    for _, row in df.iterrows():
        if row['From V3S'] == 'Yes':
            row_bg = '#ccffcc'
        elif 'NOT RECOMMENDED' in str(row['Journal']):
            row_bg = '#ffe6e6'
        else:
            row_bg = ''

        journal_text = str(row['Journal'])
        if 'NOT RECOMMENDED' in journal_text:
            parts = journal_text.split(' - NOT RECOMMENDED', 1)
            journal_cell = f'{parts[0]}<br><span class="not-rec">&#9888; NOT RECOMMENDED{parts[1] if len(parts) > 1 else ""}</span>'
        else:
            journal_cell = journal_text

        v3s_color = '#1a7a1a' if row['From V3S'] == 'Yes' else '#555'

        cells = (
            f'<td class="center bold">{row["Average Score"]}</td>'
            f'<td class="journal-name">{journal_cell}</td>'
            f'<td class="center">{row["Acceptance Rate (%)"]}</td>'
            f'<td class="center bold">{row["IF2024"]}</td>'
            f'<td class="center">{row["OpenAccess"]}</td>'
            f'<td class="center">{row["Publisher"]}</td>'
            f'<td class="center bold" style="color:{v3s_color}">{row["From V3S"]}</td>'
            f'<td class="right bold">{row["Expected Reward"]}</td>'
        )
        bg_attr = f' style="background-color:{row_bg};"' if row_bg else ''
        rows_html += f'<tr{bg_attr}>{cells}</tr>'

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 15px; background: transparent; }}

  .wrap {{
    overflow-x: auto;
    max-height: 620px;
    overflow-y: auto;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.15);
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
  }}

  thead tr {{
    background-color: #2c5f8a;
    color: white;
    position: sticky;
    top: 0;
    z-index: 10;
  }}

  th {{
    padding: 13px 14px;
    text-align: left;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    white-space: nowrap;
    cursor: pointer;
    user-select: none;
    border-bottom: 2px solid #1a3f5f;
  }}
  th:hover {{ background-color: #1e4a70; }}
  th.asc  .sort-icon,
  th.desc .sort-icon {{ color: #ffe066; font-weight: bold; }}
  .sort-icon {{ margin-left: 5px; font-size: 12px; opacity: 0.8; }}

  td {{
    padding: 11px 14px;
    border-bottom: 1px solid #dde3ea;
    vertical-align: middle;
    line-height: 1.45;
  }}
  tbody tr:hover {{ filter: brightness(0.96); cursor: default; }}
  tbody tr:nth-child(even):not([style]) {{ background-color: #f4f7fb; }}

  .center {{ text-align: center; }}
  .right  {{ text-align: right;  }}
  .bold   {{ font-weight: 700;   }}
  .journal-name {{ min-width: 280px; }}
  .not-rec {{ color: #cc0000; font-weight: 600; font-size: 13px; }}
</style>
</head>
<body>
<div class="wrap">
  <table id="jtable">
    <thead><tr>{header_html}</tr></thead>
    <tbody id="tbody">{rows_html}</tbody>
  </table>
</div>

<script>
var sortCol = -1;
var sortAsc = true;

function sortTable(th, col) {{
  var tbody = document.getElementById('tbody');
  var rows  = Array.from(tbody.querySelectorAll('tr'));

  if (sortCol === col) {{
    sortAsc = !sortAsc;
  }} else {{
    sortCol = col;
    sortAsc = true;
  }}

  document.querySelectorAll('th').forEach(function(h) {{
    h.classList.remove('asc', 'desc');
    h.querySelector('.sort-icon').innerHTML = '&#x21C5;';
  }});
  th.classList.add(sortAsc ? 'asc' : 'desc');
  th.querySelector('.sort-icon').textContent = sortAsc ? '\u25B2' : '\u25BC';

  rows.sort(function(a, b) {{
    var aVal = a.querySelectorAll('td')[col].innerText.trim();
    var bVal = b.querySelectorAll('td')[col].innerText.trim();
    var aNum = parseFloat(aVal.replace(/[\s\u00a0]/g, '').replace(',', '.'));
    var bNum = parseFloat(bVal.replace(/[\s\u00a0]/g, '').replace(',', '.'));
    var cmp;
    if (!isNaN(aNum) && !isNaN(bNum)) {{
      cmp = aNum - bNum;
    }} else {{
      cmp = aVal.localeCompare(bVal);
    }}
    return sortAsc ? cmp : -cmp;
  }});

  rows.forEach(function(r) {{ tbody.appendChild(r); }});
}}
</script>
</body>
</html>"""


components.html(build_html_table(df_filtered), height=680, scrolling=False)

st.markdown("---")

# ── REWARD CALCULATOR ────────────────────────────────────────────────────────

st.header("🧮 Reward Calculator")

col1, col2 = st.columns([1, 1])

with col1:
    points = st.number_input(
        "Enter publication points (0.5 - 10.0):",
        min_value=0.5,
        max_value=10.0,
        value=1.0,
        step=0.1,
        format="%.1f"
    )

    reward = calculate_reward(points)

    st.markdown("---")
    st.subheader("Your Reward:")
    st.markdown(f"### **{format_number(reward)}**")
    st.markdown(f"*For {points} points*")

    st.markdown("---")
    st.subheader("Reward Scale:")
    st.markdown("""
    - **0.5 points** → 5 000
    - **1.0 points** → 20 000
    - **2.0 points** → 30 000
    - **2.4 points** → 40 000
    - **4.0 points** → 50 000
    - **10.0 points** → 100 000
    """)

with col2:
    st.header("Reward Curve Visualization")

    point_range = np.linspace(0.5, 10, 100)
    rewards = [calculate_reward(p) for p in point_range]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=point_range,
        y=rewards,
        mode='lines',
        name='Reward Curve',
        line=dict(color='#1f77b4', width=3)
    ))

    fig.add_trace(go.Scatter(
        x=[points],
        y=[reward],
        mode='markers',
        name='Your Point',
        marker=dict(color='red', size=15, symbol='star')
    ))

    milestones = [0.5, 1, 2, 2.4, 4, 10]
    milestone_rewards = [calculate_reward(m) for m in milestones]
    fig.add_trace(go.Scatter(
        x=milestones,
        y=milestone_rewards,
        mode='markers',
        name='Milestones',
        marker=dict(color='green', size=10)
    ))

    fig.update_layout(
        xaxis_title="Publication Points",
        yaxis_title="Reward",
        hovermode='x unified',
        height=400,
        font=dict(size=16, color='black'),
        xaxis=dict(
            title=dict(font=dict(size=18, color='black')),
            tickfont=dict(size=14, color='black')
        ),
        yaxis=dict(
            title=dict(font=dict(size=18, color='black')),
            tickfont=dict(size=14, color='black')
        ),
        hoverlabel=dict(
            font_size=16,
            font_color='black'
        ),
        legend=dict(
            font=dict(size=14, color='black')
        )
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("💡 Note: Rewards are calculated using a piecewise linear function that increases progressively with publication points.")
