from django.shortcuts import render, redirect
from . import helpers
from .forms import MetricsForm
from datetime import date

def index(request):
    metrics = [{"id": "10e7a9fe-7bc2-4324-a983-0147f17144f5", "creator": "297cb656c0054fa98b070504e85e07c9:eb65f9e29c134540987622dd60c8dc27", "name": "humidity", "unit": "null", "resource_id": "null", "archive_policy": {"name": "low", "back_window": 0, "definition": [{"timespan": "30 days, 0:00:00", "granularity": "0:05:00", "points": 8640}], "aggregation_methods": ["count", "min", "std", "max", "sum", "mean"]}, "created_by_user_id": "297cb656c0054fa98b070504e85e07c9", "created_by_project_id": "eb65f9e29c134540987622dd60c8dc27"}, {"id": "ca3ac69a-67d0-4bd4-bd8b-22debdab0fb3", "creator": "297cb656c0054fa98b070504e85e07c9:eb65f9e29c134540987622dd60c8dc27", "name": "temperature", "unit": "null", "resource_id": "null", "archive_policy": {"name": "medium", "back_window": 0, "definition": [{"timespan": "7 days, 0:00:00", "granularity": "0:01:00", "points": 10080}, {"timespan": "365 days, 0:00:00", "granularity": "1:00:00", "points": 8760}], "aggregation_methods": ["count", "min", "std", "max", "sum", "mean"]}, "created_by_user_id": "297cb656c0054fa98b070504e85e07c9", "created_by_project_id": "eb65f9e29c134540987622dd60c8dc27"}, {"id": "e96fb878-7eb1-41b7-a2e2-91209818a84c", "creator": "297cb656c0054fa98b070504e85e07c9:eb65f9e29c134540987622dd60c8dc27", "name": "wind speed", "unit": "null", "resource_id": "null", "archive_policy": {"name": "high", "back_window": 0, "definition": [{"timespan": "1:00:00", "granularity": "0:00:01", "points": 3600}, {"timespan": "7 days, 0:00:00", "granularity": "0:01:00", "points": 10080}, {"timespan": "365 days, 0:00:00", "granularity": "1:00:00", "points": 8760}], "aggregation_methods": ["count", "min", "std", "max", "sum", "mean"]}, "created_by_user_id": "297cb656c0054fa98b070504e85e07c9", "created_by_project_id": "eb65f9e29c134540987622dd60c8dc27"}]

    return render(request, 'metrics.html', { "metrics": metrics })


def detail(request, id, definition = 0, aggregation = 'mean', start_date = None, stop_date = None):

  if request.method == 'POST':
    form = MetricsForm(request.POST)

    if form.is_valid():
      definition = form.cleaned_data.get('definition')
      aggregation = form.cleaned_data.get('aggregation')
      startdate = form.cleaned_data.get('startdate')
      stopdate = form.cleaned_data.get('stopdate')

      return redirect(detail, id, definition, aggregation, startdate, stopdate)

  if start_date == None:
    start_date = date.today().replace(day=1)

  if stop_date == None:
    stop_date = helpers.getLastDateOfMonth()

  metric = {
      "id":"10e7a9fe-7bc2-4324-a983-0147f17144f5",
      "creator":"297cb656c0054fa98b070504e85e07c9:eb65f9e29c134540987622dd60c8dc27",
      "name":"humidity",
      "unit": "null",
      "resource_id": "null",
      "archive_policy":{
         "name":"low",
         "back_window":0,
         "definition":[
            {
               "timespan":"30 days, 0:00:00",
               "granularity":"0:05:00",
               "points":8640
            }
         ],
         "aggregation_methods":[
            "count",
            "min",
            "std",
            "max",
            "sum",
            "mean"
         ]
      },
      "created_by_user_id":"297cb656c0054fa98b070504e85e07c9",
      "created_by_project_id":"eb65f9e29c134540987622dd60c8dc27"
   }

  values = [
  ["2020-06-10T16:40:00+00:00", 300.0, 57.013062521671884],
  ["2020-06-10T16:45:00+00:00", 300.0, 60.96430624660876],
  ["2020-06-10T16:50:00+00:00", 300.0, 40.85293391772962],
  ["2020-06-10T16:55:00+00:00", 300.0, 61.971238021727615],
  ["2020-06-10T17:00:00+00:00", 300.0, 56.56529251040247],
  ["2020-06-10T17:05:00+00:00", 300.0, 47.71236036419723],
  ["2020-06-10T17:10:00+00:00", 300.0, 48.39607345539477],
  ["2020-06-10T17:15:00+00:00", 300.0, 56.09292152158552],
  ["2020-06-10T17:20:00+00:00", 300.0, 58.20539502381264],
  ["2020-06-10T17:25:00+00:00", 300.0, 52.58915302713453]
]

  granularity = helpers.getTimeInSeconds(metric["archive_policy"]["definition"][definition]["granularity"])
  dates = [ element[0] for element in values if element[1] == granularity ]
  values = [ element[2] for element in values if element[1] == granularity ]

  data = {
    "start_date": start_date,
    "stop_date": stop_date,
    "metric": metric,
    "dates": dates,
    "values": values,
    "selectedDefinition": definition,
    "selectedAggregation": aggregation
  }

  return render(request, 'detail.html', data)




