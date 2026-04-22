import csv

import re

 

# Output file

output_file = "Windows-11-CIS-Stand-alone-Audit-L1^26200.csv"

 

# Write header

with open(output_file, "w", newline='', encoding='utf-8') as f:

    writer = csv.writer(f)

    header = ['Status', 'Name', 'Rationale', 'Solution', 'See Also', 'Reference', 'Policy Value', 'Actual Value']

    writer.writerow(header)

 

# Input CSV file (replace with your actual filename)

with open("Windows-11-CIS-Stand-alone-Audit-L1^26200__$_9q9seh.csv", mode='r', encoding='utf-8') as file:

    reader = csv.reader(file)

    next(reader)  # Skip header if present

 

    for row in reader:

        if len(row) < 5:

            continue

 

        status = row[0]  # Column A

        description_block = row[4]  # Column E

 

        # Extract Name (first line before colon)

        name_match = re.match(r'^"(.+?)"\s*:', description_block)

        name = name_match.group(1) if name_match else "----"

 

        # Rationale

        rationale_match = re.search(r'^".+?"\s*:\s*\[.*?\]\s*\n+(.*?)(?=^Solution:)', description_block, re.DOTALL | re.MULTILINE)

        rationale = rationale_match.group(1).strip() if rationale_match else "----"

 

        # Solution

        solution_match = re.search(r"Solution:\s*\n(.*?)(?=\nSee Also:)", description_block, re.DOTALL)

        solution = solution_match.group(1).strip() if solution_match else "----"

 

        # See Also

        see_also_match = re.search(r"See Also:\s*(.*?)(?=\n\S|$)", description_block, re.DOTALL)

        see_also = see_also_match.group(1).strip() if see_also_match else "----"

 

        # Reference

        reference_match = re.search(r"Reference:\s*(.*?)(?=\n\S|$)", description_block, re.DOTALL)

        reference = reference_match.group(1).strip() if reference_match else "----"

 

        # Policy Value

        policy_match = re.search(r"Policy Value:\s*\n(.*?)\n(?=Actual Value:)", description_block, re.DOTALL)

        policy_value = policy_match.group(1).strip() if policy_match else "----"

 

        # Actual Value

        actual_value_match = re.search(r"Actual Value:\s*(.*)", description_block, re.DOTALL)

        actual_value = actual_value_match.group(1).strip() if actual_value_match else "----"

 

        # Append to CSV

        with open(output_file, "a", newline='', encoding='utf-8') as f:

            writer = csv.writer(f)

            writer.writerow([status, name, rationale, solution, see_also, reference, policy_value, actual_value])

 

print(f"✅ Parsed data written to '{output_file}' successfully.")