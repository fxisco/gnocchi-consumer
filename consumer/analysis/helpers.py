import datetime
import time
import subprocess
import requests

def getTimeInSeconds(granularity):
    x = time.strptime(granularity,'%H:%M:%S')

    return datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()

def getLastDateOfMonth():
    any_date = datetime.date.today()

    # Guaranteed to get the next month. Force any_date to 28th and then add 4 days.
    next_month = any_date.replace(day=28) + datetime.timedelta(days=4)

    # Subtract all days that are over since the start of the month.
    last_day_of_month = next_month - datetime.timedelta(days=next_month.day)

    return last_day_of_month

# Gets the token to do the requests
def get_token():
  # runs command "openstack token issue" to generate token
  out = subprocess.Popen(['openstack', 'token', 'issue'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

  # Gets the output of the command.
  # stdout: normal output of the command.
  # stderr: contains any error if the command fails.
  stdout,stderr = out.communicate()

  # if we have errors return None
  # if errors are empty, go with getting the token
  if stderr == None:
    # The response is in binary format, we convert to "utf-8" characters
    # Splits the text with the "|" because the response is in this format.
    response = stdout.decode("utf-8").split("|")

    # if we were able to split by "|", we had a successful response
    # if not, return None
    if len(response) > 0:
      return response[8].strip()
    else:
      return None
  else:
    return None

# Gets the session to do the requests
def get_requests_session(token):
  sess = requests.Session()
  sess.headers.update({'X-AUTH-TOKEN': token,'Content-type':'application/json'})

  return sess

