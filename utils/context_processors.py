from accounts.models import UserProfiles

def get_user_profile_context(request):
    if request.user.is_authenticated:
        if not request.user.is_staff:
            user_profile = UserProfiles.objects.get(user=request.user.id)
            return {'user_profile': user_profile}
        else:
            return {}
    else:
        return {}