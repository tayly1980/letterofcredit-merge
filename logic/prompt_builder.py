def build_generation_prompt(sequence):
    lines = []

    lines.append("Generate synthetic SWIFT messages based on the sequence below.")
    lines.append("Each message must:")
    lines.append("• Begin with the correct heading (see below)")
    lines.append("• Use valid SWIFT field tags (e.g., :20:, :23B:, etc.)")
    lines.append("• Contain fictitious but realistic bank names, BICs, company names, and addresses")
    lines.append("• Format corrections/amendments logically (MT707/MT799 should refer back to earlier messages)")
    lines.append("• Always use MSC00X (e.g., MSC001) in message references — never CORR00X")
    lines.append("• Include a short title line above each message, exactly as described")
    lines.append("")

    for index, msg_type in enumerate(sequence):
        if msg_type == "MT700":
            lines.append("### MT700 – Letter of Credit")
            lines.append(
                "Include typical fields like :20:, :23B:, :30T:, :40A:, :50:, :59:, :32B:, :41D:, :45A:, :46A:, :71B:, :78:, :57D:, :72:. "
                "Use realistic values for LC numbers, currency, amount, company names, and ports."
            )
        elif msg_type == "MT707":
            lines.append("### MT707 – Amendment to Documentary Credit")
            lines.append(
                "Include fields like :20:, :21:, :30:, :45B:, :46A:, :47A:, and :79:. "
                "Clearly indicate what field(s) are being amended. Use logical and traceable changes from previous MT700 values."
            )
        elif msg_type == "MT799":
            lines.append("### MT799 – Free Format Message")
            lines.append(
                "Only use :79: field. Describe corrections, additions, or deletions to earlier MT700/MT707/MT799 messages. "
                "Format the reference as MSC00X (e.g., MSC001, MSC002). "
                "Message must clearly refer to which previous field(s) are being corrected or clarified."
            )
        lines.append("")  # Spacer between message blocks

    # Reinforce correct formatting
    lines.append("Important:")
    lines.append("• Label each message with its proper heading: MT700 – Letter of Credit, MT707 – Amendment..., MT799 – Free Format Message.")
    lines.append("• Include all SWIFT field tags with colons.")
    lines.append("• Use fully fictitious banks, BICs, and company names.")
    lines.append("• Do not use real organizations or locations unless they are generic placeholders (e.g., City, Country).")

    return "\n".join(lines)

