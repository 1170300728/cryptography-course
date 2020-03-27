from caapi import caapi
import base64
a='testcaapiOKornot1234'
print a
ct=hash(a)
privkey_pem = caapi.read_file("C:/Users/ttn91/Documents/Tencent Files/2964175191/FileRecv/Shop 22/Shop 2/Shop/mysite/e8e030701288007563a60c037ae9003b.priv")
privkey = caapi.load_privkey(privkey_pem)
signature = caapi.sign(privkey, str(ct))
#myhash=signature.encode("base64")
sig64 = base64.urlsafe_b64encode(signature)
ct64=base64.urlsafe_b64encode(str(ct))


ct = base64.urlsafe_b64decode(ct64)
signature = base64.urlsafe_b64decode(sig64)
#signature=myhash.decode("base64")
pubkey_cert = caapi.read_file("C:/Users/ttn91/Documents/Tencent Files/2964175191/FileRecv/Shop 22/Shop 2/Shop/mysite/shop_cert")
pubkey = caapi.load_pubkey_from_cert(pubkey_cert)


if caapi.verify(pubkey,ct, signature):
    print "OK"
else:
    print "gg"

a='ttnttnttn'
print hash(a)