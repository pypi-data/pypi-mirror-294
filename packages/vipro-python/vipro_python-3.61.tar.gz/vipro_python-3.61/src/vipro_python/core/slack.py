import requests
import json

class Slack:
  def __init__(self, webhook_url: str):
    self.url = webhook_url

  def send(self, message: dict):
    requests.post(
      self.url,
      data=json.dumps(message),
      headers={
        'Content-Type': "application/json",
      }
    )

  def send_simple(self, message: str, channel: str, mrkdwn: bool = True):
    return self.send({
      "channel": channel,
      "text": message,
      "mrkdwn": mrkdwn,
    })
