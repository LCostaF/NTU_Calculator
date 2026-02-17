import streamlit as st
import pandas as pd
from itertools import product
import random
import logging
import pathlib

# Constants
MAX_LTP_VALUE = 6560
MAX_LBP_VALUE = 255

# Set page config must be the first Streamlit command
st.set_page_config(layout="wide", initial_sidebar_state="auto", page_title="Texture Unit Calculator", page_icon=None, menu_items=None)

# Later in the script (best place: right after st.set_page_config)
st.html(pathlib.Path("assets/styles.css"))

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
    Create a grid of squares with grayscale background
    matching the Texture Unit values.
    """
    st.markdown('<div class="section-header">Neighborhood Visualization</div>', unsafe_allow_html=True)

    # Random central pixel (avoid extremes to guarantee space on both sides)
    central_pixel = random.randint(32, 223)

    aux_neighbors = []

    for value in tu_array:
        if mode == 'LTP':
            if value == 0:
                # strictly less than central
                neighbor = random.randint(0, central_pixel - 1)
            elif value == 1:
                # equal to central
                neighbor = central_pixel
            else:
                # strictly greater than central
                neighbor = random.randint(central_pixel + 1, 255)
        else:  # LBP
            if value == 0:
                # less than central
                neighbor = random.randint(0, central_pixel - 1)
            else:
                # greater or equal to central
                neighbor = random.randint(central_pixel, 255)

        aux_neighbors.append(neighbor)

    def build_cell(value):
        bg_color = f"rgb({value},{value},{value})"
        text_color = "white" if value < 90 else "black"

        return f'<div class="grid-cell" style="background-color:{bg_color}; color:{text_color};">{value}</div>'

    grid_html = (
        '<div class="grid-container">'
        + build_cell(aux_neighbors[0])
        + build_cell(aux_neighbors[1])
        + build_cell(aux_neighbors[2])
        + build_cell(aux_neighbors[7])
        + build_cell(central_pixel)
        + build_cell(aux_neighbors[3])
        + build_cell(aux_neighbors[6])
        + build_cell(aux_neighbors[5])
        + build_cell(aux_neighbors[4])
        + '</div>'
    )

    st.markdown(grid_html, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Nucleotide Example</div>', unsafe_allow_html=True)
    st.write("9-nucleotides matching sequence:")

    nucleotide_values = {'G': 0.0806,
                         'A': 0.1260,
                         'T': 0.1335,
                         'C': 0.1340}
    
    aminoacid_values = {'Leu': 0.0000,
                        'Ile': 0.0000,
                        'Asn': 0.0036,
                        'Gly': 0.0050,
                        'Val': 0.0057,
                        'Glu': 0.0058,
                        'Pro': 0.0198,
                        'His': 0.0242,
                        'Lys': 0.0371,
                        'Ala': 0.0373,
                        'Tyr': 0.0516,
                        'Trp': 0.0548,
                        'Gln': 0.0761,
                        'Met': 0.0823,
                        'Ser': 0.0829,
                        'Cys': 0.0829,
                        'Thr': 0.0941,
                        'Phe': 0.0946,
                        'Arg': 0.0959,
                        'Asp': 0.1263}

    values = sorted(nucleotide_values.values())
    min_val = values[0]
    max_val = values[-1]

    if mode == 'LTP':
        if 2 in tu_array and 0 in tu_array:
            # central must not be min or max
            valid_central_chars = [
                k for k, v in nucleotide_values.items()
                if min_val < v < max_val
            ]
        elif 2 in tu_array:
            # central cannot be maximum
            valid_central_chars = [
                k for k, v in nucleotide_values.items()
                if v < max_val
            ]
        elif 0 in tu_array:
            # central cannot be minimum
            valid_central_chars = [
                k for k, v in nucleotide_values.items()
                if v > min_val
            ]
        else:
            valid_central_chars = list(nucleotide_values.keys())
    else:  # LBP
        if 0 in tu_array:
            valid_central_chars = [
                k for k, v in nucleotide_values.items()
                if v > min_val
            ]
        else:
            valid_central_chars = list(nucleotide_values.keys())


    central_char = random.choice(valid_central_chars)
    central_value = nucleotide_values[central_char]

    neighbors = []
    for value in tu_array:
        if mode == 'LTP':
            if value == 0:
                neighbor_char = random.choice([k for k, v in nucleotide_values.items() if v < central_value])
            elif value == 1:
                neighbor_char = central_char
            else:
                neighbor_char = random.choice([k for k, v in nucleotide_values.items() if v > central_value])
        else:
            if value == 0:
                neighbor_char = random.choice([k for k, v in nucleotide_values.items() if v < central_value])
            else:
                neighbor_char = random.choice([k for k, v in nucleotide_values.items() if v >= central_value])
        neighbors.append(neighbor_char)

    string_example = ''.join([central_char] + neighbors)

    st.markdown(
        f'<div class="string-example"><span class="central">{string_example[0]}</span>{string_example[1:]}</div>',
        unsafe_allow_html=True
    )

    # -------------------------
    # Aminoacid Example
    # -------------------------
    st.markdown('<div class="section-header">Aminoacid Example</div>', unsafe_allow_html=True)
    st.write("9-aminoacids matching sequence:")

    values = sorted(aminoacid_values.values())
    min_val = values[0]
    max_val = values[-1]

    if mode == 'LTP':
        if 2 in tu_array and 0 in tu_array:
            valid_central_chars = [
                k for k, v in aminoacid_values.items()
                if min_val < v < max_val
            ]
        elif 2 in tu_array:
            valid_central_chars = [
                k for k, v in aminoacid_values.items()
                if v < max_val
            ]
        elif 0 in tu_array:
            valid_central_chars = [
                k for k, v in aminoacid_values.items()
                if v > min_val
            ]
        else:
            valid_central_chars = list(aminoacid_values.keys())
    else:
        if 0 in tu_array:
            valid_central_chars = [
                k for k, v in aminoacid_values.items()
                if v > min_val
            ]
        else:
            valid_central_chars = list(aminoacid_values.keys())

    central_char = random.choice(valid_central_chars)
    central_value = aminoacid_values[central_char]

    neighbors = []
    for value in tu_array:
        if mode == 'LTP':
            if value == 0:
                neighbor_char = random.choice(
                    [k for k, v in aminoacid_values.items() if v < central_value]
                )
            elif value == 1:
                neighbor_char = central_char
            else:
                neighbor_char = random.choice(
                    [k for k, v in aminoacid_values.items() if v > central_value]
                )
        else:
            if value == 0:
                neighbor_char = random.choice(
                    [k for k, v in aminoacid_values.items() if v < central_value]
                )
            else:
                neighbor_char = random.choice(
                    [k for k, v in aminoacid_values.items() if v >= central_value]
                )

        neighbors.append(neighbor_char)

    amino_string = [central_char] + neighbors

    st.markdown(
        f'<div class="string-example"><span class="central">{amino_string[0]}</span>{"".join(amino_string[1:])}</div>',
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
                    with row1_col1:
                        st.markdown('<div class="section-header">Texture Unit Array</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="array-display">{{{", ".join(map(str, tu_array))}}}</div>', unsafe_allow_html=True)
                    with results_col1:
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

                        # Prepare DataFrame
                        df = pd.DataFrame(
                            {
                                "i Value": [row[0] for row in rows],
                                f"Power of {'3' if st.session_state.mode == 'LTP' else '2'}": [row[1] for row in rows],
                                "Array value": [row[2] for row in rows],
                                "Iteration sum": [row[3] for row in rows],
                                "Cumulative bin sum": [row[4] for row in rows],
                            }
                        )

                        # Hide index
                        st.dataframe(
                            df,
                            use_container_width=True,
                            hide_index=True
                        )

                        # Resulting Bin with success message styling
                        st.markdown(f'<div class="success-message">Resulting Bin = {tu_number}</div>', unsafe_allow_html=True)
                else:
                    st.error(f"No tu_array found for the target Texture Unit number {tu_number}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            st.error(f"An error occurred: {e}")