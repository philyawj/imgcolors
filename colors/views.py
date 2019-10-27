from django.shortcuts import render, get_object_or_404
from .models import Color
from django.utils import timezone
import numpy as np
import cv2
import os
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


def index(request):
    # variable defaults to prevent front end errors
    just_saved_image = None
    error = None
    number_of_colors = None
    just_saved_output = None

    if request.method == 'POST':
        # if file exists: process it and save to db
        if request.FILES:

            # calc file size in kb
            filesize = len(request.FILES['image'])
            filesizek = filesize / 1000

            # prevent images that are too small or too large
            if filesizek >= 500:
                error = 'Images must be smaller than 500k'
            elif filesizek <= 10:
                error = 'Images must be larger than 10k'
            # continue processing since image size is valid
            else:
                # create object
                image = Color()
                image.image = request.FILES['image']
                image.filename = request.FILES['image'].name
                # save object to db
                image.save()

                number_of_colors = request.POST['numberOfColors']

                # convert number of colors to int
                num_clusters = int(number_of_colors)
                # split image percentage to equal 100%
                equal_percent = (100/num_clusters)/100
                equal_hist = np.zeros(num_clusters)
                equal_hist = equal_hist.astype("float")
                equal_hist[:] = equal_percent

                # create object queried from id of just saved image
                just_saved_image = Color.objects.get(pk=image.id)

                # get image path and trim first /
                path = just_saved_image.image.url[1:]

                # get image width and height
                img = cv2.imread(path)

                # fail with error if cv2 determines not a valid image
                if img is None:
                    error = 'Image must be a png jpg or jpeg'
                    return render(request, 'colors/index.html', {'error': error})
                # continue if image is valid image file type
                else:
                    # read image and convert to RGB
                    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                    # reshape the image to be a list of pixels
                    image = image.reshape((image.shape[0] * image.shape[1], 3))

                    # cluster the pixel intensities
                    clt = KMeans(n_clusters=num_clusters)
                    clt.fit(image)

                    # create a figure representing the % of pixels labeled to each color
                    hist = centroid_histogram(clt)
                    rgbcolors = clt.cluster_centers_
                    rgbints = rgbcolors.astype(int)
                    rgblist = list(rgbints)
                    print(rgbints)

                    s = hist.tolist()
                    # adds commas and puts into list

                    rgbdict = {}
                    # loop through and add key value to dict for later sorting
                    for r, p in zip(rgblist, s):
                        rgbdict[p] = r
                    # combines them into an unsorted dictionary as key value pairs

                    # assign key(percentages) values(rgb) in order
                    sorted_rgb_list = []

                    for key in sorted(rgbdict, reverse=True):
                        sorted_rgb_list.append(rgbdict[key])

                    sorted_rgb_list_formatted = np.array(sorted_rgb_list)

                    sorted_hist = sorted(hist, reverse=True)

                    # passing in equal_hist makes contents evenly space
                    output_equal = plot_colors(
                        equal_hist, sorted_rgb_list_formatted)

                    # 2nd version with weighted spacing
                    output_weighted = plot_colors(
                        sorted_hist, sorted_rgb_list_formatted)

                    # check if outputs folder exists. create it if not
                    if not os.path.exists('media/outputs'):
                        os.makedirs('media/outputs')
                    # save as image
                    plt.imsave("media/outputs/output-equal.png", output_equal)
                    plt.imsave("media/outputs/output-weighted.png",
                               output_weighted)

                    height, width = img.shape[:2]
                    print(height)
                    print(width)

                    if width > height:
                        print('the image width is larger than the height')
                    else:
                        print('the image height is larger than the width')
                    # TODO use css to set max width/max height when it displays image

                    just_saved_output = '/media/outputs/output-equal.png'

                    # TODO calculate the HEX values + front end show circles
                    hexes = []
                    hexesdict = {}

                    # loop through and convert to hex
                    for r in rgblist:
                        hexes.append(rgb_to_hex(r))

                    # loop through and add key value to dict for later sorting
                    for r, p in zip(rgblist, s):
                        hexesdict[p] = rgb_to_hex(r)

                    print('HEXES BELOW')
                    print(hexes)
                    print('HEXES DICT BELOW')
                    print(hexesdict)
                    print('----SORTED BELOW-----')
                    for key in sorted(hexesdict, reverse=True):
                        print("%s: %s" % (key, hexesdict[key]))

                    hexeslist = []

                    print('----JUST HEXES IN ORDER-----')
                    for key in sorted(hexesdict, reverse=True):
                        hexeslist.append(hexesdict[key])
                    print(hexeslist)

                    # TODO javascript prevent double submits by making button disabled. show loady while it processes
                    # TODO possibly make the image half the size and run the analysis on that for faster load

                    # return back to homepage and display the img/output/hexes

        # if file doesn't exist: return error message
        else:
            error = 'You must add an image'
            return render(request, 'colors/index.html', {'error': error, 'just_saved_image': just_saved_image})

    return render(request, 'colors/index.html', {'error': error, 'just_saved_image': just_saved_image, 'number_of_colors': number_of_colors, 'just_saved_output': just_saved_output})


def centroid_histogram(clt):
    # grab the number of different clusters and create a histogram
    # based on the number of pixels assigned to each cluster
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    # normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()

    # return the histogram
    return hist

# plot image - hist arg is already ordered by most dominant to least dominant


def plot_colors(hist, centroids):
    # create square image with equal % bars
    w = 300
    h = 300
    bar = np.zeros((w, h, 3), dtype="uint8")
    startX = 0

    # loop over the equal percentage of each cluster and the color of each cluster
    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 300),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar


def rgb_to_hex(rgb):
    return '#%s' % ''.join(('%02x' % p for p in rgb))
