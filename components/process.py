from components.detectors import *
from components.plot_fixations import *
import pandas as pd
import os

FILENAME = 'all_gaze_data-958009508617'
IMAGENAME = 'liberte1080.jpg'


def process_fixations(df, maxdist=175, mindur=2000):
    print(df.shape)
    df = df[(df['left_gaze_point_validity'] == 1) | (df['right_gaze_point_validity'] == 1)].reset_index()
    print(df.shape)

    df['x'] = df['x'].astype(int)
    df['y'] = df['y'].astype(int)

    df['mean_pupil_diameter'] = (df['left_pupil_diameter'] + df['right_pupil_diameter']) / 2

    # for maxdist in [100, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400]:
    # Sfix, Efix = old_fixation_detection(df['x'], df['y'], df['system_time_stamp'], maxdist=maxdist, mindur=2000)
    # print(Sfix)

    Sfix, Efix = fixation_detection(df['x'], df['y'], df['mean_pupil_diameter'], df['system_time_stamp'],
                                    maxdist=maxdist, mindur=mindur)

    df_fixations = pd.DataFrame(data=Efix, columns=['starttime', 'endtime', 'duration', 'x', 'y', 'dilatation'])

    df_fixations = df_fixations.sort_values(by=['starttime'])

    # print(df)
    return df_fixations


def normalize_col(col):
    norm = (col - min(col)) / (max(col) - min(col))
    return norm


def process_one_image(filename=FILENAME, imagename=IMAGENAME, default_path='', maxdist=175, mindur=2000):
    df = pd.read_excel(default_path + r'data/' + filename + '.xlsx')

    df_fixations = process_fixations(df, maxdist, mindur)

    df_fixations.to_excel(default_path + r'processed_data/' + filename + '-fixations.xlsx', index=False)

    # plot_path(df['x'], df['y'], imagename, linewidth=0.3, markersize=0.6, default_path=default_path)
    plotly_fixations_points(df_fixations, imagename,
                            default_path=default_path,
                            output_ind=str(maxdist))


def process_many_images(filename=FILENAME, default_path='', maxdist=175, mindur=2000):
    df = pd.read_excel(default_path + r'data/' + filename + '.xlsx')

    df_fixations = process_fixations(df, maxdist, mindur)
    df_fixations.to_excel(default_path + r'processed_data/' + filename + '-fixations.xlsx', index=False)

    for directory in [default_path + 'images/' + filename, default_path + 'processed_images/' + filename]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    df_fixations['norm_dilatation'] = normalize_col(df_fixations['dilatation']) * 70

    export_video(df_fixations, filename, default_path)


if __name__ == '__main__':
    # process_one_image(FILENAME, IMAGENAME, default_path=r'../')
    FILENAME = 'all_gaze_data-247733222521'
    process_many_images(FILENAME, default_path=r'../', maxdist=100)