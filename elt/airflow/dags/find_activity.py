"""
### Fetch data from an API

This DAG fetches an activity from the boredapi.com API and writes it to a file
using task flow tasks.
"""

from airflow.decorators import dag, task
from airflow.models import Variable
from pendulum import datetime
import requests

API = "https://bored-api.appbrewery.com/random"

@dag(
  start_date=datetime(2024, 1, 1),
  schedule="@daily",
  tags=["activity"],
  catchup=False,
)
def find_activity():
  @task
  def get_activity():
    r = requests.get(API, timeout=10)
    return r.json()

  @task
  def write_activity_to_file(response):
    filepath = Variable.get("activity_file")
    with open(filepath, "a") as f:
      f.write(f"Today you will: {response['activity']}\r\n")
    return filepath

  @task
  def read_activity_from_file(filepath):
    with open(filepath, "r") as f:
      print(f.read())

  read_activity_from_file(write_activity_to_file(get_activity()))

find_activity()