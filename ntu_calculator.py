import streamlit as st
from itertools import product
import random
import logging

# Constants
MAX_LTP_VALUE = 6560
MAX_LBP_VALUE = 255

# Set page config must be the first Streamlit command
st.set_page_config(layout="wide", initial_sidebar_state="auto", page_title="Texture Unit Calculator", page_icon=None, menu_items=None)

# Initialize session state for mode
if 'mode' not in st.session_state:
    st.session_state.mode = 'LTP'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Reduce header height style
reduce_header_height_style = """
    <style>
        div.block-container {padding-top:1rem;}
    </style>
"""
st.markdown(reduce_header_height_style, unsafe_allow_html=True)

# Custom CSS for styling
custom_css = """
    <style>        
        /* Section headers */
        .section-header {
            color: #2c3e50;
            font-size: 1.2rem;
            font-weight: bold;
            margin: 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #eee;
        }
        
        /* Input section */
        .stNumberInput {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 0.5rem;
        }
        
        /* Button styling */
        .stButton > button {
            border-radius: 5px;
            padding: 0.5rem 1rem;
            background-color: #f8f9fa;
            border: 1px solid #ddd;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background-color: #e9ecef;
            border-color: #bbb;
        }
        
        /* Table styling */
        .stTable {
            border: 2px solid #e0e0e0 !important;
            border-radius: 5px;
            overflow: hidden;
        }
        
        .stTable thead tr th {
            background-color: #f8f9fa !important;
            font-weight: bold !important;
            border-bottom: 2px solid #dee2e6 !important;
            padding: 0.75rem !important;
        }
        
        .stTable tbody tr td {
            padding: 0.75rem !important;
            border-bottom: 1px solid #dee2e6 !important;
        }
        
        /* Grid container for neighborhood visualization */
        .grid-container {
            display: grid;
            grid-template-columns: repeat(3, auto);
            gap: 0;
            justify-content: center;
            margin: 1rem auto;
            width: fit-content;
        }
        
        /* Grid cell styling */
        .grid-cell {
            border: 2px solid #2c3e50;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: monospace;
            background-color: white;
            margin: 0;
        }
        
        /* String example styling */
        .string-example {
            text-align: center;
            font-family: monospace;
            font-size: 1.2rem;
            margin: 1rem 0;
        }
        
        .string-example span.central {
            text-decoration: underline;
        }
        
        /* Array display */
        .array-display {
            font-family: monospace;
            background-color: #f8f9fa;
            padding: 0.5rem;
            border-radius: 5px;
            border: 1px solid #dee2e6;
        }
        
        /* Success message styling */
        .success-message {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 1rem;
            border-radius: 5px;
            margin-top: 1rem;
        }
        
        /* Title styling */
        h1 {
            color: #2c3e50;
            padding-bottom: 1rem;
            border-bottom: 3px solid #eee;
            margin-bottom: 2rem;
        }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Title with dynamic mode
st.title(f"Texture Unit Number Reverse Engineering ({st.session_state.mode} Mode)")


def calc_tu_number(array, mode='LTP'):
    """
    Find the Texture Unit Number based on the Texture Unit array passed (tu_array).
    """
    flank = len(array)
    total_sum = 0

    for i in range(flank):
        if mode == 'LTP':
            term = 3 ** i * array[i]
        else:  # LBP mode
            term = 2 ** i * array[i]
        total_sum += term

    if mode == 'LTP':
        return min(round(total_sum), MAX_LTP_VALUE)
    else:  # LBP mode
        return min(round(total_sum), MAX_LBP_VALUE)


def find_tu_array(tu_number, mode='LTP'):
    """
    Find the tu_array using itertools.product.
    """
    if mode == 'LTP':
        range_values = range(3)
        repeat = 8
    else:  # LBP mode
        range_values = range(2)
        repeat = 8

    for candidate in product(range_values, repeat=repeat):
        candidate_sum = calc_tu_number(candidate, mode)
        if candidate_sum == tu_number:
            return list(candidate)
    return None


def get_neighborhood(tu_array, mode='LTP'):
    """
    Create a grid of squares with the corresponding Texture Unit values and generate a string example.
    """
    st.markdown('<div class="section-header">Neighborhood Visualization</div>', unsafe_allow_html=True)

    if mode == 'LTP':
        # Original logic for LTP mode
        aux_neighbors = [0 if value == 0 else 128 if value == 1 else 255 for value in tu_array]
    else:
        # LBP mode: Randomly choose between 128 and 255 for non-zero values
        aux_neighbors = [0 if value == 0 else random.choice([128, 255]) for value in tu_array]

    # Create the grid container
    grid_html = """
    <div class="grid-container">
        <div class="grid-cell">{}</div>
        <div class="grid-cell">{}</div>
        <div class="grid-cell">{}</div>
        <div class="grid-cell">{}</div>
        <div class="grid-cell">128</div>
        <div class="grid-cell">{}</div>
        <div class="grid-cell">{}</div>
        <div class="grid-cell">{}</div>
        <div class="grid-cell">{}</div>
    </div>
    """.format(
        aux_neighbors[0], aux_neighbors[1], aux_neighbors[2],
        aux_neighbors[7], aux_neighbors[3],
        aux_neighbors[6], aux_neighbors[5], aux_neighbors[4]
    )

    st.markdown(grid_html, unsafe_allow_html=True)

    # Generate a string example based on the tu_array
    st.markdown('<div class="section-header">String Example</div>', unsafe_allow_html=True)
    st.write("One possible 9-character sequence that matches the input array:")
    
    # Define the character values
    char_values = {'G': 1, 'A': 2, 'T': 3, 'C': 4}
    
    # Determine valid central characters based on the tu_array
    if mode == 'LTP':
        if 2 in tu_array and 0 in tu_array:
            valid_central_chars = [k for k, v in char_values.items() if v < 4 and v > 1]
        elif 2 in tu_array:
            # If any neighbor must be greater than the central value, central_char cannot be 'C'
            valid_central_chars = [k for k, v in char_values.items() if v < 4]
        elif 0 in tu_array:
            # If any neighbor must be less than the central value, central_char cannot be 'G'
            valid_central_chars = [k for k, v in char_values.items() if v > 1]
        else:
            # No restrictions on central_char
            valid_central_chars = list(char_values.keys())
    else:  # LBP mode
        if 0 in tu_array:
            # If any neighbor must be less than or equal to the central value, central_char cannot be 'G'
            valid_central_chars = [k for k, v in char_values.items() if v > 1]
        else:
            # No restrictions on central_char
            valid_central_chars = list(char_values.keys())
    
    # Randomly choose a central character from the valid options
    central_char = random.choice(valid_central_chars)
    central_value = char_values[central_char]
    
    # Generate the 8 neighbors based on the tu_array
    neighbors = []
    for value in tu_array:
        if mode == 'LTP':
            if value == 0:
                # Neighbor is less than central value
                neighbor_char = random.choice([k for k, v in char_values.items() if v < central_value])
            elif value == 1:
                # Neighbor is equal to central value
                neighbor_char = central_char
            else:
                # Neighbor is greater than central value
                neighbor_char = random.choice([k for k, v in char_values.items() if v > central_value])
        else:  # LBP mode
            if value == 0:
                # Neighbor is less than central value
                neighbor_char = random.choice([k for k, v in char_values.items() if v < central_value])
            else:
                # Neighbor is greater or equal to than central value
                neighbor_char = random.choice([k for k, v in char_values.items() if v >= central_value])
        neighbors.append(neighbor_char)
    
    # Construct the 9-character sequence
    string_example = ''.join([central_char] + neighbors[:])
    st.markdown(
        f'<div class="string-example"><span class="central">{string_example[0]}</span>{string_example[1:]}</div>',
        unsafe_allow_html=True
    )

# Main layout
row1_col1, row1_col2 = st.columns([1, 3])

# First row - Mode switch and reset buttons
with row1_col1:
    # Toggle button to switch between LTP and LBP modes
    if st.button(
        f"Switch to {'LBP' if st.session_state.mode == 'LTP' else 'LTP'} Mode",
        key="mode_switch_button"
    ):
        st.session_state.mode = 'LBP' if st.session_state.mode == 'LTP' else 'LTP'
        st.rerun()

    # Reset button to clear session state
    if st.button("Reset Calculator", key="reset_button"):
        st.session_state.clear()
        st.rerun()

    # Input field
    max_value = MAX_LTP_VALUE if st.session_state.mode == 'LTP' else MAX_LBP_VALUE
    tu_number = st.number_input(
        "Texture Unit Number:",
        min_value=0,
        max_value=max_value,
        value=max_value // 2,
        step=1,
        format="%d",
        help="Enter a number between 0 and 6560 for LTP mode or 0 and 255 for LBP mode.",
        key="texture_unit_input"
    )

    # Calculate button
    calculate_pressed = st.button("Calculate", key="calculate_button")

# Second row - Results area
with row1_col2:
    # Create two columns for the results
    results_col1, results_col2 = st.columns([1, 2])
    
    if calculate_pressed:
        try:
            # Validate input
            if not isinstance(tu_number, int):
                st.error("Please enter a valid integer.")
            elif tu_number < 0 or tu_number > max_value:
                st.error(f"Please enter a number between 0 and {max_value}.")
            else:
                # Find the tu_array
                tu_array = find_tu_array(tu_number, st.session_state.mode)
                if tu_array:
                    with results_col1:
                        # Input Array
                        st.markdown('<div class="section-header">Texture Unit Array</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="array-display">{{{", ".join(map(str, tu_array))}}}</div>', unsafe_allow_html=True)

                        # Neighborhood example
                        get_neighborhood(tu_array, st.session_state.mode)
                    
                    with results_col2:
                        st.markdown('<div class="section-header">Calculation Table</div>', unsafe_allow_html=True)
                        
                        # Prepare table
                        rows = []
                        for i, value in enumerate(tu_array):
                            if st.session_state.mode == 'LTP':
                                power_of = 3 ** i
                            else:
                                power_of = 2 ** i
                            iteration_sum = value * power_of
                            total_bin = sum(tu_array[j] * (3 if st.session_state.mode == 'LTP' else 2) ** j for j in range(i + 1))
                            rows.append([i, power_of, value, iteration_sum, total_bin])

                        # Display table
                        st.table(
                            {
                                "i Value": [row[0] for row in rows],
                                f"Power of {'3' if st.session_state.mode == 'LTP' else '2'}": [row[1] for row in rows],
                                "Array value": [row[2] for row in rows],
                                "Iteration sum": [row[3] for row in rows],
                                "Cumulative bin sum": [row[4] for row in rows],
                            }
                        )

                        # Resulting Bin with success message styling
                        st.markdown(f'<div class="success-message">Resulting Bin = {tu_number}</div>', unsafe_allow_html=True)
                else:
                    st.error(f"No tu_array found for the target Texture Unit number {tu_number}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            st.error(f"An error occurred: {e}")