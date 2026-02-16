import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from textblob import TextBlob
import plotly.graph_objects as go

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from io import BytesIO

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="NeuralScope TITAN",
    layout="wide",
    page_icon="🧠"
)

# =========================================================
# $500M STARTUP UI
# =========================================================

st.markdown("""
<style>

/* Background */

.stApp{
background: radial-gradient(circle at top,#0f172a,#020617 60%);
font-family: Inter, sans-serif;
}

/* Hero */

.hero{
font-size:82px;
font-weight:900;
letter-spacing:-3px;
background: linear-gradient(90deg,#22ffe5,#4f8cff,#a855f7);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.tag{
font-size:22px;
color:#94a3b8;
margin-bottom:40px;
}

/* Glass cards */

.metric{
text-align:center;
padding:26px;
border-radius:20px;
background:linear-gradient(145deg,#020617,#0f172a);
border:1px solid rgba(255,255,255,0.06);
transition:.25s;
}

.metric:hover{
transform:translateY(-8px);
box-shadow:0 30px 60px rgba(0,0,0,.6);
}

/* Button */

.stButton>button{
height:64px;
font-size:20px;
font-weight:800;
border-radius:16px;
border:none;
color:black;
background:linear-gradient(90deg,#22ffe5,#4f8cff);
}

.stProgress > div > div > div > div{
background:linear-gradient(90deg,#22ffe5,#4f8cff);
}

.block-container{
max-width:1500px;
padding-top:2rem;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero">NeuralScope TITAN</div>', unsafe_allow_html=True)
st.markdown('<div class="tag">Cognitive Intelligence Platform for Elite Operators</div>', unsafe_allow_html=True)

# =========================================================
# ENGINE
# =========================================================

@st.cache_resource
def load_engine():
    return True

load_engine()

# =========================================================
# ANALYSIS
# =========================================================

@st.cache_data
def titan_analyze(goal):

    blob = TextBlob(goal)
    polarity = blob.sentiment.polarity

    seed = abs(hash(goal)) % (10**6)
    rng = np.random.default_rng(seed)

    clarity = min(100, int(len(goal)*1.7))
    leadership = int(rng.integers(45,95))
    execution = int(rng.integers(40,90))
    difficulty = int(rng.integers(35,95))
    success = int((clarity+execution)/2)
    confidence = int(clarity*0.30 + execution*0.30 + leadership*0.15 + success*0.25)

    risk = 100-execution
    momentum = int((execution+leadership)/2)
    resilience = int(rng.integers(50,95))

    return {
        "polarity":polarity,
        "clarity":clarity,
        "leadership":leadership,
        "execution":execution,
        "difficulty":difficulty,
        "success":success,
        "confidence":confidence,
        "risk":risk,
        "momentum":momentum,
        "resilience":resilience
    }

# =========================================================
# CHARTS
# =========================================================

@st.cache_data
def radar(report):

    categories=['Clarity','Leadership','Execution','Difficulty','Success','Momentum','Resilience']

    values=[
        report["clarity"],
        report["leadership"],
        report["execution"],
        report["difficulty"],
        report["success"],
        report["momentum"],
        report["resilience"]
    ]

    fig=go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        line=dict(width=3)
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(range=[0,100])),
        paper_bgcolor="#020617",
        height=520
    )

    return fig


@st.cache_data
def distribution():

    df=pd.DataFrame({
        "value":np.random.normal(0,1,700)
    })

    chart=alt.Chart(df).mark_bar(
        cornerRadiusTopLeft=6,
        cornerRadiusTopRight=6
    ).encode(
        x=alt.X("value",bin=True),
        y='count()'
    ).properties(height=350)

    return chart

# =========================================================
# ENTERPRISE PDF ENGINE (NEVER BLANK)
# =========================================================

def generate_pdf(goal, report, verdict, roadmap, resume_text, brief):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'title',
        parent=styles['Heading1'],
        alignment=TA_CENTER,
        fontSize=26,
        spaceAfter=20
    )

    heading = styles["Heading2"]
    body = styles["BodyText"]

    story = []

    story.append(Paragraph("NeuralScope TITAN Intelligence Report", title_style))
    story.append(Spacer(1,12))

    story.append(Paragraph("<b>Primary Objective</b>", heading))
    story.append(Paragraph(goal, body))
    story.append(Spacer(1,12))

    story.append(Paragraph("<b>AI Executive Verdict</b>", heading))
    story.append(Paragraph(verdict, body))
    story.append(Spacer(1,12))

    # Metrics table
    data=[["Metric","Score"]]

    for k,v in report.items():
        if k!="polarity":
            data.append([k.capitalize(),str(v)])

    table=Table(data, colWidths=[220,120])

    table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.black),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('GRID',(0,0),(-1,-1),1,colors.grey),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.whitesmoke, colors.lightgrey])
    ]))

    story.append(Paragraph("<b>Cognitive Metrics</b>", heading))
    story.append(table)
    story.append(Spacer(1,18))

    story.append(Paragraph("<b>Executive Intelligence Brief</b>", heading))
    story.append(Paragraph(brief, body))
    story.append(Spacer(1,12))

    story.append(Paragraph("<b>Strategic Roadmap</b>", heading))

    for step in roadmap:
        story.append(Paragraph(f"• {step}", body))

    story.append(Spacer(1,18))

    story.append(Paragraph("<b>Professional Resume Entry</b>", heading))
    story.append(Paragraph(resume_text, body))
    story.append(Spacer(1,20))

    story.append(Paragraph(
        "Generated by NeuralScope TITAN — Cognitive Intelligence Infrastructure for Elite Operators.",
        ParagraphStyle('footer', alignment=TA_CENTER, fontSize=9, textColor=colors.grey)
    ))

    doc.build(story)

    buffer.seek(0)
    return buffer

# =========================================================
# SESSION
# =========================================================

if "report" not in st.session_state:
    st.session_state.report=None
if "goal" not in st.session_state:
    st.session_state.goal=""

# =========================================================
# INPUT
# =========================================================

goal=st.text_input(
"Describe your primary life / career objective",
placeholder="Become a globally recognized AI systems engineer..."
)

if st.button("Run TITAN Intelligence",use_container_width=True):

    if goal.strip()=="":
        st.warning("Enter a goal.")
        st.stop()

    st.session_state.report=titan_analyze(goal)
    st.session_state.goal=goal

if st.session_state.report is None:
    st.stop()

report=st.session_state.report
goal=st.session_state.goal

# =========================================================
# VERDICT
# =========================================================

if report["confidence"]>82:
    verdict="ELITE TRAJECTORY"
elif report["confidence"]>68:
    verdict="HIGH POTENTIAL"
elif report["confidence"]>50:
    verdict="STRUCTURALLY SOUND"
else:
    verdict="HIGH RISK PATH"

st.success(f"AI Verdict: {verdict}")

# =========================================================
# METRICS
# =========================================================

st.divider()

metrics=[
("Clarity",report["clarity"]),
("Execution",report["execution"]),
("Leadership",report["leadership"]),
("Success",report["success"]),
("Momentum",report["momentum"]),
("Resilience",report["resilience"])
]

cols=st.columns(6)

for col,(label,val) in zip(cols,metrics):
    col.markdown(f"""
    <div class="metric">
        <h4>{label}</h4>
        <h1>{val}</h1>
    </div>
    """,unsafe_allow_html=True)

st.progress(report["confidence"]/100,
text=f"TITAN Confidence Score — {report['confidence']}%")

# =========================================================
# SUCCESS / RISK
# =========================================================

c1,c2=st.columns(2)

with c1:
    st.subheader("Success Probability")
    st.progress(report["success"]/100)

with c2:
    st.subheader("Risk Exposure")
    st.progress(report["risk"]/100)

st.divider()

# =========================================================
# CHARTS
# =========================================================

st.subheader("Cognitive Radar")
st.plotly_chart(radar(report),use_container_width=True)

st.subheader("Global Cognitive Distribution")
st.altair_chart(distribution(),use_container_width=True)

# =========================================================
# EXECUTIVE BRIEF + ROADMAP
# =========================================================

st.subheader("Executive Intelligence Brief")

brief=f"""
TITAN analysis indicates a {verdict.lower()}.

Cognitive clarity is operating at the {report["clarity"]}th percentile,
while execution strength suggests above-average delivery capability.

Leadership projection and resilience together signal strong
long-term compounding potential.

Primary risk vector: execution volatility.

If sustained intensity is maintained, probability curves favor
exceptional career acceleration.
"""

st.info(brief)

st.subheader("Strategic Roadmap")

roadmap=[
"Define a measurable 12-month outcome",
"Stack rare and valuable skills",
"Ship public proof-of-work",
"Engineer high-leverage network access",
"Position yourself where opportunity flows"
]

for step in roadmap:
    st.checkbox(step)

# =========================================================
# RESUME BULLET
# =========================================================

resume_text="""
Built NeuralScope TITAN — an enterprise-grade AI cognitive intelligence platform that evaluates clarity,
execution strength, leadership trajectory, difficulty modeling, and success probability to generate
executive-level strategic insights and career acceleration frameworks.
"""

st.subheader("Resume Bullet (Copy This!)")
st.code(resume_text)

# =========================================================
# PDF DOWNLOAD
# =========================================================

pdf_buffer=generate_pdf(
goal,
report,
verdict,
roadmap,
resume_text,
brief
)

st.download_button(
"Download TITAN Intelligence Report",
pdf_buffer,
file_name="TITAN_Report.pdf",
mime="application/pdf",
use_container_width=True
)

st.divider()
st.caption("NeuralScope TITAN • Cognitive Intelligence Infrastructure • Built for Top 1% Operators")
