import matplotlib.pyplot as plt
import pandas as pd


# df = pd.read_excel('../gaze_data/analyze/all_gaze_data-952409502500-analyze.xlsx')


def plot_fixations_points(x, y, image_name, pointsize, default_path='', output_ind=''):

    image_name = default_path+'examples/liberte1080.jpg'
    im = plt.imread(image_name)
    implot = plt.imshow(im)

    print(x.shape)
    print(y.shape)

    n = [x for x in range(1, len(x)+1)]
    print(n)
    #plt.scatter(x, y, c='r', s=pointsize)

    for i, txt in enumerate(n):
        plt.text(x[i], y[i], txt, c='r', fontsize=3)


    plt.savefig(default_path+'examples/testplot_points'+output_ind+'.png', dpi=300)
    plt.show()


def plot_path(x, y, image_name, linewidth, markersize, default_path=''):
    image_name = default_path+'examples/liberte1080.jpg'
    im = plt.imread(image_name)
    implot = plt.imshow(im)

    plt.plot(x, y, linewidth=linewidth, markersize=markersize)
    plt.savefig(default_path+'examples/testplot_path.png', dpi=300)
    plt.show()
