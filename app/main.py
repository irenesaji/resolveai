
import io
import uuid

import streamlit as st
import pandas as pd
from pypdf import PdfReader

from database.db import (
    initialize_database,
    create_ticket,
    get_all_tickets,
    get_ticket_by_id,
    update_ticket_analysis,
    update_response_review,
    update_ticket_status
)

from app.services.ticket_analyzer import analyze_ticket

from app.services.knowledge_base import (
    add_document,
    search_knowledge_base,
    get_knowledge_count
)


# --------------------------------------------------
# APPLICATION INITIALIZATION
# --------------------------------------------------

st.set_page_config(
    page_title="ResolveAI",
    page_icon="🤖",
    layout="wide"
)

initialize_database()


def load_tickets():
    return get_all_tickets()


tickets = load_tickets()


# --------------------------------------------------
# APPLICATION HEADER
# --------------------------------------------------

st.title("🤖 ResolveAI")

st.subheader(
    "Intelligent Customer Support & Operations Copilot"
)

st.write(
    "An AI-powered platform that helps support teams "
    "understand, prioritize and resolve customer queries."
)

st.divider()


# --------------------------------------------------
# SHOW SUCCESS MESSAGES AFTER RERUNS
# --------------------------------------------------

if st.session_state.get("last_submitted_ticket"):

    ticket_id = st.session_state.pop("last_submitted_ticket")

    st.success(
        f"Ticket submitted successfully! Ticket ID: {ticket_id}"
    )


if st.session_state.get("last_analyzed_ticket"):

    ticket_id = st.session_state.pop("last_analyzed_ticket")

    st.success(
        f"AI analysis completed for {ticket_id}"
    )


if st.session_state.get("last_resolved_ticket"):

    ticket_id = st.session_state.pop("last_resolved_ticket")

    st.success(
        f"Ticket {ticket_id} marked as resolved."
    )


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

page = st.sidebar.selectbox(
    "Navigation",
    [
        "Dashboard",
        "Submit Customer Ticket",
        "AI Ticket Analysis",
        "Knowledge Base",
        "Ticket History"
    ]
)


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

total_tickets = len(tickets)

open_tickets = sum(
    1 for ticket in tickets if ticket[8] == "Open"
)

resolved_tickets = sum(
    1 for ticket in tickets if ticket[8] == "Resolved"
)

high_priority = sum(
    1 for ticket in tickets if ticket[7] == "High"
)


if page == "Dashboard":

    st.header("Support Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Tickets", total_tickets)
    col2.metric("Open Tickets", open_tickets)
    col3.metric("Resolved Tickets", resolved_tickets)
    col4.metric("High Priority", high_priority)

    st.divider()

    st.subheader("Ticket Analytics")

    if tickets:

        dataframe = pd.DataFrame(
            tickets,
            columns=[
                "ID",
                "Ticket ID",
                "Customer",
                "Email",
                "Issue",
                "Category",
                "Sentiment",
                "Priority",
                "Status",
                "AI Response",
                "Created At",
                "Response Review"
            ]
        )

        st.subheader("Tickets by Category")

        category_counts = (
            dataframe["Category"]
            .value_counts()
            .rename_axis("Category")
            .reset_index(name="Tickets")
        )

        st.bar_chart(
            category_counts,
            x="Category",
            y="Tickets"
        )

        st.subheader("Priority Distribution")

        priority_counts = (
            dataframe["Priority"]
            .value_counts()
            .rename_axis("Priority")
            .reset_index(name="Tickets")
        )

        st.bar_chart(
            priority_counts,
            x="Priority",
            y="Tickets"
        )

        st.subheader("Recent Tickets")

        st.dataframe(
            dataframe[
                [
                    "Ticket ID",
                    "Customer",
                    "Category",
                    "Priority",
                    "Status"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No tickets available yet.")


# --------------------------------------------------
# SUBMIT CUSTOMER TICKET
# --------------------------------------------------

elif page == "Submit Customer Ticket":

    st.header("Submit a Customer Ticket")

    with st.form("ticket_form", clear_on_submit=True):

        customer_name = st.text_input("Customer Name")

        customer_email = st.text_input("Customer Email")

        issue = st.text_area(
            "Describe your issue",
            placeholder="Explain your problem here..."
        )

        submitted = st.form_submit_button("Submit Ticket")

        if submitted:

            if not customer_name.strip() or not issue.strip():

                st.warning(
                    "Please enter the customer name and issue."
                )

            elif (
                customer_email
                and "@" not in customer_email
            ):

                st.warning("Please enter a valid email address.")

            else:

                ticket_id = "RES-" + uuid.uuid4().hex[:8].upper()

                try:

                    create_ticket(
                        ticket_id,
                        customer_name.strip(),
                        customer_email.strip(),
                        issue.strip()
                    )

                    st.session_state["last_submitted_ticket"] = ticket_id

                    st.rerun()

                except Exception as error:

                    st.error(
                        f"Could not submit ticket: {error}"
                    )


# --------------------------------------------------
# AI TICKET ANALYSIS
# --------------------------------------------------

elif page == "AI Ticket Analysis":

    st.header("AI Ticket Analysis")

    if not tickets:

        st.info("Submit a ticket before running AI analysis.")

    else:

        ticket_options = {
            f"{ticket[1]} - {ticket[2]}": ticket[1]
            for ticket in tickets
        }

        selected_label = st.selectbox(
            "Select a customer ticket",
            list(ticket_options.keys())
        )

        selected_ticket_id = ticket_options[selected_label]

        # --------------------------------------------------
        # RESTORE KNOWLEDGE SOURCES AFTER STREAMLIT RERUN
        # --------------------------------------------------

        matches = []

        if (
            st.session_state.get("knowledge_matches_ticket_id")
            == selected_ticket_id
        ):

            matches = st.session_state.get(
                "knowledge_matches",
                []
            )

        # Get selected ticket

        ticket = get_ticket_by_id(selected_ticket_id)

        if ticket is None:

            st.error("Ticket not found.")

        else:

            st.subheader("Customer Complaint")

            st.write(ticket[4])

            # --------------------------------------------------
            # RUN GEMINI ANALYSIS
            # --------------------------------------------------

            if st.button("Analyze Ticket with Gemini"):

                try:

                    with st.spinner(
                        "Gemini is analyzing the ticket..."
                    ):

                        # Retrieve relevant knowledge

                        matches = search_knowledge_base(
                            ticket[4],
                            results_count=3
                        )

                        # Preserve retrieved knowledge across reruns

                        st.session_state["knowledge_matches"] = matches

                        st.session_state[
                            "knowledge_matches_ticket_id"
                        ] = selected_ticket_id

                        # Prepare knowledge context

                        knowledge_context = "\n\n".join(
                            [
                                f"Source: {match['source']}\n"
                                f"{match['text']}"
                                for match in matches
                            ]
                        )

                        # Run AI analysis

                        analysis = analyze_ticket(
                            ticket[4],
                            knowledge_context
                        )

                        # Save AI results in database

                        update_ticket_analysis(
                            selected_ticket_id,
                            analysis["category"],
                            analysis["sentiment"],
                            analysis["priority"],
                            analysis["suggested_response"]
                        )

                        st.session_state[
                            "last_analyzed_ticket"
                        ] = selected_ticket_id

                        st.rerun()

                except Exception as error:

                    st.error(
                        f"AI analysis failed: {error}"
                    )

            # --------------------------------------------------
            # REFRESH TICKET AFTER ANALYSIS
            # --------------------------------------------------

            ticket = get_ticket_by_id(selected_ticket_id)

            if ticket is not None and ticket[9]:

                st.divider()

                st.subheader("AI Analysis Results")

                col1, col2, col3 = st.columns(3)

                col1.metric("Category", ticket[5])
                col2.metric("Sentiment", ticket[6])
                col3.metric("Priority", ticket[7])

                st.subheader("Suggested Customer Response")

                st.info(ticket[9])

                st.caption(
                    "This is an AI-generated suggestion. "
                    "A human agent must review it before use."
                )

                st.write(
                    "Review Status:",
                    ticket[11]
                )

                # --------------------------------------------------
                # HUMAN REVIEW
                # --------------------------------------------------

                col1, col2 = st.columns(2)

                with col1:

                    if st.button("Approve Suggestion"):

                        update_response_review(
                            selected_ticket_id,
                            "Approved"
                        )

                        st.rerun()

                with col2:

                    if st.button("Request Changes"):

                        update_response_review(
                            selected_ticket_id,
                            "Changes Requested"
                        )

                        st.rerun()

                # --------------------------------------------------
                # RESOLVE TICKET
                # --------------------------------------------------

                if st.button("Mark Ticket as Resolved"):

                    update_ticket_status(
                        selected_ticket_id,
                        "Resolved"
                    )

                    st.session_state[
                        "last_resolved_ticket"
                    ] = selected_ticket_id

                    st.rerun()

            # --------------------------------------------------
            # DISPLAY RETRIEVED KNOWLEDGE SOURCES
            # --------------------------------------------------

            if matches:

                st.divider()

                st.subheader("Retrieved Knowledge Sources")

                for match in matches:

                    with st.expander(
                        match.get("source", "Knowledge Source")
                    ):

                        st.write(match.get("text", ""))

            else:

                st.caption(
                    "No knowledge sources have been retrieved "
                    "for this ticket yet."
                )


# --------------------------------------------------
# KNOWLEDGE BASE
# --------------------------------------------------

elif page == "Knowledge Base":

    st.header("Knowledge Base Management")

    st.write(
        "Upload company documents to provide relevant "
        "information to the AI support assistant."
    )

    st.metric(
        "Stored Knowledge Chunks",
        get_knowledge_count()
    )

    uploaded_files = st.file_uploader(
        "Upload PDF, TXT or Markdown documents",
        type=["pdf", "txt", "md"],
        accept_multiple_files=True
    )

    if st.button("Process Documents"):

        if not uploaded_files:

            st.warning(
                "Please upload at least one document."
            )

        else:

            for uploaded_file in uploaded_files:

                try:

                    file_bytes = uploaded_file.getvalue()

                    # Extract text from PDF

                    if uploaded_file.name.lower().endswith(".pdf"):

                        reader = PdfReader(
                            io.BytesIO(file_bytes)
                        )

                        text = "\n".join(
                            page.extract_text() or ""
                            for page in reader.pages
                        )

                    # Read TXT and Markdown files

                    else:

                        text = file_bytes.decode(
                            "utf-8",
                            errors="replace"
                        )

                    if not text.strip():

                        st.warning(
                            f"No readable text found in {uploaded_file.name}."
                        )

                        continue

                    # Store document in knowledge base

                    chunks_added = add_document(
                        text,
                        uploaded_file.name
                    )

                    st.success(
                        f"{uploaded_file.name}: "
                        f"{chunks_added} chunks processed."
                    )

                except Exception as error:

                    st.error(
                        f"Could not process "
                        f"{uploaded_file.name}: {error}"
                    )

            st.rerun()


# --------------------------------------------------
# TICKET HISTORY
# --------------------------------------------------

elif page == "Ticket History":

    st.header("Customer Ticket History")

    if tickets:

        for ticket in tickets:

            with st.expander(
                f"{ticket[1]} - {ticket[2]}"
            ):

                st.write("Customer:", ticket[2])

                st.write("Email:", ticket[3])

                st.write("Issue:", ticket[4])

                st.write("Category:", ticket[5])

                st.write("Sentiment:", ticket[6])

                st.write("Priority:", ticket[7])

                st.write("Status:", ticket[8])

                st.write(
                    "Response Review:",
                    ticket[11]
                )

                if ticket[9]:

                    st.subheader("AI Suggested Response")

                    st.write(ticket[9])

    else:

        st.info("No tickets have been submitted yet.")
