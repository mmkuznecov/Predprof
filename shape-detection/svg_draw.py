import svgwrite

dwg = svgwrite.Drawing('svgwrite-example.svg', profile='tiny')

# draw a red box
dwg.add(dwg.rect((10, 10), (300, 200),
    stroke=svgwrite.rgb(10, 10, 16, '%'),
    fill='red')
)
dwg.save

import webbrowser
browser = webbrowser.get("google-chrome")
browser.open("svgwrite-example.svg")