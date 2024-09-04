from typing import Any, Dict, List, Optional
import requests,json
from fakturowniaAPI import enums,errors
from fakturowniaAPI.enums import Kind,PaymentType
class Product:
    name: str
    total_price_gross: float
    quantity: int
    tax : float


class Issuer:
    def __init__(self,seller_name : str,
                      seller_tax_no : str,
                      seller_tax_no_kind : str,
                      seller_bank_account : str,
                      seller_bank : str,
                      seller_post_code : str,
                      seller_city : str,
                      seller_street : str,
                      seller_country : str,
                      invoice_issuer: str,
                      seller_email : Optional[str] = "",
                      seller_www : Optional[str] = "",
                      seller_fax : Optional[str] = "",
                      seller_phone : Optional[str] = "",
                      seller_bd_no : Optional[str] = ""):
        self.seller_name = seller_name
        self.seller_tax_no = seller_tax_no
        self.seller_tax_no_kind = seller_tax_no_kind
        self.seller_bank_account = seller_bank_account
        self.seller_bank = seller_bank
        self.seller_post_code = seller_post_code
        self.seller_city = seller_city
        self.seller_street = seller_street
        self.seller_country = seller_country
        self.invoice_issuer = invoice_issuer
        self.seller_email = seller_email
        self.seller_www = seller_www
        self.seller_fax = seller_fax
        self.seller_phone = seller_phone
        self.seller_bd_no = seller_bd_no

        self.customerDict = {
            "seller_name": self.seller_name,
            "seller_tax_no": self.seller_tax_no,
            "seller_tax_no_kind": self.seller_tax_no_kind,
            "seller_bank_account": self.seller_bank_account,
            "seller_bank": self.seller_bank,
            "seller_post_code": self.seller_post_code,
            "seller_city": self.seller_city,
            "seller_street": self.seller_street,
            "seller_country": self.seller_country,
            "invoice_issuer": self.invoice_issuer,
            "seller_email": self.seller_email,
            "seller_www": self.seller_www,
            "seller_fax": self.seller_fax,
            "seller_phone": self.seller_phone,
            "seller_bd_no": self.seller_bd_no
        }


    def updateValue(self):
        pass

    def deleteValue(self):
        pass





class Client:

    url_headers = {
            "Accept":"application/json",
            "Content-Type":"application/json"
        }

    def __init__(self,api_token : str,domain : str):
        self.api_token = api_token
        self.domain = domain

    def addCustomer(self,
                    name : str,
                    tax_no: str,
                    post_code : str,
                    city : str,
                    street : str,
                    first_name : str,
                    last_name : str,
                    kind : str,
                    bank : str,
                    bank_account : str,
                    external_id : str,
                    default_payment_type: PaymentType,
                    person: Optional[str] = "",
                    discount: Optional[str] = "",
                    www: Optional[str] = "",
                    register_number : Optional[str] = "",
                    note : Optional[str] = "",
                    email: Optional[str] = "",
                    phone: Optional[str] = "",
                    mobile_phone: Optional[str] = "",
                    use_delivery_address: Optional[str] = "1",
                    delivery_address : Optional[str] = "",
                    payment_to_kind: str = "30",
                    default_tax: Optional[str] = "23",
                    company: Optional[str] = "1",
                    country: str = "PL",

                    tax_no_kind: str = "NIP",
                    accounting_id : Optional[str] = "",
                    shortcut : Optional[str] = "",

                    ):

        url_data = {"api_token":self.api_token,"client":{
            "name":name,
            "shortcut":shortcut,
            "tax_no_kind":tax_no_kind,
            "tax_no":tax_no,
            "register_number":register_number,
            "accounting_id":accounting_id,
            "post_code":post_code,
            "city":city,
            "street":street,
            "country":country,
            "use_delivery_address":use_delivery_address,
            "delivery_address":delivery_address,
            "first_name":first_name,
            "last_name":last_name,
            "email":email,
            "phone":phone,
            "mobile_phone":mobile_phone,
            "www":www,
            "note":note,
            "company":company,
            "kind":kind,
            "bank":bank,
            "bank_account":bank_account,
            "discount":discount,
            "default_tax":default_tax,
            "payment_to_kind":payment_to_kind,
            "default_payment_type":default_payment_type,
            "person":person,
            "external_id":external_id

        }}

        url = f"https://{self.domain}.fakturownia.pl/clients.json"

        try:
            p = requests.post(url,headers=self.url_headers,json=url_data)
        except requests.exceptions.ProxyError:
            raise errors.fakturowniaAPIError

        return p


    def addBasicCustomer(self,
                         name : str,
                         tax_no : str,
                         bank : str,
                         bank_account : str,
                         city : str,
                         country : str,
                         email : str,
                         person : str,
                         post_code : str,
                         phone : str,
                         street : str
                         ):

        url_data = {
            "api_token":self.api_token,
            "client":{
                "name":name,
                "tax_no":tax_no,
                "bank":bank,
                "bank_account":bank_account,
                "city":city,
                "country":country,
                "email":email,
                "person":person,
                "post_code":post_code,
                "phone":phone,
                "street":street
            }
        }

        url = f"https://{self.domain}.fakturownia.pl/clients.json"

        p = requests.post(url,headers=self.url_headers,json=url_data)

        return p


    def getAllCustomers(self):
        url = f"https://{self.domain}.fakturownia.pl/clients.json?page=1&per_page=50&api_token={self.api_token}"
        p = requests.get(url,headers=self.url_headers)
        if p.status_code == 200:
            jsoned_text = json.loads(p.text)
        else:
            raise errors.fakturowniaAPIError("Blad podczas")
        return jsoned_text

    def deleteCustomer(self,client_id : int):
        url = f"https://{self.domain}.fakturownia.pl/clients/{client_id}.json?api_token={self.api_token}"

        d = requests.delete(url,headers=self.url_headers)


        return d


    def getCustomer(self,tax_no : Optional[str] = "", id : Optional[int] = '',name : Optional[str] = ""):
        if tax_no != "":
            filter_value = tax_no
            filter_field = "tax_no"
        elif id != "":
            filter_value = id
            filter_field = "id"
        elif name != "":
            filter_value = name
            filter_field = "name"
        else:
            filter_value = None
            filter_field = None
        for client in self.getAllCustomers():
            if client[filter_field] == filter_value:
                return client

        return f"Nie znaleziono klienta o filtrze '{filter_field}:{filter_value}'"

    def setIssuerData(self,
                      seller_name : str,
                      seller_tax_no : str,
                      seller_tax_no_kind : str,
                      seller_bank_account : str,
                      seller_bank : str,
                      seller_post_code : str,
                      seller_city : str,
                      seller_street : str,
                      seller_country : str,
                      invoice_issuer: str,
                      seller_email : Optional[str] = "",
                      seller_www : Optional[str] = "",
                      seller_fax : Optional[str] = "",
                      seller_phone : Optional[str] = "",
                      seller_bd_no : Optional[str] = ""
                      ):

        newCustomer = Issuer(seller_name,seller_tax_no,seller_tax_no_kind,seller_bank_account,seller_bank,seller_post_code,seller_city,seller_street,seller_country,invoice_issuer,
                               seller_email,seller_www,seller_fax,seller_phone,seller_bd_no)


        return newCustomer


    def addProduct(self,
                   name: str,
                   code: str,
                   price_net: str,
                   tax: str,
                   ean_code: Optional[str] = None,
                   description: Optional[str] = None,
                   price_gross: Optional[str] = None,
                   currency: Optional[str] = None,
                   category_id: Optional[str] = None,
                   tag_list: Optional[List[str]] = None,
                   service: Optional[str] = None,
                   electronic_service: Optional[str] = None,
                   gtu_codes: Optional[str] = None,
                   limited: Optional[str] = None,
                   stock_level: Optional[str] = None,
                   purchase_price_net: Optional[str] = None,
                   purchase_tax: Optional[str] = None,
                   purchase_price_gross: Optional[str] = None,
                   package: Optional[str] = None,
                   quantity_unit: Optional[str] = None,
                   quantity: Optional[str] = None,
                   additional_info: Optional[str] = None,
                   supplier_code: Optional[str] = None,
                   accounting_id: Optional[str] = None,
                   disabled: Optional[str] = None,
                   use_moss: Optional[str] = None,
                   use_product_warehouses: Optional[str] = None,
                   size: Optional[str] = None,
                   size_width: Optional[str] = None,
                   size_height: Optional[str] = None,
                   size_unit: Optional[str] = None,
                   weight: Optional[str] = None,
                   weight_unit: Optional[str] = None
                   ):
        url = f"https://{self.domain}.fakturownia.pl/products.json"

        url_json = {
            "api_token":self.api_token,
            "product":{
                "name": name,
            "code": code,
            "price_net": price_net,
            "tax": tax,
            "ean_code": ean_code,
            "description": description,
            "price_gross": price_gross,
            "currency": currency,
            "category_id": category_id,
            "tag_list": tag_list,
            "service": service,
            "electronic_service": electronic_service,
            "gtu_codes": gtu_codes,
            "limited": limited,
            "stock_level": stock_level,
            "purchase_price_net": purchase_price_net,
            "purchase_tax": purchase_tax,
            "purchase_price_gross": purchase_price_gross,
            "package": package,
            "quantity_unit": quantity_unit,
            "quantity": quantity,
            "additional_info": additional_info,
            "supplier_code": supplier_code,
            "accounting_id": accounting_id,
            "disabled": disabled,
            "use_moss": use_moss,
            "use_product_warehouses": use_product_warehouses,
            "size": size,
            "size_width": size_width,
            "size_height": size_height,
            "size_unit": size_unit,
            "weight": weight,
            "weight_unit": weight_unit
            }
        }

        p = requests.post(url,headers=self.url_headers,json=url_json)

        return p


