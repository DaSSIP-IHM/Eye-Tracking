from components.detectors import fixation_detection, saccade_detection
from components.plot_fixations import plot_fixations_path, plot_fixations_points
import pandas as pd
FILENAME = 'all_gaze_data-958009508617'
IMAGENAME = 'liberte1080.jpg'

def test(filename=FILENAME, imagename=IMAGENAME, default_path=''):
    df = pd.read_excel(default_path +r'data/' + filename + '.xlsx')

    print(df)

    Sfix, Efix = fixation_detection(df['x'], df['y'], df['system_time_stamp'], 500)
    df_fixations = pd.DataFrame(data=Efix, columns=['starttime', 'endtime', 'duration', 'endx', 'endy'])
    df_fixations[['startx', 'starty']] = df_fixations[['endx', 'endy']]
    df_fixations['type'] = 'fixation'

    Ssac, Esac = saccade_detection(df['x'], df['y'], df['system_time_stamp'], minlen=40, maxvel=1000)
    df_saccades = pd.DataFrame(data=Esac, columns=['starttime', 'endtime', 'duration', 'startx', 'starty', 'endx', 'endy'])
    df_saccades['type'] = 'saccade'

    df_output = pd.concat([df_fixations, df_saccades])
    df_output = df_output.sort_values(by=['starttime'])
    df_output = df_output[['starttime', 'endtime', 'duration', 'startx', 'starty', 'endx', 'endy', 'type']]
    df_output.to_excel(default_path +r'processed_data/' + filename + '-analyze.xlsx', index=False)

    #plot_fixations_points(df['x'], df['y'], image_name, 1)
    plot_fixations_path(df['x'], df['y'], imagename, linewidth=0.3, markersize=0.6, default_path=default_path)
    plot_fixations_points(df_output['startx'], df_output['starty'], imagename, 0.2, default_path=default_path)

if __name__ == '__main__':

    test(FILENAME, IMAGENAME, default_path=r'../')