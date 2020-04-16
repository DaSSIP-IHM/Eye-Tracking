import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import plotly.express as px

# df = pd.read_excel('../gaze_data/analyze/all_gaze_data-952409502500-analyze.xlsx')


def plotly_fixations_points(x, y, duration, image_name, default_path='', output_ind=''):
    image_name = default_path + 'examples/liberte1080.jpg'
    fig = go.Figure()

    n = [x for x in range(1, len(x) + 1)]


    hoverduration = duration * 60 / max(duration)

    duration =duration / 1000000
    print(duration.sum)

    hovertext = '<b>Durée</b> : ' + duration.astype(str) + 's<br><b>Fixation n°</b> ' + duration.index.astype(str)

    # Add trace
    fig.add_trace(
        go.Scatter(x=x, y=y, mode='markers', marker_size=hoverduration, hoverinfo="text",
                   hovertext=hovertext)
    )
    fig.update_layout(title='La liberté guidant le peuple', xaxis=dict(range=[0, 1920], showgrid=False),
                      yaxis=dict(range=[1080, 0], showgrid=False, scaleanchor="x", scaleratio=1), height=1080,
                      width=1820)
    # Add images
    fig.add_layout_image(
        dict(
            source=Image.open(image_name),
            xref="x",
            yref="y",
            x=0,
            y=0,
            sizex=1920,
            sizey=1080,
            sizing="stretch",
            opacity=1,
            layer="below")
    )

    fig.show()
    fig.write_html(default_path + 'examples/testplot_points' + output_ind + '.html')



def plot_path(x, y, image_name, linewidth, markersize, default_path=''):
    image_name = default_path + 'examples/liberte1080.jpg'
    im = plt.imread(image_name)
    implot = plt.imshow(im)

    plt.plot(x, y, linewidth=linewidth, markersize=markersize)
    plt.savefig(default_path + 'examples/testplot_path.png', dpi=300)
    plt.show()


def matplotlib_fixations_points(x, y, image_name, pointsize, default_path='', output_ind=''):
    image_name = default_path + 'examples/liberte1080.jpg'
    im = plt.imread(image_name)
    implot = plt.imshow(im)

    n = [x for x in range(1, len(x) + 1)]
    # plt.scatter(x, y, c='r', s=pointsize)

    for i, txt in enumerate(n):
        plt.text(x[i], y[i], txt, c='r', fontsize=3)

    plt.savefig(default_path + 'examples/testplot_points' + output_ind + '.png', dpi=300)
    plt.show()
