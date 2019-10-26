from django.shortcuts import render, get_object_or_404
from .models import Color
from django.utils import timezone


def index(request):
    # TODO add an input dropdown between 3-7 with default 5
    # default to just_saved_image empty
    just_saved_image = None

    if request.method == 'POST':
        # if file exists: process it and save to db
        if request.FILES:

            image = Color()
            image.image = request.FILES['image']
            image.filename = request.FILES['image'].name
            image.save()

            # create object queried from id of just saved image
            just_saved_image = Color.objects.get(pk=image.id)

            # get the px dimensions
            # resize a thumbnail to a smaller image
            # analyze the colors
            # save an img file
            # calculate the hex values + front end show circles
            # return back to homepage and display the img and hexes

        # if file doesn't exist: return error message
        else:
            return render(request, 'colors/index.html', {'error': 'You must add an image.', 'just_saved_image': just_saved_image})

    return render(request, 'colors/index.html', {'just_saved_image': just_saved_image})
