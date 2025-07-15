from django.contrib.auth import get_user_model

User = get_user_model()


class SuperUser(User):
    # To be assigned to the Group HeadStaff
    class Meta:
        abstract = True


class HeadStaff(User):
    # To be assigned to the Group HeadStaff
    class Meta:
        abstract = True


class NormalStaff(User):
    # To be assigned to the Group HeadStaff
    class Meta:
        abstract = True
