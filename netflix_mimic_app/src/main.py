import requests
import json

key = None
def main():
    global key
    with open("/secret/key.txt") as key_file:
        key = str(key_file.read().strip())
    a = requests.get("http://movies_api:8000/users/10001?does_account_exists=false", headers={"x-access-token": key})
    b = requests.post('http://movies_api:8000/accounts/create_account',headers={"x-access-token": key}, data=json.dumps({
  "user_id": 10001,
  "payment_method": "checking",
  "billing_cycle": "monthly",
  "account_status": "active",
  "device_type": "tv"
}))
    print(a.json())


if __name__ == "__main__":
    main()
