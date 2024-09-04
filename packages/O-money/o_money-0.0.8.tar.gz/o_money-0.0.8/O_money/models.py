from dataclasses import dataclass, asdict
import json


@dataclass
class WebPayment:
    status: int
    message: str
    pay_token: str
    notif_token: str
    payment_url: str

    def to_json(self):
        return json.dumps(asdict(self))


@dataclass
class WebPaymentStatus:
    status: int
    order_id: str
    txnid: str

    def to_json(self):
        return json.dumps(asdict(self))
