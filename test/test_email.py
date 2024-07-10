from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch, ANY

# from email_libs.letter import send_email
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(smtp_server, smtp_port, from_addr, to_addr, subject, body):
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(from_addr, "MyPassword")
    text = msg.as_string()
    server.sendmail(from_addr, to_addr, text)
    server.quit()



class TestEmail(TestCase):

    @patch('smtplib.SMTP')
    def test_send_mail_params(self, mock_smtp):
        instance = mock_smtp.return_value
        smtp_server = "smtp.example.com"
        smtp_port = 587
        from_addr = "mymail@wxample.com"
        to_addr = "hismail@example.com"
        subject = "Subject"
        body = "Mail content"
        password = "MyPassword"

        send_email(
            smtp_server=smtp_server,
            smtp_port=smtp_port,
            from_addr=from_addr,
            to_addr=to_addr,
            subject=subject,
            body=body
        )

        mock_smtp.assert_called_with(smtp_server, 587)

        instance.starttls.assert_called_with()
        instance.login.assert_called_with(from_addr, password)
        instance.sendmail.assert_called_with(from_addr,
                                             to_addr,
                                             ANY)
        instance.quit.assert_called_with()

# assert_called_once_with(1, 2, 3)
# mock.assert_any_call(1, 2, arg='thing')
# mock.assert_has_calls(calls, any_order=True)
# assert_not_called()
#
# mock = Mock(return_value=None)
# mock('hello')
# mock.called
# True
# mock.reset_mock()
# mock.called
# False
# mock.call_args_list == expected
# mock.assert_awaited()
# mock.method.assert_awaited_once()
# mock.assert_any_await('other')
# mock.assert_not_awaited()
