
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from common.utils import CommonUtils

class HealthView(APIView):
    permission_classes = (AllowAny,)

    def get(self, _):
        """
        @description: This API used to check if server is active or not
        @param _:
        @return: "SUCCESS"
        """
        return CommonUtils.dispatch_success("SUCCESS")