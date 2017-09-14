from __future__ import absolute_import

from janus.config      import BaseConfig
from janus.util.color import Color

class AppConfig(BaseConfig):
    NAME                 = 'janus'
    VERSION              = (0,0,1)
    LOGO                 = \
"""
    o8o                                            
    `"'                                            
   oooo  .oooo.   ooo. .oo.   oooo  oooo   .oooo.o 
   `888 `P  )88b  `888P"Y88b  `888  `888  d88(  "8 
    888  .oP"888   888   888   888   888  `"Y88b.  
    888 d8(  888   888   888   888   888  o.  )88b 
    888 `Y888""8o o888o o888o  `V88V"V8P' 8""888P' 
    888                                            
.o. 88P                                            
`Y888P    """
    COLOR_PRIMARY        = Color.BLUE

    WINDOW_ASPECT_RATIO  = 3 / 2
    WINDOW_WIDTH         = 320
    WINDOW_HEIGHT        = int(WINDOW_WIDTH * WINDOW_ASPECT_RATIO)

    PLOT_STYLE           = 'seaborn'

    ENVIRONMENT_VARIABLE = {
        'tiingo_api_key': 'BULBEA_TIINGO_API_KEY'
    }