import svgwrite
import time

from .themes.circles_theme import CirclesTheme
from .themes.default_highres import DefaultHighResTheme
from .themes.default import DefaultTheme

def create(data, settings={}):
    
    # Initialize the theme based on the template parameter
    theme_name = settings.get('theme_name', 'default') or 'default'
    color_scheme = settings.get('color_scheme', 'main') or 'main'

    if theme_name == 'circles':
        theme = CirclesTheme(data, settings)
    elif theme_name == 'default_highres':
        theme = DefaultHighResTheme(data, settings)
    else:  # default theme
        theme = DefaultTheme(data, settings)

    # Check if the color scheme passed in settings is available in the theme
    if color_scheme not in theme.COLOR_SCHEMES:
        raise ValueError(f"Color scheme '{color_scheme}' is not available in the theme.")        

    # Calculate the viewBox parameters
    bounds = theme.get_entity_bounds()    
    viewbox_width = bounds['max_x'] - bounds['min_x']
    viewbox_height = bounds['max_y'] - bounds['min_y']
    
    # Create the SVG drawing object optimized for screen
    dwg = svgwrite.Drawing(
        profile='full',
        size=('100%', '100%'),
        viewBox=f"0 0 {viewbox_width} {viewbox_height}"
    )

    # Do the rendering
    theme.render(dwg) 
    svg_string = dwg.tostring()
    
    # Prepare the return dictionary
    result = {
        'svg_string': svg_string,
        'bounds': bounds,
        'viewbox': {
            'x': 0,
            'y': 0,
            'width': viewbox_width,
            'height': viewbox_height
        },
        'theme_name': theme_name,   
    }

    return result
