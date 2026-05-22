import re

with open('/Users/nithin/.gemini/antigravity-ide/scratch/systemlab/systemlab-v2.html', 'r') as f:
    html = f.read()

# The exact block to move
pattern = re.compile(r'(  </div>\n)\n    <!-- TEAM VIEW -->\n    <div id="v-team".*?    </div>\n</div>\n', re.DOTALL)
match = pattern.search(html)

if match:
    # Everything after the first </div> (which is the closing tag for #main)
    # is the injected block, up to the </div> that closes #app
    # Actually let's just grab the block and place it before the `  </div>`
    
    # Let's write a simple string replacement
    # We want to swap:
    #   </div>
    # 
    #     <!-- TEAM VIEW -->
    #     ...
    #     <!-- EMPLOYEE DETAIL VIEW -->
    #     ...
    #     </div>
    # </div>
    
    # Into:
    #     <!-- TEAM VIEW -->
    #     ...
    #     <!-- EMPLOYEE DETAIL VIEW -->
    #     ...
    #     </div>
    #   </div>
    # </div>
    
    # Let's extract the views
    views_pattern = re.compile(r'    <!-- TEAM VIEW -->.*?    </div>\n', re.DOTALL)
    views_match = views_pattern.search(html)
    
    if views_match:
        views_html = views_match.group(0)
        # Remove it from its current location
        html = html.replace('\n' + views_html, '')
        
        # Now find the closing tag of #main, which is `  </div>\n</div>\n\n<!-- FLOWCHART MODAL -->`
        html = html.replace('  </div>\n</div>\n\n<!-- FLOWCHART MODAL -->', f'{views_html}  </div>\n</div>\n\n<!-- FLOWCHART MODAL -->')
        
        with open('/Users/nithin/.gemini/antigravity-ide/scratch/systemlab/systemlab-v2.html', 'w') as f:
            f.write(html)
        print("Successfully moved!")
    else:
        print("Could not find views block")
else:
    print("Pattern did not match")
