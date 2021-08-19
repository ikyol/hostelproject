from django.core.mail import send_mail


def send_activation_code(email, activation_code, status):
    #     activation_url = f'http://localhost:8000/api/v1/account/activate/{activation_code}'
    #     message = f"""
    #         Спасибо за регистрацию!
    #         Пожалуйста активируйте ваш аккаунт.
    #         Код активации: {activation_url}
    # """
    #     send_mail(
    #         'Активируйте ваш аккаунт',
    #         message,
    #         'krakem.nc@gmail.com',
    #         [email, ],
    #         fail_silently=False
    #     )
    if status == 'register':
        url = f'http://localhost:8000/api/v1/account/activate/{activation_code}'
        message = f'Код для активации аккаунта {url}'
        send_mail(
            'Активируйте ваш аккаунт',
            message,
            'krakem.nc@gmail.com',
            [email, ],
            fail_silently=False
        )
    elif status == 'reset_password':
        send_mail(
            'Сбросить пароль',
            f'Код активации: {activation_code}',
            'krakem.nc@gmail.com',
            [email, ],
            fail_silently=False
        )
