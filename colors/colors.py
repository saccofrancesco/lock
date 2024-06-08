# Creating the color palette for the App
NORD_PALETTE = {

    # Polar Night
    'nord0': '#2E3440',
    'nord1': '#3B4252',
    'nord2': '#434C5E',
    'nord3': '#4C566A',

    # Snow Storm
    'nord4': '#D8DEE9',
    'nord5': '#E5E9F0',
    'nord6': '#ECEFF4',

    # Frost
    'nord7': '#8FBCBB',
    'nord8': '#88C0D0',
    'nord9': '#81A1C1',
    'nord10': '#5E81AC',

    # Aurora
    'nord11': '#BF616A',
    'nord12': '#D08770',
    'nord13': '#EBCB8B',
    'nord14': '#A3BE8C',
    'nord15': '#B48EAD',
}

# Method to get color based on given key
def color(key: str) -> str:
    """
    Retrieves the hex color code from the NORD_PALETTE dictionary based on the provided key.

    Args:
        key (str): The key representing the desired color in the NORD_PALETTE.

    Returns:
        str: The hex color code corresponding to the key. Returns None if the key is not found.
    """
    return NORD_PALETTE.get(key, None)

# Method to get a bit more dark shaded color given the nord hex
def darken_color(hex_color, factor=0.8):
    """
    Darkens a given hex color by a specified factor.

    Args:
        hex_color (str): The hex color code to be darkened.
        factor (float, optional): The factor by which to darken the color. Default is 0.8.

    Returns:
        str: The darkened hex color code.

    Example:
        darken_color('#88C0D0', 0.8) -> '#6E99A4'
    """
    # Convert hex to RGB
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

    # Darken RGB components
    darkened_rgb = tuple(int(comp * factor) for comp in rgb_color)

    # Convert back to hex
    darkened_hex = "#{:02X}{:02X}{:02X}".format(*darkened_rgb)

    return darkened_hex
