__author__ = 'Amir H. Nejati'

import mandrill


class EmailClient:
    api_key = None
    async_mode = None

    def __init__(self, api_key, async_mode=True):
        self.api_key = api_key
        self.async_mode = async_mode

    def send(self, html_content, email_subject,
             from_email, recipients_email_list, from_name=None, reply_to_email=None,
             track_clicks=False, track_opens=False, tracking_domain=None, attachments=[{}]):
        """find reference here: https://mandrillapp.com/api/docs/messages.python.html
        HOWTO: use these sample signature:
        recipients = [{'email': 'recipient.email@example.com',
                       'name': 'Recipient Name',
                       'type': 'to'}]

        attachments = [{'content': 'ZXhhbXBsZSBmaWxl',
                        'name': 'myfile.txt',
                        'type': 'text/plain'}]
       """
        recipients = [{'email': i, 'type': 'to'} for i in recipients_email_list]
        message = {  #
                     'attachments': attachments,
                     'from_email': from_email,
                     'from_name': from_name,
                     'headers': {'Reply-To': reply_to_email} if reply_to_email else {},
                     'html': html_content,
                     'important': False,
                     'merge': True,
                     'merge_language': 'mailchimp',
                     'preserve_recipients': False,
                     'signing_domain': None,
                     # a custom domain to use for SPF/DKIM signing instead of mandrill (for "via" or "on behalf of" in email clients)
                     'subject': email_subject,
                     'to': recipients,
                     'track_clicks': track_clicks,
                     'track_opens': track_opens,
                     'tracking_domain': tracking_domain,
                     'url_strip_qs': True,
                     'view_content_link': None}  # set to false to remove content logging for sensitive emails

        try:
            mandrill_client = mandrill.Mandrill(self.api_key)
            mandrill_client.messages.send(message=message, async=self.async_mode,
                                          ip_pool='Main Pool')  # , send_at='YYYY-MM-DD HH:MM:SS')
        except Exception as e:
            raise e
