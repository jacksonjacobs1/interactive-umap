from dash import Dash, dcc, html, Input, Output, no_update
import plotly.graph_objects as go
import pandas as pd
import h5py
from dash_canvas.utils import array_to_data_url
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data_path', type=str)
parser.add_argument('--plot_title', type=str)
args = parser.parse_args()

data_path = args.data_path
plot_title = args.plot_title

with h5py.File(data_path, 'r') as f:

	df = pd.DataFrame({
		"x_coords": f['umap_coords'][:].T[0],
		"y_coords": f['umap_coords'][:].T[1],
		"colors": f['ground_truth_label'][:],
		"fnames": f['fname'][:]
	})


fig = go.Figure(data=[
	go.Scatter(
		x=df["x_coords"],
		y=df["y_coords"],
		mode="markers",
		marker=dict(
			colorscale='viridis',
			color=df["colors"],
			# size=df["MW"],
			colorbar={"title": "image label"},
			line={"color": "#444"},
			reversescale=True,
			sizeref=45,
			sizemode="diameter",
			opacity=0.8,
		)
	)
])

# turn off native plotly.js hover effects - make sure to use
# hoverinfo="none" rather than "skip" which also halts events.
fig.update_traces(hoverinfo="none", hovertemplate=None)

fig.update_layout(
	xaxis=dict(title='x axis'),
	yaxis=dict(title='y axis'),
	plot_bgcolor='rgba(124,159,247,0.5)',
	height=800,
	title={'text': plot_title,
			'x':0.5,}
)
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)


app = Dash(__name__)

app.layout = html.Div([
	dcc.Graph(id="graph-basic-2", figure=fig, clear_on_unhover=True),
	dcc.Tooltip(id="graph-tooltip"),
])


@app.callback(
	Output("graph-tooltip", "show"),
	Output("graph-tooltip", "bbox"),
	Output("graph-tooltip", "children"),
	Input("graph-basic-2", "hoverData"),
)
def display_hover(hoverData):
	if hoverData is None:
		return False, no_update, no_update

	# demo only shows the first point, but other points may also be available
	pt = hoverData["points"][0]
	bbox = pt["bbox"]
	num = pt["pointNumber"]
	with h5py.File(data_path, 'r') as f:
		img = np.array(f['patch'][num][:,:,:], dtype='uint8')
	
	img_src = array_to_data_url(img)
	label = df['colors'][num]
	fn = df['fnames'][num].decode()
	# df_row = df.iloc[num]
	# img_src = df_row['IMG_URL']
	# name = df_row['NAME']
	# form = df_row['FORM']
	# desc = df_row['DESC']
	# if len(desc) > 300:
	#     desc = desc[:100] + '...'

	children = [
		html.Div([
			html.Img(src=img_src, style={"width": "100%"}),
			# html.H2(f"{name}", style={"color": "darkblue"}),
			html.P(f"label: {label}"),
			html.P(f"file name: {fn}"),
		], style={'width': '200px', 'white-space': 'normal'})
	]

	return True, bbox, children


if __name__ == "__main__":
	app.run_server(debug=True)