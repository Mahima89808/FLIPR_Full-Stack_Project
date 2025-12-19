import streamlit as st
import random
import string

from app.database import init_db
from app.landing_page import show_landing_page
from app.admin_panel import show_admin_panel


def main():
    init_db()

    st.sidebar.markdown("### Navigation")
    go_landing = st.sidebar.button("Landing Page")
    go_admin = st.sidebar.button("Admin Panel")

    if "page" not in st.session_state:
        st.session_state.page = "Landing"
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if go_landing:
        st.session_state.page = "Landing"
    if go_admin:
        st.session_state.page = "Admin"

    if st.session_state.page == "Landing":
        show_landing_page()
    else:
        show_admin_login_or_panel()


def show_admin_login_or_panel():
    # if already logged in, show admin panel
    if st.session_state.admin_logged_in:
        show_admin_panel()
        return

    st.title("Admin Login")

    with st.form("admin_login_form"):
        email = st.text_input("Admin Email")
        password = st.text_input("Password", type="password")

        # simple captcha: 4 random uppercase letters/digits
        if "captcha_code" not in st.session_state:
            st.session_state.captcha_code = "".join(
                random.choices(string.ascii_uppercase + string.digits, k=4)
            )

        st.write(f"Captcha: **{st.session_state.captcha_code}**")
        captcha_input = st.text_input("Enter Captcha Exactly")

        submitted = st.form_submit_button("Login")

        if submitted:
            # allow any email/password, only check captcha
            if captcha_input == st.session_state.captcha_code:
                st.session_state.admin_logged_in = True
                st.success("Login successful.")
                st.rerun()
            else:
                st.error("Incorrect captcha. Please try again.")
                st.session_state.captcha_code = "".join(
                    random.choices(string.ascii_uppercase + string.digits, k=4)
                )


if __name__ == "__main__":
    main()
