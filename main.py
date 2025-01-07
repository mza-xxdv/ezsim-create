import requests as r, random, re, time as t, os
from fake_useragent import UserAgent as FUA
from faker import Faker
from bs4 import BeautifulSoup

class GeneratorEmail:
    def __init__ (self):
        self.api = r.Session()
        self.ua = FUA().random
    
    def validate(self, domain, user):
        data = f"usr={user}&dmn={domain}"
        headers = {
            "Cookie":f"surl={domain}/{user}",
            "User-Agent":self.ua,
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"
        }
        try:
            return self.api.post("https://generator.email/check_adres_validation3.php", data=data, headers=headers)
        except Exception as e:
            print(e)

    def check_email(self, domain, user):
        headers = {
            "Cookie":f"surl={domain}/{user}",
            "User-Agent":self.ua
        }
        try:
            return self.api.get(f"https://generator.email/{domain}/{user}",timeout=(5), headers=headers)
        except Exception as e:
            print(e)
class utama:
    def __init__(self):
        self.api = r.Session()
        self.ua = FUA().random
    
    def regist(self, fname, lname, email, password, PROXY):
        data = {
            'firstName': fname,
            'lastName': lname,
            'password': password,
            'confirmPassword': password,
            'loginID': email,
            'locale': 'en',
            'versionNumber': '5.0.0'
        }
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': self.ua,
        }
        try:
            return self.api.post('https://www.ezsim.com/api/v2/auth/register/', json=data, headers=headers, proxies={"http": PROXY, "https": PROXY})
        except Exception as e:
            print(e)
    
    def confirm(self, email, otp, PROXY):
        data = {
            'loginID': email,
            'code': otp,
        }
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': self.ua,
        }
        try:
            return self.api.post('https://www.ezsim.com/api/v2/auth/confirm/', json=data, headers=headers, proxies={"http": PROXY, "https": PROXY})
        except Exception as e:
            print(e)
    
    def adduser(self, fname, lname, email, password, PROXY):
        data = {
            'firstName': fname,
            'lastName': lname,
            'loginID': email,
            'locale': 'en',
            'versionNumber': '5.0.0',
            'email': email,
            'password': password,
        }
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': self.ua,
        }
        try:
            return self.api.post('https://www.ezsim.com/api/v2/auth/addUser/', json=data, headers=headers, proxies={"http": PROXY, "https": PROXY})
        except Exception as e:
            print(e)
    
    def login(self, email, password, PROXY):
        data = {
            'loginID': email,
            'password': password,
            'deviceType': 'browser',
            'locale': 'en',
            'versionNumber': '5.0.0',
        }
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': self.ua,
        }
        try:
            return self.api.post('https://www.ezsim.com/api/v2/auth/login/', json=data, headers=headers, proxies={"http": PROXY, "https": PROXY})
        except Exception as e:
            print(e)
            
os.system('cls' if os.name == "nt" else 'clear')
utils = utama()
generatormail = GeneratorEmail()
count = 0
berapakali = 1 #mau berapa akun??
while count < berapakali:
    PROXY = f"http://username:password@host:port/" #change ur proxy dude.
    fname = Faker().first_name().capitalize()
    lname = Faker().last_name().capitalize()
    user = f"{fname}{lname}{random.randint(11, 999)}".lower()
    html_content = r.get("http://generator.email").text
    soup = BeautifulSoup(html_content, "html.parser")
    domain_regex = re.compile(r'^[a-zA-Z0-9-]{1,63}(\.[a-zA-Z0-9-]{1,63})+$')
    domain = random.choice([p.text for p in soup.findAll('p') if domain_regex.match(p.text.strip())])
    email = f"{user}@{domain}"
    password = f"{Faker().word().capitalize()}{Faker().word()}{random.randint(1, 9999)}"
    validate_email = generatormail.validate(domain, user)
    if validate_email.json()['status'] != "good":
        print(f" > Bad Email.")
    else:
        print(f" > {email};{password}")
        register = utils.regist(fname, lname, email, password, PROXY)
        if register.status_code == 200:
            print(f" > Send OTP True")
            t.sleep(2)
            check_email = generatormail.check_email(domain, user).text
            
            def extract_otp(check_email):
                soup = BeautifulSoup(check_email, 'html.parser')
                peler = soup.find('span', style="font-family: bold; font-size: 36px; letter-spacing: 5px")
                if peler:
                    return peler.text.strip()
                else:
                    return None
            
            otp = None
            for attempt in range(10): #retry 10kali
                otp = extract_otp(check_email)
                if otp:
                    print(f" > OTP: {otp}")
                    break
                else:
                    print(" > Waiting for OTP...")
                    t.sleep(1)
            validate_otp = utils.confirm(email, otp, PROXY)
            if validate_otp.status_code == 200:
                print(f" > Validate OTP True")
                add_user = utils.adduser(fname, lname, email, password, PROXY)
                if "id" in add_user.text:
                    user_id = add_user.json()['id']
                    add_user_email = add_user.json()['email']
                    print(f" > {user_id} | {add_user_email}")
                    login = utils.login(email, password, PROXY)
                    if "authToken" in login.text:
                        auth = login.json()['authToken']
                        print(f" > Token: {auth}")
                        with open("akun.txt", "a") as f:
                            f.write(f"{email};{password} || {auth}\n")
                        count += 1
                    else:
                        print(f" ! Error login: {login.text}")
                else:
                    print(f" ! Error add_user: {add_user.text}")
            else:
                print(f" ! Error validate_otp: {validate_otp.status_code}")
        else:
            print(f" ! Error register: {register.status_code}")
