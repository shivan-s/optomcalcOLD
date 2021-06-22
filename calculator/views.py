import logging
import math
import os

from django.shortcuts import render
from django.views import View 
from django.views.generic import TemplateView
from django.http import HttpResponse

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

class IndexView(TemplateView):
    template_name = 'calculator/index.html'

class MinimumBlankSizeView(TemplateView):
    template_name = 'calculator/minimum_blank_size.html'
    
class MBSCalculate(View):
    def post(self, request):
        err = []
        ref = (self.request.POST).dict()
        logging.info(ref)
        if '' in ref.values():
            answer = 'Please enter all values'
        else:
            ref = {k:float(v) for k, v in ref.items()}
            right_pd = ref['right_pd'] 
            left_pd = ref['left_pd']
            frame_size = ref['frame_size']
            frame_dbl = ref['frame_dbl']
            effective_diameter = ref['effective_diameter']
        # source of information - https://www.insightnews.com.au/finding-the-minimum-lens-blank-size-part-2-2/
            frame_pd = frame_size + frame_dbl
            def minimum_blank_size(mono_pd: float):
                """Calculates minimal blank size given a monocular pd"""
                decentration = abs( (frame_pd / 2) - mono_pd)
                return decentration + effective_diameter

            right_mbs = minimum_blank_size(right_pd)
            left_mbs = minimum_blank_size(left_pd)

            answer = f"""
            Right Minimum Blank Size: {right_mbs} mm <br />
            Left Minimum Blank Size: {left_mbs} mm
            """
        return HttpResponse(answer)
