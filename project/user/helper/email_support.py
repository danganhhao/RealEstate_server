import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def reset_password_email(user):
    """
    Send a email to user email. It be attached a pin code
    :param user, pin
    :return: status of sending 1 for success 0 for failed
    """

    send_from = 'myrealestatedf@gmail.com'
    password = 'anhhao0909'
    send_to = user.email
    username = user.username
    name = user.name
    pin = user.pin
    subject = u'[Reset password] - Đặt lại mật khẩu'
    body = u'Xin chào ' + name + ', \n' \
           + u'\nBạn vừa yêu cầu đặt lại cho tài khoản của bạn' \
           + u'\nTên đăng nhập của bạn là: ' + username \
           + u'\nĐây là mã PIN của bạn: ' \
           + '\n____________' \
           + '\n|                     |' \
           + '\n|     ' + str(pin) + '     |' \
           + '\n|___________|' \
           + u'\nNếu bạn không yêu cầu đổi lại mật khẩu, hãy bỏ qua email này!' \
           + u'\n\nTrân trọng'

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(send_from, password)
        server.sendmail(send_from, send_to, text)
        server.quit()
        return 1
    except Exception as e:
        print(e)
        return 0
