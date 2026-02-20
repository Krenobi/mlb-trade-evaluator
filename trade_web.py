import streamlit as st

st.set_page_config(page_title="MLB The Show 26 Trade Evaluator", layout="wide")

st.title("⚾ MLB The Show 26: Financial Trade Evaluator")
st.markdown("---")

def calculate_value(ovr, age, pot, ctrl, sal, contract_type):
    if ovr is None or age is None: 
        return 0
    
    pot_map = {"A": 1.5, "B": 1.2, "C": 1.0, "D": 0.8}
    
    # Core Talent Value
    base = (ovr - 50) * 10
    age_penalty = (age - 20) * 4 if age > 28 else 0
    talent_score = (base * pot_map[pot]) - age_penalty
    
    # Financial Logic
    control_bonus = (ctrl if ctrl is not None else 0) * 25
    
    # Adjust Salary Tax based on Contract Type
    # Pre-Arb/Arb players are worth MORE because they are cheaper than their OVR suggests
    if contract_type == "Pre-Arb (Cheap)":
        actual_sal = 0.75
    elif contract_type == "Arbitration (Scaling)":
        actual_sal = (ovr - 70) * 0.5 # Estimate: higher OVR = higher Arb award
    else:
        actual_sal = sal if sal is not None else 0
        
    salary_tax = actual_sal * 2
    
    return talent_score + control_bonus - salary_tax

# Layout
col1, col2 = st.columns(2)

with col1:
    st.header("📤 THEY GET")
    val1 = 0
    for i in range(3):
        with st.expander(f"Player {i+1}", expanded=True):
            o = st.number_input("Overall", 50, 99, value=None, key=f"o1_{i}")
            a = st.number_input("Age", 18, 45, value=None, key=f"a1_{i}")
            p = st.selectbox("Potential", ["A", "B", "C", "D"], index=1, key=f"p1_{i}")
            c = st.number_input("Years of Control", 0, 10, value=None, key=f"c1_{i}")
            
            # New Financial Inputs
            type_1 = st.selectbox("Contract Type", ["Standard/Signed", "Pre-Arb (Cheap)", "Arbitration (Scaling)"], key=f"t1_{i}")
            s = None
            if type_1 == "Standard/Signed":
                s = st.number_input("Current Salary ($M)", 0.0, 50.0, value=None, key=f"s1_{i}")
            
            val1 += calculate_value(o, a, p, c, s, type_1)

with col2:
    st.header("📥 YOU GET")
    val2 = 0
    for i in range(3):
        with st.expander(f"Player {i+1}", expanded=True):
            o = st.number_input("Overall", 50, 99, value=None, key=f"o2_{i}")
            a = st.number_input("Age", 18, 45, value=None, key=f"a2_{i}")
            p = st.selectbox("Potential", ["A", "B", "C", "D"], index=1, key=f"p2_{i}")
            c = st.number_input("Years of Control", 0, 10, value=None, key=f"c2_{i}")
            
            type_2 = st.selectbox("Contract Type", ["Standard/Signed", "Pre-Arb (Cheap)", "Arbitration (Scaling)"], key=f"t2_{i}")
            s = None
            if type_2 == "Standard/Signed":
                s = st.number_input("Current Salary ($M)", 0.0, 50.0, value=None, key=f"s2_{i}")
            
            val2 += calculate_value(o, a, p, c, s, type_2)

st.markdown("---")
diff = val2 - val1
if val1 == 0 and val2 == 0:
    st.info("Input player data to see the trade verdict.")
else:
    if abs(diff) < 30: st.success(f"⚖️ FAIR TRADE (Score: {int(diff)})")
    elif diff > 30: st.info(f"✅ WINNING TRADE (Score: {int(diff)})")
    else: st.error(f"❌ LOSING TRADE (Score: {int(diff)})")
