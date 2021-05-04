from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return render(request, 'calculator/index.html')

def minimum_blank_size(request):
    interpupillary_distance = 55
    if request.method == 'POST':
        right_pupillary_distance = float(request.POST.get('right_pupillary_distance'))
        left_pupillary_distance = float(request.POST.get('left_pupillary_distance'))
        frame_size = request.POST.get('frame_size')
        frame_bridge = request.POST.get('frame_bridge')
        effective_diameter = float(request.POST.get('effective_diameter'))
        
        # source of information https://www.youtube.com/watch?v=5Gh1bPzB0JU
        # minimum_blank_size = effective_diameter + 2 * decentration
        # decentration = average_pd - mono_pd

        average_pd = ( float(right_pupillary_distance) + float(left_pupillary_distance) ) / 2
        right_minimum_blank_size = effective_diameter + 2 * ( average_pd - right_pupillary_distance )
        left_minimum_blank_size = effective_diameter + 2 *  ( average_pd - left_pupillary_distance )

        answer = """
        Right Minimum Blank Size: {right_minimum_blank_size}
        Left Minimum Blank Size: {left_minimum_blank_size}
        """.format(
                right_minimum_blank_size=str(right_minimum_blank_size), 
                left_minimum_blank_size=str(left_minimum_blank_size)) 
        return render(request, 'calculator/minimum_blank_size.html', {'answer': answer })
    return render(request, 'calculator/minimum_blank_size.html')
