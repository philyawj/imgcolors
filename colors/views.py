from django.shortcuts import render, get_object_or_404
from .models import Color
from django.utils import timezone
import numpy as np
import cv2
import os


def index(request):
    # TODO add an input dropdown between 3-7 with default 5

    # TODO only accept certain kinds of image files

    # default just_saved_image and error to empty
    just_saved_image = None
    error = None

    if request.method == 'POST':
        # if file exists: process it and save to db
        if request.FILES:

            # TODO only accept images under a certain size
            filesize = len(request.FILES['image'])
            filesizek = filesize / 1000

            if filesizek >= 500:
                error = 'Images must be smaller than 500k'
            elif filesizek <= 10:
                error = 'Images must be larger than 10k'
            else:
                image = Color()
                image.image = request.FILES['image']
                image.filename = request.FILES['image'].name

                image.save()

                # create object queried from id of just saved image
                just_saved_image = Color.objects.get(pk=image.id)

                # get image path and trim first /
                path = just_saved_image.image.url[1:]

                # get image width and height -- 0 flag is grayscale
                img = cv2.imread(path, 0)

                if img is None:
                    error = 'Image must be a png jpg or jpeg'
                    return render(request, 'colors/index.html', {'error': error})
                else:
                    height, width = img.shape[:2]
                    print(height)
                    print(width)

                    if width > height:
                        print('the image width is larger than the height')
                    else:
                        print('the image height is larger than the width')

                    # TODO resize a thumbnail to a smaller image
                    # if image size is greater than 500k, downsize it by 50%
                    if filesizek > 500:
                        scale_percent = 50  # percent of original size
                        width = int(img.shape[1] * scale_percent / 100)
                        height = int(img.shape[0] * scale_percent / 100)
                        dim = (width, height)

                        # resize image
                        resized = cv2.resize(
                            img, dim, interpolation=cv2.INTER_AREA)
                        rheight, rwidth = resized.shape[:2]
                        print('Resized Dimensions : ', resized.shape)
                        print('Resized Width : ', rwidth)
                        print('Resized Height : ', rheight)

                    # analyze the colors
                    # save an img file
                    # calculate the hex values + front end show circles
                    # return back to homepage and display the img and hexes

        # if file doesn't exist: return error message
        else:
            error = 'You must add an image'
            return render(request, 'colors/index.html', {'error': error, 'just_saved_image': just_saved_image})

    return render(request, 'colors/index.html', {'error': error, 'just_saved_image': just_saved_image})
