def process_lead(lead):
    analysis = analyze_with_llm(lead)

    if check_duplicate(lead["email"]):
        update_crm(lead, analysis)
        return

    if analysis["needs_followup"]:
        send_followup_email(
            lead["email"],
            analysis["missing_fields"]
        )
        return

    if analysis["department"] == "Sales":
        owner = assign_sales_rep()

        if analysis["book_meeting"]:
            meeting = book_meeting(lead["email"])

        create_lead(
            lead,
            owner,
            meeting if analysis["book_meeting"] else None
        )

    else:
        add_to_marketing_campaign(lead)

    notify_sales_if_high_priority(analysis)