from django.views.generic import TemplateView

from .calc_modules.minimum_blank_size import MBSCalculate
from .calc_modules.back_vertex_power import BVPCalculate
from .calc_modules.cylinder_transpose import CTCalculate
from .calc_modules.mean_ocular_perfusion_pressure import MOPPCalculate

class IndexView(TemplateView):
    template_name = 'calculator/index.html'

class MinimumBlankSizeView(TemplateView):
    template_name = 'calculator/minimum_blank_size.html'

class BackVertexPowerView(TemplateView):
    template_name = 'calculator/back_vertex_power.html'

class CylinderTranposeView(TemplateView):
    template_name = 'calculator/cylinder_transpose.html'

class MeanOcularPerfusionPressureView(TemplateView):
    template_name = 'calculator/mean_ocular_perfusion_pressure.html'
