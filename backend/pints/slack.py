import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import pints
from logger import logger

token = os.environ.get('PAPER_SLACK_TOKEN')
CLIENT_ID = os.environ.get('PAPER_SLACK_CLIENT_ID')
CLIENT_SECRET = os.environ.get('PAPER_SLACK_SECRET')

# client = WebClient(token=token)

def testPush(d, token):
    print('testPush...')
    client = WebClient(token=token)
    response = client.chat_postMessage(
        channel='#demo',
        blocks = [
            {
                "type": "section", 
                "text": {
                    "type": "plain_text", 
                    "text": d.get('msg', 'test msg...')
                    },
            }
        ]
    )
    print('testPush result...', response["message"])

def getToken(code):
    client = WebClient()
    oauth_response = client.oauth_v2_access(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri='https://pulse.trypaper.io/slack2',
        code=code
    )
    installed_enterprise = {}
    is_enterprise_install = oauth_response.get("is_enterprise_install")
    if is_enterprise_install:
        installed_enterprise = oauth_response.get("enterprise", {})
    installed_team = oauth_response.get("team", {})
    installer = oauth_response.get("authed_user", {})
    incoming_webhook = oauth_response.get("incoming_webhook", {})

    bot_token = oauth_response.get("access_token")
    # NOTE: oauth.v2.access doesn't include bot_id in response
    bot_id = None
    enterprise_url = None
    if bot_token is not None:
        auth_test = client.auth_test(token=bot_token)
        bot_id = auth_test["bot_id"]
        if is_enterprise_install is True:
            enterprise_url = auth_test.get("url")

    installation = {
        'app_id': oauth_response.get("app_id"),
        'enterprise_id': installed_enterprise.get("id"),
        'enterprise_name': installed_enterprise.get("name"),
        'enterprise_url': enterprise_url,
        'team_id': installed_team.get("id"),
        'team_name': installed_team.get("name"),
        'bot_token': bot_token,
        'bot_id': bot_id,
        'bot_user_id': oauth_response.get("bot_user_id"),
        'bot_scopes': oauth_response.get("scope"),  # comma-separated string
        'user_id': installer.get("id"),
        # 'user_token': installer.get("access_token"),
        'user_scopes': installer.get("scope"),  # comma-separated string
        'incoming_webhook_url': incoming_webhook.get("url"),
        'incoming_webhook_channel': incoming_webhook.get("channel"),
        'incoming_webhook_channel_id': incoming_webhook.get("channel_id"),
        'incoming_webhook_configuration_url': incoming_webhook.get("configuration_url"),
        'is_enterprise_install': is_enterprise_install,
        'token_type': oauth_response.get("token_type"),
    }
    logger.info(f'getToken... {installation}')
    return installation

def weekly(d, token):
    logger.info(f'push...')
    client = WebClient(token=token)
    try:
        # response = client.chat_postMessage(channel='#random', text="Hello world!")
        response = client.chat_postMessage(
            channel='#demo',
            text="Paper Alert",
            blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f":moneybag: MRR: ${d['summary']['currentMrrK']}k",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": d['summary']['mrrMsg']
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": d['mrrChartUrl'],
                        "alt_text": "MRR"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f":smiley: Customers: {d['summary']['currentCustomers']}",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": d['summary']['customerMsg']
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": d['customerChartUrl'],
                        "alt_text": "MRR"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Open Pulse",
                                "emoji": True
                            },
                            "value": "open_paper",
                            "url": "https://pulse.trypaper.io?ref=slack_alert",
                            "action_id": "open_paper"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Update Goals",
                                "emoji": True
                            },
                            "value": "set_goals",
                            "url": "https://pulse.trypaper.io?ref=set_goals",
                            "action_id": "set_goals"
                        }
                    ]
                },
            ]
        )
        print('push...', response)
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"slack pints error: {e.response['error']}")

def customerAlert(d, token):
    logger.info(f'customerAlert...')
    client = WebClient(token=token)
    try:
        # response = client.chat_postMessage(channel='#random', text="Hello world!")
        response = client.chat_postMessage(
            channel=f"#{d['slackChannel']}",
            text="Paper Alert",
            blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f":moneybag: New MRR: ${d['mrr']} from {d['email']}",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": d['msg']
                    },
                },
                {
                    "type": "divider"
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Open Pulse",
                                "emoji": True
                            },
                            "value": "open_paper",
                            "url": "https://pulse.trypaper.io?ref=slack_alert",
                            "action_id": "open_paper"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Update Goals",
                                "emoji": True
                            },
                            "value": "set_goals",
                            "url": "https://pulse.trypaper.io?ref=set_goals",
                            "action_id": "set_goals"
                        }
                    ]
                },
            ]
        )
        print('push...', response)
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"slack pints error: {e.response['error']}")

def churnAlert(d, token):
    logger.info(f'churnAlert...')
    client = WebClient(token=token)
    try:
        # response = client.chat_postMessage(channel='#random', text="Hello world!")
        response = client.chat_postMessage(
            channel=f"#{d['slackChannel']}",
            text="Pulse Alert",
            blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"Churned ${d['prev_mrr']} from {d['email']}",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": d['msg']
                    },
                },
                {
                    "type": "divider"
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Open Pulse",
                                "emoji": True
                            },
                            "value": "open_paper",
                            "url": "https://pulse.trypaper.io?ref=slack_alert",
                            "action_id": "open_paper"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Update Goals",
                                "emoji": True
                            },
                            "value": "set_goals",
                            "url": "https://pulse.trypaper.io?ref=set_goals",
                            "action_id": "set_goals"
                        }
                    ]
                },
            ]
        )
        print('push...', response)
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"slack pints error: {e.response['error']}")