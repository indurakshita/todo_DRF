from rest_framework.throttling import AnonRateThrottle,UserRateThrottle

from rest_framework.exceptions import Throttled
from django.utils.translation import gettext_lazy as _


class AnonUserThrottle(AnonRateThrottle):
    THROTTLE_RATES = {
        'anon': '5/hour',  
    }

    def allow_request(self, request, view):
        if not request.user.is_authenticated:
            if super().allow_request(request, view):
                return True
            else:
                raise Throttled(
                            detail=_("Anonymous user request limit exceeded. Sign up to increase the limit.\n"
                                "Visit - http://127.0.0.1:8000/signup/"),
                                )
        return super().allow_request(request, view)


class BasicUserThrottle(UserRateThrottle):
    rate = '5/minute' 
    
    
class AdvanceUserThrottle(UserRateThrottle):
    rate = '10/minute' 
    
    
class PremiumUserThrottle(UserRateThrottle):
    rate = '15/minute' 