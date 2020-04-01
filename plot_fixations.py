import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_excel('gaze_data/analyze/all_gaze_data-952409502500-analyze.xlsx')


def plot_fixations_points(x, y, image_name, pointsize):
    print(df)

    image_name = 'examples/liberte1080.jpg'
    im = plt.imread(image_name)
    implot = plt.imshow(im)



    # put a red dot, size 40, at 2 locations:
    plt.scatter(x, y, c='r', s=pointsize)
    plt.savefig('testplot.png', dpi=300)
    plt.show()


def plot_fixations_path(x, y, image_name, linewidth, markersize):
    print(df)

    image_name = 'examples/liberte1080.jpg'
    im = plt.imread(image_name)
    implot = plt.imshow(im)



    # put a red dot, size 40, at 2 locations:
    plt.plot(x, y, linewidth=linewidth, markersize=markersize)
    plt.savefig('examples/testplot_path.png', dpi=300)
    plt.show()
