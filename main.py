from pynput.mouse import Controller
import tobii_research as tobii
import pandas as pd
import d3dshot
from components.process import *
import time
from multiprocessing import Process, Manager
import cv2

duree = 20 # DUREE DE L'ACQUISITION EN SECONDES
RESOLUTION = (1920, 1080)  # RESOLUTION DE L'ECRAN A DEFINIR
# image = True
mouse = Controller()
image_acquisition = True  # CHOIX SI ACQUISITION DE L'IMAGE A L'ECRAN
monitor = 0
all_gaze_data = []

def timestamp():
    return int(round(time.time() * 1000))


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


    gaze_data['timestamp'] = timestamp()
    all_gaze_data.append(gaze_data)
    print(gaze_data)


def launch_acquisition_image(dict_images):
    d = d3dshot.create(capture_output="numpy")
    d.display = d.displays[monitor]
    while True:
        im = d.screenshot()
        dict_images[str(timestamp())] = im


def export_images(dict_images, first_timestamp):
    export = True
    list_len_images = []
    directory = 'images/'+first_timestamp+'/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    while export:
        list_len_images.append(len(dict_images))
        if len(dict_images) > 0:
            timestamp, im = dict_images.popitem()
            print(len(dict_images))
            im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            cv2.imwrite(directory + timestamp + ".jpg", im)

if __name__ == '__main__':

    lestobii = tobii.find_all_eyetrackers()
    montobii = lestobii[0]
    print("Son adresse IP: " + montobii.address)
    print("Le modèle: " + montobii.model)
    print("Son numéro de série: " + montobii.serial_number)
    print("Et voici le flux durant les prochaines secondes : ", duree)
    montobii.subscribe_to(tobii.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
    first_timestamp = str(timestamp())
    if image_acquisition:
        manager = Manager()
        dict_images = manager.dict()

        p2 = Process(target=launch_acquisition_image, args=(dict_images,))
        p3 = Process(target=export_images, args=(dict_images, first_timestamp,))

        p2.start()
        p3.start()

        p2.join(timeout=duree/2)
        p3.join(timeout=duree/2)

        p2.terminate()
        p3.terminate()
    else:
        time.sleep(duree)
    montobii.unsubscribe_from(tobii.EYETRACKER_GAZE_DATA, gaze_data_callback)
    df = pd.DataFrame.from_records(all_gaze_data)
    df['mean_pupil_diameter'] = (df['left_pupil_diameter'] + df['right_pupil_diameter']) / 2
    df.to_csv('data/all_gaze_data-' + first_timestamp + '.csv', index=False)

    if image_acquisition:
        process_many_images(df, first_timestamp)
    else:
        process_one_image(df, first_timestamp)