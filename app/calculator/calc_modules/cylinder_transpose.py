from django.http import HttpResponse
from django.views import View


class CTCalculate(View):
    def post(self, request):
        """Calculates the cylindrical tranposition"""
        names = {
            "sphere": "Sphere",
            "cylinder": "Cylinder",
            "axis": "Axis",
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
            ref = {k: float(v) for k, v in ref.items()}
            sphere = ref["sphere"]
            cylinder = ref["cylinder"]
            axis = ref["axis"]

            warning = ""
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

            answer = (
                warning
                + f"""
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
            )
        return HttpResponse(answer)
