from base64 import b64encode, b64decode
from datetime import datetime, timedelta
import re

import jwt
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.response import Response

from common.constants import PAGINATION_COUNT
from environment.main import JWT_SECRET_KEY, JWT_ALGORITHM, CIPHER_SECRET_KEY, CIPHER_BLOCK_SIZE

from web3.auto import w3
from eth_account.messages import encode_defunct, defunct_hash_message

from urllib.parse import urlencode
from abc import ABC, abstractmethod
from typing import Tuple, Optional, Callable, List, Iterable, Dict, Any
from web3 import Web3

from web3.contract import Contract
from web3.datastructures import AttributeDict
from web3.exceptions import BlockNotFound
from eth_abi.codec import ABICodec
from rest_framework_simplejwt.tokens import RefreshToken

# Currently this method is not exposed over official web3 API,
# but we need it to construct eth_getLogs parameters
from web3._utils.filters import construct_event_filter_params
from web3._utils.events import get_event_data
from web3.middleware import geth_poa_middleware
from django.utils import timezone

class CommonUtils(object):
    @staticmethod
    def format_url(url, params):
        if params:
            params_str = '?' + urlencode(params) if params else ''
        else:
            params_str = ''

        return url + params_str

    @staticmethod
    def dispatch_success(data, status_code=status.HTTP_200_OK, headers=None):
        return Response({'status': 'success', 'data': data}, status=status_code, headers=headers)

    @staticmethod
    def get_paginated(query_set, serializer, current_page, per_page=PAGINATION_COUNT, order_by=None, context=None):
        """
        This method paginates the provided query set based on
        requested page and returns the paginated response body
        @param query_set: Queryset object of a model
        @param serializer: Serializer to use on query set
        @param current_page: Requested Page
        @param per_page: Required records per page
        @param order_by: Sorting Field
        @param context: Context dictionary to pass into the serializer
        @return: Paginated response body
        """

        if order_by:
            query_set = query_set.order_by(order_by)

        paginator = Paginator(query_set, per_page)
        total_pages = paginator.num_pages
        if total_pages >= int(current_page):
            page = paginator.page(current_page)
            result_data = page.object_list
            if serializer is not None:
                serializer = serializer(page.object_list, many=True, context=context)
                result_data = serializer.data

            return {
                'page': current_page,
                'total_pages': total_pages,
                'total_count': paginator.count,
                'records_per_page': per_page,
                'data': result_data
            }
        raise Exception('Page not found')

    @staticmethod
    def create_access(user):
        try:
            refresh_token = RefreshToken.for_user(user)
            refresh_token.set_exp(lifetime=timedelta(days=360))

            payload = {
                "user_id": user.id,
                "wallet_address": user.wallet_address,
                "email": user.email,
                "exp": int((timezone.now() + timedelta(days=360)).timestamp())
            }

            token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")

            payload["access_token"] = token
            payload["refresh_token"] = str(refresh_token)

            return payload
        except Exception as e:
            print(f"Error in create_access: {e}")
            raise e


# Utils class to encrypt and decrypt strings
class CipherUtils:

    @staticmethod
    def get_cipher_object():
        return AES.new(CIPHER_SECRET_KEY.encode(), AES.MODE_ECB)

    @staticmethod
    def encrypt(string):
        """
        @note Encrypts the string using AES cipher and
        return the encrypted string the base64 encoded string
        @param string: String to encrypt
        @return: base64 encoded - encrypted string
        """
        cipher = CipherUtils.get_cipher_object()
        return b64encode(
            cipher.encrypt(
                pad(string.encode(), CIPHER_BLOCK_SIZE)
            )
        ).decode()

    @staticmethod
    def decrypt(string):
        """
        @note Decrypts the base64 encoded AES Cipher text and
        returns the plain string
        @param string: Base64 encoded AES cipher text
        @return: Plain text
        """
        cipher = CipherUtils.get_cipher_object()
        return unpad(cipher.decrypt(b64decode(string)), CIPHER_BLOCK_SIZE).decode()

# Utils help to generate signature from wallet and validate 
class WalletUtils:
    @staticmethod
    def generateMessageHash(wallet_address):

        # This message needs to be signed by user to validate authenticate wallet connection
        expiry_time = datetime.now() + timedelta(minutes=2)
        expiry_time_formatted = expiry_time.strftime("%Y-%m-%d %H:%M:%S")
        validation_message = "This message is used for signature validation from Acquire for the wallet address {} which expires at {}"
        message = (validation_message.format(wallet_address, expiry_time_formatted))
        return message
    
    @staticmethod
    def validateSignature(wallet_address, challenge, signature):
        try:
            # Validate the message
            if not re.search(wallet_address, challenge):
                return False
            
            # if the signature expired by 2 minutes, throw false
            expiry_time = datetime.strptime(challenge[-19:],"%Y-%m-%d %H:%M:%S")
            current_time = datetime.now()
            if not expiry_time >= current_time:
                return False

            # Verify the signature signed by user.
            message = encode_defunct(text=challenge)
            signed_address = (w3.eth.account.recover_message(message, signature=signature)).lower()
            
            # Same wallet address means same user.
            if str(wallet_address).lower() == str(signed_address):
                # Valid User
                return True
            else:
               return False
        except:
            return False
        
    @staticmethod
    def validateWithdrawSignature(wallet_address, challenge, signature):
        try:
            # Encode the message using encode_defunct
            message = encode_defunct(hexstr=challenge)

            signed_address = w3.eth.account.recover_message(message, signature=signature).lower()
    
            if str(wallet_address).lower() == str(signed_address).lower():
                # Valid User
                return True
            else:
               return False
        except  Exception as e:
            return False
        