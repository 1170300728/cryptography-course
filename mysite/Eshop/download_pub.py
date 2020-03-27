from caapi import caapi

name = {
            'C': "CN",
            'ST': "JS",
            'L': "NJ",
            'O': "ZM",
            'OU': "ZM",
            'CN': "ZM",
            'emailAddress': 'ttn912@126.com'
}
cert = caapi.query_one_cert(**name)
if cert:
    caapi.write_file("C:/Users/ttn91/Documents/Tencent Files/2964175191/FileRecv/Shop 22/Shop 2/Shop/mysite/cert", cert)
else:
    print "No such subject" # error handling

pubkey = caapi.load_pubkey_from_cert(caapi.read_file("C:/Users/ttn91/Documents/Tencent Files/2964175191/FileRecv/Shop 22/Shop 2/Shop/mysite/cert"))
print pubkey

pubkey_pem = caapi.dump_pubkey(pubkey)
caapi.write_file("C:/Users/ttn91/Documents/Tencent Files/2964175191/FileRecv/Shop 22/Shop 2/Shop/mysite/pub.pem",pubkey_pem)