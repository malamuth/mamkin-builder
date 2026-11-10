# Current work

Task: customer labels must collapse repeated whitespace and trim outer whitespace. Preserve name case. Empty names produce `Customer: `.
Progress: complete. customer_label now uses clean_name, collapsing repeated whitespace and trimming outer whitespace while preserving case. Empty and whitespace-only names produce `Customer: `.
Verification: `python3 -B -m unittest discover -s tests` passed (3 tests). Label checks cover outer and repeated spaces, tabs and line breaks, mixed case, empty names, and whitespace-only names.
Adjacent idea: empty cart total is wrong; outside this task.
