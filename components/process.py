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
    print(df['mean_pupil_diameter'])
    Sfix, Efix = fixation_detection(df['x'], df['y'], df['mean_pupil_diameter'], df['system_time_stamp'],
                                    maxdist=maxdist, mindur=mindur)

    df_fixations = pd.DataFrame(data=Efix, columns=['starttime', 'endtime', 'duration', 'x', 'y', 'dilatation'])

    df_fixations = df_fixations.sort_values(by=['starttime'])

    return df_fixations


def normalize_col(col):
    norm = (col - min(col)) / (max(col) - min(col))
    return norm


def process_one_image(df, filename=FILENAME, imagename=IMAGENAME, default_path='', maxdist=175, mindur=2000):

    df_fixations = process_fixations(df, maxdist, mindur)

    df_fixations.to_csv(default_path + r'processed_data/' + filename + '-fixations.csv', index=False)

    plotly_fixations_points(df_fixations, imagename,
                            default_path=default_path,
                            output_ind=str(maxdist))


def process_many_images(dict_images, df, filename, default_path='', maxdist=175, mindur=2000):

    df_fixations = process_fixations(df, maxdist, mindur)
    df_fixations.to_csv(default_path + r'processed_data/' + filename + '-fixations.csv', index=False)

    df_fixations['dilatation'] = df_fixations['dilatation'].fillna(35)

    df_fixations['norm_dilatation'] = normalize_col(df_fixations['dilatation']) * 1500


    export_video(df_fixations, dict_images, filename, default_path)


if __name__ == '__main__':
    FILENAME = 'all_gaze_data-533914344803'
    #df = pd.read_excel(r'../data/' + FILENAME + '.xlsx')
    #process_fixations(df)
