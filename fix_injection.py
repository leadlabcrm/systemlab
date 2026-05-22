import re

path = '/Users/nithin/.gemini/antigravity-ide/scratch/systemlab/systemlab-v2.html'
with open(path, 'r') as f:
    html = f.read()

# 1. Extract the misplaced JS functions
start_marker = "// RECURRING TASKS"
end_marker = "// Ensure the functions exist"

# We find the block that was mistakenly put inside the SortableJS script tag
if start_marker in html:
    start_idx = html.find(start_marker)
    end_idx = html.find(end_marker) + len(end_marker)
    
    # Extract the block
    js_block = html[start_idx:end_idx]
    
    # Remove it from its current position
    html = html[:start_idx] + html[end_idx:]
    
    # Find the END of the MAIN script block.
    # The main script block starts right after <script> and ends before </script>
    # There are multiple <script> tags. The main one contains "function init()"
    
    # We can inject it right before the "window.onload = init;" or similar
    if "function init()" in html:
        injection_point = "function init()"
        html = html.replace(injection_point, js_block + "\n\n" + injection_point)

with open(path, 'w') as f:
    f.write(html)

print("Fixed script injection!")
