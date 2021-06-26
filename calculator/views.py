import logging
import math
import os
from typing import NamedTuple

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
    def __init__(self):
        self.bino_pd = 0
    
    def post(self, request):
        def _minimum_blank_size(mono_pd: float):
            """
            Calculates minimal blank size given a monocular pd
            """
            decentration = abs( (frame_pd / 2) - mono_pd)
            return decentration + effective_diameter + 2

        names = { 
                'right_pd': 'Right PD',
                'left_pd': 'Left PD',
                'frame_size': 'Frame Size',
                'frame_dbl': 'Frame DBL',
                'effective_diameter': 'Effective Diameter'
                }

        ref = (self.request.POST).dict()
        
        logging.info(ref) # all of the post data - form inputs

        if ref['right_pd']:
            self.bino_pd = float(ref['right_pd'])
        if not all(ref.values()):
            # checking for invalid values (nulls) and listing them
            err = [names[k] for k, v in ref.items() if not v]
            answer = f"""
            <div class="alert alert-danger" role="alert">
                Missing Values: <b>{'</b>, <b>'.join(err)}</b>
            </div>
            """
        else:
            ref = {k:float(v) for k, v in ref.items()}
            right_pd = ref['right_pd'] 
            left_pd = ref['left_pd']
            frame_size = ref['frame_size']
            frame_dbl = ref['frame_dbl']
            effective_diameter = ref['effective_diameter']
            # source of information - https://www.insightnews.com.au/finding-the-minimum-lens-blank-size-part-2-2/
            frame_pd = frame_size + frame_dbl
             
            right_mbs = _minimum_blank_size(right_pd)
            left_mbs = _minimum_blank_size(left_pd)

            answer = f"""
            <table class="table table-striped table-hover"
                <thead></thead>
                <tbody>
                    <tr>
                        <th scope="row">Right Minimum Blank Size:</th>
                        <td>{right_mbs} mm </td>
                    </tr>
                    <tr> 
                        <th scope="row">Left Minimum Blank Size:</th>
                        <td>{left_mbs} mm</td>
                    </tr>
                </tbody>
            </table>
            """
            # TODO: create checks and ranges for appropriate sizes
            # TODO: if mono pd is above 45, then split this between left and right
        return HttpResponse(answer)
    
    def get(self, request):
        right_pd = 30
        left_pd = 30
        if self.bino_pd:
            right_pd = self.bino_pd / 2
            left_pd = self.bino_pd / 2
        return HttpResponse(right_pd, left_pd)
