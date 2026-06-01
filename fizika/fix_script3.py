import sys

with open('/Users/ugniusvaitiekenas/srotas-ai-agent/fizika/generate_pdf_ready.py', 'r') as f:
    content = f.read()

# Fix Kunas AE schema M1
content = content.replace(
    '<text x="{oAx-30}" y="{oAy-25}" font-style="italic" font-weight="bold">M&#8321;</text>',
    '{get_vector_text(oAx-30, oAy-25, "M", "1")}'
)

# Fix Kunas BD schema M2
content = content.replace(
    '<text x="{oBx+15}" y="{oBy-35}" font-style="italic" font-weight="bold">M&#8322;</text>',
    '{get_vector_text(oBx+15, oBy-35, "M", "2")}'
)

kunas_ae_angles = """
    <!-- Angles -->
    <line x1="{oAx}" y1="{oAy}" x2="{oAx+50}" y2="{oAy}" stroke="gray" stroke-width="1"/>
    <path d="M {oAx+40} {oAy} A 40 40 0 1 0 {oAx+40*math.cos(rad(-30))} {oAy-40*math.sin(rad(-30))}" fill="none" stroke="gray" stroke-width="1"/>
    <text x="{oAx+45}" y="{oAy+20}" fill="gray" font-size="12">330&deg;</text>
    
    <path d="M {oEx+20*math.cos(rad(-30))} {oEy-20*math.sin(rad(-30))} A 20 20 0 0 0 {oEx+20*math.cos(rad(-90))} {oEy-20*math.sin(rad(-90))}" fill="none" stroke="gray" stroke-width="1"/>
    <text x="{oEx+25}" y="{oEy-15}" fill="gray" font-size="12">90&deg;</text>
"""
if kunas_ae_angles not in content:
    content = content.replace('    <!-- Moments -->\n    <path d="M {oAx+30} {oAy+20} A 30 30 0 1 0 {oAx-20} {oAy-20}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>\n    {get_vector_text(oAx-30, oAy-25, "M", "1")}', kunas_ae_angles + '    <!-- Moments -->\n    <path d="M {oAx+30} {oAy+20} A 30 30 0 1 0 {oAx-20} {oAy-20}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>\n    {get_vector_text(oAx-30, oAy-25, "M", "1")}')

# Add angles to Kunas BD schema
kunas_bd_angles = """
    <!-- Angles -->
    <line x1="{oDx-l9*scale}" y1="{oDy}" x2="{oDx-l9*scale-50}" y2="{oDy}" stroke="gray" stroke-width="1"/>
    <path d="M {oDx-l9*scale-30} {oDy} A 30 30 0 0 1 {oDx-l9*scale+30*math.cos(rad(100))} {oDy-30*math.sin(rad(100))}" fill="none" stroke="gray" stroke-width="1"/>
    <text x="{oDx-l9*scale-40}" y="{oDy+20}" fill="gray" font-size="12">100&deg;</text>
"""
if kunas_bd_angles not in content:
    content = content.replace('    <path d="M {oBx+50} {oBy+20} A 30 30 0 1 0 {oBx+10} {oBy-30}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>\n    {get_vector_text(oBx+15, oBy-35, "M", "2")}', kunas_bd_angles + '    <path d="M {oBx+50} {oBy+20} A 30 30 0 1 0 {oBx+10} {oBy-30}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>\n    {get_vector_text(oBx+15, oBy-35, "M", "2")}')

with open('/Users/ugniusvaitiekenas/srotas-ai-agent/fizika/generate_pdf_ready.py', 'w') as f:
    f.write(content)
