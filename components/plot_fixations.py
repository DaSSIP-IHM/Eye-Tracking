import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import cv2
import os
import copy
import numpy as np
import plotly.express as px

def plotly_fixations_points(df, image_name, res, default_path='', output_ind=''):

    fig = go.Figure()
    # x, y, duration

    x_res = res[0]
    y_res = res[1]

    n = [x for x in range(1, len(df['x']) + 1)]

    hoverduration = df['duration'] * 100 / max(df['duration'])

    df['duration'] = df['duration'] / 1000000

    hovertext = '<b>Durée</b> : ' + df['duration'].round(2).astype(str) + 's<br><b>Moyenne de dilatation</b> :' + df[
        'mean_dilatation'].round(2).astype(str) + 'mm<br><b>Fixation n°</b> ' + (df.index + 1).astype(str)

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


def export_video(df_fixations, first_timestamp, default_path='', fps=16, res=(1920,1080)):
    path = default_path + 'images/' + first_timestamp

    out = cv2.VideoWriter(default_path + 'videos/' + first_timestamp + '.avi', cv2.VideoWriter_fourcc(*'DIVX'),
                          fps=fps, frameSize=res)

    for picname in os.listdir(path):
        imagename, file_extension = os.path.splitext(picname)

        path_file = path + r'/' + imagename + file_extension
        print(path_file)
        img = cv2.imread(path_file)

        temp_df = df_fixations[
            (df_fixations['starttime'] <= int(imagename)) & (df_fixations['endtime'] > int(imagename))]

        x = temp_df['x']
        y = temp_df['y']
        radius = temp_df['norm_dilatation']
        if len(x) == 1:
            overlay = img.copy()
            circle = cv2.circle(overlay, center=(x, y), radius=radius, color=(255, 135, 111), thickness=-1)
            alpha = 0.4
            img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
        out.write(img)
    out.release()


'''
def boxplot(df):
    lst_col = 'list_dilats'

    r = pd.DataFrame({
        col: np.repeat(df[col].values, df[lst_col].str.len())
        for col in df.columns.drop(lst_col)}
    ).assign(**{lst_col: np.concatenate(df[lst_col].values)})[df.columns]



    fig = px.box(r, x="starttime", y="list_dilats")
    fig.show()

    print(r)

def plot_path(x, y, image_name, linewidth, markersize, default_path=''):
    print('This function plot_path is deprecated.')
    image_name = default_path + 'examples/liberte1080.jpg'
    im = plt.imread(image_name)
    implot = plt.imshow(im)

    plt.plot(x, y, linewidth=linewidth, markersize=markersize)
    plt.savefig(default_path + 'examples/testplot_path.png', dpi=300)
    plt.show()
'''