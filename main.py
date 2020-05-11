from pynput.mouse import Controller
import tobii_research as tobii
import pandas as pd
import d3dshot
from components.process import *
import time
import gc
import sys

lestobii = tobii.find_all_eyetrackers()
montobii = lestobii[0]
duree = 290  # DUREE DE L'ACQUISITION EN SECONDES
RESOLUTION = (1920, 1080)  # RESOLUTION DE L'ECRAN A DEFINIR
# image = True
mouse = Controller()
image_acquisition = True  # CHOIX SI ACQUISITION DE L'IMAGE A L'ECRAN

print("Son adresse IP: " + montobii.address)
print("Le modèle: " + montobii.model)
print("Son petit nom (souvent vide): " + montobii.device_name)
print("Son numéro de série: " + montobii.serial_number)
print("Et voici le flux durant l.a.es prochaine.s seconde.s : ", duree)

list_positions = []
dict_images = dict()  # DICTIONNAIRE QUI VA CONTENIR TOUTES LES IMAGES SI ON FAIT UNE ACQUISITION
all_gaze_data = []

d = d3dshot.create(capture_output="numpy")
d.display = d.displays[0]


def get_image(name, d):
    """Fonction qui permet de faire un screenshot"""
    im = d.screenshot()
    dict_images[name] = im


def move_mouse(gaze_data):

    """Fonction qui permet de déplacer la souris"""
    x = gaze_data['x']
    y = gaze_data['y']

    list_positions.append((x, y))

    number_mean = 40
    if len(list_positions) > 11:
        x = 0
        y = 0
        for k in range(-number_mean, 0):
            x += list_positions[k][0]
            y += list_positions[k][1]
        x = x / number_mean
        y = y / number_mean

        print(x, y)
    mouse.position = (x, y)


def gaze_data_callback(gaze_data):
    """Fonction qui est appelée à l'acquisition de chaque frame"""
    gaze_data['mouse_position'] = mouse.position
    if gaze_data['left_gaze_point_validity'] == 1 and gaze_data['right_gaze_point_validity']:
        gaze_data['x'] = round(
            (gaze_data['left_gaze_point_on_display_area'][0] + gaze_data['right_gaze_point_on_display_area'][0]) / 2, 2)
        gaze_data['y'] = round(
            (gaze_data['left_gaze_point_on_display_area'][1] + gaze_data['right_gaze_point_on_display_area'][1]) / 2, 2)

    elif gaze_data['left_gaze_point_validity'] == 1 and gaze_data['right_gaze_point_validity'] == 0:
        gaze_data['x'] = gaze_data['left_gaze_point_on_display_area'][0]
        gaze_data['y'] = gaze_data['left_gaze_point_on_display_area'][1]

    elif gaze_data['left_gaze_point_validity'] == 0 and gaze_data['right_gaze_point_validity'] == 1:
        gaze_data['x'] = gaze_data['right_gaze_point_on_display_area'][0]
        gaze_data['y'] = gaze_data['right_gaze_point_on_display_area'][1]

    if gaze_data['left_gaze_point_validity'] == 1 or gaze_data['right_gaze_point_validity'] == 1:
        gaze_data['x'] = min(max(0, int(gaze_data['x'] * RESOLUTION[0])), RESOLUTION[0])
        gaze_data['y'] = min(max(0, int(gaze_data['y'] * RESOLUTION[1])), RESOLUTION[1])

    if image_acquisition:
        if all_gaze_data == []:
            gaze_data['image_acquisition'] = False
            all_gaze_data.append(gaze_data)

        if all_gaze_data[-1]['image_acquisition']:
            gaze_data['image_acquisition'] = False
            all_gaze_data.append(gaze_data)
        else:
            gaze_data['image_acquisition'] = True
            all_gaze_data.append(gaze_data)
            get_image(gaze_data['system_time_stamp'], d)
    else:
        all_gaze_data.append(gaze_data)
    print(gaze_data)

#LANCEMENT DE L'ACQUISITION
montobii.subscribe_to(tobii.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

time.sleep(duree)
montobii.unsubscribe_from(tobii.EYETRACKER_GAZE_DATA, gaze_data_callback)

start_time = time.time()
del d, mouse
gc.collect()
#On place la gaze data dans un dataframe pandas
df = pd.DataFrame.from_records(all_gaze_data)
del all_gaze_data
gc.collect()
first_system_timestamp = str(df['system_time_stamp'].values[0])



# print(list_images)
'''
for timestamp in dict_images:
    # print(list_images[timestamp])
    im = Image.fromarray(dict_images[timestamp]).save(directory + str(timestamp) + ".png")
    del im

del dict_images
'''
print("Temps d'export des screenshots en PNG : %s secondes ---" % (time.time() - start_time))


if image_acquisition:
    process_many_images(df, first_system_timestamp, dict_images)
else:
    process_one_image(df, first_system_timestamp, res=RESOLUTION)

df.to_csv('data/all_gaze_data-' + first_system_timestamp + '.csv', index=False)

print("Temps total de post-traitement des données après l'acquisition : %s secondes ---" % (time.time() - start_time))
