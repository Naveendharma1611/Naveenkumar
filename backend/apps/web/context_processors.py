from apps.portfolio.models import SiteProfile


def site(request):
    """Makes the site owner's profile available to every template as `profile`."""
    return {"profile": SiteProfile.load()}
