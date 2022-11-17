# from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
# from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
#
# @receiver(post_save, sender=settings.AUTH_USER_MODEL, weak=False)
# def create_jwt_token(sender, instance=None, created=False, **kwargs):
#     user = sender.objects.last()
#     if created:
#         access_token = AccessToken.for_user(user)
#         refresh_token = RefreshToken.for_user(user)
#         data = f'Access token is {access_token}\nRefresh token is {refresh_token}'
#         print(data)
#
