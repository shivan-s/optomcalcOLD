import json

import bs4
from django.test import Client
from django.urls import reverse

from calculator.calc_modules.minimum_blank_size import MBSCalculate
from calculator.calc_modules.back_vertex_power import BVPCalculate
from calculator.calc_modules.cylinder_transpose import CTCalculate
from calculator.calc_modules.mean_ocular_perfusion_pressure import MOPPCalculate


class TestMBSCalculate:
    def test_post(self):
        client = Client()
        response = client.post(
            reverse("mbs_calculate"),
            {
                "right_pd": "30",
                "left_pd": "31",
                "frame_size": "53",
                "frame_dbl": "16",
                "effective_diameter": "55",
            },
            follow=True,
            secure=True,
        )
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        soup_result = [_.get_text() for _ in soup.find_all("td")]
        assert response.status_code == 200
        assert soup_result == ["61.5 mm", "60.5 mm"]

    def test_get(self):
        client = Client()
        response = client.get(
            reverse("mbs_calculate"),
            {"right_pd": "60", "left_pd": ""},
            follow=True,
            secure=True,
        )
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        soup_result = [_["value"] for _ in soup.find_all("input")]
        assert response.status_code == 200
        assert soup_result == ["30.0", "30.0"]


class TestBVPCalculateView:
    def test_post(self):
        client = Client()
        response = client.post(
            reverse("bvp_calculate"),
            {
                "right_sphere": "-10.00",
                "right_cylinder": "-2.00",
                "left_sphere": "+10.00",
                "left_cylinder": "-0.00",
                "original_bvd": "12",
                "new_bvd": "0",
            },
            follow=True,
            secure=True,
        )  # only including important features
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        soup_result = [
            _.get_text().replace("\n", "").replace(" ", "").strip()
            for _ in soup.find_all("td")
        ]
        assert response.status_code == 200
        assert soup_result == ["-9.00/-1.50xNone", "+11.25/-0.00xNone"]


class TestCTCalculateView:
    def test_post(self):
        client = Client()
        response = client.post(
            reverse("ct_calculate"),
            {
                "sphere": "+1.00",
                "cylinder": "+2.00",
                "axis": "90",
            },
            follow=True,
            secure=True,
        )
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        soup_result = [_.get_text() for _ in soup.find_all("td")]
        assert response.status_code == 200
        assert soup_result == ["+ 3.00", "- 2.00", "180.0"]


class TestMOPPCalculateView:
    def test_post(self):
        client = Client()
        response = client.post(
            reverse("mopp_calculate"),
            {"systolic_bp": "120", "diastolic_bp": "80", "iop": "21"},
            follow=True,
            secure=True,
        )
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        soup_result = [_.get_text() for _ in soup.find_all("td")]
        assert response.status_code == 200
        assert soup_result == [" 93.33 mmHg", " 48.22 mmHg"]
