from detectors import *
from plot_fixations import *

filename = 'all_gaze_data-952409502500'
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

image_name = 'liberte1080.jpg'

plot_fixations(df['x'], df['y'], image_name, 1)
