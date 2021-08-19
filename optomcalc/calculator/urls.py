from django.urls import path

from .views import ( IndexView, MinimumBlankSizeView, MBSCalculate,
                    BackVertexPowerView, BVPCalculate, CylinderTranposeView,
                   CTCalculate, MeanOcularPerfusionPressureView, MOPPCalculate )

urlpatterns = [
        path('', IndexView.as_view(), name='index'),
        path('minimum_blank_size/', MinimumBlankSizeView.as_view(), name='minimum_blank_size'),
        path('mbs_calculate/', MBSCalculate.as_view(), name='mbs_calculate'),
        path('back_vertex_power/', BackVertexPowerView.as_view(), name='back_vertex_power'),
        path('bvp_calculate/', BVPCalculate.as_view(), name='bvp_calculate'),
        path('cylinder_transpose/', CylinderTranposeView.as_view(), name='cylinder_transpose'),
        path('ct_calculate/', CTCalculate.as_view(), name='ct_calculate'),
        path('mean_ocular_perfusion_pressure/', MeanOcularPerfusionPressureView.as_view(), name='mean_ocular_perfusion_pressure'),
        path('mopp_calculate/', MOPPCalculate.as_view(), name='mopp_calculate'),
        ]
