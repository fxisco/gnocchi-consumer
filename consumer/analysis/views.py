from django.shortcuts import render, redirect
from . import helpers
from .forms import MetricsForm
from datetime import date
import json

def getSession(request):
  # Need a Token
  token = helpers.get_token()

  # if token wasn't found
  if token == None:
    return render(request, 'error_page.html', { "error": "Token not found!" })

  # Gets Session to make the requests
  session = helpers.get_requests_session(token)

  return session


def index(request):

    sess = getSession(request)

    # Do the request, this returns TEXT
    response = sess.get("http://252.3.36.203:8041/v1/metric")

    # Parse the TEXT response to JSON
    metrics = json.loads(response.text)

    # Check errors in response
    if "error" in metrics:
      return render(request, 'error_page.html', { "error": metrics["error"]["message"] })

    # if successful, print response
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

  sess = getSession(request)

  # Do the request, this returns TEXT
  response = sess.get("http://252.3.36.203:8041/v1/metric/" + id)

  metric = json.loads(response.text)

  # Check errors in response
  if "error" in metric:
    return render(request, 'error_page.html', { "error": metric["error"]["message"] })

  # Do the request, this returns TEXT
  response_values = sess.get("http://252.3.36.203:8041/v1/metric/" + id + "/measures")

  values = json.loads(response_values.text)

  # Check errors in response
  if "error" in values:
    return render(request, 'error_page.html', { "error": values["error"]["message"] })

  # We pick the definition from the response, by default the first one (i.e.: index: 0)
  granularity_value = metric["archive_policy"]["definition"][definition]["granularity"]
  # Convert granularity time in seconds (e.g.: "0:01:00" -> 60)
  granularity_in_seconds = helpers.getTimeInSeconds(granularity_value)

  # We filter values by granularity chosen to get the DATES
  dates = [ element[0] for element in values if element[1] == granularity_in_seconds ]

  # We filter values by granularity chosen to get the VALUES
  values = [ element[2] for element in values if element[1] == granularity_in_seconds ]

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




