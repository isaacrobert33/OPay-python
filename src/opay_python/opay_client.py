from requests import post
from .util import generate_ref


class Opay:
    BASE_URL = 'https://cashierapi.opayweb.com/api/v3'
    OPAY_TRANSFER_API = f'{BASE_URL}/transfer/toWallet'
    BANK_TRANSFER_API = f'{BASE_URL}/transfer/toBank'
    OPAY_TRANSFER_STATUS_API = f'{BASE_URL}/transfer/status/toWallet'
    BANK_TRANSFER_STATUS_API = f'{BASE_URL}/transfer/status/toBank'
    BANK_LIST_API = f'{BASE_URL}/banks'
    BALANCE_API = f'{BASE_URL}/balances'
    USER_INFO_API = f'{BASE_URL}/info/user'
    MERCHANT_INFO_API = f'{BASE_URL}/info/merchant'
    BANK_VALIDATE_API = f'{BASE_URL}/verification/accountNumber/resolve'
    SEND_OTP_API = f'{BASE_URL}/info/user/sendOTP'
    CREATE_ACCOUNT_API = f'{BASE_URL}/info/user/create'
    CARD_PAYMENT_API = F'{BASE_URL}/transaction/initialize'
    BANK_ACCOUNT_PAYMENT_API = f'{BASE_URL}/transaction/banks'
    TRANSACTION_STATUS = f'{BASE_URL}/transaction/status'

    def __init__(self, public_key: str, merchant_id: str) -> None:
        self.public_key = public_key
        self.merchant_id = merchant_id
        self.auth = f'Bearer {self.public_key}'

        self.headers = {
            'Authorization': self.auth,
            'Content-Type': 'application/json',
            'MerchantId': self.merchant_id
        }


class OPayInquiry(Opay):
    def get_balance(self):
        response = post(self.BALANCE_API, headers=self.headers)
        return response.json()
    
    def validate_user(self, user_phone: str):
        body = {
            'phoneNumber': user_phone
        }
        response = post(self.USER_INFO_API, headers=self.headers, json=body)
        return response.json()


    def validate_merchant(self, merchant_email: str):
        body = {
            'email': merchant_email
        }
        response = post(self.MERCHANT_INFO_API, headers=self.headers, json=body)
        return response.json()

    def validate_bank(
            self, bank_code: str, 
            account_number: str, 
            country_code: str="NG"):
        body = {
            'bankCode': bank_code,
            'bankAccountNo': account_number,
            'countryCode': country_code
        }
        response = post(self.BANK_VALIDATE_API, headers=self.headers, json=body)
        return response.json()
    

class OpayTransfers(Opay):

    def to_opay_wallet(self, amount: str, 
            reason: str, 
            phone_number: str=None,
            merchant_id: str=None,
            name: str=None,
            currency: str="NGN",
            country: str="NG",
            wallet_type: str="USER"):
        """
        Transfer to Opay wallet

        Args:
            amount (str): Amount to transfer
            phone_number (str): Beneficiary's phone number [Optional]
            merchant_id (str): Merchant's ID [Optional]
            name (str): Beneficiary's Name [Optional]
            currency (str): Currency (defaults to `NGN`)
            country (str): Country (defaults to `NG`)
            wallet_type (str): Wallet type i.e USER or MERCHANT (defaults to `USER`)
        """
        tranx_ref = generate_ref()
        body = {
            "reference": tranx_ref,
            "amount": amount,
            "currency": currency,
            "country": country,
            "receiver": {
                "type": wallet_type
            },
            "reason": reason
        }

        if name:
            body['receiver']['name'] = name

        if wallet_type == "USER":
            body['receiver']['phoneNumber'] = phone_number
        else:
            body['receiver']['merchantId'] = merchant_id
        
        response = post(self.OPAY_TRANSFER_API, headers=self.headers, json=body)

        return response.json()

    def to_bank(self, amount: str, 
            name: str,
            bank_code: str,
            account_number: str,  
            reason: str,
            currency="NGN",
            country: str="NG"):
        """
        Transfer to Bank Account
        
        Args:
            amount (str): Amount to transfer
            name (str): Beneficiary's Name 
            bank_code (str): Beneficiary's bank code
            account_number (str): Beneficiary's account number
            reason (str): Transaction reason (remark)
            currency (str): Currency (defaults to `NGN`)
            country (str): Country (defaults to `NG`)
        """
        tranx_ref = generate_ref()
        body = {
            "reference": tranx_ref,
            "amount": amount,
            "currency": currency,
            "country": country,
            "receiver": {
                "name": name,
                "bankCode": bank_code,
                "bankAccountNumber": account_number
            },
            "reason": reason
        }
        response = post(self.BANK_TRANSFER_API, headers=self.headers, json=body)
        return response.json()
    
    def transfer_status(self, reference: str, order_no: str, recipient_type: str='opay'):
        """
        Get transfer status for opay wallet / bank

        Args:
            reference (str): Transaction reference
            order_no (str): Order number
            recipient_type (str): Recipient type i.e opay or bank (defaults to `opay`)
        """
        body = {
            "referrence": reference,
            "orderNo": order_no
        }
        api = self.OPAY_TRANSFER_STATUS_API if recipient_type == "opay" else self.BANK_TRANSFER_STATUS_API
        response = post(api, headers=self.headers, json=body)

        return response.json()

    def fetch_bank_list(self, country_code: str="NG") -> list:
        """
        fetch available bank list

        ARGS:
            country_code (str): Country code (defaults to `NG`)
        """
        body = {
            "countryCode": country_code
        }
        response = post(self.BANK_LIST_API, headers=self.headers, json=body)

        return response.json()


class OpayAccount(Opay):
    
    def send_otp(self, phone_number: str):
        """
        Send OTP

        ARGS:
            phone_number (str): Phone number to send otp to
        """
        body = {
            "phoneNumber": phone_number
        }

        response = post(self.SEND_OTP_API, headers=self.headers, json=body)

        return response.json()
    
    def create_account(
            self, phone_number: str, 
            email: str, 
            first_name: str, 
            last_name: str, 
            password: str, 
            address: str,
            otp: str
        ):
        """
        Create an Opay User account

        ARGS:
            phone_number (str): Account phone number
            email (str): Account email
            first_name (str): First name
            last_name (str): Last Name
            password (str): User password
            address (str): User's address
            otp (str): Sent OTP
        """
        
        body = {
            "phoneNumber": phone_number,
            "email": email,
            "firstName": first_name,
            "lastName": last_name,
            "password": password,
            "address": address,
            "otp": otp
        }

        response = post(self.CREATE_ACCOUNT_API, headers=self.headers, json=body)

        return response.json()
    

class OpayPayments(Opay):

    def card_payment(self, **kwargs):
        """
        Recieve Payment to Opay from a card
        """
        tranx_ref = generate_ref()
        try:
            body = {
                "reference": tranx_ref,
                "amount": kwargs['amount'],
                "currency": kwargs['currency'],
                "country": kwargs.get('country', "NG"),
                "payType": kwargs.get("pay_type", "bankcard"),
                "firstName;": kwargs['first_name'],
                "lastName": kwargs['last_name'],
                "customerEmail": kwargs['customer_email'],
                "cardNumber": kwargs['card_number'],
                "cardDateMonth": kwargs['card_month'],
                "cardDateYear": kwargs['card_year'],
                "cardCVC": kwargs['card_cvv'],
                "return3dsUrl": kwargs['return_url'],
                "bankAccountNumber": kwargs['account_number'],
                "bankCode": kwargs['bank_code'],
                "reason": kwargs['reason'],
                "callbackUrl": kwargs['callback_url'],
                "expireAt": kwargs['expire_at'],
                "billingZip": kwargs['billing_zip'],
                "billingCity": kwargs['billing_city'],
                "billingAddress": kwargs['billing_address'],
                "billingState": kwargs['billing_state'],
                "billingCountry": kwargs['billing_country']
            }
        except KeyError:
            raise("Required parameter missing!")

        response = post(self.CARD_PAYMENT_API, headers=self.headers, json=body)

        return response.json()

    def bank_account_payment(
            self, amount: str, 
            account_number: str,
            bank_code: str, 
            return_url: str, 
            reason: str, 
            customer_phone: str, 
            bvn: str, 
            dob_day: str, 
            dob_month: str, 
            dob_year: str, 
            pay_type: str="bankaccount",
            currency: str="NGN", 
            country: str="NG"
        ):
        """
        Receive payment to an Opay account from a bank account
        """
        tranx_ref = generate_ref()
        body = {
            "reference": tranx_ref,
            "amount": amount,
            "currency": currency,
            "country": country,
            "payType": pay_type,
            "bankAccountNumber": account_number,
            "bankCode": bank_code,
            "return3dsUrl": return_url,
            "reason": reason,
            "customerPhone": customer_phone,
            "bvn": bvn,
            "dobDay": dob_day,
            "dobMonth": dob_month,
            "dobYear": dob_year
        }

        response = post(self.BANK_ACCOUNT_PAYMENT_API, headers=self.headers, json=body)

        return response.json()

    def transcation_status(self, reference: str, order_no: str):
        """
        Get transaction status

        ARGS:
            reference (str): Reference string
            order_no (str): Order number
        """
        body = {
            "orderNo": order_no,
            "reference": reference
        }

        response = post(self.TRANSACTION_STATUS, headers=self.headers, json=body)

        return response.json()
    