from django.contrib.auth.base_user import BaseUserManager
from rest_framework.views import APIView
from web3 import Web3
from rest_framework.response import Response
from rest_framework import status
from common.utils import CommonUtils, WalletUtils
from common.permissions import ValidClient, IsValidated
from exceptions import InvalidParameterException, InvalidUserCredentials
from user.models import User
from user.serializers import  UserLookupSerializer, UserPatchSerializer, UserCreateSerializer
from django.contrib.auth.hashers import make_password
from django.db.models import Q
import requests
from rest_framework.utils import json
from .models import  User
from common.pagination import CustomPagination


class LoginView(APIView):
    permission_classes = (ValidClient,)

    def post(self, request):
        """
        This method checks the user's wallet address in users and
        generates access token for that user
        @param request: Http Request
        @return: user details & access token
        """
        auth_type = request.GET.get('auth', 'WALLET')

        if auth_type == 'WALLET':
            
            wallet_address = request.data.get("wallet_address", None)
            challenge = request.data.get("challenge", None)
            signature = request.data.get("signature", None)

            if wallet_address == None or wallet_address == "":
                raise InvalidParameterException("wallet_address")

            if challenge == None or challenge == "":
                raise InvalidParameterException("challenge")
            if signature == None  or signature == "":
                raise InvalidParameterException("signature")
            
            wallet_address = Web3.to_checksum_address(wallet_address)

            if WalletUtils.validateSignature(wallet_address,challenge,signature) is True:
                user = User.objects.filter(Q(username=wallet_address) | Q(wallet_address=wallet_address)).first()
                if user is None:
                    user = User.objects.create(username=wallet_address, wallet_address=wallet_address)
                    user.save()
                response = CommonUtils.create_access(user)
                return CommonUtils.dispatch_success(response)
            else:
                raise InvalidParameterException("Invalid Signature. Please login with valid signature.")

        if auth_type == 'GOOGLE':
            payload = {'access_token': request.data.get("token")}  # validate the token
            r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
            data = json.loads(r.text)

            if 'error' in data:
                content = {'message': 'wrong google token / this google token is already expired.'}
                return Response(content)

            # create user if not exist
            try:
                user = User.objects.get(email=data['email'])
            except User.DoesNotExist:
                user = User()
                user.username = data['email']
                # provider random default password
                user.password = make_password(BaseUserManager().make_random_password())
                user.email = data['email']
                user.email_address = data['email']
                user.save()
            response = CommonUtils.create_access(user)
            return CommonUtils.dispatch_success(response)
        elif auth_type == 'ACCOUNT' or auth_type == 'ADMIN':
            email = request.data.get('email')
            password = request.data.get('password')
            user = User.objects.filter(username=email, is_active=True).first()
            if not user:
                user = User.objects.filter(email=email, is_active=True).first()
            if not user or not user.check_password(password) or (auth_type == 'ADMIN' and not user.is_superuser):
                raise InvalidUserCredentials()
            response = CommonUtils.create_access(user)
            return CommonUtils.dispatch_success(response)
        else:
            raise InvalidParameterException("Invalid auth value")



class SignatureView(APIView):
    permission_classes = (ValidClient,)

    def get(self, request):
        """
        This method pulls the message to be signed by the user wallet
        @param request: Http Request
        @return: message to be signed by wallet
        """
        wallet_address = request.GET.get("wallet_address", None)

        if wallet_address is None or wallet_address is "":
            raise InvalidParameterException("wallet_address")
        
        wallet_address = Web3.to_checksum_address(wallet_address)
        
        return CommonUtils.dispatch_success(WalletUtils.generateMessageHash(wallet_address))


class CurrentUserView(APIView):
    permission_classes = (ValidClient, IsValidated,)
    serializer = UserLookupSerializer

    def get(self, request):
        return CommonUtils.dispatch_success(self.serializer(request.user).data)


class AccountView(APIView):
    permission_classes = (ValidClient,)
    pagination_class = CustomPagination()

    def get(self, request, *args, **kwargs):
        queryset = User.objects.filter(is_superuser=False).order_by('-date_joined')

        paginator = self.pagination_class
        result_page = paginator.paginate_queryset(queryset, request, view=self)
        
        serializer = UserLookupSerializer(result_page, many=True)
        
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = {
            **request.data
        }

        if "username" not in data:
            # instead of asking users to register with both email and username we make their email their username
            data["username"] = data["email_address"]
        

        serializer = UserCreateSerializer(data=data)

        if serializer.is_valid():
            password = make_password(request.data['password'])
            user = serializer.save(password=password)
          
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors,)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        return
        try:
            user = User.objects.get(pk=kwargs.get('pk'))
        except User.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserPatchSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            if 'password' in request.data and request.data['password']:
                password = make_password(request.data['password'])
                serializer.save(password=password)
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
class AllUsersView(APIView):
    permission_classes = (ValidClient,)

    def get(self, request, *args, **kwargs):
        queryset = User.objects.filter(is_superuser=False).order_by('-date_joined')
        serializer = UserLookupSerializer(queryset, many=True)
        return Response(serializer.data)
