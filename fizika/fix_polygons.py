import sys, math

with open('/Users/ugniusvaitiekenas/srotas-ai-agent/fizika/generate_kinematics_html_v2.py', 'r') as f:
    content = f.read()

# I need to modify build_polygon to draw angles.
# Let's find build_polygon in the content and replace it.

old_build_polygon = """def build_polygon(origin, vectors, resultant, scale, title):
    svg = SVGBuilder(scale=scale)
    svg.line((-2, 0), (2, 0), color="lightgray")
    svg.line((0, -2), (0, 2), color="lightgray")
    svg.text((2, 0), "x", color="gray", offset=(-10, 15))
    svg.text((0, 2), "y", color="gray", offset=(5, -5))
    svg.circle((0,0), r=3)
    svg.text((0,0), origin, offset=(-15, 15))
    
    cur = (0,0)
    for v, label, sub, offset in vectors:
        nxt = add(cur, v)
        svg.line(cur, nxt, color="black", marker="arrow")
        mid = add(cur, mult(v, 0.5))
        svg.text(mid, label, offset=offset, is_vector=True, sub=sub)
        cur = nxt
    
    if resultant:
        v, label, sub, offset = resultant
        svg.line((0,0), v, color="blue" if label=="V" else "red", marker="arrow-blue" if label=="V" else "arrow-red")
        mid = mult(v, 0.5)
        svg.text(mid, label, offset=offset, color="blue" if label=="V" else "red", is_vector=True, sub=sub)
    
    return f'<div class="schema-container">{svg.render(width=300)}<p><i>{title}</i></p></div>'"""

new_build_polygon = """def build_polygon(origin, vectors, resultant, scale, title):
    svg = SVGBuilder(scale=scale)
    svg.line((-2, 0), (2, 0), color="lightgray")
    svg.line((0, -2), (0, 2), color="lightgray")
    svg.text((2, 0), "x", color="gray", offset=(-10, 15))
    svg.text((0, 2), "y", color="gray", offset=(5, -5))
    svg.circle((0,0), r=3)
    svg.text((0,0), origin, offset=(-15, 15))
    
    def draw_vec_angle(start, vec):
        angle = math.degrees(math.atan2(vec[1], vec[0]))
        norm_ang = angle % 360
        r = 0.3
        # draw a small dashed horizontal line
        svg.line(start, (start[0]+r*1.5, start[1]), color="gray", dash="2,2", width=1)
        # draw arc
        svg.arc(start, r*scale, 0, norm_ang if norm_ang <= 180 else norm_ang - 360, "")
        # draw text
        mx = start[0] + (r*1.5) * math.cos(rad(angle/2))
        my = start[1] + (r*1.5) * math.sin(rad(angle/2))
        svg.text((mx, my), f"{norm_ang:.1f}&deg;", offset=(0, 0), color="gray")

    cur = (0,0)
    for v, label, sub, offset in vectors:
        nxt = add(cur, v)
        svg.line(cur, nxt, color="black", marker="arrow")
        draw_vec_angle(cur, v)
        mid = add(cur, mult(v, 0.5))
        svg.text(mid, label, offset=offset, is_vector=True, sub=sub)
        cur = nxt
    
    if resultant:
        v, label, sub, offset = resultant
        svg.line((0,0), v, color="blue" if label=="V" else "red", marker="arrow-blue" if label=="V" else "arrow-red")
        draw_vec_angle((0,0), v)
        mid = mult(v, 0.5)
        svg.text(mid, label, offset=offset, color="blue" if label=="V" else "red", is_vector=True, sub=sub)
    
    return f'<div class="schema-container">{svg.render(width=300)}<p><i>{title}</i></p></div>'"""

# The scale for arc in polygon is not the global scale, we need to pass a small radius. 
# In build_polygon, the points are already in mathematical scale.
# Let's write a better new_build_polygon.

better_build_polygon = """def build_polygon(origin, vectors, resultant, scale, title):
    svg = SVGBuilder(scale=scale)
    svg.line((-2, 0), (2, 0), color="lightgray")
    svg.line((0, -2), (0, 2), color="lightgray")
    svg.text((2, 0), "x", color="gray", offset=(-10, 15))
    svg.text((0, 2), "y", color="gray", offset=(5, -5))
    svg.circle((0,0), r=3)
    svg.text((0,0), origin, offset=(-15, 15))
    
    def draw_vec_angle(start, vec):
        angle = math.degrees(math.atan2(vec[1], vec[0]))
        norm_ang = angle % 360
        if abs(norm_ang) < 1 or abs(norm_ang - 360) < 1: return
        r = 30.0 / scale # radius in math units so it scales to 30px
        svg.line(start, (start[0]+r*1.5, start[1]), color="gray", dash="2,2", width=1)
        svg.arc(start, 20, 0, norm_ang if norm_ang <= 180 else norm_ang - 360, f"{norm_ang:.0f}&deg;")

    cur = (0,0)
    for v, label, sub, offset in vectors:
        nxt = add(cur, v)
        svg.line(cur, nxt, color="black", marker="arrow")
        draw_vec_angle(cur, v)
        mid = add(cur, mult(v, 0.5))
        svg.text(mid, label, offset=offset, is_vector=True, sub=sub)
        cur = nxt
    
    if resultant:
        v, label, sub, offset = resultant
        svg.line((0,0), v, color="blue" if label=="V" else "red", marker="arrow-blue" if label=="V" else "arrow-red")
        draw_vec_angle((0,0), v)
        mid = mult(v, 0.5)
        svg.text(mid, label, offset=offset, color="blue" if label=="V" else "red", is_vector=True, sub=sub)
    
    return f'<div class="schema-container">{svg.render(width=300)}<p><i>{title}</i></p></div>'"""

if old_build_polygon in content:
    content = content.replace(old_build_polygon, better_build_polygon)
    print("Replaced build_polygon")
else:
    print("Could not find old_build_polygon")

with open('/Users/ugniusvaitiekenas/srotas-ai-agent/fizika/generate_kinematics_html_v2.py', 'w') as f:
    f.write(content)

