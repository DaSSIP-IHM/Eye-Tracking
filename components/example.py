from components.detectors import *
from components.plot_fixations import plot_path, plotly_fixations_points, matplotlib_fixations_points
import pandas as pd

FILENAME = 'all_gaze_data-958009508617'
IMAGENAME = 'liberte1080.jpg'




def process_fixations(filename=FILENAME, default_path=''):
    df = pd.read_excel(default_path + r'data/' + filename + '.xlsx')
    print(df.shape)
    df = df[(df['left_gaze_point_validity'] == 1) | (df['right_gaze_point_validity'] == 1)].reset_index()
    print(df.shape)

    df['x'] = df['x'].astype(int)
    df['y'] = df['y'].astype(int)

    df['mean_pupil_diameter'] = (df['left_pupil_diameter'] + df['right_pupil_diameter']) / 2
    # for maxdist in [100, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400]:
    # Sfix, Efix = old_fixation_detection(df['x'], df['y'], df['system_time_stamp'], maxdist=maxdist, mindur=2000)
    # print(Sfix)
    maxdist = 175
    Sfix, Efix = fixation_detection(df['x'], df['y'], df['mean_pupil_diameter'], df['system_time_stamp'],
                                    maxdist=maxdist, mindur=2000)

    df_fixations = pd.DataFrame(data=Efix, columns=['starttime', 'endtime', 'duration', 'x', 'y', 'dilatation'])

    df_fixations = df_fixations.sort_values(by=['starttime'])

    df_fixations.to_excel(default_path + r'processed_data/' + filename + '-fixations.xlsx', index=False)
    # print(df)
    return df_fixations

def process_one_image(filename=FILENAME, imagename=IMAGENAME, default_path=''):
    df_fixations = process_fixations(filename, default_path)
    # plot_path(df['x'], df['y'], imagename, linewidth=0.3, markersize=0.6, default_path=default_path)
    plotly_fixations_points(df_fixations, imagename,
                            default_path=default_path,
                            output_ind=str(175))

def process_many_images(filename=FILENAME, imagename=IMAGENAME, default_path=''):
    df_fixations = process_fixations(filename, default_path)


if __name__ == '__main__':
    process_one_image(FILENAME, IMAGENAME, default_path=r'../')
