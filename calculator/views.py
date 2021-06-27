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
            
            warning = ''
            if effective_diameter < frame_size:
                warning = """
                <div class="alert alert-warning" role="alert">
                    Warning: <b>Effective Diameter</b> is smaller than <b>Frame Size</b>
                </div>
                """
             
            right_mbs = _minimum_blank_size(right_pd)
            left_mbs = _minimum_blank_size(left_pd)

            answer = warning + f"""
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
        return HttpResponse(answer)
    
    def get(self, request):
        logging.info('GET METHOD:')
        logging.info('bino_pd: ' + str(self.bino_pd))  
        logging.info((self.request.GET).dict()) 

        ref = (self.request.GET).dict()

        def _check_pd(mono_pd: str):
            """
            Checks if pd is above 45 and returns as float
            """
            if mono_pd:
                mono_pd = float(mono_pd)
                if mono_pd > 45:
                    mono_pd = mono_pd / 2
            return mono_pd

        right_pd = ref['right_pd']
        left_pd = ref['left_pd']
        
        if right_pd and not left_pd:
            right_pd = _check_pd(right_pd)
            left_pd = right_pd

        if left_pd and not right_pd:
            left_pd = _check_pd(left_pd)
            right_pd = left_pd

        output = f"""
        	<div class="row"
				     id="pds">
					<div class="col-sm">
						<label for="right_pd">Right PD (mm)</label>
						<input hx-get="/mbs_calculate/"
						       hx-target="#pds"
                               hx-swap="innerHTML"
						       class="form-control"
						       value="{right_pd}"
						       type="number" 
						       step="0.5" 
						       min="0" 
						       name="right_pd">
					</div>
					<div class="col-sm">
						<label for="left_pd">Left PD (mm)</label>
						<input hx-get="/mbs_calculate"
                               hx-target="#pds"
                               hx-swap="innerHTML"
                               class="form-control" 
						       value="{left_pd}"
						       type="number" 
						       step="0.5" 
						       min="0" 
						       name="left_pd">
					</div>
				</div>
                """

        return HttpResponse(output)
