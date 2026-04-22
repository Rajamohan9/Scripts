import re
import csv
from openpyxl import Workbook

input_file = "Windows-11.csv"
output_file = "final_output1.csv"

wb = Workbook()
ws = wb.active
ws.title = "CIS Report"

# Headers
headers = [
    "Title",
    "Threat Description",
    "Impact for you",
    "Remediation Steps",
    "Affected Assets",
    "Profile Applicability",
    "Assessment Status",
    "Default Value",
    "Rationale",
    "References"
]

ws.append(headers)

with open(input_file, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        if len(row) < 2:
            continue

        status = row[0].strip()
        description_block = row[1].replace('"""', '"').strip()

        # Skip empty
        if not description_block:
            continue

        # -------------------------
        # TITLE (works for all formats)
        # -------------------------
        title_match = re.search(r'"(.*?)"\s*:\s*\[', description_block)
        title = title_match.group(1).strip() if title_match else "Unknown"

        # -------------------------
        # CONTROL NUMBER (Affected Assets)
        # -------------------------
        control_match = re.search(r'"([\d\.]+)', description_block)
        affected_asset = control_match.group(1) if control_match else "N/A"

        # -------------------------
        # PROFILE (L1/L2)
        # -------------------------
        level_match = re.search(r'\((L\d)\)', description_block)
        profile = level_match.group(1) if level_match else "N/A"

        # -------------------------
        # THREAT DESCRIPTION
        # -------------------------
        threat_match = re.search(
            r'\]\s*(.*?)(?=\nSolution:|\nImpact:|\nSee Also:|$)',
            description_block,
            re.DOTALL
        )
        threat_desc = threat_match.group(1).strip() if threat_match else description_block[:200]

        # -------------------------
        # IMPACT
        # -------------------------
        impact_match = re.search(
            r'Impact:\s*(.*?)(?=\nSolution:|\nSee Also:|$)',
            description_block,
            re.DOTALL
        )
        impact = impact_match.group(1).strip() if impact_match else "Not Defined"

        # -------------------------
        # SOLUTION
        # -------------------------
        solution_match = re.search(
            r'Solution:\s*(.*?)(?=\nImpact:|\nSee Also:|$)',
            description_block,
            re.DOTALL
        )
        solution = solution_match.group(1).strip() if solution_match else "Not Available"

        # -------------------------
        # DEFAULT VALUE (Policy + Actual)
        # -------------------------
        default_match = re.search(
            r'(Policy Value:.*?Actual Value:.*?)(?=\n\S|$)',
            description_block,
            re.DOTALL
        )
        default_value = default_match.group(1).strip() if default_match else "Not Available"

        # -------------------------
        # REFERENCES
        # -------------------------
        ref_match = re.search(
            r'See Also:\s*(.*?)(?=\nReference:|\n\S|$)',
            description_block,
            re.DOTALL
        )
        references = ref_match.group(1).strip() if ref_match else "Not Available"

        # -------------------------
        # RATIONALE (same as threat)
        # -------------------------
        rationale = threat_desc

        # -------------------------
        # WRITE TO EXCEL
        # -------------------------
        ws.append([
            title,
            threat_desc,
            impact,
            solution,
            affected_asset,
            profile,
            status,
            default_value,
            rationale,
            references
        ])

# -------------------------
# AUTO FORMAT (VERY IMPORTANT)
# -------------------------
for col in ws.columns:
    max_length = 0
    col_letter = col[0].column_letter
    for cell in col:
        if cell.value:
            max_length = max(max_length, len(str(cell.value)))
    ws.column_dimensions[col_letter].width = min(max_length + 2, 50)

# Freeze header
ws.freeze_panes = "A2"

# Save file
wb.save(output_file)

print(f"✅ Done: {output_file}")


