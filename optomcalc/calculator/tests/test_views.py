import json

import bs4
from django.test import Client
from django.urls import reverse

from calculator.views import (
        IndexView,
        MinimumBlankSizeView,
        MBSCalculate,
        BackVertexPowerView,
        BVPCalculate,
        CylinderTranposeView,
        CTCalculate,
        )

class TestIndexView:
    def test_loads_page(self):
        client = Client()
        response = client.get(reverse('index'), follow=True, secure=True)
        assert response.status_code == 200

class TestMinimumBlankSizeView:
    def test_loads_page(self):
        client = Client()
        response = client.get(reverse('minimum_blank_size'), follow=True, secure=True)
        assert response.status_code == 200

class TestMBSCalculate:
    def test_post(self):
        client = Client()
        response = client.post(reverse('mbs_calculate'), {
            'right_pd': '30',
            'left_pd': '31',
            'frame_size': '53',
            'frame_dbl': '16',
            'effective_diameter': '55'
            }, follow=True, secure=True)
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        soup_result = [_.get_text() for _ in soup.find_all('td')]
        assert response.status_code == 200
        assert soup_result == ['61.5 mm', '60.5 mm']

    def test_get(self):
        client = Client()
        response = client.get(reverse('mbs_calculate'), {
            'right_pd': '60',
            'left_pd': ''
            }, follow=True, secure=True)
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        soup_result = [_['value'] for _ in soup.find_all('input')]
        assert response.status_code == 200
        assert soup_result == ['30.0', '30.0']

class TestBackVertexPowerView:
    def test_loads_page(self):
        client = Client()
        response = client.get(reverse('back_vertex_power'), follow=True, secure=True)
        assert response.status_code == 200

class TestBVPCalculateView:
    def test_post(self):
        client = Client()
        response = client.post(reverse('bvp_calculate'), {
            'right_sphere': '-10.00',
            'right_cylinder': '-2.00',
            'left_sphere': '+10.00',
            'left_cylinder': '-0.00',
            'original_bvd': '12',
            'new_bvd': '0',
            }, follow=True, secure=True) # only including important features
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        soup_result = [_.get_text().replace('\n', '').replace(' ', '').strip() for _ in soup.find_all('td')]
        assert response.status_code == 200
        assert soup_result == ['-8.93/-1.56xNone', '+11.36/-0.00xNone'] 

class TestCylinderTransposeView:
    def test_loads_page(self):
        client = Client()
        response = client.get(reverse('cylinder_transpose'), follow=True, secure=True)
        assert response.status_code == 200
    
class TestCTCalculateView:
    def test_post(self):
        client = Client()
        response = client.post(reverse('ct_calculate'), {
            'sphere': '+1.00',
            'cylinder': '+2.00',
            'axis': '90',
            }, follow=True, secure=True) 
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        soup_result = [_.get_text() for _ in soup.find_all('td')]
        assert response.status_code == 200
        assert soup_result == ['+ 3.00', '- 2.00', '180.0'] 


