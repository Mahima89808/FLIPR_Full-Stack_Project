import streamlit as st
import os
from pathlib import Path
from app.database import (
    add_project,
    get_projects,
    add_client,
    get_clients,
    get_contacts,
    get_newsletter_emails,
    delete_project,
    update_project,
    update_client,
    delete_client,
)

BASE_DIR = Path(__file__).resolve().parent.parent
def show_admin_panel():
    st.set_page_config(page_title="Admin Panel", layout="wide")

    st.title("Admin Panel - Business Manager")

    st.sidebar.markdown("### Navigation")

    menu = st.sidebar.radio(
        "Navigation",
        [
             "View Projects",
            "Add Project",
            "Edit Project",
            "Delete Project",
            "View Clients",
            "Add Client",
            "Edit Client",
            "Delete Client",
            "Contact Form Responses",
            "Newsletter Subscribers",
        ],
    )
    # -------- Add Project --------
    if menu == "Add Project":
        st.header("Add New Project")

        with st.form("add_project_form"):
            image_path = st.text_input(
                "Project Image Path (relative, e.g. assets/house1.jpg)"
            )
            name = st.text_input("Project Name")
            description = st.text_area("Project Description", height=150)
            submitted = st.form_submit_button("Save Project")

            if submitted:
                if image_path and name and description:
                    add_project(image_path, name, description)
                    st.success("Project added successfully.")
                else:
                    st.error("Please fill all fields.")

    elif menu == "Edit Project":
        st.header("Edit Existing Project")
        projects = get_projects()

        if not projects:
            st.info("No projects to edit.")
        else:
        # dropdown to select which project to edit
            options = {f"{p['id']} - {p['name']}": p for p in projects}
            label = st.selectbox("Select a project", list(options.keys()))
            selected = options[label]

        # pre-fill current values
            with st.form("edit_project_form"):
                new_image_path = st.text_input(
                    "Project Image Path",
                    value=selected["image_path"] or "",
                )
                new_name = st.text_input("Project Name", value=selected["name"])
                new_description = st.text_area(
                    "Project Description",
                    value=selected["description"],
                    height=150,
                )
                save_changes = st.form_submit_button("Update Project")

                if save_changes:
                    if new_image_path and new_name and new_description:
                        update_project(
                            selected["id"],
                            new_image_path,
                            new_name,
                            new_description,
                        )
                        st.success("Project updated successfully. Go to 'View Projects' or the Landing Page to see changes.")
                    else:
                        st.error("Please fill all fields.")


    elif menu == "Delete Project":
        st.header("Delete Project")
        projects = get_projects()
        if not projects:
            st.info("No projects to delete.")
        else:
        # create a mapping of label -> id
            options = {f"{p['id']} - {p['name']}": p["id"] for p in projects}
            label = st.selectbox("Select a project to delete", list(options.keys()))
            if st.button("Delete Selected Project"):
                delete_project(options[label])
                st.success("Project deleted. Please refresh or change page to see update.")


    # -------- Add Client --------
    elif menu == "Add Client":
        st.header("Add New Client")

        with st.form("add_client_form"):
            image_path = st.text_input(
                "Client Image Path (relative, e.g. assets/client1.jpg)"
            )
            name = st.text_input("Client Name")
            designation = st.text_input("Client Designation (e.g. CEO)")
            description = st.text_area("Client Feedback / Description", height=150)
            submitted = st.form_submit_button("Save Client")

            if submitted:
                if image_path and name and designation and description:
                    add_client(image_path, name, description, designation)
                    st.success("Client added successfully.")
                else:
                    st.error("Please fill all fields.")

    elif menu == "Edit Client":
        st.header("Edit Client")

        clients = get_clients()
        if not clients:
            st.info("No clients to edit.")
        else:
            options = {f"{c['id']} - {c['name']}": c for c in clients}
            label = st.selectbox("Select a client", list(options.keys()))
            selected = options[label]

            with st.form("edit_client_form"):
                new_image_path = st.text_input(
                    "Client Image Path (e.g. assets/client1.jpg)",
                    value=selected["image_path"] or "",
                )
                new_name = st.text_input("Client Name", value=selected["name"])
                new_designation = st.text_input(
                    "Designation (e.g. CEO, Designer)",
                    value=selected["designation"],
                )
                new_description = st.text_area(
                    "Client Feedback / Description",
                    value=selected["description"],
                    height=150,
                )

                save_changes = st.form_submit_button("Update Client")

                if save_changes:
                    if new_image_path and new_name and new_designation and new_description:
                        update_client(
                            selected["id"],
                            new_image_path,
                            new_name,
                            new_description,
                            new_designation,
                        )
                        st.success("Client updated successfully.")
                    else:
                        st.error("Please fill all fields.")

    elif menu == "Delete Client":
        st.header("Delete Client")

        clients = get_clients()
        if not clients:
            st.info("No clients to delete.")
        else:
            options = {f"{c['id']} - {c['name']}": c["id"] for c in clients}
            label = st.selectbox("Select a client to delete", list(options.keys()))
            if st.button("Delete Selected Client"):
                delete_client(options[label])
                st.success("Client deleted. Refresh or change page to see the update.")


    # -------- View Projects --------
    elif menu == "View Projects":
        st.header("All Projects")
        projects = get_projects()

        if not projects:
            st.info("No projects found. Please add some projects first.")
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

            # right: details
                with cols[1]:
                    st.subheader(project["name"])
                    st.write(project["description"])
                    st.write(f"ID: {project['id']}")



    elif menu == "View Clients":
        st.header("All Clients")
        clients = get_clients()

        if not clients:
            st.info("No clients found. Please add some clients first.")
        else:
        # 2 client cards per row
            cols = st.columns(2)
            for idx, client in enumerate(clients):
                with cols[idx % 2]:
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

                # name + designation + feedback under image
                    st.markdown(
                        f"<p style='font-weight:600;margin-top:10px;'>{client['name']}</p>",
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                       f"<p style='color:#777;margin-bottom:5px;'>{client['designation']}</p>",
                       unsafe_allow_html=True,
                    )
                    st.write(client["description"])

                    st.markdown("</div>", unsafe_allow_html=True)


    # -------- Contact Form Responses --------
    elif menu == "Contact Form Responses":
        st.header("Contact Form Responses")
        contacts = get_contacts()

        if not contacts:
            st.info("No contact form submissions yet.")
        else:
            st.write(f"Total responses: {len(contacts)}")
            for contact in contacts:
                st.markdown("---")
                st.write(f"**Name:** {contact['full_name']}")
                st.write(f"**Email:** {contact['email']}")
                st.write(f"**Mobile:** {contact['mobile']}")
                st.write(f"**City:** {contact['city']}")
                st.write(f"**Submitted At:** {contact['created_at']}")

    # -------- Newsletter Subscribers --------
    elif menu == "Newsletter Subscribers":
        st.header("Newsletter Subscribers")
        emails = get_newsletter_emails()

        if not emails:
            st.info("No newsletter subscriptions yet.")
        else:
            st.write(f"Total subscribers: {len(emails)}")
            for row in emails:
                st.markdown("---")
                st.write(f"**Email:** {row['email']}")
                st.write(f"**Subscribed At:** {row['subscribed_at']}")
