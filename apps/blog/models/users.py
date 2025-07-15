from django.contrib.auth import get_user_model

User = get_user_model()


class BloggerStaff(User):
    # To be assigned to the Group bloggerstaff
    class Meta:
        abstract = True
