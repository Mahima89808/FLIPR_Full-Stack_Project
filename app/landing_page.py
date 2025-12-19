import streamlit as st
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

from app.database import (
    get_projects,
    get_clients,
    add_contact,
    add_newsletter_email,
)


def show_landing_page():
    st.set_page_config(page_title="Business Landing Page", layout="wide")

        # ----- Top Navigation Bar -----
    st.markdown(
        """
        <div style="background-color:#0d6efd;
                    padding:12px 40px;
                    border-radius:0;
                    color:white;
                    display:flex;
                    align-items:center;
                    gap:150px;">
            <span style="font-weight:700;font-size:18px;margin-right:40px;">FLIPR </span>
            <span>Home</span>
            <span>Services</span>
            <span>Projects</span>
            <span>Testimonials</span>
            <span>Contact</span>
            <span>Login/Signup</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")  # small spacing


    # ----- Hero / Header -----
    st.markdown(
        """
        <div style="background-color:#1f3b64;padding:40px;border-radius:10px;color:white;text-align:center;">
            <h1>Grow Your Real Estate Business</h1>
            <p>Manage projects, clients, and enquiries from a single full‑stack app.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    col_main, col_contact = st.columns([2, 1])

    # ----- Our Projects -----
    with col_main:
        st.subheader("Our Projects")
        projects = get_projects()

        if not projects:
            st.info("No projects added yet. Please add projects from the admin panel.")
        else:
           for project in projects:
            st.markdown("---")
            cols = st.columns([1, 3])

            # left: image
            with cols[0]:
                img_rel = project["image_path"] or ""
                img_path = BASE_DIR / img_rel
                if img_rel and img_path.exists():
                    st.image(str(img_path), width=250)
                else:
                    st.write("No image")

            # right: project details
            with cols[1]:
                st.markdown(f"**{project['name']}**")
                st.write(project["description"])
                st.button("Read More", key=f"proj_btn_{project['id']}")

        
        # ----- Happy Clients -----
    st.subheader("Happy Clients")
    clients = get_clients()

    if not clients:
        st.info("No clients added yet. Please add clients from the admin panel.")
    else:
    # 2 cards per row
        cols = st.columns(2)
        for idx, client in enumerate(clients):
            with cols[idx % 2]:
            # card container
                st.markdown(
                    """
                    <div style="border:1px solid #e0e0e0;
                                border-radius:10px;
                                padding:15px;
                                margin-bottom:20px;
                                box-shadow:0 2px 6px rgba(0,0,0,0.05);">
                    """,
                    unsafe_allow_html=True,
                )

            # image on top
                img_rel = client["image_path"] or ""
                img_path = BASE_DIR / img_rel
                if img_rel and img_path.exists():
                    st.image(str(img_path), width=200)
                else:
                    st.write("No image")

            # name and feedback below
                st.markdown(f"<p style='font-weight:600;margin-top:10px;'>{client['name']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:#777;margin-bottom:5px;'>{client['designation']}</p>", unsafe_allow_html=True)
                st.write(client["description"])

                st.markdown("</div>", unsafe_allow_html=True)



    # ----- Contact Form -----
    with col_contact:
        st.markdown(
            """
            <div style="background-color:#384a7c;
                        padding:25px 20px;
                        border-radius:10px;
                        color:white;
                        text-align:center;
                        margin-bottom:10px;">
                <h3 style="margin-bottom:5px;">Get a Free</h3>
                <h2 style="margin-top:0;">Consultation</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("contact_form"):
            st.markdown(
                "<p style='font-size:13px;color:#666;margin-bottom:5px;'>Full Name</p>",
                unsafe_allow_html=True,
            )
            full_name = st.text_input("", key="contact_name")

            st.markdown(
                "<p style='font-size:13px;color:#666;margin-bottom:5px;'>Email Address</p>",
                unsafe_allow_html=True,
            )
            email = st.text_input("", key="contact_email")

            st.markdown(
                "<p style='font-size:13px;color:#666;margin-bottom:5px;'>Mobile Number</p>",
                unsafe_allow_html=True,
            )
            mobile = st.text_input("", key="contact_mobile")

            st.markdown(
                "<p style='font-size:13px;color:#666;margin-bottom:5px;'>Area, City</p>",
                unsafe_allow_html=True,
            )
            city = st.text_input("", key="contact_city")

            submitted = st.form_submit_button(
                "Get Quick Quote",
                use_container_width=True,
            )

            if submitted:
            # simple validation
                if not (full_name and email and mobile and city):
                    st.error("Please fill all the fields.")
                elif "@" not in email or "." not in email:
                    st.error("Please enter a valid email address.")
                elif not mobile.isdigit() or len(mobile) < 8:
                    st.error("Please enter a valid mobile number.")
                else:
                    add_contact(full_name, email, mobile, city)
                    st.success("Thank you! Your details have been submitted.")

                    # Newsletter subscribe below contact form
        st.write("")  # small spacing
        st.markdown(
            "<p style='font-weight:600;margin-top:10px;'>Subscribe Us</p>",
            unsafe_allow_html=True,
        )
        with st.form("newsletter_form_side", clear_on_submit=True):
            c1, c2 = st.columns([3, 1])
            with c1:
                newsletter_email = st.text_input(
                    "Enter Email Address",
                    label_visibility="collapsed",
                )
            with c2:
                sub_clicked = st.form_submit_button("Subscribe")

            if sub_clicked:
                if not newsletter_email:
                    st.error("Please enter an email address.")
                elif "@" not in newsletter_email or "." not in newsletter_email:
                    st.error("Please enter a valid email address.")
                else:
                    add_newsletter_email(newsletter_email)
                    st.success("Subscribed successfully!")



    
    # ----- Footer -----
    st.write("---")
    st.markdown(
        """
        <div style="text-align:center; padding:15px 0; color:#aaaaaa; font-size:13px;">
            <p>© 2025 FLIPR Business Manager. All rights reserved.</p>
            <p>Contact: info@flipr-business.com | +91-98765-43210 | Indore, MP</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
