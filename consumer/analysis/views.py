from django.shortcuts import render, redirect
from . import helpers
from .forms import MetricsForm
from datetime import date, datetime
import json

global_url = "http://252.3.36.203:8041/v1/metric/"

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
    response = sess.get(global_url)

    # Parse the TEXT response to JSON
    metrics = json.loads(response.text)

    # Check errors in response
    if "error" in metrics:
      return render(request, 'error_page.html', { "error": metrics["error"]["message"] })

    # if successful, print response
    return render(request, 'metrics.html', { "metrics": metrics })

def detail(request, id, definition = 0, aggregation = 'mean'):
  if request.method == 'POST':
    form = MetricsForm(request.POST)

    if form.is_valid():
      definition = form.cleaned_data.get('definition')
      aggregation = form.cleaned_data.get('aggregation')


      return redirect(detail, id, definition, aggregation)


  sess = getSession(request)

  # Do the request, this returns TEXT (REST GET)
  response = sess.get(global_url + id)

  metric = json.loads(response.text)

  # Check errors in response
  if "error" in metric:
    return render(request, 'error_page.html', { "error": metric["error"]["message"] })



  # Do the request, this returns TEXT (REST GET METHOD)
  response_values = sess.get(global_url + id + "/measures?aggregation=" + aggregation)

  values = json.loads(response_values.text)

  # Check errors in response
  if "error" in values:
    return render(request, 'error_page.html', { "error": values["error"]["message"] })

  # We pick the definition from the response, by default the first one (i.e.: index: 0)
  granularity_value = metric["archive_policy"]["definition"][definition]["granularity"]
  # Convert granularity time in seconds (e.g.: "0:01:00" -> 60)
  granularity_in_seconds = helpers.getTimeInSeconds(granularity_value)

  # We filter values by granularity chosen to get the DATES
  labels = [ element[0] for element in values if element[1] == granularity_in_seconds ]

  # We filter values by granularity chosen to get the VALUES
  values = [ element[2] for element in values if element[1] == granularity_in_seconds ]

  # Gnocchi accepted fomat: ISO format (datatime)
  # Calendar accepted fomat: data
  data = {
    "metric": metric,
    "labels": labels,
    "values": values,
    "selectedDefinition": definition,
    "selectedAggregation": aggregation
  }

  return render(request, 'detail.html', data)




