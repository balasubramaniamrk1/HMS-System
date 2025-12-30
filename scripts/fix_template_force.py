import os

file_path = 'templates/staff_mgmt/admin/staff_list.html'

with open(file_path, 'r') as f:
    content = f.read()

# Normalize spacing
fixed_content = content.replace(
    '{{ person.shift.start_time|time:"H:i" }} - {{\n                                person.shift.end_time|time:"H:i" }}',
    '{{ person.shift.start_time|time:"H:i" }} - {{ person.shift.end_time|time:"H:i" }}'
)

# Also try the version without spaces just in case
fixed_content = fixed_content.replace(
    '{{ person.shift.start_time|time:"H:i" }}-{{\n                                person.shift.end_time|time:"H:i" }}',
    '{{ person.shift.start_time|time:"H:i" }}-{{ person.shift.end_time|time:"H:i" }}'
)

if content != fixed_content:
    print("Found and replaced broken pattern.")
    with open(file_path, 'w') as f:
        f.write(fixed_content)
else:
    print("Pattern NOT found. Content might be different.")
    # Print the relevant section to debug
    import re
    match = re.search(r'shift\.name.*?end_time', content, re.DOTALL)
    if match:
        print(f"Current content snippet:\n{match.group(0)!r}")
