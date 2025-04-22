import streamlit as st
import re
import math

st.set_page_config(page_title="Password Strength Checker", page_icon="🔐")
st.title("🔐 Ultimate Password Strength Checker")

#  Description
st.markdown("""
Check your password's strength in real time and get instant feedback to improve it.  
Criteria include:
- 🔢 Minimum Length (8+)
- 🔠 Mixed Case
- 🔣 Special Characters
- 🔟 Numbers
""")


def check_password_strength(password):
    score = 0
    feedback = []
    matched = {}

    matched["length"] = len(password) >= 8
    matched["upper"] = bool(re.search(r"[A-Z]", password))
    matched["lower"] = bool(re.search(r"[a-z]", password))
    matched["digit"] = bool(re.search(r"\d", password))
    matched["special"] = bool(re.search(r"[!@#$%^&*()_\-+=\[{\]};:'\",<.>/?\\|`~]", password))

    if matched["length"]: score += 1
    else: feedback.append("🔴 Use **at least 8 characters**.")

    if matched["upper"] and matched["lower"]: score += 1
    else: feedback.append("🔴 Use **both uppercase and lowercase** letters.")

    if matched["digit"]: score += 1
    else: feedback.append("🔴 Add **at least one number**.")

    if matched["special"]: score += 1
    else: feedback.append("🔴 Include **a special character (!@#$%^&*)**.")

    return score, feedback, matched

def estimate_entropy(password):
    charset_size = 0
    if re.search(r"[a-z]", password): charset_size += 26
    if re.search(r"[A-Z]", password): charset_size += 26
    if re.search(r"\d", password): charset_size += 10
    if re.search(r"[!@#$%^&*()_\-+=\[{\]};:'\",<.>/?\\|`~]", password): charset_size += 32
    return len(password) * math.log2(charset_size) if charset_size else 0

col1, col2 = st.columns([1, 4])
with col1:
    show = st.checkbox("👁", value=False)
with col2:
    password = st.text_input("🔑 Enter Password", type="default" if show else "password")

if password:
    score, feedback, matched = check_password_strength(password)
    entropy = estimate_entropy(password)

    st.markdown("---")
    st.subheader("📊 Strength Analysis")

    strength_levels = ["🔴 Very Weak", "🟠 Weak", "🟡 Moderate", "🟢 Strong"]
    st.markdown(f"### {strength_levels[min(score, 3)]} Password")
    st.progress(score / 4)

    st.markdown("#### 🔍 Criteria Match:")
    cols = st.columns(5)
    labels = ["Length", "Upper", "Lower", "Digit", "Special"]
    keys = ["length", "upper", "lower", "digit", "special"]
    for i, key in enumerate(keys):
        status = "✅" if matched.get(key) else "❌"
        cols[i].markdown(f"{status} **{labels[i]}**")

    st.markdown(f"🧠 **Entropy:** `{entropy:.2f}` bits")

    if feedback:
        st.warning("💡 **Suggestions to Improve:**")
        for tip in feedback:
            st.write("- " + tip)
    else:
        st.success("✅ Excellent! Your password is strong and meets all security standards.")
else:
    st.info("📝 Enter your password above to check its strength.")
