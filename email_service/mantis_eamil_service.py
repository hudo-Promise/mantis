import json

from common_tools.tools import async_task, op11_redis_client
from email_service import send_email
from common_tools.tools import create_current_format_time


general_mantis_email_template = """
        Dear User:

            **This is an automated message from the MANTIS**

            Notification Timestamp: %(timestamp)s

            %(content)s

            To remove yourself from the cc list of such notification emails, 
            please change mail recipient permissions to “no” within your mantis project settings.

            Any questions/comments/concerns please contact the TA team from C/EI-11.

        Best,

        Testing Automations Team

"""


mantis_email_content = {
    'share_by_email': """
            %(sender_name)s recommends a dashboard %(dashboard_name)s with you in Mantis，containing cards as below:

            CardName: %(card_name)s

            MilestoneName: %(milestone_name)s

            Click URL to see detail:

            URL: %(url)s

            %(share_time)s
    """
}


mantis_email_theme = {
    'share_by_email': """
        【Mantis】 %(sender_name)s share a dashboard %(dashboard_name)s with you at %(share_time)s
"""
}


mantis_email_info = {
    'mail_user': 'taeechn_mantis@126.com',
    'mail_pass': 'ONCSGGQREDQKEUGV',
    'sender': 'taeechn_mantis@126.com'
}


def generate_mantis_email_text(email_info_dict):
    email_content = mantis_email_content.get('share_by_email') % email_info_dict
    theme = mantis_email_theme.get('share_by_email') % email_info_dict
    email_text = general_mantis_email_template % {
        'timestamp': create_current_format_time(),
        'content': email_content,
    }
    return email_text, theme


@async_task
def async_send_mantis_email(params_dict):
    receivers = params_dict.get('receivers')
    cc = []
    card_name = ''
    milestone_name = ''
    for row in params_dict.get('data'):
        if row.get('type') == 'card':
            card_name += '【%s】' % row.get('card_name')
        elif row.get('type') == 'milestone':
            milestone_name += '【%s】' % row.get('card_name')
    break_flag = 0
    for receiver in receivers:
        if break_flag < 1:
            receiver_email = json.loads(op11_redis_client.get('tms_user_info')).get(str(receiver)).get('account')
            mail_dict = {
                'sender_name': params_dict.get('sender_name').get('username'),
                'dashboard_name': params_dict.get('dashboard_name'),
                'card_name': card_name,
                'milestone_name': milestone_name,
                'url': params_dict.get('url'),
                'share_time': params_dict.get('share_time')
            }
            email_content, theme = generate_mantis_email_text(mail_dict)
            send_email([receiver_email], cc, theme, email_content, 1, mantis_email_info)
        break_flag += 1

