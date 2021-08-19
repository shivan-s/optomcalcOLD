from django.http import HttpResponse
from django.views import View

from . import special_return as sr

class MOPPCalculate(View):

    def post(self, request):
        """Calculates the mean ocular perfusion pressure
        """
        names = {
                'systolic_bp': 'Systolic BP',
                'diastolic_bp': 'Diastolic BP',
                'iop': 'IOP'
                }

        ref = (self.request.POST).dict()

        if not all(ref.values()):
            # checking for invalid values (nulls) and listing them
            answer = sr.err(ref, names)

        else:
            ref = {k:float(v) for k, v in ref.items()}
            systolic_bp = ref['systolic_bp']
            diastolic_bp = ref['diastolic_bp']
            iop = ref['iop']

            mean_ap = diastolic_bp + (1/3) * (systolic_bp - diastolic_bp)
            mean_opp = (2/3) * (mean_ap - iop) 
            
            outputs = {
                    'Mean Arterial Pressure': mean_ap,
                    'Mean Ocular Perfusion Pressure': mean_opp
                    }

            # if below 50 mmHg, then increased prevalence of glaucoma
            if mean_opp < 50:
                add_on = sr.alert('<b>Risk</b>: MOPP falls under 50 mmHg',
                                  'warning')
            else:
                add_on = sr.alert('<b>Low Risk</b>: MOPP falls above 50 mmHg',
                                  'success')
            answer = sr.output_results(outputs) + add_on
            
        return HttpResponse(answer)
