from components.detectors import fixation_detection
from components.plot_fixations import plot_path, plot_fixations_points
import pandas as pd

FILENAME = 'all_gaze_data-958009508617'
IMAGENAME = 'liberte1080.jpg'


def process(filename=FILENAME, imagename=IMAGENAME, default_path=''):
    df = pd.read_excel(default_path + r'data/' + filename + '.xlsx')
    print(df.shape)
    df = df[(df['left_gaze_point_validity'] == 1) | (df['right_gaze_point_validity'] == 1)].reset_index()
    print(df.shape)

    df['x'] = df['x'].astype(int)
    df['y'] = df['y'].astype(int)

    maxdist = 175
    # for maxdist in [100, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400]:
    Sfix, Efix = fixation_detection(df['x'], df['y'], df['system_time_stamp'], maxdist=maxdist, mindur=20)
    df_fixations = pd.DataFrame(data=Efix, columns=['starttime', 'endtime', 'duration', 'x', 'y'])

    df_fixations = df_fixations.sort_values(by=['starttime'])
    df_fixations = df_fixations[['starttime', 'endtime', 'duration', 'x', 'y']]
    df_fixations.to_excel(default_path + r'processed_data/' + filename + '-fixations.xlsx', index=False)


    # plot_path(df['x'], df['y'], imagename, linewidth=0.3, markersize=0.6, default_path=default_path)
    plot_fixations_points(df_fixations['x'], df_fixations['y'], df_fixations['duration'], imagename, default_path=default_path,
                          output_ind=str(maxdist))


if __name__ == '__main__':
    process(FILENAME, IMAGENAME, default_path=r'../')
