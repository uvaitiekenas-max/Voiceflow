import sys

with open('/Users/ugniusvaitiekenas/srotas-ai-agent/fizika/generate_pdf_ready.py', 'r') as f:
    content = f.read()

# I will find the exact string to replace.
# The SVG block for the schema starts at <p><b><u>Užduoties schema:</u></b></p>
# and ends at </svg>\n</div>

start_idx = content.find('<p><b><u>Užduoties schema:</u></b></p>')
end_idx = content.find('</svg>\n</div>', start_idx) + len('</svg>\n</div>')

original_svg_block = content[start_idx:end_idx]

uzduoties_schema = """<p><b><u>Užduoties schema:</u></b></p>
<div class="schema-container">
<svg width="800" height="400" viewBox="0 0 800 400">
    {get_marker()}
    
    <!-- Supports -->
    <path d="M {oAx} {oAy} L {oAx-15} {oAy+20} L {oAx+15} {oAy+20} Z" fill="none" stroke="black" stroke-width="2"/>
    <line x1="{oAx-25}" y1="{oAy+20}" x2="{oAx+25}" y2="{oAy+20}" stroke="black" stroke-width="2"/>
    {get_hatch(oAx-25, oAx+25, oAy+20)}
    
    <circle cx="{oDx-10}" cy="{oDy+25}" r="5" fill="none" stroke="black" stroke-width="2"/>
    <circle cx="{oDx+10}" cy="{oDy+25}" r="5" fill="none" stroke="black" stroke-width="2"/>
    <path d="M {oDx} {oDy} L {oDx-15} {oDy+20} L {oDx+15} {oDy+20} Z" fill="none" stroke="black" stroke-width="2"/>
    <line x1="{oDx-25}" y1="{oDy+30}" x2="{oDx+25}" y2="{oDy+30}" stroke="black" stroke-width="2"/>
    {get_hatch(oDx-25, oDx+25, oDy+30)}
    
    <circle cx="{oCx-10}" cy="{oCy+25}" r="5" fill="none" stroke="black" stroke-width="2"/>
    <circle cx="{oCx+10}" cy="{oCy+25}" r="5" fill="none" stroke="black" stroke-width="2"/>
    <path d="M {oCx} {oCy} L {oCx-15} {oCy+20} L {oCx+15} {oCy+20} Z" fill="none" stroke="black" stroke-width="2"/>
    <line x1="{oCx-25}" y1="{oCy+30}" x2="{oCx+25}" y2="{oCy+30}" stroke="black" stroke-width="2"/>
    {get_hatch(oCx-25, oCx+25, oCy+30)}

    <!-- Bodies -->
    <line x1="{oAx}" y1="{oAy}" x2="{oEx}" y2="{oEy}" stroke="black" stroke-width="4" />
    <line x1="{oBx}" y1="{oBy}" x2="{oDx}" y2="{oDy}" stroke="black" stroke-width="4" />
    <circle cx="{oAx}" cy="{oAy}" r="4" fill="white" stroke="black" stroke-width="2"/>
    <circle cx="{oBx}" cy="{oBy}" r="4" fill="white" stroke="black" stroke-width="2"/>
    
    <!-- Dimensions for BD -->
    <line x1="{oBx}" y1="{oBy-60}" x2="{oDx}" y2="{oDy-60}" stroke="gray" stroke-width="1"/>
    <line x1="{oBx}" y1="{oBy-65}" x2="{oBx}" y2="{oBy-55}" stroke="gray" stroke-width="1"/>
    <line x1="{oBx+2*scale}" y1="{oBy-65}" x2="{oBx+2*scale}" y2="{oBy-55}" stroke="gray" stroke-width="1"/>
    <line x1="{oBx+4*scale}" y1="{oBy-65}" x2="{oBx+4*scale}" y2="{oBy-55}" stroke="gray" stroke-width="1"/>
    <line x1="{oBx+6*scale}" y1="{oBy-65}" x2="{oBx+6*scale}" y2="{oBy-55}" stroke="gray" stroke-width="1"/>
    <line x1="{oDx}" y1="{oDy-65}" x2="{oDx}" y2="{oDy-55}" stroke="gray" stroke-width="1"/>
    <line x1="{oBx}" y1="{oBy-60}" x2="{oBx}" y2="{oBy-15}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
    <line x1="{oDx}" y1="{oDy-60}" x2="{oDx}" y2="{oDy-15}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
    <text x="{oBx+1*scale-10}" y="{oBy-65}" fill="gray">{fmt(l3 - l4 - l9)}</text>
    <text x="{oBx+3*scale-10}" y="{oBy-65}" fill="gray">{fmt(l9)}</text>
    <text x="{oBx+5*scale-10}" y="{oBy-65}" fill="gray">{fmt(l8/2)}</text>
    <text x="{oBx+7*scale-10}" y="{oBy-65}" fill="gray">{fmt(l7)}</text>

    <!-- Dimensions for AE -->
    <g transform="translate({oAx}, {oAy}) rotate(30)">
        <line x1="0" y1="50" x2="{6*scale}" y2="50" stroke="gray" stroke-width="1"/>
        <line x1="0" y1="45" x2="0" y2="55" stroke="gray" stroke-width="1"/>
        <line x1="{1*scale}" y1="45" x2="{1*scale}" y2="55" stroke="gray" stroke-width="1"/>
        <line x1="{3*scale}" y1="45" x2="{3*scale}" y2="55" stroke="gray" stroke-width="1"/>
        <line x1="{6*scale}" y1="45" x2="{6*scale}" y2="55" stroke="gray" stroke-width="1"/>
        <line x1="0" y1="10" x2="0" y2="50" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <line x1="{6*scale}" y1="10" x2="{6*scale}" y2="50" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <text x="{0.5*scale-10}" y="40" fill="gray">{fmt(l5)}</text>
        <text x="{2*scale-10}" y="40" fill="gray">{fmt(l6)}</text>
        <text x="{4.5*scale-10}" y="40" fill="gray">{fmt(l1 - l5 - l6)}</text>
    </g>

    <!-- Angles -->
    <line x1="{oAx}" y1="{oAy}" x2="{oAx+50}" y2="{oAy}" stroke="gray" stroke-width="1"/>
    <path d="M {oAx+40} {oAy} A 40 40 0 1 0 {oAx+40*math.cos(rad(-30))} {oAy-40*math.sin(rad(-30))}" fill="none" stroke="gray" stroke-width="1"/>
    <text x="{oAx+45}" y="{oAy+20}" fill="gray" font-size="12">330&deg;</text>

    <line x1="{oDx-l9*scale}" y1="{oDy}" x2="{oDx-l9*scale-50}" y2="{oDy}" stroke="gray" stroke-width="1"/>
    <path d="M {oDx-l9*scale-30} {oDy} A 30 30 0 0 1 {oDx-l9*scale+30*math.cos(rad(100))} {oDy-30*math.sin(rad(100))}" fill="none" stroke="gray" stroke-width="1"/>
    <text x="{oDx-l9*scale-40}" y="{oDy+20}" fill="gray" font-size="12">100&deg;</text>
    
    <!-- F1 angle -->
    <path d="M {oEx+20*math.cos(rad(-30))} {oEy-20*math.sin(rad(-30))} A 20 20 0 0 0 {oEx+20*math.cos(rad(-90))} {oEy-20*math.sin(rad(-90))}" fill="none" stroke="gray" stroke-width="1"/>
    <text x="{oEx+25}" y="{oEy-15}" fill="gray" font-size="12">90&deg;</text>

    <text x="{oAx-25}" y="{oAy+15}" font-style="italic" font-size="18">A</text>
    <text x="{oBx-15}" y="{oBy+25}" font-style="italic" font-size="18">B</text>
    <text x="{oDx+20}" y="{oDy-10}" font-style="italic" font-size="18">D</text>
    <text x="{oCx-10}" y="{oCy-15}" font-style="italic" font-size="18">C</text>
    <text x="{oEx+10}" y="{oEy+10}" font-style="italic" font-size="18">E</text>

    <!-- F1, F2 -->
    <line x1="{oEx}" y1="{oEy-50}" x2="{oEx}" y2="{oEy}" stroke="black" stroke-width="2" marker-end="url(#arrow)" />
    {get_vector_text(oEx-15, oEy-25, 'F', '1')}
    
    <line x1="{oDx-l9*scale+50*math.cos(rad(100))}" y1="{oDy-50*math.sin(rad(100))}" x2="{oDx-l9*scale}" y2="{oDy}" stroke="black" stroke-width="2" marker-end="url(#arrow)" />
    {get_vector_text(oDx-l9*scale-20, oDy-25, 'F', '2')}
    
    <!-- Distributed Loads q2 (Pointing UP) -->
    <rect x="{oDx-6*scale}" y="{oDy}" width="{4*scale}" height="25" fill="none" stroke="black"/>
    <line x1="{oDx-6*scale}" y1="{oDy+25}" x2="{oDx-6*scale}" y2="{oDy}" stroke="black" marker-end="url(#arrow)"/>
    <line x1="{oDx-5*scale}" y1="{oDy+25}" x2="{oDx-5*scale}" y2="{oDy}" stroke="black" marker-end="url(#arrow)"/>
    <line x1="{oDx-4*scale}" y1="{oDy+25}" x2="{oDx-4*scale}" y2="{oDy}" stroke="black" marker-end="url(#arrow)"/>
    <line x1="{oDx-3*scale}" y1="{oDy+25}" x2="{oDx-3*scale}" y2="{oDy}" stroke="black" marker-end="url(#arrow)"/>
    <line x1="{oDx-2*scale}" y1="{oDy+25}" x2="{oDx-2*scale}" y2="{oDy}" stroke="black" marker-end="url(#arrow)"/>
    <text x="{oDx-4*scale}" y="{oDy+45}" font-style="italic">q&#8322;</text>
    
    <!-- Distributed Loads q11, q12 -->
    <g transform="translate({oAx}, {oAy}) rotate(30)">
        <polygon points="{1*scale},0 {1*scale},-30 {3*scale},0" fill="none" stroke="black"/>
        <line x1="{1.0*scale}" y1="-30" x2="{1.0*scale}" y2="0" stroke="black" marker-end="url(#arrow)"/>
        <line x1="{1.5*scale}" y1="-22.5" x2="{1.5*scale}" y2="0" stroke="black" marker-end="url(#arrow)"/>
        <line x1="{2.0*scale}" y1="-15" x2="{2.0*scale}" y2="0" stroke="black" marker-end="url(#arrow)"/>
        <line x1="{2.5*scale}" y1="-7.5" x2="{2.5*scale}" y2="0" stroke="black" marker-end="url(#arrow)"/>
        <text x="{1.5*scale}" y="-35" font-style="italic" transform="rotate(-30, {1.5*scale}, -35)">q&#8311;&#8321;</text>
    </g>

    <!-- Moments -->
    <path d="M {oAx+30} {oAy+20} A 30 30 0 1 0 {oAx-20} {oAy-20}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oAx-30, oAy-25, 'M', '1')}
    <path d="M {oBx+50} {oBy+20} A 30 30 0 1 0 {oBx+10} {oBy-30}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oBx+15, oBy-35, 'M', '2')}
</svg>
</div>"""

skaiciuojamoji_schema = """<p><b><u>Skaičiuojamoji schema:</u></b></p>
<div class="schema-container">
<svg width="800" height="400" viewBox="0 0 800 400">
    {get_marker()}
    
    <!-- Bodies -->
    <line x1="{oAx}" y1="{oAy}" x2="{oEx}" y2="{oEy}" stroke="black" stroke-width="4" />
    <line x1="{oBx}" y1="{oBy}" x2="{oDx}" y2="{oDy}" stroke="black" stroke-width="4" />
    
    <!-- Dimensions for BD -->
    <line x1="{oBx}" y1="{oBy-60}" x2="{oDx}" y2="{oDy-60}" stroke="gray" stroke-width="1"/>
    <line x1="{oBx}" y1="{oBy-65}" x2="{oBx}" y2="{oBy-55}" stroke="gray" stroke-width="1"/>
    <line x1="{oBx+2*scale}" y1="{oBy-65}" x2="{oBx+2*scale}" y2="{oBy-55}" stroke="gray" stroke-width="1"/>
    <line x1="{oBx+4*scale}" y1="{oBy-65}" x2="{oBx+4*scale}" y2="{oBy-55}" stroke="gray" stroke-width="1"/>
    <line x1="{oBx+6*scale}" y1="{oBy-65}" x2="{oBx+6*scale}" y2="{oBy-55}" stroke="gray" stroke-width="1"/>
    <line x1="{oDx}" y1="{oDy-65}" x2="{oDx}" y2="{oDy-55}" stroke="gray" stroke-width="1"/>
    <line x1="{oBx}" y1="{oBy-60}" x2="{oBx}" y2="{oBy-15}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
    <line x1="{oDx}" y1="{oDy-60}" x2="{oDx}" y2="{oDy-15}" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
    <text x="{oBx+1*scale-10}" y="{oBy-65}" fill="gray">{fmt(l3 - l4 - l9)}</text>
    <text x="{oBx+3*scale-10}" y="{oBy-65}" fill="gray">{fmt(l9)}</text>
    <text x="{oBx+5*scale-10}" y="{oBy-65}" fill="gray">{fmt(l8/2)}</text>
    <text x="{oBx+7*scale-10}" y="{oBy-65}" fill="gray">{fmt(l7)}</text>

    <!-- Dimensions for AE -->
    <g transform="translate({oAx}, {oAy}) rotate(30)">
        <line x1="0" y1="50" x2="{6*scale}" y2="50" stroke="gray" stroke-width="1"/>
        <line x1="0" y1="45" x2="0" y2="55" stroke="gray" stroke-width="1"/>
        <line x1="{1.667*scale}" y1="45" x2="{1.667*scale}" y2="55" stroke="gray" stroke-width="1"/>
        <line x1="{3*scale}" y1="45" x2="{3*scale}" y2="55" stroke="gray" stroke-width="1"/>
        <line x1="{6*scale}" y1="45" x2="{6*scale}" y2="55" stroke="gray" stroke-width="1"/>
        <line x1="0" y1="10" x2="0" y2="50" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <line x1="{6*scale}" y1="10" x2="{6*scale}" y2="50" stroke="gray" stroke-width="1" stroke-dasharray="2"/>
        <text x="{0.83*scale-15}" y="40" fill="gray">{fmt(a1)}</text>
        <text x="{2.33*scale-15}" y="40" fill="gray">{fmt(l2 - a1)}</text>
        <text x="{4.5*scale-15}" y="40" fill="gray">{fmt(l1 - l2)}</text>
    </g>

    <!-- Angles -->
    <line x1="{oAx}" y1="{oAy}" x2="{oAx+50}" y2="{oAy}" stroke="gray" stroke-width="1"/>
    <path d="M {oAx+40} {oAy} A 40 40 0 1 0 {oAx+40*math.cos(rad(-30))} {oAy-40*math.sin(rad(-30))}" fill="none" stroke="gray" stroke-width="1"/>
    <text x="{oAx+45}" y="{oAy+20}" fill="gray" font-size="12">330&deg;</text>

    <line x1="{oDx-l9*scale}" y1="{oDy}" x2="{oDx-l9*scale-50}" y2="{oDy}" stroke="gray" stroke-width="1"/>
    <path d="M {oDx-l9*scale-30} {oDy} A 30 30 0 0 1 {oDx-l9*scale+30*math.cos(rad(100))} {oDy-30*math.sin(rad(100))}" fill="none" stroke="gray" stroke-width="1"/>
    <text x="{oDx-l9*scale-40}" y="{oDy+20}" fill="gray" font-size="12">100&deg;</text>
    
    <!-- F1 angle -->
    <path d="M {oEx+20*math.cos(rad(-30))} {oEy-20*math.sin(rad(-30))} A 20 20 0 0 0 {oEx+20*math.cos(rad(-90))} {oEy-20*math.sin(rad(-90))}" fill="none" stroke="gray" stroke-width="1"/>
    <text x="{oEx+25}" y="{oEy-15}" fill="gray" font-size="12">90&deg;</text>

    <text x="{oAx-15}" y="{oAy+15}" font-style="italic" font-size="18">A</text>
    <text x="{oBx-15}" y="{oBy+25}" font-style="italic" font-size="18">B</text>
    <text x="{oDx+20}" y="{oDy-10}" font-style="italic" font-size="18">D</text>
    <text x="{oCx-10}" y="{oCy-15}" font-style="italic" font-size="18">C</text>
    <text x="{oEx+10}" y="{oEy+10}" font-style="italic" font-size="18">E</text>

    <!-- A Reactions -->
    <line x1="{oAx}" y1="{oAy}" x2="{oAx+50}" y2="{oAy}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oAx+45, oAy-15, 'R', 'Ax')}
    <line x1="{oAx}" y1="{oAy+50}" x2="{oAx}" y2="{oAy}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oAx+15, oAy+45, 'R', 'Ay')}
    
    <!-- D Reaction -->
    <line x1="{oDx}" y1="{oDy+50}" x2="{oDx}" y2="{oDy}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oDx-25, oDy+35, 'R', 'D')}
    
    <!-- C Reaction -->
    <line x1="{oCx}" y1="{oCy+50}" x2="{oCx}" y2="{oCy}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oCx-25, oCy+35, 'R', 'C')}

    <!-- F1, F2 -->
    <line x1="{oEx}" y1="{oEy-50}" x2="{oEx}" y2="{oEy}" stroke="black" stroke-width="2" marker-end="url(#arrow)" />
    {get_vector_text(oEx-20, oEy-25, 'F', '1')}
    
    <line x1="{oDx-l9*scale+50*math.cos(rad(100))}" y1="{oDy-50*math.sin(rad(100))}" x2="{oDx-l9*scale}" y2="{oDy}" stroke="black" stroke-width="2" marker-end="url(#arrow)" />
    {get_vector_text(oDx-l9*scale-20, oDy-25, 'F', '2')}
    
    <!-- Q1, Q2 -->
    <line x1="{oDx-a2_from_D*scale}" y1="{oDy+40}" x2="{oDx-a2_from_D*scale}" y2="{oDy}" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oDx-a2_from_D*scale+10, oDy+30, 'Q', '2')}
    
    <g transform="translate({oAx}, {oAy}) rotate(30)">
        <line x1="{1.667*scale}" y1="-40" x2="{1.667*scale}" y2="0" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        {get_vector_text(1.667*scale-20, -20, 'Q', '1').replace('fill="black"', 'fill="black" transform="rotate(-30, '+str(1.667*scale-20)+', -20)"')}
    </g>

    <!-- Moments -->
    <path d="M {oAx+30} {oAy+20} A 30 30 0 1 0 {oAx-20} {oAy-20}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oAx-30, oAy-25, 'M', '1')}
    <path d="M {oBx+50} {oBy+20} A 30 30 0 1 0 {oBx+10} {oBy-30}" fill="none" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    {get_vector_text(oBx+15, oBy-35, 'M', '2')}
</svg>
</div>"""

new_content = content[:start_idx] + uzduoties_schema + "\n\n" + skaiciuojamoji_schema + content[end_idx:]

with open('/Users/ugniusvaitiekenas/srotas-ai-agent/fizika/generate_pdf_ready.py', 'w') as f:
    f.write(new_content)
