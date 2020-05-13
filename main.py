from pynput.mouse import Controller
import tobii_research as tobii
import pandas as pd
import d3dshot
from components.process import *
import time
import gc
import sys
from multiprocessing import Process, Manager

duree = 20  # DUREE DE L'ACQUISITION EN SECONDES
RESOLUTION = (1920, 1080)  # RESOLUTION DE L'ECRAN A DEFINIR
# image = True
mouse = Controller()
image_acquisition = True  # CHOIX SI ACQUISITION DE L'IMAGE A L'ECRAN

all_gaze_data = []


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

    all_gaze_data.append(gaze_data)
    print(gaze_data)


def launch_acquisition_image(dict_images):
    d = d3dshot.create(capture_output="numpy")
    d.display = d.displays[1]
    while True:
        im = d.screenshot()
        dict_images[str(round(time.time() * 1000))] = im


def export_images(dict_images):
    export = True
    list_len_images = []
    while export:
        list_len_images.append(len(dict_images))
        if len(dict_images) > 0:
            timestamp, im = dict_images.popitem()
            print(len(dict_images))
            Image.fromarray(im).save('images/' + timestamp + ".png")


if __name__ == '__main__':

    lestobii = tobii.find_all_eyetrackers()
    montobii = lestobii[0]
    print("Son adresse IP: " + montobii.address)
    print("Le modèle: " + montobii.model)
    print("Son numéro de série: " + montobii.serial_number)
    print("Et voici le flux durant les prochaines secondes : ", duree)
    montobii.subscribe_to(tobii.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

    if image_acquisition:
        manager = Manager()
        dict_images = manager.dict()

        p2 = Process(target=launch_acquisition_image, args=(dict_images,))
        p3 = Process(target=export_images, args=(dict_images,))
        # p1.start()
        p2.start()
        p3.start()
        # p1.join(timeout=duree)

        p2.join(timeout=duree)
        p3.join(timeout=duree)

        p2.terminate()
        p3.terminate()
    else:
        time.sleep(duree)
    montobii.unsubscribe_from(tobii.EYETRACKER_GAZE_DATA, gaze_data_callback)
    df = pd.DataFrame.from_records(all_gaze_data)
    first_system_timestamp = str(df['system_time_stamp'].values[0])
    df.to_csv('data/all_gaze_data-' + first_system_timestamp + '.csv', index=False)
    # https://stackoverflow.com/questions/47903791/how-to-terminate-a-multiprocess-in-python-when-a-given-condition-is-met
    # Variable globale
