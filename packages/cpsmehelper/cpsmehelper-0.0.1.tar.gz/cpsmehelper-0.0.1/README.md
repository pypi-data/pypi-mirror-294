# Export Figure Function

The CPSME has developed a function enabling users to effortlessly export Python matplotlib figures to .png, .svg, .pdf, and .tikz files. This function is called [export_figure()](https://git.tu-berlin.de/merten.stender/cpsme-wiki/-/blob/main/corporate_identity/export_figure.py?ref_type=heads).

```python
def export_figure(fig, 
                  name: str, 
                  savedir: str = None, 
                  style: str = None, 
                  width: float = None, 
                  height: float = None, 
                  resolution: int = 300)
```
Users can customize several parameters according to their preferences, which then will be reflected in the exported file. A quick explanation of the parameters, peculiarities as well as a minimal working example of how to use the function can be found below.

## Parameters
<details><summary>fig</summary>
Needs to be set to the plt figure object, that is to be exported.
</details>
<details><summary>name</summary>
Sets the file name and needs to include the desired file ending.
</details>
<details><summary>savedir</summary>
Sets the directory, where the file is saved. The default is set to the current working directory.
</details>
<details><summary>style</summary>
Several predefined styles can be set. Those styles determine the width and height of the exported file.<br>
For presentations, based on the CPSME guidelines:<ul>
<li> <b>presentation_1x1</b>  indicates a full PowerPoint textbox
<li> <b>presentation_1x2</b>  indicates a PowerPoint textbox split into halves in width 
<li> <b>presentation_1x3</b>  indicates a PowerPoint textbox split into thirds in width 
<li> <b>presentation_2x1</b>  indicates a PowerPoint textbox split into halves in height
<li> <b>presentation_2x2</b>  indicates a PowerPoint textbox split into halves in height and halves in width 
<li> <b>presentation_2x3</b>  indicates a PowerPoint textbox split into halves in height and thirds in width
</ul>
</details>
<details><summary>width</summary>
Sets the exported file to an individually set width. Over-writes the style argument.
</details>
<details><summary>height</summary>
Sets the exported file to an individually set height. Over-writes the style argument.
</details>
<details><summary>resolution</summary>
Sets the resolution of the .png file. The default DPI is set to 300.
</details>


## Peculiarities
- for plots with equal axes the input for the width is favored 
- small offsets can happen randomly
- when exporting .tikz files the compatibility of Matplotlib and the library used for exporting the .tikz file needs to be accounted for; more detailed information can be found in the [Exporting .tikz files from Python Matplotlib](https://git.tu-berlin.de/merten.stender/cpsme-wiki/-/wikis/home/How-To/Export-.tikz-files-from-Python-Matplotlib) entry


## Minimal Working Example
```python
import numpy as np
from matplotlib import pyplot as plt

# import export_figure function from cpsmehelper library
from cpsmehelper import export_figure
from export_figure import export_figure

# create plot 
data = np.random.randn(10)
fig, ax = plt.subplots()
ax.plot(data, data)
ax.plot(data, -data)
plt.xlabel('xlabel')
plt.ylabel('ylabel')
plt.legend(['some data', 'different data'])

# export figure to a .svg file with a set presentation style of one full PP textbox
export_figure(fig, name='test_presentation_1x1.svg', style='presentation_1x1')
```

# Custom Colors Set

The cpsme has a set of 'official' colors, which can be seen below. The gradation of colors from 1 to 4 indicates a gradient from light to dark. The `get_colors()` function can be used to load a dict of the color set, which can then be used as shown in the minimal working example below. The colors are called according to the 'variable' parameter in the table below.

| variable | rgb (decimal) | RGB (percentage) | # hash| usage
| ------ | ------ | ------ | ------ | ------ |
| cpsme_black | 50, 50, 50 | 19.6, 19.6, 19.6 | `#323232`| font for highlight box 1|
| cpsme_white | 250, 250, 250 | 98, 98, 98 | `#FAFAFA` | font for highlight box 2 |
| cpsme_blue_4 | 29, 53, 87 | 11.4, 20.8, 34.1 | `#1D3557`| icons, plots |
| cpsme_red | 230, 57, 70 | 90.2, 22.4, 27.5 | `#E63946` | attention color, highlights, icons |
| cpsme_green | 0, 182, 149 | 0, 71.4, 58.4 | `#00b695`| highlights, icons |
| cpsme_blue_2 | 0, 139, 154 | 0, 54.5, 60.4 | `#008b9a`| plots |
| cpsme_blue_3| 69, 123, 157 | 27.1, 48.2, 61.6| `#457B9D`| plots |
| cpsme_blue_1 | 168, 218, 220 | 65.9, 85.5, 86.3 | `#A8DADC`| plots |
| cpsme_grey_4 | 100, 100, 100 | 39.2, 39.2, 39.2 | `#646464`| filling for highlight box 2|
| cpsme_grey_1 | 225, 225, 225 | 88.2, 88.2, 88.2 | `#E1E1E1`| filling for highlight box 1|
| cpsme_grey_2 | 200, 200, 200 | 78.4, 78.4, 78.4 | `#C8C8C8`| plots |
| cpsme_grey_3 | 150, 150, 150 | 58.8, 58.8, 58.8 | `#969696`| plots |
| cpsme_mint_green | 241, 250, 238 | 94.5, 98, 93.3 | `#F1FAEE`| plots |

## Minimal Working example

```python
import matplotlib.pyplot as plt
import numpy as np

# import dict for cpsme colors
import cpsmehelper
from cmpsmehelper import get_colors
from get_colors import get_colors

cpsme_colors = get_colors()


# generate data
x = np.linspace(0, 10, 100)  # 100 points from 0 to 10
y = np.sin(x)                # sine function

# create the plot
plt.figure(figsize=(8, 5))
plt.plot(x, y, label='Sine Wave', color=cpsme_colors['cpsme_red'], linestyle='-', marker='o')  # use cpsme red for plot

# add labels and title
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Simple Sine Wave Plot')
plt.grid(True)
plt.legend()

# show the plot
plt.show()
```