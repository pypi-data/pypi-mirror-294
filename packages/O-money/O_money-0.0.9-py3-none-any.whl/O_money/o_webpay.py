import os
from dotenv import load_dotenv

from datetime import datetime, timedelta
import os, argparse, logging
import requests
from .models import WebPayment, WebPaymentStatus
from dotenv import load_dotenv

load_dotenv()


class Webpay:
    _CLIENT_ID = os.getenv("client_id")
    _MERCHANT_KEY = os.getenv("merchant_key")

    _RETURN_URL = os.getenv("return_url")
    _CANCEL_URL = os.getenv("cancel_url")
    _NOTIF_URL = os.getenv("notif_url")

    def __init__(
        self, logger: logging.Logger, currency: str = "OUV", verbose=False
    ) -> None:
        self.logger = logger
        self.verbose = verbose
        self.currency = currency
        self.base_url = "https://api.orange.com"

        self._expire_at = None

    def _get_token(self):
        if not self._CLIENT_ID:
            self.logger.error("Didn't found CLIENTID in system env, export it first")
            exit(-1)
        try:
            response = requests.post(
                f"{self.base_url}/oauth/v3/token",
                headers={
                    "Authorization": f"Basic {self._CLIENT_ID}",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/json",
                },
                data={"grant_type": "client_credentials"},
            )

            current_time = datetime.now()

            response = response.json()
            self.logger.info("response: %s", response)
            self._access_token = response["access_token"]

            self._expire_at = current_time + timedelta(seconds=response["expires_in"])

        except requests.exceptions.RequestException as e:
            self.logger.error("Request failed : %s", e)

    @property
    def token(self):
        if self._expire_at is None or self._expire_at <= datetime.now():
            self._get_token()

        return self._access_token

    def init_pay(self, amount: int, order_id: str, reference: str, lang: str = "fr"):
        try:
            response = requests.post(
                f"{self.base_url}/orange-money-webpay/dev/v1/webpayment",
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                json={
                    "merchant_key": self._MERCHANT_KEY,
                    "currency": self.currency,
                    "order_id": order_id,
                    "amount": amount,
                    "return_url": self._RETURN_URL,
                    "cancel_url": self._CANCEL_URL,
                    "notif_url": self._NOTIF_URL,
                    "lang": lang,
                    "reference": reference,
                },
            )
            response = response.json()
            if "status" in response and response["status"] == 201:  # TODO:
                return WebPayment(**response)

        except requests.exceptions.RequestException as e:
            self.logger.error("Request failed : %s", e)

    def payment_status(self, order_id: str, amount: int, pay_token: str):
        try:
            response = requests.post(
                f"{self.base_url}/orange-money-webpay/dev/v1/transactionstatus",
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/json",
                },
                json={"order_id": order_id, "amount": amount, "pay_token": pay_token},
            )
            response = response.json()
            self.logger.info("Payment Status Response: %s", response)
            if response["status"] == 201:
                return WebPaymentStatus(**response)

        except requests.exceptions.RequestException as e:
            self.logger.error("Request failed : %s", e)
