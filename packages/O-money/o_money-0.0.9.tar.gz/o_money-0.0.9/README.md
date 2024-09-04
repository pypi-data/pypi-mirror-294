# O_money

**Introduction**

For use Orange Money Web Payment on web.

**Installation**

The latest version can be obtained from PyPI:

`pip install O-money`

**Usage**

For use O_money create .env file and define the following variable

## `_client_id, merchant_key, return_url, cancel_url, notif_url_`

**Example**

```python
from O_money import o_webpay
import logging

l = logging.Logger("test")
webpay = o_webpay.Webpay(logger=l)
response = webpay.init_pay(amount=2500, order_id="5f64v", reference="154f5", lang="us")
print(response)

```
