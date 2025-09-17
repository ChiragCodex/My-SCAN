"""
table_theme.py
------------------
Purpose:
    Defines a reusable theme for styling tables using the `rich` library.

Functions:
    get_table_headers():
        -> Returns a list of tuples for table headers and their styles.
"""

def get_table_headers():
    """
    Defines the columns and their styles for the rich tables.

    Returns:
        list[tuple]: A list of (column_name, style) tuples.
    """
    return [
        ("Symbol", "bold cyan"),
        ("Stock Name", "bold yellow"),
        ("% Change", "green"),
        ("Lot Size", "White"),
        ("Nearest OTM Strike", "magenta"),
        ("Nearest OTM CE", "bright_blue"),
        ("Nearest OTM PE", "bright_red"),
        ("New OTM Strike", "magenta"),
        ("New OTM CE", "bright_blue"),
        ("New OTM PE", "bright_red"),
        ("CE P/L", "bold yellow")
    ]