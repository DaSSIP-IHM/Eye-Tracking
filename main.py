from pynput.mouse import Button, Controller
import tobii_research as tobii
import time
import pandas as pd
import d3dshot
from PIL import Image

lestobii = tobii.find_all_eyetrackers()
montobii = lestobii[0]
duree = 40
mouse = Controller()

print("Son adresse IP: " + montobii.address)
print("Le modèle: " + montobii.model)
print("Son petit nom (souvent vide): " + montobii.device_name)
print("Son numéro de série: " + montobii.serial_number)
print("Et voici le flux durant l.a.es prochaine.s seconde.s : ", duree)

list_positions = []
list_images = dict()
all_gaze_data = []

d = d3dshot.create(capture_output="numpy")


def get_image(name, d):
    # im = ImageGrab.grab()
    # im.save(name+'.png')
    im = d.screenshot()
    # im = getscreenNP(reduction=4)
    list_images[name] = im


def move_mouse(gaze_data):
    x = gaze_data['x']
    y = gaze_data['y']

    # print(x)
    # print(y)
    list_positions.append((x, y))
    # print(l)

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


image = True


def gaze_data_callback(gaze_data):
    # print(gaze_data)
    '''
    print("OG: ({gaze_left_eye}) \t OD: ({gaze_right_eye})".format(
        gaze_left_eye=gaze_data['left_gaze_point_on_display_area'],
        gaze_right_eye=gaze_data['right_gaze_point_on_display_area']))
    '''
    # print(gaze_data)
    gaze_data['mouse_position'] = mouse.position

    gaze_data['x'] = round(
        (gaze_data['left_gaze_point_on_display_area'][0] + gaze_data['right_gaze_point_on_display_area'][0]) / 2, 2)
    gaze_data['y'] = round(
        (gaze_data['left_gaze_point_on_display_area'][1] + gaze_data['right_gaze_point_on_display_area'][1]) / 2, 2)

    gaze_data['x'] = min(max(0, int(gaze_data['x'] * 1920)), 1920)
    gaze_data['y'] = min(max(0, int(gaze_data['y'] * 1080)), 1080)

    print(gaze_data)
    '''
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
    '''
    # move_mouse(gaze_data)
    all_gaze_data.append(gaze_data)

    print(gaze_data['system_time_stamp'])


montobii.subscribe_to(tobii.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

time.sleep(duree)
montobii.unsubscribe_from(tobii.EYETRACKER_GAZE_DATA, gaze_data_callback)
df = pd.DataFrame.from_records(all_gaze_data)
print(df)

first_system_timestamp = str(df['system_time_stamp'].values[0])
df.to_excel('gaze_data/all_gaze_data-' + first_system_timestamp + '.xlsx', index=False)

# print(list_images)
for timestamp in list_images:
    # print(list_images[timestamp])
    Image.fromarray(list_images[timestamp]).save('images/' + str(timestamp) + ".png")
