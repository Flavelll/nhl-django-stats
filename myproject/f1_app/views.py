from django.shortcuts import render
from .models import Session, Lap
from .forms import FilterForm
import json

def dashboard(request):
    chart_data = {}

    session_id = request.GET.get('session')
    if session_id:
        selected_session = Session.objects.filter(session_key=session_id).first()
    else:
        selected_session = Session.objects.filter(session_type="Race").order_by("-date_start").first()

    driver_choices = []
    if selected_session:
        drivers = (
            Lap.objects
            .filter(session_key=selected_session.session_key)
            .values_list("driver_number", flat=True)
            .distinct()
            .order_by("driver_number")
        )
        driver_choices = [(str(d), f"Driver {d}") for d in drivers]

    form = FilterForm(request.GET or None, driver_choices=driver_choices)

    if not session_id and selected_session:
        form.fields['session'].initial = selected_session.session_key

    if form.is_valid():
        selected_drivers = form.cleaned_data.get("drivers")

        if selected_drivers and selected_session:
            laps = Lap.objects.filter(
                session_key=selected_session.session_key,
                driver_number__in=selected_drivers
            ).order_by("lap_number")

            for d_num in selected_drivers:
                d_laps = [l for l in laps if str(l.driver_number) == str(d_num)]
                chart_data[d_num] = {
                    "laps": [l.lap_number for l in d_laps],
                    "times": [l.lap_duration if l.lap_duration else 0 for l in d_laps]
                }

    return render(request, "f1_app/dashboard.html", {
        "form": form,
        "chart_data": json.dumps(chart_data),
    })
