# Theme Colors
theme_colors = {
    'primary': '#007bff',
    'secondary': '#343a40',
    'background': '#ffffff',
    'accent': '#ffc107',
    'text': '#495057',
    'success': '#28a745',
    'error': '#dc3545',
    'info': '#17a2b8'
}

# Base Font Styles
font_styles = {
    'base': '"Arial", sans-serif',
    'heading': '"Helvetica Neue", Arial, sans-serif',
    'text': '"Open Sans", sans-serif'
}

# Base Style
base_style = {
    'textAlign': 'left',
    'borderRadius': '8px',
    'margin': '15px 0',
    'fontFamily': font_styles['base']
}

# Table Styles
table_style = {
    **base_style,
    'overflowX': 'auto',
    'border': '1px solid #dee2e6',
    'borderRadius': '0.375rem',
    'boxShadow': '0 0.5rem 1rem rgba(0, 0, 0, 0.15)',
    'marginTop': '1rem',
}

table_header_style = {
    'color': '#ffffff',
    'backgroundColor': theme_colors['primary'],
    'fontWeight': 'bold',
    'padding': '1rem',
    'borderBottom': '2px solid #dee2e6',
}

table_cell_style = {
    'backgroundColor': theme_colors['background'],
    'color': theme_colors['text'],
    'padding': '0.75rem',
    'borderBottom': '1px solid #dee2e6',
    'textAlign': 'left',
    'fontSize': '0.9rem',
}

# Base Button Style
button_base = {
    'border': 'none',
    'borderRadius': '5px',
    'fontSize': '18px',
    'margin': '10px',
    'cursor': 'pointer',
    'outline': 'none',
}

# Primary and Secondary Button Styles
primary_button_style = {**button_base, 'backgroundColor': theme_colors['primary'], 'color': '#ffffff',
                        'padding': '12px 18px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.12)'}
secondary_button_style = {**button_base, 'backgroundColor': theme_colors['accent'], 'color': '#ffffff',
                          'padding': '12px 18px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}

# Input and Dropdown Styles
input_style = {
    'padding': '12px',
    'border': f"2px solid {theme_colors['secondary']}",
    'borderRadius': '8px',
    'outline': 'none',
    'boxSizing': 'border-box',
    'fontFamily': font_styles['base'],
    'fontSize': '16px',
    'color': theme_colors['text'],
}

dropdown_style = {
    'outline': 'none',
    'boxSizing': 'border-box',
    'fontFamily': font_styles['base'],
    'fontSize': '16px',
    'color': theme_colors['text'],
    'backgroundColor': theme_colors['background'],
    'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.05)',
}

# Text and Heading Styles
text_style = {
    'fontSize': '16px',
    'lineHeight': '1.6',
    'color': theme_colors['text'],
    'fontFamily': font_styles['text'],
}

heading2_style = {
    'fontFamily': font_styles['heading'],
    'fontWeight': '600',
    'color': theme_colors['primary'],
    'textShadow': '0px 1px 2px rgba(0, 0, 0, 0.1)',
    'marginBottom': '15px',
    'paddingTop': '10px',
    'lineHeight': '1.4',
    'textTransform': 'uppercase',
    'letterSpacing': '1px',
}

heading5_style = {
    'fontFamily': font_styles['heading'],
    'fontWeight': '500',
    'color': theme_colors['secondary'],
    'marginBottom': '10px',
    'paddingTop': '5px',
    'lineHeight': '1.3',
    'fontSize': '14px',
    'textTransform': 'none',
    'letterSpacing': '0.5px',
}

# Navigation Styles
navigation_style = {
    'padding': '20px 15px',
    'backgroundImage': 'linear-gradient(to right, #6a11cb 0%, #2575fc 100%)',
    'fontSize': '18px',
    'textAlign': 'center',
    'fontWeight': 'bold',
    'color': 'white',
    'boxShadow': '0 2px 4px 0 rgba(0,0,0,.2)',
}

link_style = {
    'color': 'white',
    'textDecoration': 'none',
    'padding': '5px 15px',
    'fontWeight': '500',
    'display': 'inline-block',
    'transition': 'color 0.3s',
}

navigation_separator_style = {
    'color': 'rgba(255, 255, 255, 0.7)',
    'padding': '0 10px',
}

# User Balance and Error Message Styles
user_balance_style = {
    **base_style,
    'color': theme_colors['secondary'],
    'backgroundColor': '#e2e3e5',
    'padding': '10px 20px',
    'borderRadius': '5px',
    'fontWeight': 'bold',
    'boxShadow': 'inset 0 1px 3px rgba(0,0,0,.3)',
    'fontSize': '20px',
}

error_message_style = {
    **base_style,
    'padding': '12px',
    'border': f"1px solid {theme_colors['error']}",
    'color': theme_colors['error'],
    'backgroundColor': '#fff3cd',
    'borderRadius': '5px',
    'fontWeight': 'bold',
    'display': 'flex',
    'alignItems': 'center',
    'gap': '10px',
}

# Page Content
page_content_style = {'margin': '20px'}
