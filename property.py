import requests
import json
from bs4 import BeautifulSoup

def get_tax_balance(brt):
    r2 = requests.post("http://www.phila.gov/revenue/realestatetax/default.aspx",
        data='__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwUINTc0MTgxMzAPZBYCZg9kFgICAw9kFgICDQ9kFgYCAQ9kFgICAw9kFgICAQ8QZGQWAGQCBQ8PFgIeBFRleHQFM1NvcnJ5LCB5b3VyIEJSVCBudW1iZXIgd2FzIG5vdCBmb3VuZCBpbiB0aGUgc3lzdGVtLmRkAg0PZBYGAgEPPCsACgEADxYEHgtfIURhdGFCb3VuZGceC18hSXRlbUNvdW50ZmRkAgUPFCsAAmRkZAIHDzwrAA0BAA8WBB8BZx8CZmRkGAIFQWN0bDAwJEJvZHlDb250ZW50UGxhY2VIb2xkZXIkR2V0VGF4SW5mb0NvbnRyb2wkZ3JkUGF5bWVudHNIaXN0b3J5DzwrAAoBCGZkBTJjdGwwMCRCb2R5Q29udGVudFBsYWNlSG9sZGVyJEdldFRheEluZm9Db250cm9sJGZybQ9nZCI5Sh3aCW80yONcvZEQdPSEkRmO&__EVENTVALIDATION=%2FwEWBQKy9o29AQLRzsWTBwLlpIbACAKV6q2KDQKIvdHyCbZeoQ9Uy6RXJ%2BIDRDdBlsWsilrN&ctl00%24BodyContentPlaceHolder%24SearchByAddressControl%24txtLookup=by+Property+Address&ctl00%24BodyContentPlaceHolder%24SearchByBRTControl%24txtTaxInfo=' + brt + 'ctl00%24BodyContentPlaceHolder%24SearchByBRTControl%24btnTaxByBRT=+%3E%3E',
        headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "DNT": "1",
            "Origin": "http://www.phila.gov",
            "Referer": "http://www.phila.gov/revenue/realestatetax/default.aspx",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36",
        },
        cookies={
            "BIGipServerphila.gov_pool": "2199824576.20480.0000",
        },
    )

    rev = BeautifulSoup(r2.text)
    balance = rev.find("table", id="ctl00_BodyContentPlaceHolder_GetTaxInfoControl_grdPaymentsHistory").find_all("tr")[-1].find_all("td")[5].text
    lien = rev.find("span", id="ctl00_BodyContentPlaceHolder_GetTaxInfoControl_frm_lblLienSaleAccount").text
    return balance, lien

in_url = "http://property.phila.gov/#block/700/43rd"
block = "700"
street = "43rd"
url = "http://api.phila.gov/opa/v1.0/block/%s %s/?format=json" % (block, street)
r = requests.get(url).json()

for prop in r['data']['properties']:
    print prop['full_address']
    print prop['characteristics']['description']
    brt = prop['account_number']
    print brt
    print get_tax_balance(brt)

