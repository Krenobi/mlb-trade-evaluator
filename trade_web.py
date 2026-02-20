import streamlit as st

# Page Config for a professional look
st.set_page_config(page_title="MLB The Show 26 Trade Evaluator", layout="wide")

st.title("⚾ MLB The Show 26: Trade Evaluator")
st.markdown("---")

def calculate_value(ovr, age, pot, ctrl, sal):
    if not ovr: return 0
    pot_map = {"A": 1.5, "B": 1.2, "C": 1.0, "D": 0.8}
    
    # Core Logic
    base = (ovr - 50) * 10
    age_penalty = (age - 20) * 4 if age > 28 else 0
    control_bonus = ctrl * 25
    salary_tax = sal * 2
    
    return ((base * pot_map[pot]) - age_penalty + control_bonus) - salary_tax

# Layout: Two Columns
col1, col2 = st.columns(2)

with col1:
    st.header("📤 THEY GET")
    val1 = 0
    for i in range(3):
        with st.expander(f"Player {i+1}", expanded=True):
            o = st.number_input(f"OVR ##{i+1}", 50, 99, 75, key=f"o1_{i}")
            a = st.number_input(f"Age ##{i+1}", 18, 45, 25, key=f"a1_{i}")
            p = st.selectbox(f"Potential ##{i+1}", ["A", "B", "C", "D"], index=1, key=f"p1_{i}")
            c = st.number_input(f"Yrs Control ##{i+1}", 0, 10, 3, key=f"c1_{i}")
            s = st.number_input(f"Salary ($M) ##{i+1}", 0.0, 50.0, 1.0, key=f"s1_{i}")
            val1 += calculate_value(o, a, p, c, s)

with col2:
    st.header("📥 YOU GET")
    val2 = 0
    for i in range(3):
        with st.expander(f"Player {i+1}", expanded=True):
            o = st.number_input(f"OVR ##{i+2}", 50, 99, 75, key=f"o2_{i}")
            a = st.number_input(f"Age ##{i+2}", 18, 45, 25, key=f"a2_{i}")
            p = st.selectbox(f"Potential ##{i+2}", ["A", "B", "C", "D"], index=1, key=f"p2_{i}")
            c = st.number_input(f"Yrs Control ##{i+2}", 0, 10, 3, key=f"c2_{i}")
            s = st.number_input(f"Salary ($M) ##{i+2}", 0.0, 50.0, 1.0, key=f"s2_{i}")
            val2 += calculate_value(o, a, p, c, s)

# Result Section
st.markdown("---")
diff = val2 - val1

if abs(diff) < 30:
    st.success(f"⚖️ FAIR TRADE (Score: {int(diff)})")
elif diff > 30:
    st.info(f"✅ WINNING TRADE (Score: {int(diff)})")
else:
    st.error(f"❌ LOSING TRADE (Score: {int(diff)})")
            
