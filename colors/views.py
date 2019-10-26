from django.shortcuts import render
from .models import Color


def index(request):
    if request.method == 'POST':
        # get the file name
        filename = request.FILES['image'].name

        color = Color()
        color.image = request.FILES['image']
        print(color)
        # print(filename)

        # get the px dimensions
        # resize a thumbnail to a smaller image
        # analyze the colors
        # save an img file
        # calculate the hex values
        # return back to homepage and display the img and hexes
    else:
        filename = 'no file submitted yet'
    return render(request, 'colors/index.html', {'filename': filename})
