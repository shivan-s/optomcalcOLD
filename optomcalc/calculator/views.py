import logging
import math
import os
from typing import Tuple

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
                        <td>{right_mbs} mm</td>
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
        ref = (self.request.GET).dict()

        # if enters above 50 in right_pd, then this is likely a 
        # bino pd and needs to be halved
        right_pd = ref['right_pd']
        left_pd = ref['left_pd']

        if right_pd: 
            right_pd = float(right_pd)
            if right_pd > 50:
                right_pd = right_pd / 2
                left_pd = right_pd

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

class BackVertexPowerView(TemplateView):
    template_name = 'calculator/back_vertex_power.html'

class BVPCalculate(View):

    def post(self, request):

        warning = ''

        names = { 
                'right_sphere': 'Right Sphere',
                'right_cylinder': 'Right Cylinder',
                'right_axis': 'Right Axis',
                'left_sphere': 'Left Sphere',
                'left_cylinder': 'Left Cylinder',
                'left_axis': 'Right Axis',
                'original_bvd': 'Orignal BVD',
                'new_bvd': 'New BVD'
                }

        ref = (self.request.POST).dict()

        important_features = {
                'right_sphere': ref['right_sphere'],
                'right_cylinder': ref['right_cylinder'],
                'left_sphere': ref['left_sphere'],
                'left_cylinder': ref['left_cylinder'],
                'original_bvd': ref['original_bvd'],
                'new_bvd': ref['new_bvd'],
                }

        # checks to see if sphere and cyl entered
        # minimum needed to activate script is sphere, cyl for one eye, orignal bvd and new bvd 

        right_entered = all([ref['right_sphere'], ref['right_cylinder']])  
        left_entered = all([ref['left_sphere'], ref['left_cylinder']])
        
        if not ref['original_bvd'] or not ref['new_bvd'] and ( not right_entered or not left_entered ):
            # checking for empty fields
            err = [names[k] for k, v in important_features.items() if not v]
            answer = f"""
            <div class="alert alert-danger" role="alert">
                Missing Values: <b>{'</b>, <b>'.join(err)}</b>
            </div>
            """
            return HttpResponse(answer)
        else:
            ref = {k:float(v) for k, v in ref.items() if v}
            right_sphere = ref.get('right_sphere')
            right_cylinder = ref.get('right_cylinder')
            right_axis = ref.get('right_axis')
            left_sphere = ref.get('left_sphere') 
            left_cylinder = ref.get('left_cylinder')
            left_axis = ref.get('left_axis')
            original_bvd = ref['original_bvd']
            new_bvd = ref['new_bvd']

            if not all([right_axis, left_axis]):
                warning = """
                <div class="alert alert-warning" role="alert">
                    Warning: <b>Axis</b> not entered returns <b>None</b>.
                </div>
                """

            def _calculate_vertex_power(sphere: float, cylinder: float) -> Tuple[float, float]:
                """
                Calculates the vertex power
                """
                meridian_sph = sphere
                meridian_cyl = sphere + cylinder

                # FIXME: divide by zero hotfix
                if meridian_cyl == 0:
                    meridian_cyl = 1

                new_meridian_sph = 1 / ((1 / meridian_sph) - ((original_bvd - new_bvd)*10**-3))
                new_meridian_cyl = 1 / ((1 / meridian_cyl) - ((original_bvd - new_bvd)*10**-3))
                
                new_meridian_cyl = new_meridian_cyl - new_meridian_sph

                return new_meridian_sph, new_meridian_cyl

            right_answer, left_answer = '', ''

            if right_entered:
                new_right_sphere, new_right_cylinder = _calculate_vertex_power(right_sphere, right_cylinder)
                right_answer = f"""
                            {"+" if new_right_sphere >= 0 else "-"}{abs(new_right_sphere): .2f} /
                            {"+" if new_right_cylinder > 0 else "-"}{abs(new_right_cylinder): .2f} x  
                            {right_axis} 
                """
            if left_entered:
                new_left_sphere, new_left_cylinder  = _calculate_vertex_power(left_sphere, left_cylinder)
                left_answer = f"""
                            {"+" if new_left_sphere >= 0 else "-"}{abs(new_left_sphere): .2f} /
                            {"+" if new_left_cylinder > 0 else "-"}{abs(new_left_cylinder): .2f} x  
                            {left_axis}
                """

            answer = warning + f"""
            <table class="table table-striped table-hover"
                <thead></thead>
                <tbody>
                    <tr>
                        <th scope="row">Right:</th>
                        <td>
                            {right_answer} 
                        </td>
                    </tr>
                    <tr> 
                        <th scope="row">Left:</th>
                        <td>
                            {left_answer} 
                        </td>
                    </tr>
                </tbody>
            </table>
            """
            return HttpResponse(answer)

class CylinderTranposeView(TemplateView):
    template_name = 'calculator/cylinder_transpose.html'

class CTCalculate(View):

    def post(self, request):
        """Calculates the cylindrical tranposition
        """
        names = { 
                'sphere': 'Sphere',
                'cylinder': 'Cylinder',
                'axis': 'Axis',
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
            sphere = ref['sphere'] 
            cylinder = ref['cylinder']
            axis = ref['axis']

            warning = ''
            if cylinder == 0:
                warning = """
                <div class="alert alert-warning" role="alert">
                    Warning: <b>Cylinder</b> is zero.
                </div>
                """
            if axis > 180:
                error_axis = """
                <div class="alert alert-danger" role="alert">
                   <b>Axis</b> must between 0 to 180 degrees 
                </div>
                """
                return HttpResponse(error_axis)
            trans_sphere = sphere + cylinder
            trans_cylinder = cylinder * -1
            if axis <= 90:
                trans_axis = axis + 90
            if axis == 180:
                trans_axis = 90
            elif axis > 90:
                trans_axis = 180 - axis 

            answer = warning + f"""
            <table class="table table-striped table-hover"
                <thead>
                    <th scope="row">Sphere:</th>
                    <th scope="row">Cylinder:</th>
                    <th scope="row">Axis:</th>
                </thead>
                <tbody>
                    <tr>
                    <td>{"+" if trans_sphere >= 0 else "-"}{abs(trans_sphere): .2f}</td>
                    <td>{"+" if trans_cylinder > 0 else "-"}{abs(trans_cylinder): .2f}</td>
                    <td>{trans_axis}</td>
                        <!-- <th scope="row">Right Minimum Blank Size:</th> -->
                    </tr>
                </tbody>
            </table>
            """
        return HttpResponse(answer)

