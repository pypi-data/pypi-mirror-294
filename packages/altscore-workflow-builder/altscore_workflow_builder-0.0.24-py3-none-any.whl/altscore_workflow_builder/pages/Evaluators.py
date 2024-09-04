import streamlit as st
from altscore_workflow_builder.utils import hide_deploy_button

hide_deploy_button()
st.title("Evaluators")


@st.cache_resource
def altscore_login():
    from altscore import AltScore
    from decouple import config
    altscore = AltScore(
        client_id=config("ALTSCORE_CLIENT_ID"),
        client_secret=config("ALTSCORE_CLIENT_SECRET"),
        environment=config("ENVIRONMENT")
    )
    return altscore


altscore = altscore_login()

evaluators = altscore.borrower_central.evaluators.retrieve_all()

st.selectbox("Evaluator", [None] + list(sorted([e.data.label for e in evaluators])))
