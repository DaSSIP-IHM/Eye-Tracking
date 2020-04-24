import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import cv2
import os


# df = pd.read_excel('../gaze_data/analyze/all_gaze_data-952409502500-analyze.xlsx')


def plotly_fixations_points(df, image_name, default_path='', output_ind=''):
    image_name = default_path + 'examples/liberte1080.jpg'
    fig = go.Figure()
    # x, y, duration

    x_res = 1920
    y_res = 1080

    n = [x for x in range(1, len(df['x']) + 1)]

    hoverduration = df['duration'] * 100 / max(df['duration'])

    df['duration'] = df['duration'] / 1000000
    # print(duration.sum)

    hovertext = '<b>Durée</b> : ' + df['duration'].round(2).astype(str) + 's<br><b>Moyenne de dilatation</b> :' + df[
        'dilatation'].round(2).astype(str) + 'mm<br><b>Fixation n°</b> ' + (df.index + 1).astype(str)

    fig.add_trace(
        go.Scatter(x=df['x'], y=df['y'], mode='markers', marker_size=hoverduration, hoverinfo="text",
                   hovertext=hovertext)
    )

    fig.add_trace(
        go.Scatter(x=df['x'], y=df['y'], hoverinfo='skip', marker_size=3, line=dict(width=1))
    )
    fig.update_layout(title='Affichage des fixations',
                      xaxis=dict(range=[0, x_res], showgrid=False),
                      yaxis=dict(range=[y_res, 0], showgrid=False, scaleanchor="x", scaleratio=1), height=y_res,
                      width=x_res, showlegend=False)

    fig.add_layout_image(
        dict(
            source=Image.open(image_name),
            xref="x",
            yref="y",
            x=0,
            y=0,
            sizex=x_res,
            sizey=y_res,
            sizing="stretch",
            opacity=1,
            layer="below")
    )

    fig.show()
    fig.write_html(default_path + 'examples/testplot_points' + output_ind + '.html')


def export_video(df_fixations, filename, default_path='', fps=30):
    path = default_path + 'images/' + filename

    img_list = []

    for picname in os.listdir(path):
        imagename, file_extension = os.path.splitext(picname)

        path_file = path + r'/' + imagename + file_extension
        print(path_file)
        img = cv2.imread(path_file)

        temp_df = df_fixations[
            (df_fixations['starttime'] <= int(imagename)) & (df_fixations['endtime'] > int(imagename))]

        x = temp_df['x']
        y = temp_df['y']
        size = temp_df['norm_dilatation']
        if len(x) == 1:
            overlay = img.copy()
            cv2.circle(overlay, center=(x, y), radius=size, color=(255, 135, 111), thickness=-1)
            alpha = 0.4
            img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

        height, width, layers = img.shape
        size = (width, height)
        img_list.append(img)

    out = cv2.VideoWriter(default_path + 'videos/' + filename + '.avi', cv2.VideoWriter_fourcc(*'DIVX'),
                          fps=fps, frameSize=size)

    for i in range(len(img_list)):
        out.write(img_list[i])
    out.release()


def plot_path(x, y, image_name, linewidth, markersize, default_path=''):
    print('This function plot_path is deprecated.')
    image_name = default_path + 'examples/liberte1080.jpg'
    im = plt.imread(image_name)
    implot = plt.imshow(im)

    plt.plot(x, y, linewidth=linewidth, markersize=markersize)
    plt.savefig(default_path + 'examples/testplot_path.png', dpi=300)
    plt.show()
