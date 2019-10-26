from django.shortcuts import render
from .models import Color
from django.utils import timezone


def index(request):
    if request.method == 'POST':
        if request.FILES:
            # get the file name
            filename = request.FILES['image'].name

            color = Color()
            color.image = request.FILES['image']
            color.filename = request.FILES['image'].name

            print(color)
            color.save()

            # print(filename)

            # get the px dimensions
            # resize a thumbnail to a smaller image
            # analyze the colors
            # save an img file
            # calculate the hex values
            # return back to homepage and display the img and hexes

        else:
            print('no image')
            return render(request, 'colors/index.html', {'error': 'You must add an image.'})

    # temporarily loop all images in db
    images = Color.objects

    return render(request, 'colors/index.html', {'images': images})
