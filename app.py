import streamlit as st
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


col1, col2 = st.columns([1, 1])

with col1:
    st.header("Calculate Your Reward")

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
st.header("📋 Recommended Journals by Average Score")


journals = [
    (6.1, "Journal of Materials Science & Technology", "", 14.3, "OA Only", "Elsevier"),
    (4.0, "Acta Materialia", "", 9.3, "No", "Elsevier"),
    (3.6, "CORROSION SCIENCE", 19, 8.5, "No", "Elsevier"),
    (3.6, "npj Computational Materials", "", 11.9, "OA Only", "Nature"),
    (3.3, "Materials Science and Engineering: A", 18, 7, "No", "Elsevier"),
    (3.1, "Ceramics International", 33, 5.6, "No", "Elsevier"),
    (3.0, "Applied Surface Science Advances", "", 8.7, "OA Only", "Elsevier"),
    (2.8, "Journal of Materials Research & Technology", "", 6.6, "OA Only", "Nature"),
    (2.8, "Scientific reports (Nature portfolio) - NOT RECOMMENDED, BAD REPUTATION RECENTLY", "", 3.9, "OA Only",
     "Nature"),
    (2.6, "Matter and Radiation at Extremes", "", 4.73, "No", "AIP"),
    (2.4, "Journal of Alloys and Compounds", 23, 6.3, "No", "Elsevier"),
    (2.4, "MATERIALS & DESIGN", 27, 7.9, "OA only", "Elsevier"),
    (2.4, "Applied Surface Science", 16, 6.9, "No", "Elsevier"),
    (2.2, "ACS Applied Materials & Interfaces", "", 8.2, "No", "Elsevier"),
    (2.2, "Surface & Coatings Technology", 16, 6.1, "No", "Elsevier"),
    (2.2, "Surfaces and Interfaces", 22, 6.3, "No", "Elsevier"),
    (2.1, "Journal of Chemical Theory & Computation", "", 5.5, "No", "ACS"),
    (2.1, "Machine Learning: Science and Technology", 26, 4.6, "No", "IOP"),
    (2.1, "Chemistry of materials", "", 7, "No", "ACS"),
    (1.9, "JOURNAL OF COMPUTATIONAL PHYSICS", 28, 3.8, "No", "Elsevier"),
    (1.9, "Intermetallics", 24, 4.8, "No", "Elsevier"),
    (1.8, "Journal of Chemical Information and Modeling", "", 5.3, "No", "ACS"),
    (1.8, "Journal of Computational Science", "", 3.7, "No", "Elsevier"),
    (1.7, "Computer Physics Communications", 38, 3.4, "No", "Elsevier"),
    (1.4, "Materials Chemistry and Physics", 16, 4.7, "No", "Elsevier"),
    (0.0, "Computational Condensed Matter - NOT RECOMMENDED, CURRENTLY in ESCI index, not SCIE", 16, 3.9, "NO", "Elsevier"),
    (1.3, "Journal of Applied Crystallography", "", 2.8, "No", "Willey"),
    (1.2, "Journal of Physical Chemistry C", "", 3.2, "No", "ACS"),
    (1.0, "Computational Materials Science", 21, 3.3, "No", "Elsevier"),
    (0.8, "Modelling and Simulation in Materials Science and Engineering", 25, 2.4, "No", "IOP"),
    (0.8, "Molecular simulation", 13, 2, "No", "Taylor and Francis"),
    (0.8, "CALPHAD-COMPUTER COUPLING OF PHASE DIAGRAMS AND THERMOCHEMISTRY", "", 1.9, "No", "Elsevier"),
    (0.7, "NUCLEAR INSTRUMENTS & METHODS IN PHYSICS RESEARCH SECTION B-BEAM INTERACTIONS WITH MATERIALS AND ATOMS", 52,
     1.3, "No", "Elsevier"),
    (9.3, "Reports on Progress in Physics", 4,
         20.3, "No", "IOP"),
]

df = pd.DataFrame(journals,
                  columns=["Average Score", "Journal", "Acceptance Rate (%)", "IF2024", "OpenAccess", "Publisher"])

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

st.dataframe(
    df_filtered.style.apply(
        lambda x: ['background-color: #ffe6e6' if 'NOT RECOMMENDED' in str(v) else '' for v in x],
        subset=['Journal']
    ),
    use_container_width=True,
    height=600
)

st.markdown("---")
st.caption(
    "💡 Note: Rewards are calculated using a piecewise linear function that increases progressively with publication points.")
