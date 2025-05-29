import streamlit as st

# ==========================
# 1. Neonatal BP Reference Table (26-44 weeks PMA, 50th/95th SBP/DBP)
# ==========================
neonate_bp_data = {
    26: {'SBP': (55, 72), 'DBP': (30, 50)},
    28: {'SBP': (60, 75), 'DBP': (38, 50)},
    30: {'SBP': (65, 80), 'DBP': (40, 55)},
    32: {'SBP': (68, 83), 'DBP': (40, 55)},
    34: {'SBP': (70, 85), 'DBP': (40, 55)},
    36: {'SBP': (72, 87), 'DBP': (50, 65)},
    38: {'SBP': (77, 92), 'DBP': (50, 65)},
    40: {'SBP': (80, 95), 'DBP': (50, 65)},
    42: {'SBP': (85, 98), 'DBP': (50, 65)},
    44: {'SBP': (88, 105), 'DBP': (50, 68)}
}

# ==========================
# 2. Infant BP Reference Table (1–12 months, by sex, 50th/95th SBP/DBP)
# ==========================
infant_bp_data = {
    1:  {'SBP': {'male': (84, 94),  'female': (82, 91)},  'DBP': {'male': (46, 55),  'female': (46, 56)}},
    3:  {'SBP': {'male': (90, 103), 'female': (89, 100)}, 'DBP': {'male': (54, 65),  'female': (54, 64)}},
    6:  {'SBP': {'male': (96, 105), 'female': (92, 102)}, 'DBP': {'male': (58, 68),  'female': (56, 66)}},
    12: {'SBP': {'male': (94, 103), 'female': (95, 104)}, 'DBP': {'male': (56, 65),  'female': (56, 66)}}
}

# ==========================
# 3. Children & Adolescents BP Data (1–17 years, by age, sex, height) -- Simplified
#    (For full AAP logic, a full table by height percentile is needed. Below is a demonstration structure.)
# ==========================
# This is a very simplified version for demonstration. Replace/expand for clinical use.
children_bp_data = {
    # age: (SBP_90, SBP_95, DBP_90, DBP_95) -- for average height
    'male': {
        1:  (94, 98, 49, 54),
        5:  (104, 108, 65, 69),
        10: (111, 115, 73, 77),
        13: (120, 130, 80, 80),  # >=13yo use adult cutoff
        17: (120, 130, 80, 80)
    },
    'female': {
        1:  (97, 100, 52, 56),
        5:  (103, 107, 66, 70),
        10: (112, 116, 74, 78),
        13: (120, 130, 80, 80),  # >=13yo use adult cutoff
        17: (120, 130, 80, 80)
    }
}
def interpolate_child_bp(age, sex):
    """Linear interpolation of child BP percentiles between available ages."""
    data = children_bp_data[sex]
    keys = sorted(data.keys())
    if age <= keys[0]:
        return data[keys[0]]
    if age >= keys[-1]:
        return data[keys[-1]]
    for i in range(len(keys)-1):
        if keys[i] <= age <= keys[i+1]:
            a0, a1 = keys[i], keys[i+1]
            break
    v0, v1 = data[a0], data[a1]
    frac = (age - a0) / (a1 - a0)
    return tuple(round(v0[j] + frac*(v1[j]-v0[j])) for j in range(4))

# ==========================
# 4. Utility Functions
# ==========================
def interpolate_bp(month, sex, bp_type):
    """Linear interpolate infant BP (by month, sex, SBP/DBP). Returns (50th, 95th) tuple."""
    keys = sorted(infant_bp_data.keys())
    if month <= keys[0]:
        return infant_bp_data[keys[0]][bp_type][sex]
    if month >= keys[-1]:
        return infant_bp_data[keys[-1]][bp_type][sex]
    for i in range(len(keys) - 1):
        if keys[i] <= month <= keys[i+1]:
            m0, m1 = keys[i], keys[i+1]
            break
    v0 = infant_bp_data[m0][bp_type][sex]
    v1 = infant_bp_data[m1][bp_type][sex]
    frac = (month - m0) / (m1 - m0)
    bp_50 = v0[0] + frac * (v1[0] - v0[0])
    bp_95 = v0[1] + frac * (v1[1] - v0[1])
    return (round(bp_50), round(bp_95))

def interpolate_neonate_bp(pma, bp_type):
    """Linear interpolate neonatal BP (PMA weeks, SBP/DBP). Returns (50th, 95th) tuple."""
    keys = sorted(neonate_bp_data.keys())
    if pma <= keys[0]:
        return neonate_bp_data[keys[0]][bp_type]
    if pma >= keys[-1]:
        return neonate_bp_data[keys[-1]][bp_type]
    for i in range(len(keys) - 1):
        if keys[i] <= pma <= keys[i+1]:
            k0, k1 = keys[i], keys[i+1]
            break
    v0 = neonate_bp_data[k0][bp_type]
    v1 = neonate_bp_data[k1][bp_type]
    frac = (pma - k0) / (k1 - k0)
    bp_50 = v0[0] + frac * (v1[0] - v0[0])
    bp_95 = v0[1] + frac * (v1[1] - v0[1])
    return (round(bp_50), round(bp_95))

# ==========================
# 5. Streamlit UI
# ==========================
st.set_page_config(page_title="Pediatric BP Percentile Chart", layout="centered")
st.title("Pediatric Blood Pressure Reference: Neonate, Infant, Child, Adolescent")

mode = st.selectbox(
    "Select Patient Group",
    ["Neonate (PMA weeks)", "Infant (months)", "Child/Adolescent (1–17 years)"]
)

if mode == "Neonate (PMA weeks)":
    pma = st.slider("Postmenstrual Age (weeks)", 26, 44, 38)
    st.markdown("**Neonate, after 2 weeks of age:** SBP/DBP 50th and 95th percentiles")
    sbp_50, sbp_95 = interpolate_neonate_bp(pma, 'SBP')
    dbp_50, dbp_95 = interpolate_neonate_bp(pma, 'DBP')
    st.markdown(
        f"- **SBP:** 50th percentile: {sbp_50} mmHg, 95th percentile: {sbp_95} mmHg\n"
        f"- **DBP:** 50th percentile: {dbp_50} mmHg, 95th percentile: {dbp_95} mmHg"
    )

elif mode == "Infant (months)":
    sex = st.selectbox("Sex", ["male", "female"])
    month = st.slider("Age (months)", 1, 12, 6)
    st.markdown("**Infant BP percentiles by month and sex:**")
    sbp_50, sbp_95 = interpolate_bp(month, sex, "SBP")
    dbp_50, dbp_95 = interpolate_bp(month, sex, "DBP")
    # Estimate 90th percentile as 80% between 50th and 95th
    sbp_90 = round(sbp_50 + 0.8 * (sbp_95 - sbp_50))
    dbp_90 = round(dbp_50 + 0.8 * (dbp_95 - dbp_50))
    sbp_stage2 = sbp_95 + 12
    dbp_stage2 = dbp_95 + 12

    st.markdown(f"### Reference for {month}-month-old {sex}:")
    st.markdown(f"- **50th percentile:** SBP {sbp_50} / DBP {dbp_50} mmHg")
    st.markdown(f"- **90th percentile (est):** SBP {sbp_90} / DBP {dbp_90} mmHg")
    st.markdown(f"- **95th percentile:** SBP {sbp_95} / DBP {dbp_95} mmHg")
    st.markdown(f"- **Stage 2 cutoff:** SBP {sbp_stage2} / DBP {dbp_stage2} mmHg (_95th + 12_)")

elif mode == "Child/Adolescent (1–17 years)":
    sex = st.selectbox("Sex", ["male", "female"])
    age = st.slider("Age (years)", 1, 17, 10)
    st.markdown("**Child/Adolescent BP percentiles:** (simplified; average height)")
    sbp_90, sbp_95, dbp_90, dbp_95 = interpolate_child_bp(age, sex)
    sbp_stage2 = sbp_95 + 12
    dbp_stage2 = dbp_95 + 12
    st.markdown(f"- **90th percentile:** SBP {sbp_90} / DBP {dbp_90} mmHg")
    st.markdown(f"- **95th percentile:** SBP {sbp_95} / DBP {dbp_95} mmHg")
    st.markdown(f"- **Stage 2 cutoff:** SBP {sbp_stage2} / DBP {dbp_stage2} mmHg (_95th + 12_)")
    if age >= 13:
        st.info("For adolescents ≥13 years, use adult thresholds: Elevated ≥120/80, Stage 1 ≥130/80, Stage 2 ≥140/90 mmHg (per AAP 2017).")

st.info("Data sources: Dionne JM et al. Arch Dis Child 2017 (neonate), ChildrensMercy/AAP PEARS 2017 (infant/child).")