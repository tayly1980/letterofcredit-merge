def build_generation_prompt(sequence):
    prompt = (
        "You are a SWIFT trade finance expert. Generate the following SWIFT messages in the order provided.\n\n"
        "Instructions for all messages:\n"
        "- Start with the SWIFT message type and a short description (e.g., 'MT700 – Letter of Credit')\n"
        "- For each field:\n"
        "  - Use the SWIFT field tag (e.g., :20:) followed by a short label (e.g., ':20: Documentary Credit Number')\n"
        "  - On the next line, provide a realistic, fictitious value\n"
        "  - Leave a blank line between fields\n"
        "- Do not use markdown, summaries, or explanations\n"
        "- Use the same value for :20: across all messages (e.g., LC2024ABC001)\n"
        "- For MT707 and MT799:\n"
        "  - Include :21: as a fictitious LC advising bank reference (e.g., ADVREF789123)\n"
        "  - Generate this :21: once and reuse it in all MT707/MT799 messages\n"
        "- After each message, add a line of 50 dashes to separate it:\n"
        "  --------------------------------------------------\n\n"
    )

    has_advising_ref = False

    for msg_type in sequence:
        if msg_type == "MT700":
            prompt += (
                "MT700 – Letter of Credit\n"
                "Generate a complete MT700 message with appropriate SWIFT fields.\n"
                "Assign a consistent :20: reference (e.g., LC2024ABC001).\n"
                "Include short descriptions for all fields, such as:\n"
                "- :20: Documentary Credit Number\n"
                "- :32B: Currency and Amount\n"
                "- :50: Applicant\n"
                "- :59: Beneficiary\n"
                "- :31D: Date and Place of Expiry\n"
                "- :45A: Description of Goods\n"
                "- :46A: Documents Required\n"
                "- :71B: Charges\n"
                "- :78: Instructions to Bank\n"
                "- Add a separator line after the message:\n"
                "  --------------------------------------------------\n\n"
            )

        elif msg_type == "MT707":
            prompt += (
                "MT707 – Amendment\n"
                "Generate an MT707 that amends the MT700.\n"
                "Use the same :20: reference as in the MT700.\n"
            )
            if not has_advising_ref:
                prompt += (
                    "Generate :21: as a fictitious LC advising bank reference (e.g., ADVREF789123).\n"
                )
                has_advising_ref = True
            else:
                prompt += (
                    "Use the same :21: advising bank reference as generated earlier.\n"
                )
            prompt += (
                "Amend at least 2–3 fields.\n"
                "Include short descriptions for all used fields.\n"
                "Add a separator line after the message:\n"
                "  --------------------------------------------------\n\n"
            )

        elif msg_type == "MT799":
            prompt += (
                "MT799 – Free Format Message\n"
                "Generate a correction or clarification related to the MT700 or its amendment.\n"
                "Use the same :20: reference as in the MT700.\n"
            )
            if not has_advising_ref:
                prompt += (
                    "Generate :21: as a fictitious LC advising bank reference (e.g., ADVREF789123).\n"
                )
                has_advising_ref = True
            else:
                prompt += (
                    "Use the same :21: advising bank reference as generated earlier.\n"
                )
            prompt += (
                "Include :79: with a clear correction or explanation.\n"
                "Include short descriptions for all used fields.\n"
                "Add a separator line after the message:\n"
                "  --------------------------------------------------\n\n"
            )

    prompt += (
        "Only output the messages listed above, in the given order. "
        "Do not include markdown formatting, bullet points, or any extra commentary."
    )

    return prompt