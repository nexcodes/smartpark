"""
Modern UI Theme Configuration for SmartPark
Centralized color scheme and styling constants
"""

class Theme:
    """Centralized theme configuration"""
    
    # Color Palette - Modern and Professional
    COLORS = {
        # Primary Colors
        'primary': '#2563eb',          # Blue - Main brand color
        'primary_dark': '#1d4ed8',     # Darker blue for hover states
        'primary_light': '#3b82f6',    # Lighter blue
        
        # Secondary Colors
        'secondary': '#10b981',        # Green
        'secondary_dark': '#16a34a',   # Darker green
        
        # Status Colors
        'success': '#22c55e',          # Success green
        'danger': '#ef4444',           # Error red
        'danger_dark': '#dc2626',      # Darker red
        'warning': '#f59e0b',          # Warning orange
        'warning_dark': '#d97706',     # Darker orange
        'info': '#3b82f6',            # Info blue
        
        # Neutral Colors
        'dark': '#1e293b',            # Dark blue-gray (headers, text)
        'gray': '#64748b',            # Medium gray (secondary text)
        'light_gray': '#94a3b8',      # Light gray (placeholders)
        'lighter_gray': '#cbd5e1',    # Even lighter gray
        'lightest_gray': '#e2e8f0',   # Border color
        'background': '#f8fafc',      # Main background
        'card_bg': '#ffffff',         # Card background
        
        # Special Colors
        'purple': '#8b5cf6',          # Purple accent
        'purple_dark': '#7c3aed',     # Darker purple
        
        # Info backgrounds
        'info_bg': '#dbeafe',         # Light blue background
        'info_border': '#3b82f6',     # Blue border
        'info_text': '#1e40af',       # Dark blue text
    }
    
    # Typography
    FONTS = {
        'family': 'Segoe UI',
        'family_mono': 'Consolas',
        'size_title': 24,
        'size_subtitle': 20,
        'size_heading': 14,
        'size_body': 11,
        'size_small': 10,
        'size_tiny': 9,
    }
    
    # Spacing
    SPACING = {
        'xs': 5,
        'sm': 10,
        'md': 15,
        'lg': 20,
        'xl': 25,
        'xxl': 30,
    }
    
    # Component Styles
    BUTTON_STYLE = {
        'relief': 'flat',
        'cursor': 'hand2',
        'padx': 20,
        'pady': 10,
    }
    
    CARD_STYLE = {
        'bg': COLORS['card_bg'],
        'highlightbackground': COLORS['lightest_gray'],
        'highlightthickness': 1,
    }
    
    @staticmethod
    def get_button_style(color_type='primary'):
        """Get button styling for a specific color type"""
        color_map = {
            'primary': (Theme.COLORS['primary'], Theme.COLORS['primary_dark']),
            'success': (Theme.COLORS['success'], Theme.COLORS['secondary_dark']),
            'danger': (Theme.COLORS['danger'], Theme.COLORS['danger_dark']),
            'warning': (Theme.COLORS['warning'], Theme.COLORS['warning_dark']),
            'secondary': (Theme.COLORS['secondary'], Theme.COLORS['secondary_dark']),
        }
        
        bg, active_bg = color_map.get(color_type, color_map['primary'])
        
        return {
            'bg': bg,
            'fg': 'white',
            'activebackground': active_bg,
            'activeforeground': 'white',
            'relief': 'flat',
            'cursor': 'hand2',
            'font': (Theme.FONTS['family'], Theme.FONTS['size_body'], 'bold'),
        }
    
    @staticmethod
    def get_label_style(style_type='title'):
        """Get label styling for a specific type"""
        styles = {
            'title': {
                'font': (Theme.FONTS['family'], Theme.FONTS['size_title'], 'bold'),
                'fg': Theme.COLORS['dark'],
                'bg': Theme.COLORS['background'],
            },
            'subtitle': {
                'font': (Theme.FONTS['family'], Theme.FONTS['size_small']),
                'fg': Theme.COLORS['gray'],
                'bg': Theme.COLORS['background'],
            },
            'heading': {
                'font': (Theme.FONTS['family'], Theme.FONTS['size_heading'], 'bold'),
                'fg': Theme.COLORS['dark'],
                'bg': Theme.COLORS['card_bg'],
            },
            'body': {
                'font': (Theme.FONTS['family'], Theme.FONTS['size_body']),
                'fg': Theme.COLORS['dark'],
                'bg': Theme.COLORS['card_bg'],
            },
        }
        
        return styles.get(style_type, styles['body'])
