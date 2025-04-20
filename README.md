<div align="center" style="display: display_block">

# NTU-Calculator

### Texture Unit Number Reverse Engineering

</div>

<div align="center">
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" width="100" height="100" />
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/streamlit/streamlit-original.svg" width="100" height="100" />
</div>

## Overview

[NTU-Calculator](https://ntu-calculator.streamlit.app/) is a helper tool developed to facilitate the understanding and visualization of the mathematical operations involved in calculating the Texture Unit Number, given the input of a given pixel neighborhood or
or a string of nucleotides in a genetic sequence. The original concepts for which this calculator was developed were discussed by **Li Wang** and **He D. C.**, in a paper entitled **A new statistical approach for texture analysis**[^1]

It was developed using the [Python](https://www.python.org/) programming language, and made available online with the [Streamlit](https://streamlit.io/) framework.

The calculator is available online via the following URL:

`https://ntu-calculator.streamlit.app/`

## Usage

The tool initially will show a page like in the image below, with three buttons and a number input field:

<div align="center">

![image](https://github.com/user-attachments/assets/8b23ad87-e537-42d0-bc7a-36ea2bf58394)

</div>

- **Switch to LBP/LTP Mode**

This button alternates between the **Local Ternary Pattern** (LTP) and **Local Binary Pattern** (LBP) modes for the calculator. The different modes modify the mathematical operations, with LTP performing a summation over the powers of 3, while LBP performs a summation over the powers of 2.

For the calculator tool, in practice this simply alters the upper limit for the number input field, **[0, ..., 6560]** for LTP and **[0, ... 255]** for LBP.

<div align="center">

![image](https://github.com/user-attachments/assets/38829385-759a-4e1a-ad14-cc3e8355f784)

![image](https://github.com/user-attachments/assets/32f5de7c-32cc-4ce0-ac69-6c0e360f1a24)

</div>

---

- **Texture Unit Number**

This input field accepts only numbers, in intervals specific to each mode (**[0, ..., 6560]** for LTP and **[0, ... 255]** for LBP).

By default, each mode will set the value for this input field at the middle of the intervals (3280 for LTP and 127 for LBP).

The value in this input field corresponds to a histogram bin of its respective mode, and is the basis for the Reverse Engineering calculations.

---

- **Calculate**

This button performs the calculations over the value in the Texture Unit Number input field. Based on the number, it will:

- Iterate possible combinations of an array that results in the Texture Unit Number in question
- Provide examples of pixel neighborhoods and string of nucleotides that would result in that array
- Show the calculation table for the array, which results in the Texture Unit Number via summation

The images below show examples of the calculator after using the Calculate button for the default LTP and LBP values:

<div align="center">

![image](https://github.com/user-attachments/assets/97d63016-2d1d-413f-93cd-7e6384e90c7e)

![image](https://github.com/user-attachments/assets/7e8acd56-2e3a-4978-b1dc-88322aa6f557)

</div>

The examples section shows the visualization for the pixel neighborhood that would result in the Texture Unit Array, and a string of nucleotides that would also result in the same array.

<div align="center">

![image](https://github.com/user-attachments/assets/8d86fe9c-b5b7-4e6a-a7e2-55307e8b5cae)

</div>

Each element of the array, `Ei`, for `i = {1, 2, ..., 8}`, is determined by the formulas:

**LTP**
<div align="center">
  
![image](https://github.com/user-attachments/assets/7cbe9bc4-e8ee-4240-a004-7c48c2c7b78a)

</div>

**LBP**
<div align="center">
  
![image](https://github.com/user-attachments/assets/d1d685f2-b1b7-4b0b-8e72-f7ab69809b81)

</div>

Where `Vi` is the value of the `i`th neighbor, and `V0` is the value of the base. In the pixel neighborhood, the base is the central pixel, whereas in the nucleotide string, the base is the leftmost nucleotide (underlined).

These values are then used to calculate the Texture Unit Number, via summation, as shown by the formulas:

**LTP**
<div align="center">
  
![image](https://github.com/user-attachments/assets/64637134-6f2b-4005-9f0b-1e0d9b874870)

</div>

**LBP**
<div align="center">
  
![image](https://github.com/user-attachments/assets/5310f327-bd13-44d5-932e-cd66c6a39eb9)

</div>

When performing the operations over nucleotides, the values considered are the **Electron-Ion Interaction Potential** (EIIP) values, described by **Irena Cosic** in a paper entitled **Macromolecular bioactivity: is it resonant interaction between macromolecules?-theory and applications**[^2].

The EIIP values for each nucleotide are shown in the table:

<div align="center">

| **Nucleotide** | **EIIP** |
|----------------|----------|
| **A**          | 0.1260   |
| **G**          | 0.0806   |
| **T**          | 0.1335   |
| **C**          | 0.1340   |

</div>

---

- **Reset Calculator**

This button is intended for usage after the Calculate button has been used.

The button resets the calculator, clearing away the examples and the calculation table, and setting the mode back to LTP.



## References

[^1]: https://www.asprs.org/wp-content/uploads/pers/1990journal/jan/1990_jan_61-66.pdf
[^2]: https://ieeexplore.ieee.org/abstract/document/335859/


