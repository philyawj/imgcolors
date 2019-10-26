from django.shortcuts import render, get_object_or_404
from .models import Color
from django.utils import timezone


def index(request):
    just_saved_image = None
    if request.method == 'POST':
        # if file exists process it and save to db
        if request.FILES:

            color = Color()
            color.image = request.FILES['image']
            color.filename = request.FILES['image'].name
            color.save()
            # returns the id of image just saved
            print(color.id)

            # need to find a way to return just the object with that id
            just_saved_image = Color.objects.get(pk=color.id)
            print(just_saved_image)

            # get the px dimensions
            # resize a thumbnail to a smaller image
            # analyze the colors
            # save an img file
            # calculate the hex values
            # return back to homepage and display the img and hexes

        # if file doesn't exist, return error message
        else:
            just_saved_image = None
            return render(request, 'colors/index.html', {'error': 'You must add an image.', 'just_saved_image': just_saved_image})

    # temporarily loop all images in db
    images = Color.objects

    return render(request, 'colors/index.html', {'images': images, 'just_saved_image': just_saved_image})
