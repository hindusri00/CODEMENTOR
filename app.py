import streamlit as st
from pipeline import review
from rag import Retriever

st.set_page_config(page_title="Code Mentor", page_icon="🧑‍💻", layout="wide")


@st.cache_resource
def get_retriever():
    return Retriever()


st.title("🧑‍💻 Code Mentor")
st.caption("Understand your Java code - don't just copy a fix.")

with st.sidebar:
    st.header("Settings")
    hint_level = st.radio(
        "How much help?",
        [1, 2, 3],
        index=1,
        format_func={1: "1 - Nudge only", 2: "2 - Name the technique",
                     3: "3 - Show a sketch"}.get,
    )

uploaded = st.file_uploader("Upload a .java file", type=["java"])
default = uploaded.read().decode("utf-8") if uploaded else ""
code = st.text_area("...or paste Java code", value=default, height=300)

if st.button("🔍 Analyze", type="primary", disabled=not code.strip()):
    with st.spinner("Reading your code..."):
        try:
            r = review(code, get_retriever(), hint_level)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.stop()

    st.subheader("🔍 Code Analysis")
    st.markdown(f"**Problem:**\n\n{r.get('problem', '')}")
    st.markdown(f"**Why?**\n\n{r.get('why', '')}")
    st.markdown(f"**Suggestion:**\n\n{r.get('suggestion', '')}")
    if r.get("example"):
        st.code(r["example"], language="java")
    st.markdown("**Concepts involved:**")
    for c in r.get("concepts", []):
        st.markdown(f"→ {c}")
    if r.get("check_yourself"):
        st.info(f"🧠 Check yourself: {r['check_yourself']}")

    with st.expander("How I analyzed this (static facts + sources)"):
        st.text(r["_static"])
        st.write("Reference notes used:", ", ".join(r["_sources"]) or "none")
