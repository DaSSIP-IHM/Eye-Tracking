import matplotlib.pyplot as plt
import pandas as pd


# df = pd.read_excel('../gaze_data/analyze/all_gaze_data-952409502500-analyze.xlsx')


def plot_fixations_points(x, y, image_name, pointsize, default_path=''):
    image_name = default_path+'examples/liberte1080.jpg'
    im = plt.imread(image_name)
    implot = plt.imshow(im)

    # put a red dot, size 40, at 2 locations:
    plt.scatter(x, y, c='r', s=pointsize)
    plt.savefig(default_path+'examples/testplot_points.png', dpi=300)
    plt.show()


def plot_fixations_path(x, y, image_name, linewidth, markersize, default_path=''):
    image_name = default_path+'examples/liberte1080.jpg'
    im = plt.imread(image_name)
    implot = plt.imshow(im)

    # put a red dot, size 40, at 2 locations:
    plt.plot(x, y, linewidth=linewidth, markersize=markersize)
    plt.savefig(default_path+'examples/testplot_path.png', dpi=300)
    plt.show()
