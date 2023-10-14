from django.contrib.auth.models import Group
from rest_framework import exceptions

def get_group_or_404(group_view_name, view2group_name):
        group_db_name = view2group_name.get(group_view_name)
        if group_db_name:
            return Group.objects.get(name=group_db_name)
        raise exceptions.NotFound(
            {"error": f"Group {group_view_name} does not exist"})