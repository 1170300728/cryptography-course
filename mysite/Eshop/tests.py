from caapi import caapi

key=caapi.load_privkey(caapi.read_file("C:/Users/ttn91/Documents/Tencent Files/2964175191/FileRecv/Shop 22/Shop 2/Shop/mysite/d703927c23c90c350f030bc327489d9c.priv"))
privkey_pem = caapi.dump_privkey(key)

caapi.write_file("C:/Users/ttn91/Documents/Tencent Files/2964175191/FileRecv/Shop 22/Shop 2/Shop/mysite/priv.pem",privkey_pem)
