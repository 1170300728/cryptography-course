# -*- coding: utf-8 -*-

from django.shortcuts import render,  render_to_response, RequestContext  
from Eshop.models import Account, Sale
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail, EmailMultiAlternatives
from Eshop.models import *
import uuid
import time
import random
import Eshop.des_1 as des_1
from Eshop.caapi import caapi
import datetime
from cryptography.fernet import Fernet
import pickle
import json
import requests
import base64


# Create your views here.
def mainpage(request, listtype):
    username = request.user
    logged = False
    if username.is_authenticated():
        logged = True

    sale = Sale.objects.all()

    return render(request, 'list.html',
                  {'Username': username, 'Logged': logged, 'Sale': sale},
                  context_instance=RequestContext(request))


def logout(request):
    auth.logout(request)
    return render(request, 'logout.html', {}, context_instance=RequestContext(request))


def login(request, salenum):
    error = []
    if request.method == 'POST':
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

            username = request.POST['Username']
            password = request.POST['Password']
            pwd = str(hash(password))
            user = auth.authenticate(username=username, password=pwd)
            if user is not None and user.is_active:
                auth.login(request, user)
                if salenum != -1:
                    return HttpResponseRedirect('/salesinfo/' + str(salenum))
                else:
                    return HttpResponseRedirect('/logged')
            else:
                if username == '' or password == '':
                    error.append('有未填写字段！')
                elif not User.objects.filter(username=username):
                    error.append('不存在该用户名！')
                elif not user:
                    error.append('用户名和密码不匹配！')
                request.session.set_test_cookie()
                return render(request, 'login.html', {'Error': error}, context_instance=RequestContext(request))
        else:
            return HttpResponse("Please enable cookies and try again.")
    request.session.set_test_cookie()
    return render(request, 'login.html', {'Error': error}, context_instance=RequestContext(request))


keyb = ['']


def add(request, sa, g, p):
    if request.is_ajax():
        ajax_string = 'ajax request: '
    else:
        ajax_string = 'not ajax request: '
    y = random.randint(1, 10000000)
    localsa = []
    localg = []
    localp = []
    for i in range(50):
        localsa.append(int(sa[i]))
        localg.append(int(g[i]))
        localp.append(int(p[i]))
    sb = recon(y, localg, localp)
    localsb = ''
    for i in sb:
        localsb += str(i)
    key = getkey(y, localsa, localp, localg)
    for i in range(8):
        keyb[0] += str(key[i])

    # print keyb
    r = HttpResponse(localsb)
    return r


def getkey(b, rec, p, g):
    t = []
    ans = []
    for i in range(50):
        t.append(rec[i])
        ans.append(0)

    ans[0] = 1
    for i in range(32):
        if (b & (1 << i)) != 0:
            ans = mul(ans, t)
            ans = mod(ans, p)
        t = mul(t, t)
        t = mod(t, p)
    return ans


def recon(b, g, p):
    t = []
    ans = []
    for i in range(50):
        t.append(g[i])
        ans.append(0)
    ans[0] = 1
    for i in range(32):
        if (b & (1 << i)) != 0:
            ans = mul(ans, t)
            ans = mod(ans, p)
        t = mul(t, t)
        t = mod(t, p)
    return ans


def mul(a, b):
    c = []
    d = []
    for i in range(50):
        c.append(a[i])
        d.append(b[i])
        a[i] = 0
    na = getn(c)
    nb = getn(d)
    for i in range(nb):
        for j in range(na):
            a[i + j] += d[i] * c[j]
            if a[i + j] > 9:
                a[i + 1 + j] += int(a[i + j] / 10)
                a[i + j] %= 10
    i = 0
    while i < 50 and i < (na + nb):
        if a[i] > 9:
            a[i + 1] += int(a[i] / 10)
            a[i] %= 10
        i += 1
    return a


def mod(a, b):
    f = 0
    na = getn(a)
    nb = getn(b)
    u = na - nb
    if u < 0:
        return a
    while u + 1 != 0:
        i = na - 1
        while i >= u:
            f = 0
            if a[i] > b[i - u]:
                f = 1
                break
            if a[i] < b[i - u]:
                f = -1
                break
            i -= 1
        if f == 0:
            i = na - 1
            while i >= u:
                a[i] = 0
                i -= 1
            u -= nb
            if u < 0:
                break
            continue
        if f == -1:
            u -= 1
        if f == 1:
            for i in range(u, na):
                a[i] -= b[i - u]
                if a[i] < 0:
                    a[i + 1] -= 1
                    a[i] += 10

    return a


def getn(a):
    i = 49
    while (i >= 0 and a[i] == 0):
        i -= 1
    return i + 1


def newaccount(request):
    error = []
    if request.method == 'POST':
        username = request.POST['Username']
        raw_password = request.POST['Password'].encode('utf-8')
        passwordaff = request.POST['PasswordAffirm']
        raw_password = des_1.desdecode(raw_password, keyb[0])
        keyb[0] = ''  # clear the key used in last time
        passwordaff = passwordaff.encode("utf-8")
        password = ''
        for i in raw_password:
            if ord(i) != 0:
                password += i
            else:
                break

        if username == '' or raw_password == '':
            error.append('有未填写字段！')
            return render(request, 'newaccount.html', {'Error': error}, context_instance=RequestContext(request))
        elif User.objects.filter(username=username):
            error.append('该用户名已被使用！')
            return render(request, 'newaccount.html', {'Error': error}, context_instance=RequestContext(request))
        elif len(raw_password) > 30 or len(username) > 30:
            error.append('用户名或密码设置过长！请输入小于30个字符')
            return render(request, 'newaccount.html', {'Error': error}, context_instance=RequestContext(request))
        elif password != passwordaff:
            error.append('两次输入的密码不匹配！')
            return render(request, 'newaccount.html', {'Error': error}, context_instance=RequestContext(request))
        pwd = hash(password)
        user = User.objects.create_user(username=username, password=str(pwd))
        user.save()
        testaccount = Account.objects.all()
        j = 0
        while (True):
            flag = False
            sqe = len(User.objects.all()) + j
            j += 1
            for i in testaccount:
                if sqe == int(i.Sqe):
                    flag = True
                    break
            if flag == False:
                break
        newaccount = Account(Account=username, Sqe=sqe)
        newaccount.save()
        return HttpResponseRedirect('/login')
    return render(request, 'newaccount.html', {'Error': error}, context_instance=RequestContext(request))


# calculate active code
def active_code(email):
    return uuid.uuid5(uuid.NAMESPACE_DNS, email + str(time.time())).hex


def send_active_email(username, email):
    if isinstance(email, unicode):
        email = email.encode('utf-8')
    ActiveCode = active_code(email)
    """html_content = u'<p>感谢您注册零食小站，请点击下面的链接重置密码：</p><b>链接：\
        </b><a href="http://127.0.0.1:8000/">http://newpassword/%s/%s</a>'\
        % (username, ActiveCode)
    subject, form_email, to = u'重置密码邮件', 'hitshoeshop@sina.com', email
    text_content = u'感谢您注册鞋吧，请点击下面的'
    msg = EmailMultiAlternatives(subject, text_content, form_email, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()"""
    import temprequests
    usersqe = Account.objects.filter(Account=username)[0].Sqe
    url = "http://sendcloud.sohu.com/webapi/mail.send_template.json"
    linker = "http://192.168.43.114:8000/newpassword/" + usersqe + '/' + str(ActiveCode) + '/'
    myvalues = '{"to": ["%s"], "sub": {"%%name%%": ["%s"], "%%url%%": ["%s"]}}' % (email, username, linker)
    params = {"api_user": "paulHIT_test_3HCtWF", \
              "api_key": "sC0NUdK37rVFy0RR", \
              "from": "service@sendcloud.im", \
              "fromname": "SnackShop团队", \
              "template_invoke_name": "test_template_active", \
              "substitution_vars": myvalues, \
              "subject": "密码重置邮件", \
              "resp_email_id": "true"
              }
    temprequests.requests.post(url, files={}, data=params)
    return ActiveCode


def reset(request):
    error = []
    if request.method == 'POST':
        username = request.POST['Username']
        email = request.POST['Email']
        if not User.objects.filter(username=username, email=email):
            error.append('用户名和邮箱不匹配 ！')
            return render(request, 'reset.html', {'Error': error}, context_instance=RequestContext(request))
        #activecode = send_active_email(username, email)
        Account.objects.filter(Account=username).update(Activecode=activecode)
        return render(request, "jump.html")
    return render(request, 'reset.html', {'Error': error}, context_instance=RequestContext(request))


def newpassword(request, sqe, activecode):
    account = Account.objects.filter(Sqe=sqe)[0]
    code_raw = account.Activecode
    submit = []
    if request.method == 'POST':
        if activecode != code_raw:
            submit.append('修改失败，激活码已过期！')
        else:
            newpassword = request.POST['Password']
            passwordaff = request.POST['PasswordAffirm']
            if newpassword == '':
                submit.append('密码未填写！')
                return render(request, 'newpassword.html', {'Submit': submit}, context_instance=RequestContext(request))
            elif newpassword != passwordaff:
                submit.append('两次密码输入不一致！')
                return render(request, 'newpassword.html', {'Submit': submit}, context_instance=RequestContext(request))
            elif len(newpassword) > 30:
                submit.append('新密码设置过长！请输入小于30个字符')
                return render(request, 'newpassword.html', {'Submit': submit}, context_instance=RequestContext(request))
            username = User.objects.get(username=account.Account)
            username.set_password(newpassword)
            username.save()
            submit.append('密码修改成功！')
    return render(request, 'newpassword.html', {'Submit': submit}, context_instance=RequestContext(request))


def user_logged_test(user):
    return user.is_authenticated()


def toshoppingcar(request, salenum):
    logged = False
    username = request.user
    if not username.is_authenticated():
        return HttpResponseRedirect('/login/saleinfo/' + salenum)
    else:
        logged = True
        if request.method == 'POST':
            buynum = int(request.POST['qty'])
            testbuynum = buynum
            if buynum > 0:
                account = Account.objects.filter(Account=str(username))[0]
                sale = Sale.objects.filter(Salenum=salenum)[0]
                addshoppingcar = Shoppingcar.objects.filter(Account=account, Sale=sale)

                if testbuynum > sale.Numofstore:
                    carred = "buytoomany"
                    return render(request, 'salesinfo.html',
                                  {'Username': username, 'Logged': logged, 'Sale': sale, 'Carred': carred},
                                  context_instance=RequestContext(request))

                numofstore = sale.Numofstore
                Sale.objects.filter(Salenum=salenum).update(Numofstore=numofstore - int(buynum))
                if not addshoppingcar:
                    add = Shoppingcar(Account=account, Sale=sale, Num=int(buynum))
                    add.save()
                else:
                    num = addshoppingcar[0].Num
                    addshoppingcar.update(Num=num + int(buynum))
        return HttpResponseRedirect('/shoppingcar')


@user_passes_test(user_logged_test, login_url='/login')
def shoppingcar(request):
    username = request.user
    shoppingcar = Shoppingcar.objects.filter(Account=str(username))
    sum = 0
    for i in shoppingcar:
        sum += i.Sale.Price * i.Num
    return render(request, 'shoppingcar.html', {'Shoppingcar': shoppingcar, 'Username': username, 'Sum': sum},
                  context_instance=RequestContext(request))


def order(request, addrarg):
    username = request.user
    account = Account.objects.filter(Account=username)[0]
    shoppingcar = Shoppingcar.objects.filter(Account=str(username))
    address = Address.objects.filter(Account=str(username))
    # checked = addrarg
    sum = 0
    error = False
    error1 = False
    for i in shoppingcar:
        sum += i.Sale.Price * i.Num
    if request.method == "POST":
        if sum == 0 or addrarg == '0':
            if sum == 0:
                error1 = True
            if addrarg == '0':
                error = True
        else:
            useaddr = Address.objects.filter(Account=str(username), Order=addrarg)[0]
            sn = len(Order.objects.all()) + 1
            ISOTIMEFORMAT = '%Y-%m-%d %X'
            timer = time.strftime(ISOTIMEFORMAT, time.localtime())
            order = Order(Account=account, SN=sn, Date=timer, Status='待支付', Address=useaddr)
            order.save()
            shoppingcar = Shoppingcar.objects.filter(Account=account)
            howmuch = 0
            for i in shoppingcar:
                orderitem = OrderItem(Sale=i.Sale, Fororder=order, Priceofone=i.Sale.Price, Num=i.Num)
                howmuch += i.Sale.Price * i.Num
                orderitem.save()
            Shoppingcar.objects.filter(Account=account).delete()

            # 离开本服务器，请求网银服务器
            rcv_account = shoppingcar[0].Sale.Acountformoney

            # import rsa
            privkey_pem = caapi.read_file("d8245f3866d6e2aec59e6d859d95ade1.priv")
            privkey = caapi.load_privkey(privkey_pem)
            # with open("private0.pem") as privatefile:
            # 	p = privatefile.read()
            # 	privkey = rsa.PrivateKey.load_pkcs1(p)

            # signature = rsa.sign(str(sn) + rcv_account + str(howmuch), privkey, 'SHA-1')
            message=str(sn) +"_"+ str(rcv_account) +"_"+ str(howmuch)
            print message
            ca_cert = caapi.query_ca_cert()
            caapi.write_file("./ca_cert", ca_cert)
            name = {
                'C': "CN",
                'ST': "SC",
                'L': "CD",
                'O': "BOZ",
                'OU': "BOZ",
                'CN': "BOZ",
                'emailAddress': '641723795@qq.com'
            }
            cert = caapi.query_one_cert(**name)
            if cert:
                caapi.write_file("./cert", cert)
            else:
                print "No such subject" # error handling
                pass
            if caapi.verify_certificate_chain(cert, [ca_cert]):
                # pass
            #else:
                pubkey = caapi.load_pubkey_from_cert(cert)
                ct = caapi.encrypt(pubkey, str(message))
                myhash=hash(ct)
                signature = caapi.sign(privkey, str(myhash))
                # myhash = signature.encode("base64")
                # myhash = base64.urlsafe_b64encode(signature)
                # print pub
                # temp = ''
                # for i in myhash:
                #   if i != '\n':
                #        temp += i

                # orderinfo = shopapi.OrderInfo(pickle.dumps(order))
                # oimd = shopapi.oimd(pickle.dumps(orderinfo))
                # payinfo = bankapi.PayInfo(amount=howmuch, email_address=username,
                #                           date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                # pimd = shopapi.pimd(pickle.dumps(payinfo))
                # payinfoandorderinfo = shopapi.PayInfoAndOrderInfo(oimd=oimd, pimd=pimd)
                # pomd = shopapi.pomd(payinfoandorderinfo)
                # passtobank = shopapi.PassToBank(pi=payinfo, pomd=pomd, card_num=12345678910,
                #                                 date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                # serial = pickle.dumps(passtobank)
                # priv_key = caapi.load_privkey(caapi.read_file(''))
                # signed = caapi.sign(priv_key, serial)
                # passinstance = Pass(signed)
                # passinstance.save()

                # rcv_account = 12345678910
                shop_name = "CN_JS_NJ_ZM_ZM_ZM_ttn912@126.com"
                
                ct=base64.urlsafe_b64encode(ct)
                signature=base64.urlsafe_b64encode(signature)
                shop_name = base64.urlsafe_b64encode(shop_name)
                response=HttpResponseRedirect('http://192.168.1.62:8000/fastpay/' + str(ct) + '/' + str(signature)+'/'+str(shop_name))
                return response
            else:
                pass
            # 无效处理    
    return render(request, 'order.html',{'Error1': error1, 'Error': error, 'Arg': addrarg, 'Address': address, 'Account': account,'Shoppingcar': shoppingcar, 'Username': username, 'Sum': sum},context_instance=RequestContext(request))


def finishpay(request, ct, signature, info):
    error = []
    # error.append("* 支付成功！*")
    # return render(request, 'finishpay.html', {'Error': error}, context_instance=RequestContext(request))
    # import rsa
    # with open("public1.pem") as publickfile:
    # 	p = publickfile.read()
    # 	pubkey = rsa.PublicKey.load_pkcs1(p)

    ct = ct.encode("utf-8")
    signature = signature.encode("utf-8")
    info = info.encode("utf-8")
    ct = base64.urlsafe_b64decode(ct)
    signature=base64.urlsafe_b64decode(signature)
    info = base64.urlsafe_b64decode(info)
    inform = info.split("_")
    name = {
        'C': inform[0],
        'ST': inform[1],
        'L': inform[2],
        'O': inform[3],
        'OU': inform[4],
        'CN': inform[5],
        'emailAddress': inform[6]
    }
    cert = caapi.query_one_cert(**name)
    if cert:
        caapi.write_file("./cert", cert)
    else:
        print "No such subject" # error handling
        pass
    ca_cert = caapi.query_ca_cert()
    if caapi.verify_certificate_chain(cert, [ca_cert]):
        bank_pubkey = caapi.load_pubkey_from_cert(cert)
        if caapi.verify(bank_pubkey,str(hash(ct)),signature):
            privkey_pem = caapi.read_file("d8245f3866d6e2aec59e6d859d95ade1.priv")
            privkey = caapi.load_privkey(privkey_pem)
            pt = caapi.decrypt(privkey , ct)
            pts = pt.split("_")
            error.append("* 支付成功！*")
            Order.objects.filter(SN=pts[0]).update(Status='已支付')

    # pubkey_pem = caapi.read_file("public1.pem")
    # pubkey = caapi.load_pubkey(pubkey_pem)
    #sn = sn.encode("utf-8")
    #timestamp = timestamp.encode("utf-8")
    # signature = signature.encode("utf-8")
    # message = str(sn) + str(timestamp)
    # localsignature = signature.decode("base64")
    # error = []
    # error.append("* 支付成功！*")
    # return render(request, 'finishpay.html', {'Error': error}, context_instance=RequestContext(request))
    #  try:
        # caapi.verify(pubkey, message, localsignature)
        # re = rsa.verify(message, localsignature, pubkey)
        # if re == True:
            # error.append("* 支付成功！*")
            # Order.objects.filter(SN=sn).update(Status='已支付')
        else:
            error.append("*支付信息遭到篡改，请迅速与平台联系！*")
    else:
        error.append("*支付信息遭到篡改，请迅速与平台联系！*")
    return render(request, 'finishpay.html', {'Error': error}, context_instance=RequestContext(request))


def continuefunction(request, addrarg, para):
    para = para.encode("utf-8")
    raw_para = para
    print (para)
    temp1 = ''
    for i in para:
        if i != ',' and i != '[' and i != 'u':
            temp1 += i
        if i == ',':
            break
    para = ''
    for i in temp1:
        if i != '\'':
            para += i
    # 至此，订单号赋值到变量para中,type(para)=string
    order = Order.objects.filter(SN=para)[0]
    account = Account.objects.filter(Account=order.Account)[0]
    orderitem = OrderItem.objects.filter(Fororder=para)
    address = Address.objects.filter(Account=str(account))
    sum = 0
    error = False
    for i in orderitem:
        sum += i.Sale.Price * i.Num
    if request.method == "POST":
        if addrarg == '0':
            error = True
        else:
            sn = str(para)
            useaddr = Address.objects.filter(Account=str(account), Order=addrarg)[0]
            order = Order.objects.filter(Account=account, SN=sn).update(Address=useaddr)
            howmuch = sum

            # 离开本服务器，请求网银服务器
            rcv_account = orderitem[0].Sale.Acountformoney

            # import rsa
            privkey_pem = caapi.read_file("d8245f3866d6e2aec59e6d859d95ade1.priv")
            privkey = caapi.load_privkey(privkey_pem)
            # with open("private0.pem") as privatefile:
            # 	p = privatefile.read()
            # 	privkey = rsa.PrivateKey.load_pkcs1(p)

            # signature = rsa.sign(str(sn) + rcv_account + str(howmuch), privkey, 'SHA-1')
            message=str(sn) +"_"+ str(rcv_account) +"_"+ str(howmuch)
            print message
            ca_cert = caapi.query_ca_cert()
            caapi.write_file("./ca_cert", ca_cert)
            name = {
                'C': "CN",
                'ST': "SC",
                'L': "CD",
                'O': "BOZ",
                'OU': "BOZ",
                'CN': "BOZ",
                'emailAddress': '641723795@qq.com'
            }
            cert = caapi.query_one_cert(**name)
            if cert:
                caapi.write_file("./cert", cert)
            else:
                print "No such subject" # error handling
                pass
            if caapi.verify_certificate_chain(cert, [ca_cert]):
                # pass
            #else:
                pubkey = caapi.load_pubkey_from_cert(cert)
                ct = caapi.encrypt(pubkey, str(message))
                myhash=hash(ct)
                signature = caapi.sign(privkey, str(myhash))
                # myhash = signature.encode("base64")
                # myhash = base64.urlsafe_b64encode(signature)
                # print pub
                # temp = ''
                # for i in myhash:
                #   if i != '\n':
                #        temp += i

                # orderinfo = shopapi.OrderInfo(pickle.dumps(order))
                # oimd = shopapi.oimd(pickle.dumps(orderinfo))
                # payinfo = bankapi.PayInfo(amount=howmuch, email_address=username,
                #                           date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                # pimd = shopapi.pimd(pickle.dumps(payinfo))
                # payinfoandorderinfo = shopapi.PayInfoAndOrderInfo(oimd=oimd, pimd=pimd)
                # pomd = shopapi.pomd(payinfoandorderinfo)
                # passtobank = shopapi.PassToBank(pi=payinfo, pomd=pomd, card_num=12345678910,
                #                                 date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                # serial = pickle.dumps(passtobank)
                # priv_key = caapi.load_privkey(caapi.read_file(''))
                # signed = caapi.sign(priv_key, serial)
                # passinstance = Pass(signed)
                # passinstance.save()

                # rcv_account = 12345678910
                shop_name = "CN_JS_NJ_ZM_ZM_ZM_ttn912@126.com"
                
                ct=base64.urlsafe_b64encode(ct)
                signature=base64.urlsafe_b64encode(signature)
                shop_name = base64.urlsafe_b64encode(shop_name)
                response=HttpResponseRedirect('http://192.168.1.62:8000/fastpay/' + str(ct) + '/' + str(signature)+'/'+str(shop_name))
                return response
            else:
                pass
            # 无效处理    
            # import rsa
            # with open("private0.pem") as privatefile:
            # 	p = privatefile.read()
            # 	privkey = rsa.PrivateKey.load_pkcs1(p)
            # privkey_pem = caapi.read_file("private0.pem")
            # privkey = caapi.load_privkey(privkey_pem)
            # signature = caapi.sign(privkey, str(sn) + rcv_account + str(howmuch))

            # signature = rsa.sign(str(sn) + rcv_account + str(howmuch), privkey, 'SHA-1')
            # myhash = base64.b64encode(signature)
            # print pub
            # temp = ''
            # for i in myhash:
            #    if i != '\n':
            #        temp += i
            #rcv_account = 12345678910
            #return HttpResponseRedirect(
            #    'http://127.0.0.2:8000/fastpay/' + str(sn) + '/' + str(rcv_account) + '/' + str(howmuch) + '/' + temp + '/')

    return render(request, 'continueorder.html',
                  {'Continue': raw_para, 'Account': account, 'Sum': sum, 'Arg': addrarg, 'Para': raw_para,
                   'Username': account, 'Address': address, 'Error': error, 'OrderItem': orderitem},
                  context_instance=RequestContext(request))


@user_passes_test(user_logged_test, login_url='/login')
def userinfo(request):
    tempaccount = str(request.user)
    user = User.objects.filter(username=tempaccount)[0]
    account = Account.objects.filter(Account=tempaccount)[0]
    address = Address.objects.filter(Account=tempaccount, Status='on')
    order = Order.objects.filter(Account=tempaccount)
    orderlist = []
    count = 0
    for i in order:
        orderlist.append([])
        orderlist[count].append(i.SN)
        ISOTIMEFORMAT = '%Y-%m-%d %X'
        orderlist[count].append(i.Date.strftime(ISOTIMEFORMAT))
        temp = ''
        for j in OrderItem.objects.filter(Fororder=i):
            temp += j.Sale.Salename + '(Num:' + str(j.Num) + '); '
        orderlist[count].append(temp)
        orderlist[count].append(i.Address.Province + i.Address.City + i.Address.Address)
        orderlist[count].append(i.Address.Name)
        orderlist[count].append(i.Address.Phone)
        orderlist[count].append(i.Status)
        count += 1
    error = []
    if request.method == 'POST':
        gender = request.POST['Gender']
        nickname = request.POST['Nickname']
        email = request.POST['Email']
        age = request.POST['Age']
        if nickname == '' or email == '' or age == '':
            error.append('有未填写字段！')
            return render(request, 'userinfo.html',
                          {'Error': error, 'OrderItem': orderlist, 'User': user, 'Account': account,
                           'Address': address}, context_instance=RequestContext(request))

        if len(nickname) > 30:
            error.append('请输入长度不大于30个字符的昵称！')
            return render(request, 'userinfo.html',
                          {'Error': error, 'OrderItem': orderlist, 'User': user, 'Account': account,
                           'Address': address}, context_instance=RequestContext(request))

        if ('.' not in email) or ('@' not in email) or len(email) > 50:
            error.append('错误的Email格式！')
            return render(request, 'userinfo.html',
                          {'Error': error, 'OrderItem': orderlist, 'User': user, 'Account': account,
                           'Address': address}, context_instance=RequestContext(request))

        for i in age:
            if i < '0' or i > '9':
                error.append('年龄格式不正确！禁止输入除数字以外的其它内容！')
                return render(request, 'userinfo.html',
                              {'Error': error, 'OrderItem': orderlist, 'User': user, 'Account': account,
                               'Address': address}, context_instance=RequestContext(request))

        if int(age) < 0 or int(age) > 150:
            error.append('年龄设置不在合法范围内！')
            return render(request, 'userinfo.html',
                          {'Error': error, 'OrderItem': orderlist, 'User': user, 'Account': account,
                           'Address': address}, context_instance=RequestContext(request))

        Account.objects.filter(Account=tempaccount).update(Gender=gender, Nickname=nickname, Age=age)
        User.objects.filter(username=tempaccount).update(email=email)
        user = User.objects.filter(username=tempaccount)[0]
        account = Account.objects.filter(Account=tempaccount)[0]
        error.append('修改成功！')
    return render(request, 'userinfo.html',
                  {'Error': error, 'OrderItem': orderlist, 'User': user, 'Account': account, 'Address': address},
                  context_instance=RequestContext(request))


def salesinfo(request, salenum):
    username = request.user
    logged = False
    if username.is_authenticated():
        logged = True
    sale = Sale.objects.filter(Salenum=salenum)[0]
    return render(request, 'salesinfo.html', {'Username': username, 'Logged': logged, 'Sale': sale},
                  context_instance=RequestContext(request))


def addtocar(request, salenum):
    logged = False
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/saleinfo/' + salenum)
    else:
        logged = True
    username = request.user
    sale = Sale.objects.filter(Salenum=salenum)[0]
    carred = "ok"
    if request.method == "POST":
        buynum = int(request.POST['qty'])
        testbuynum = buynum
        account = Account.objects.filter(Account=str(username))[0]
        addshoppingcar = Shoppingcar.objects.filter(Account=account, Sale=sale)

        if testbuynum > sale.Numofstore:
            carred = "buytoomany"
            return render(request, 'salesinfo.html',
                          {'Username': username, 'Logged': logged, 'Sale': sale, 'Carred': carred},
                          context_instance=RequestContext(request))

        numofstore = sale.Numofstore
        Sale.objects.filter(Salenum=salenum).update(Numofstore=numofstore - int(buynum))
        sale = Sale.objects.filter(Salenum=salenum)[0]
        if not addshoppingcar:
            add = Shoppingcar(Account=account, Sale=sale, Num=int(buynum))
            add.save()
        else:
            num = addshoppingcar[0].Num
            # Shoppingcar.objects.all().delete()
            addshoppingcar.update(Num=num + int(buynum))
        return render(request, 'salesinfo.html',
                      {'Username': username, 'Logged': logged, 'Sale': sale, 'Carred': carred, 'Buynum': buynum},
                      context_instance=RequestContext(request))
    return render(request, 'salesinfo.html', {'Username': username, 'Logged': logged, 'Sale': sale, 'Carred': carred},
                  context_instance=RequestContext(request))


def loginforcar(request, salenum):
    if request.method == 'POST':
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

            username = request.POST['Username']
            password = request.POST['Password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/salesinfo/' + salenum)
            else:
                return HttpResponseRedirect('/login')
        else:
            return HttpResponse("Please enable cookies and try again.")
    request.session.set_test_cookie()
    return render(request, 'login.html', {}, context_instance=RequestContext(request))


@user_passes_test(user_logged_test, login_url='/login')
def newaddress(request, sqe, flag, fromuserinfo):
    account = Account.objects.filter(Sqe=sqe)[0]
    error = []
    if request.method == 'POST':
        order = len(Address.objects.filter(Account=account)) + 1
        province = request.POST['Province']
        city = request.POST['City']
        address = request.POST['Address']
        name = request.POST['Name']
        phone = request.POST['Phone']
        postcode = request.POST['Postcode']
        if province == '-1':
            error.append('未选择省份！')
            return render(request, 'newaddress.html', {'Error': error, 'Account': account},
                          context_instance=RequestContext(request))

        elif city == '-1':
            error.append('未选择城市！')
            return render(request, 'newaddress.html', {'Error': error, 'Account': account},
                          context_instance=RequestContext(request))

        if address == '' or name == '' or phone == '' or postcode == '':
            error.append('有未填写字段！')
            return render(request, 'newaddress.html', {'Error': error, 'Account': account},
                          context_instance=RequestContext(request))

        elif len(address) > 50:
            error.append('地址字段输入过长，请精简输入！')
            return render(request, 'newaddress.html', {'Error': error, 'Account': account},
                          context_instance=RequestContext(request))

        elif len(name) > 30:
            error.append('收货人字段输入过长，请精简输入！')
            return render(request, 'newaddress.html', {'Error': error, 'Account': account},
                          context_instance=RequestContext(request))

        elif len(phone) > 15:
            error.append('电话字段输入过长，请精简输入！')
            return render(request, 'newaddress.html', {'Error': error, 'Account': account},
                          context_instance=RequestContext(request))

        elif len(postcode) > 6:
            error.append('邮编字段输入过长，请精简输入！')
            return render(request, 'newaddress.html', {'Error': error, 'Account': account},
                          context_instance=RequestContext(request))

        for i in phone:
            if i < '0' or i > '9':
                error.append('电话输入有非法字符!')
                return render(request, 'newaddress.html', {'Error': error, 'Account': account},
                              context_instance=RequestContext(request))

        for i in postcode:
            if i < '0' or i > '9':
                error.append('邮编输入有非法字符!')
                return render(request, 'newaddress.html', {'Error': error, 'Account': account},
                              context_instance=RequestContext(request))

        newaddress = Address(Account=account, Order=str(order), Province=province, City=city, Address=address,
                             Name=name, Phone=phone, Postcode=postcode, Status='on')
        newaddress.save()
        if int(flag) == 1:
            if fromuserinfo != '0':
                return HttpResponseRedirect('/continue/' + fromuserinfo)
            return HttpResponseRedirect('/order')
        return HttpResponseRedirect('/userinfo')
    return render(request, 'newaddress.html', {'Error': error, 'Account': account},
                  context_instance=RequestContext(request))


def editaddress(request, usernum, addrnum):
    account = Account.objects.filter(Sqe=usernum)[0]
    address = Address.objects.filter(Account=account, Order=addrnum)[0]
    error = []
    if request.method == 'POST':
        province = request.POST['Province']
        city = request.POST['City']
        detail = request.POST['Address']
        name = request.POST['Name']
        phone = request.POST['Phone']
        postcode = request.POST['Postcode']

        if detail == '' or name == '' or phone == '' or postcode == '':
            error.append('有未填写字段！')
            return render(request, 'editaddress.html', {'Account': account, 'Error': error, 'Address': address},
                          context_instance=RequestContext(request))

        elif len(detail) > 50:
            error.append('地址字段输入过长，请精简输入！')
            return render(request, 'editaddress.html', {'Account': account, 'Error': error, 'Address': address},
                          context_instance=RequestContext(request))

        elif len(name) > 30:
            error.append('收货人字段输入过长，请精简输入！')
            return render(request, 'editaddress.html', {'Account': account, 'Error': error, 'Address': address},
                          context_instance=RequestContext(request))

        elif len(phone) > 15:
            error.append('电话字段输入过长，请精简输入！')
            return render(request, 'editaddress.html', {'Account': account, 'Error': error, 'Address': address},
                          context_instance=RequestContext(request))

        elif len(postcode) > 6:
            error.append('邮编字段输入过长，请精简输入！')
            return render(request, 'editaddress.html', {'Account': account, 'Error': error, 'Address': address},
                          context_instance=RequestContext(request))

        for i in phone:
            if i < '0' or i > '9':
                error.append('电话输入有非法字符!')
                return render(request, 'editaddress.html', {'Account': account, 'Error': error, 'Address': address},
                              context_instance=RequestContext(request))

        for i in postcode:
            if i < '0' or i > '9':
                error.append('邮编输入有非法字符!')
                return render(request, 'editaddress.html', {'Account': account, 'Error': error, 'Address': address},
                              context_instance=RequestContext(request))
        Address.objects.filter(Account=account, Order=addrnum).update(Province=province, City=city, Address=detail,
                                                                      Name=name, Phone=phone, Postcode=postcode)
        return HttpResponseRedirect('/userinfo')
    return render(request, 'editaddress.html', {'Account': account, 'Error': error, 'Address': address},
                  context_instance=RequestContext(request))


def deladdress(request, usernum, addrnum):
    account = Account.objects.filter(Sqe=usernum)[0]
    Address.objects.filter(Account=account, Order=addrnum).update(Status='off')
    return HttpResponseRedirect('/userinfo')


def delete(request, salenum):
    username = request.user
    addnum = Shoppingcar.objects.filter(Sale=salenum, Account=str(username))[0].Num
    sale = Sale.objects.filter(Salenum=salenum)[0]
    numofstore = sale.Numofstore
    Sale.objects.filter(Salenum=salenum).update(Numofstore=numofstore + int(addnum))

    Shoppingcar.objects.filter(Sale=salenum, Account=str(username)).delete()
    return HttpResponseRedirect('/shoppingcar')


def alter(request, salenum):
    username = request.user
    sale = Sale.objects.filter(Salenum=salenum)[0]
    shoppingcar = Shoppingcar.objects.filter(Sale=salenum, Account=str(username))[0]
    error = []
    if request.method == 'POST':
        num = request.POST['qty']
        numofstore = Sale.objects.filter(Salenum=salenum)[0].Numofstore
        if int(num) > int(numofstore):
            error.append('购买数量太大，库存不够啦！')
            return render(request, 'alter.html',
                          {'Error': error, 'Sale': sale, 'Username': username, 'Shoppingcar': shoppingcar},
                          context_instance=RequestContext(request))

        prenum = Shoppingcar.objects.filter(Sale=salenum, Account=str(username))[0].Num
        Sale.objects.filter(Salenum=salenum).update(Numofstore=numofstore + int(prenum) - int(num))
        Shoppingcar.objects.filter(Sale=salenum, Account=str(username)).update(Num=num)
        return HttpResponseRedirect('/shoppingcar')
    return render(request, 'alter.html',
                  {'Error': error, 'Sale': sale, 'Username': username, 'Shoppingcar': shoppingcar},
                  context_instance=RequestContext(request))


# def pay(request):
#	return render(request, 'pay.html', {}, context_instance = RequestContext(request))

def dualsignature(requests):
    res = Pass.objects.all().first().Dual
    return HttpResponse(json.dumps(res))
