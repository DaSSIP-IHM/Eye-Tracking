import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_excel('gaze_data/analyze/all_gaze_data-952409502500-analyze.xlsx')


def plot_fixations(x, y, image_name, pointsize):
    print(df)

    image_name = 'liberte1080.jpg'
    im = plt.imread(image_name)
    implot = plt.imshow(im)

    # put a blue dot at (10, 20)
    plt.scatter([10], [20])

    # put a red dot, size 40, at 2 locations:
    plt.scatter(x, y, c='r', s=pointsize)
    plt.savefig('testplot.png', dpi=300)
    plt.show()
