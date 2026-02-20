import streamlit as st

# Page Config
st.set_page_config(page_title="MLB The Show 26 Trade Evaluator", layout="wide")

st.title("⚾ MLB The Show 26: Trade Evaluator")
st.markdown("---")

def calculate_value(ovr, age, pot, ctrl, sal):
    if ovr is None or age is None: 
        return 0
    
    pot_map = {"A": 1.5, "B": 1.2, "C": 1.0, "D": 0.8}
    
    # Core Logic
    base = (ovr - 50) * 10
    age_penalty = (a - 20) * 4 if a > 28 else 0
    control_bonus = (ctrl if ctrl is not None else 0) * 25
    salary_tax = (sal if sal is not None else 0) * 2
    
    return ((base * pot_map[pot]) - age_penalty + control_bonus) - salary_tax

# Layout: Two Columns
col1, col2 = st.columns(2)

with col1:
    st.header("📤 THEY GET")
    val1 = 0
    for i in range(3):
        with st.expander(f"Player {i+1}", expanded=True):
            # The 'label' is now the same for every box, but the 'key' stays unique
            o = st.number_input("Overall", 50, 99, value=None, placeholder="e.g. 85", key=f"o1_{i}")
            a = st.number_input("Age", 18, 45, value=None, placeholder="e.g. 24", key=f"a1_{i}")
            p = st.selectbox("Potential", ["A", "B", "C", "D"], index=None, placeholder="Select...", key=f"p1_{i}")
            p_final = p if p else "B"
            
            c = st.number_input("Years of Control", 0, 10, value=None, placeholder="0-10", key=f"c1_{i}")
            s = st.number_input("Salary ($M)", 0.0, 50.0, value=None, placeholder="e.g. 0.75", key=f"s1_{i}")
            
            val1 += calculate_value(o, a, p_final, c, s)

with col2:
    st.header("📥 YOU GET")
    val2 = 0
    for i in range(3):
        with st.expander(f"Player {i+1}", expanded=True):
            o = st.number_input("Overall", 50, 99, value=None, placeholder="e.g. 85", key=f"o2_{i}")
            a = st.number_input("Age", 18, 45, value=None, placeholder="e.g. 24", key=f"a2_{i}")
            p = st.selectbox("Potential", ["A", "B", "C", "D"], index=None, placeholder="Select...", key=f"p2_{i}")
            p_final = p if p else "B"
            
            c = st.number_input("Years of Control", 0, 10, value=None, placeholder="0-10", key=f"c2_{i}")
            s = st.number_input("Salary ($M)", 0.0, 50.0, value=None, placeholder="e.g. 0.75", key=f"s2_{i}")
            
            val2 += calculate_value(o, a, p_final, c, s)

# Result Section
st.markdown("---")
diff = val2 - val1

if val1 == 0 and val2 == 0:
    st.info("Waiting for player data... Enter an Overall and Age to begin.")
else:
    if abs(diff) < 30:
        st.success(f"⚖️ FAIR TRADE (Score: {int(diff)})")
    elif diff > 30:
        st.info(f"✅ WINNING TRADE (Score: {int(diff)})")
    else:
        st.error(f"❌ LOSING TRADE (Score: {int(diff)})")
