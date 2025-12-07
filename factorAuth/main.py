'''
To implement this we need to use 3 module

time - inbuilt python module for time related operations
pyotp - to generate OTP
QRCode - To generate QRCode

Users also need to Download and install the Google Authenticator app from the Playstore / Appstore onto their phones.
'''
import pyotp
import qrcode

key = pyotp.random_base32()

uri = pyotp.totp.TOTP(key).provisioning_uri(
    name='collegechatbot',
    issuer_name='admin')

print(uri)

# Qr code generation step
qrcode.make(uri).save("qr_auth.png")

"""Verifying stage starts"""
totp = pyotp.TOTP(key)
user_otp = input("\nEnter OTP from Google Authenticator: ")

# verifying the code
if totp.verify(user_otp):
    print(" OTP verified succesfully")
else:
    print(" invalid or expired OTP.")