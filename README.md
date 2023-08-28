# interactive-umap

A simple Dash app for visualizing a UMAP embedding with hoverable points. On hover, each point will display the image associated with it.

### Prerequisites

1. See requirements.txt for package requirements.

2. You will need a .h5 file with the following keys:

- umap_coords: stores an array of umap coordinates.
- ground_truth_label: stores an array of integers.
- fname: stores an array of strings.
- patch: stores an array of images with the dimension (width, height, n_channels)


### Instructions

1. Open a terminal window.

2. Navigate to the directory containing interactiveUMAP.py

3. Run the script with the following command:

   ```bash
   python interactiveUMAP.py --data_path path/to/your/data --plot_title "Your Plot Title"

4. The locally hosted Dash app may be viewed in your browser.