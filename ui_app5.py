import streamlit as st
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------
# Init theme state
# ---------------------
if "theme" not in st.session_state:
    st.session_state.theme = "dark"   # default = dark



# Try to import plotly, show friendly message if missing
try:
    import plotly.express as px
    import plotly.graph_objects as go
except Exception as e:
    st.error("Plotly is required for the enhanced visuals. Install with `pip install plotly` and restart the app.")
    st.stop()






# =====================
# Neon Dark Business Predictor UI
# =====================
BASE = Path(__file__).resolve().parent

MODEL_FILES = {
    'ratings': BASE / 'model_ratings.pkl',
    'sales': BASE / 'model_sales.pkl',
    'city': BASE / 'model_city.pkl',
    'success': BASE / 'model_success.pkl',
    'month': BASE / 'model_month.pkl',
    'enc_city': BASE / 'encoder_city.pkl',
    'enc_cuisine': BASE / 'encoder_cuisine.pkl'
}

@st.cache_resource
def load_pickle(path: Path):
    try:
        with open(path, 'rb') as f:
            return pickle.load(f)
    except Exception:
        return None

def safe_transform(le, value):
    try:
        return int(le.transform([value])[0])
    except Exception:
        try:
            return int(le.transform([le.classes_[0]])[0])
        except Exception:
            return 0


def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"


def fmt_inr(x):
    try:
        return f"₹{int(round(x)):,}"
    except:
        return str(x)

def star_html(rating):
    # Round rating to nearest 0.5
    r = round(rating * 2) / 2
    full = int(r // 1)
    half = 1 if (r - full) >= 0.5 else 0
    empty = 5 - full - half

    stars = "<span style='font-size:20px; letter-spacing:2px;'>"
    stars += "<span style='filter: drop-shadow(0 0 6px rgba(0,255,220,0.55)); color:#00ffd4;'>"

    stars += "★ " * full
    if half:
        stars += "✦ "  # neon half-star
    stars += "☆ " * empty

    stars += "</span></span>"
    return stars


# ---------------------
# Load models + encoders
# ---------------------
model_ratings = load_pickle(MODEL_FILES['ratings'])
model_sales = load_pickle(MODEL_FILES['sales'])
model_city = load_pickle(MODEL_FILES['city'])
model_success = load_pickle(MODEL_FILES['success'])
model_month = load_pickle(MODEL_FILES['month'])
le_city = load_pickle(MODEL_FILES['enc_city'])
le_cuisine = load_pickle(MODEL_FILES['enc_cuisine'])

st.set_page_config(page_title='Business Predictor (Neon)', layout='wide', initial_sidebar_state='expanded')


# ---------------------
# THEME CSS (V2 — fixed text + better colors)
# ---------------------
theme_css = f"""
<style>

:root {{
    --dark-bg: #0d0f11;
    --dark-card: #1A1C20;
    --dark-text: #ECECEC;

    --light-bg: #F6F6F6;
    --light-card: #FFFFFF;
    --light-text: #1A1A1A;
}}

[data-testid="stAppViewContainer"] {{
    background: {"var(--dark-bg)" if st.session_state.theme=="dark" else "var(--light-bg)"};
    color: {"var(--dark-text)" if st.session_state.theme=="dark" else "var(--light-text)"};
}}

[data-testid="stSidebar"] {{
    background: {"#141619" if st.session_state.theme=="dark" else "#FFFFFF"};
}}

.card {{
    background: {"var(--dark-card)" if st.session_state.theme=="dark" else "var(--light-card)"};
    padding: 20px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.08);
}}

h1,h2,h3,h4,h5,p,div,span {{
    color: {"var(--dark-text)" if st.session_state.theme=="dark" else "var(--light-text)"} !important;
}}

</style>
"""

st.markdown(theme_css, unsafe_allow_html=True)



# ---------------------
# Check models
# ---------------------
if any(v is None for v in [model_ratings, model_sales, model_city, model_success, model_month, le_city, le_cuisine]):
    st.error("One or more model/encoder files are missing. Place all required .pkl files next to this script.")
    st.stop()

# ---------------------
# Neon dark CSS tweaks
# ---------------------
NEON_CSS = """
<style>
body { background-color: #05060a; color: #e6f7ff; }
[data-testid="stSidebar"] { background: #07070a; color: #e6f7ff; }
h1, h2, h3, h4 { color: #e6f7ff; }
.neon-card { background: linear-gradient(90deg, rgba(10,12,18,0.9), rgba(12,14,20,0.85)); padding:14px; border-radius:10px; box-shadow: 0 8px 30px rgba(0,0,0,0.6); }
.small-muted { color: #9fb7c9; font-size:13px; }
</style>
"""
st.markdown(NEON_CSS, unsafe_allow_html=True)





# ---------------------
# Header
# ---------------------
col1, col2 = st.columns([0.12, 0.88])
with col1:
    st.markdown("""
    <svg width="60" height="60" viewBox="0 0 64 64" fill="none">
      <rect width="64" height="64" rx="12" fill="#001623"/>
      <path d="M18 42C18 36 24 34 28 34C32 34 38 36 38 42" stroke="#00ffd4" stroke-width="2"/>
      <path d="M26 18V30" stroke="#7c4dff" stroke-width="2"/>
    </svg>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("<h1 style='margin:0; color:#e6f7ff;'>🍽️ Business Predictor — Neon Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<div class='small-muted'>Interactive neon visuals • dark-mode optimized • hover for details</div>", unsafe_allow_html=True)

toggle_color = "#00E5C1" if st.session_state.theme == "dark" else "#FF914D"

st.markdown(f"""
<style>
.toggle-btn {{
    background-color: {toggle_color};
    padding: 10px 18px;
    border-radius: 8px;
    border: none;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    color: black;
}}
</style>
""", unsafe_allow_html=True)






# ---------------------
# Sidebar: inputs
# ---------------------
with st.sidebar.form("inputs"):
    st.header("Restaurant Details")

    user_name = st.text_input("Your Name", "Guest User")

    rest_name = st.text_input("Restaurant Name", "My Neon Bistro")
    city = st.selectbox("City", list(le_city.classes_))
    cuisine = st.selectbox("Cuisine", list(le_cuisine.classes_))
    year = st.slider("Year", 2020, 2025, 2024)
    month = st.slider("Month", 1, 12, 7)
    sales_qty = st.number_input("Expected monthly orders (qty)", min_value=0, value=20)
    sales_amount = st.number_input("Expected monthly sales (₹)", min_value=0, value=1500)
    rating_input = st.slider("Known rating (optional)", 1.0, 5.0, 4.0, 0.1)
    submitted = st.form_submit_button("Run")

if not submitted:
    st.info("Fill inputs and press Run.")
    st.stop()

# ---------------------
# Encode
# ---------------------
city_enc = safe_transform(le_city, city)
cuisine_enc = safe_transform(le_cuisine, cuisine)




# =====================================================
# USER INPUT SUMMARY SECTION
# =====================================================
def display_user_input(rest_name, city, cuisine, year, month, sales_qty, sales_amount, rating_input):
    st.write(f"Report generated for: **{user_name}**")


    st.markdown("""
    <div style="
        padding:15px; 
        border-radius:10px; 
        background:rgba(255,255,255,0.05); 
        border:1px solid rgba(255,255,255,0.15);
        margin-bottom:20px;
    ">
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"**🍽️ Restaurant:** {rest_name}")
        st.markdown(f"**🏙️ City:** {city}")
        st.markdown(f"**🍜 Cuisine:** {cuisine}")

    with col2:
        st.markdown(f"**📅 Year:** {year}")
        st.markdown(f"**🗓 Month:** {month}")
        st.markdown(f"**⭐ Given Rating:** {rating_input}")

    with col3:
        st.markdown(f"**📦 Expected Qty:** {sales_qty}")
        st.markdown(f"**💰 Expected Amount:** ₹{sales_amount:,}")

    st.markdown("</div>", unsafe_allow_html=True)




# ===========================
# MONTH INSIGHT KNOWLEDGE BASE
# ===========================
def month_reason(month, city=None, cuisine=None):

    month = int(month)
    city = city.lower() if city else ""
    cuisine = cuisine.lower() if cuisine else ""

    reasons = []

    # ==== 1. FESTIVAL REASONS ====
    festival_map = {
        10: "Durga Puja & Diwali shopping spike",
        11: "Diwali season + winter kickoff demand",
        9:  "Festive build-up demand before Puja",
        12: "Christmas & New Year outing spike",
        1:  "New Year celebrations",
        2:  "Valentine's season dine-outs"
    }
    if month in festival_map:
        reasons.append(festival_map[month])

    # ==== 2. SEASONAL REASONS ====
    summer = [4, 5, 6]
    winter = [11, 12, 1, 2]

    if month in summer:
        if "ice" in cuisine or "juice" in cuisine or "shake" in cuisine:
            reasons.append("High summer demand for cold beverages / ice-based items")
        else:
            reasons.append("Summer season brings increased footfall & outdoor eating")

    if month in winter:
        if "chinese" in cuisine:
            reasons.append("Winter boosts demand for hot Chinese dishes")
        if "north" in cuisine:
            reasons.append("North Indian cuisine performs well in colder months")
        reasons.append("Winter festival season improves overall food demand")

    # ==== 3. CITY-SPECIFIC REASONS ====
    if "kolkata" in city:
        if month in [9, 10]:
            reasons.append("Kolkata sees massive demand due to Durga Puja")
    if "delhi" in city:
        if month in winter:
            reasons.append("Delhi winters increase cravings for warm food & street food")
    if "chennai" in city and month in summer:
        reasons.append("Chennai heat increases sales of cold drinks & juices")
    if "bangalore" in city and month == 12:
        reasons.append("Holiday season + IT crowd outings boost December sales")

    # If nothing matched
    if not reasons:
        reasons.append("Stable demand patterns for this month")

    return " | ".join(reasons)


# ===========================================
# OVERALL SUMMARY GENERATOR
# ===========================================
def generate_summary(rest_name, rating, sales, city_df, best_month, reason_text):
    top_cities = city_df.head(3)
    city_list = ", ".join(top_cities["city"].tolist())

    return f"""
### 🧾 Overall Summary for **{rest_name}**

#### ⭐ Expected Rating  
Your restaurant is predicted to achieve a **rating of {rating:.2f} / 5**, indicating strong customer satisfaction potential.

#### 💰 Expected Monthly Sales  
Estimated monthly revenue: **{fmt_inr(sales)}**  
This is based on historical patterns and your cuisine/category performance.

#### 🏙️ Top 3 Recommended Cities  
Based on demand patterns, your restaurant would perform best in:  
**{city_list}**

These cities show high customer activity & strong alignment with your cuisine profile.

#### 📅 Best Month to Launch  
**Month {best_month}** is the strongest launch window.  
**Why?** → {reason_text}

Launching during this month provides the highest probability of gaining early traction, festival/season boosts, and maximizing visibility.

---

### 🎉 Final Recommendation  
If you plan to launch soon, choose **Month {best_month}** in **{top_cities['city'].iloc[0]}** for the best initial impact.  
This combination gives the strongest early-stage performance in both **sales** and **ratings**.
"""




# ---------------------
# Predict
# ---------------------
X_rating = pd.DataFrame([{
    'year': year, 'month': month, 'sales_qty': sales_qty, 'sales_amount': sales_amount,
    'City_encoded': city_enc, 'Cuisine_encoded': cuisine_enc
}])
pred_rating = model_ratings.predict(X_rating)[0]

X_sales = pd.DataFrame([{
    'year': year, 'month': month, 'sales_qty': sales_qty, 'Ratings': pred_rating,
    'City_encoded': city_enc, 'Cuisine_encoded': cuisine_enc
}])
pred_sales = model_sales.predict(X_sales)[0]

X_success = pd.DataFrame([{
    'Ratings': pred_rating, 'sales_qty': sales_qty, 'sales_amount': sales_amount,
    'City_encoded': city_enc, 'Cuisine_encoded': cuisine_enc, 'year': year, 'month': month
}])
success_prob = model_success.predict_proba(X_success)[0][1] * 100

X_city = pd.DataFrame([{
    'Cuisine_encoded': cuisine_enc, 'Ratings': pred_rating, 'sales_qty': sales_qty,
    'sales_amount': sales_amount, 'year': year, 'month': month
}])
city_probs = model_city.predict_proba(X_city)[0]
city_df = pd.DataFrame({"city": le_city.classes_, "prob": city_probs * 100}).sort_values("prob", ascending=False).reset_index(drop=True)

X_month = pd.DataFrame([{
    'Ratings': pred_rating, 'sales_qty': sales_qty, 'sales_amount': sales_amount, 'City_encoded': city_enc,
    'Cuisine_encoded': cuisine_enc, 'year': year
}])
month_probs = model_month.predict_proba(X_month)[0] * 100





# -------------------------
# Restaurant Name - Display
# -------------------------
st.markdown(f"""
<div style="
    margin-top:15px;
    padding:12px;
    border-radius:10px;
    background:rgba(255,255,255,0.07);
    backdrop-filter: blur(4px);
    border:1px solid rgba(255,255,255,0.15);
">
    <h2 style='margin:0; color:#00ffd5;'>
        🍽️ Predictions for <span style="color:#fff;">{rest_name}</span>
    </h2>
</div>
""", unsafe_allow_html=True)



# -------------------------
# Image Recogniser Link Card
# -------------------------
st.markdown("""
<div style="
    margin-top:20px;
    padding:18px;
    border-radius:12px;
    background: linear-gradient(135deg, #0A0F1F, #112233);
    border:1px solid rgba(0,255,200,0.25);
    box-shadow:0 0 18px rgba(0,255,200,0.25);
">
    <h3 style="color:#00ffd5; margin-top:0;">🔍 AI Food Image Recogniser</h3>
    <p style="color:#dcdcdc;">
        Analyse any food image using Machine Learning.<br>
        Detect dishes, classify cuisine, and more.
    </p>
    <a href="https://huggingface.co/spaces/Donyicoder2006/Food_Image_Recogniser"
       target="_blank"
       style="
            text-decoration:none;
            padding:10px 18px;
            background:#00ffd5;
            color:#000;
            border-radius:8px;
            font-weight:600;
        ">
        👉 Open Image Recogniser
    </a>
</div>
""", unsafe_allow_html=True)




st.markdown(f"### 👋 Hello, {user_name}! Here are your predictions:")



# ---------------------
# Metrics row
# ---------------------
st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
mcol1, mcol2, mcol3 = st.columns([1,1,1])
with mcol1:
    st.markdown("<div style='color:#00ffd4; font-weight:700;'>Predicted Rating</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:20px; color:#e6f7ff'>{pred_rating:.2f} / 5</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='margin-top:4px'>{star_html(pred_rating)}</div>", unsafe_allow_html=True)
with mcol2:
    st.markdown("<div style='color:#7c4dff; font-weight:700;'>Expected Monthly Sales</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:20px; color:#e6f7ff'>{fmt_inr(pred_sales)}</div>", unsafe_allow_html=True)
with mcol3:
    st.markdown("<div style='color:#ff0077; font-weight:700;'>Success Probability</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:20px; color:#e6f7ff'>{success_prob:.2f}%</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------
# Neon Gauge (plotly)
# ---------------------
gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=success_prob,
    number={'suffix':"%", 'font': {'color': '#e6f7ff', 'size': 20}},
    gauge={
        'axis': {'range':[0,100], 'tickcolor': '#cbefff'},
        'bar': {'color': '#00ffd4', 'thickness': 0.25},
        'bgcolor': "rgba(0,0,0,0)",
        'steps': [
            {'range':[0,40], 'color':'#ff4d4d'},
            {'range':[40,70], 'color':'#ffd11a'},
            {'range':[70,100], 'color':'#33ff99'}
        ],
        'threshold': {'line': {'color': "#ffffff"}, 'thickness': 0.8, 'value': success_prob}
    }
))
gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300, margin=dict(t=10,b=10,l=10,r=10))

# ---------------------
# Charts: City recommendations (neon bar) + Month probs (area + bar)
# ---------------------
chart_col1, chart_col2 = st.columns([1,1])

# City neon bar (top 6)
top_n = 6
city_plot_df = city_df.head(top_n).copy()
# color scale neon-ish
colors = ['#00ffd4','#7c4dff','#ff0099','#00b3ff','#7affb2','#ff8a00'][:len(city_plot_df)]
fig_city = px.bar(city_plot_df, x='city', y='prob', text='prob', template='plotly_dark',
                  color='city', color_discrete_sequence=colors)
fig_city.update_traces(texttemplate='%{text:.1f}%', textposition='outside', marker_line_width=0)
fig_city.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                       xaxis_tickangle=-20, yaxis=dict(range=[0, max(city_plot_df['prob'].max()*1.15, 10)]),
                       margin=dict(t=10,b=40,l=10,r=10))
# give neon glow effect via axis/ font color
fig_city.update_layout(xaxis=dict(tickfont=dict(color='#cdeaf6')), yaxis=dict(tickfont=dict(color='#cdeaf6')))

# Month area + bar
month_df = pd.DataFrame({'month': list(range(1,13)), 'prob': month_probs})
month_df['month_name'] = pd.to_datetime(month_df['month'], format='%m').dt.strftime('%b')
fig_month = go.Figure()
fig_month.add_trace(go.Scatter(x=month_df['month_name'], y=month_df['prob'],
                               mode='lines', fill='tozeroy', line=dict(color='#7c4dff', width=2),
                               hoverinfo='x+y', name='prob'))
fig_month.add_trace(go.Bar(x=month_df['month_name'], y=month_df['prob'], marker_color='#00ffd4', opacity=0.6, name='prob_bar'))
fig_month.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                        yaxis=dict(range=[0, max(20, month_df['prob'].max()*1.25)], tickfont=dict(color='#cdeaf6')),
                        xaxis=dict(tickfont=dict(color='#cdeaf6')), showlegend=False, margin=dict(t=10,b=30,l=10,r=10))

with chart_col1:
    st.markdown("### 🏙 Top City Recommendations", unsafe_allow_html=True)
    st.plotly_chart(fig_city, use_container_width=True)

with chart_col2:
    st.markdown("### 📅 Month Probabilities", unsafe_allow_html=True)
    st.plotly_chart(fig_month, use_container_width=True)

# show gauge to the right of metrics
st.markdown("### 🔮 Success Gauge", unsafe_allow_html=True)
st.plotly_chart(gauge, use_container_width=True)

# ---------------------
# Table and extra outputs
# ---------------------
st.markdown("### 📋 Top Cities (table)")
st.table(city_df.head(8).reset_index(drop=True))

st.markdown("---")
st.caption("Neon visual mode — tweak colors in the code if you'd like a different neon palette.")

# BEST MONTH INSIGHT TEXT
best_month = int(np.argmax(month_probs) + 1)
insight_text = month_reason(best_month, city=city, cuisine=cuisine)

st.markdown(f"""
### 🧠 Insight for Best Month  
**Month {best_month}** performs best for **{rest_name}**  
🔎 **Reason:** {insight_text}
""")

# SHOW USER INPUT SECTION
display_user_input(
    rest_name,
    city,
    cuisine,
    year,
    month,
    sales_qty,
    sales_amount,
    rating_input
)



# ===========================
# FINAL SUMMARY SECTION
# ===========================
summary = generate_summary(
    rest_name=rest_name,
    rating=pred_rating,
    sales=pred_sales,
    city_df=city_df,
    best_month=best_month,
    reason_text=insight_text
)

st.markdown("## 🧠 Final Business Summary")
st.markdown(summary)






# -------------------------
# Our Github link 
# -------------------------
st.markdown("""
<div style="
    margin-top:20px;
    padding:18px;
    border-radius:12px;
    background: linear-gradient(135deg, #0A0F1F, #112233);
    border:1px solid rgba(0,255,200,0.25);
    box-shadow:0 0 18px rgba(0,255,200,0.25);
">
    <h3 style="color:#00ffd5; margin-top:0;">🔍 Our GitHub Repository </h3>
    <p style="color:#dcdcdc;">
        Analyse any food image using Machine Learning.<br>
        Detect dishes, classify cuisine, and more.
    </p>
    <a href="https://github.com/Donyicoder2006/Project_works/invitations"
       target="_blank"
       style="
            text-decoration:none;
            padding:10px 18px;
            background:#00ffd5;
            color:#000;
            border-radius:8px;
            font-weight:600;
        ">
        👉 Click To Our Git Repo
    </a>
</div>
""", unsafe_allow_html=True)
