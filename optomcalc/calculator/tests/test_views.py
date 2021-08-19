import json

import bs4
from django.test import Client
from django.urls import reverse

from calculator.views import (
        IndexView,
        MinimumBlankSizeView,
        BackVertexPowerView,
        CylinderTranposeView,
        )

class TestIndexView:
    def test_loads_page(self):
        client = Client()
        response = client.get(reverse('index'), follow=True, secure=True)
        assert response.status_code == 200

class TestMinimumBlankSizeView:
    def test_loads_page(self):
        client = Client()
        response = client.get(reverse('minimum_blank_size'),
                follow=True, secure=True)
        assert response.status_code == 200

class TestBackVertexPowerView:
    def test_loads_page(self):
        client = Client()
        response = client.get(reverse('back_vertex_power'),
                follow=True, secure=True)
        assert response.status_code == 200

class TestCylinderTransposeView:
    def test_loads_page(self):
        client = Client()
        response = client.get(reverse('cylinder_transpose'),
                follow=True, secure=True)
        assert response.status_code == 200
    
class TestMeanOcularPerfusionPressureView:
    def tests_loads_page(self):
        client = Client()
        response = client.get(reverse('mean_ocular_perfusion_pressure'),
                follow=True, secure=True)
        assert response.status_code == 200
