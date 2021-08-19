import math
from typing import Tuple

from django.http import HttpResponse
from django.views import View

from . import special_return as sr

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
                #if meridian_cyl == 0:
                 #   meridian_cyl = 1
                new_meridian_sph = 1 / ((1 / meridian_sph) - ((original_bvd - new_bvd)*10**-3))
                new_meridian_cyl = 1 / ((1 / meridian_cyl) - ((original_bvd - new_bvd)*10**-3))
                new_meridian_cyl = new_meridian_cyl - new_meridian_sph

                return new_meridian_sph, new_meridian_cyl

            right_answer, left_answer = '', ''

            def _round_output(num: float) -> float:
                """Rounds num to the nearest 0.25, 0.50, 0.75, 0.00
                """
                num = abs(num)
                decimal, integer = math.modf(num)
                
                if decimal >= 0 and decimal < 0.125:
                    decimal = 0.00
                elif decimal >= 0.125 and decimal < 0.25:
                    decimal = 0.25
                elif decimal >= 0.25 and decimal < 0.375:
                    decimal = 0.25
                elif decimal >= 0.375 and decimal < 0.5:
                    decimal = 0.50
                elif decimal >= 0.5 and decimal < 0.625:
                    decimal = 0.50
                elif decimal >= 0.625 and decimal < 0.75:
                    decimal = 0.75
                elif decimal >= 0.75 and decimal < 0.875:
                    decimal = 0.75
                elif decimal >= 0.875 and decimal < 1.00:
                    decimal = 1.00

                num = integer + decimal
                return num
            try:    
                if right_entered:
                    new_right_sphere, new_right_cylinder = _calculate_vertex_power(right_sphere, right_cylinder)
                    right_answer = f"""
                                {"+" if new_right_sphere >= 0 else "-"}{_round_output(new_right_sphere): .2f} /
                                {"+" if new_right_cylinder > 0 else "-"}{_round_output(new_right_cylinder): .2f} x  
                                {right_axis} 
                    """
                if left_entered:
                    new_left_sphere, new_left_cylinder  = _calculate_vertex_power(left_sphere, left_cylinder)
                    left_answer = f"""
                                {"+" if new_left_sphere >= 0 else "-"}{_round_output(new_left_sphere): .2f} /
                                {"+" if new_left_cylinder > 0 else "-"}{_round_output(new_left_cylinder): .2f} x  
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
            except ZeroDivisionError:
                warning = sr.alert('Error: Divide by Zero', 'danger')
                caution = sr.alert('I am trying to come up with a solution', 'warning')
                return HttpResponse(warning + caution)


