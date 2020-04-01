from detectors import *
from plot_fixations import *

FILENAME = 'all_gaze_data-958009508617'
IMAGENAME = 'liberte1080.jpg'

def test(filename=FILENAME, imagename=IMAGENAME):
    df = pd.read_excel(r'gaze_data/' + filename + '.xlsx')

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
    df_output.to_excel('gaze_data/analyze/' + filename + '-analyze.xlsx', index=False)

    #plot_fixations_points(df['x'], df['y'], image_name, 1)
    plot_fixations_path(df['x'], df['y'], imagename, linewidth=0.3, markersize=0.6)
    plot_fixations_points(df_output['startx'], df_output['starty'], imagename, 0.2)

if __name__ == '__main__':

    test()