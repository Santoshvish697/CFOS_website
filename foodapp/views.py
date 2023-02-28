from django.shortcuts import render, redirect
from django.db import connection, transaction
from foodapp.forms import FoodForm, CustForm, AdminForm, CartForm, OrderForm,AddFundsForm,SubtractFundsForm
from foodapp.models import Food, Cust, Admin, Cart, Order,admin_balance,Wallet,admin_wallet,cust_balance
import datetime

cursor = connection.cursor()
pay_total = 0.00
# Create your views here.


def foodapp(request):
    return render(request, 'index.html')


def foodcatalogue(request):
    return render(request, 'foodcatalogue.html')


def addfood(request):
    if request.method == "POST":
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect("/allfood")
            except:
                return render(request, "error.html")
    else:
        form = FoodForm()
    return render(request, 'addfood.html', {'form': form})


def showfood(request):
    foods = Food.objects.all()
    return render(request, 'foodlist.html', {'foodlist': foods})


def deletefood(request, FoodId):
    foods = Food.objects.get(FoodId=FoodId)
    foods.delete()
    return redirect("/allfood")


def getfood(request, FoodId):
    foods = Food.objects.get(FoodId=FoodId)
    return render(request, 'updatefood.html', {'f': foods})


def updatefood(request, FoodId):
    foods = Food.objects.get(FoodId=FoodId)
    form = FoodForm(request.POST, request.FILES, instance=foods)
    if form.is_valid():
        form.save()
        return redirect("/allfood")
    return render(request, 'updatefood.html', {'f': foods})

def addcust(request):
    if request.method == 'POST':
        form = CustForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                username = form.cleaned_data.get('CustEmail')
                cust_instance = cust_balance(user = Cust.objects.get(CustEmail = username),balance = 0)
                cust_instance.save()
            except:
                return render(request,"error.html")
    else:
        form = CustForm()
    return render(request,'addcust.html',{'form':form})
    


def showcust(request):
    custs = Cust.objects.all()
    return render(request, 'custlist.html', {'custlist': custs})


def deletecust(request, CustId):
    custs = Cust.objects.get(CustId=CustId)
    custs.delete()
    return redirect("/allcustomer")


def getcust(request):
    print(request.session['CustId'])
    for c in Cust.objects.raw('Select * from FP_Cust where CustEmail="%s"' % request.session['CustId']):
        custs = c
    return render(request, 'updatecust.html', {'c': custs})


def updatecust(request, CustId):
    custs = Cust.objects.get(CustId=CustId)
    form = CustForm(request.POST, instance=custs)
    if form.is_valid():
        form.save()
        session_keys = list(request.session.keys())
        for key in session_keys:
            del request.session[key]
        return redirect("/login")
    return render(request, 'updatecust.html', {'c': custs})


def login(request):
    return render(request, 'login.html')


def doLogin(request):
    if request.method == "POST":
        uid = request.POST.get('userId', '')
        upass = request.POST.get('userpass', '')
        utype = request.POST.get('type', '')

        if utype == "Admin":
            for a in Admin.objects.raw('Select * from FP_Admin where AdminId="%s" and AdminPass="%s"' % (uid, upass)):
                if a.AdminId == uid:
                    request.session['AdminId'] = uid
                    return render(request, "index.html", {'success': 'Welcome '+a.AdminId})
            else:
                return render(request, "login.html", {'failure': 'Incorrect login details'})

        if utype == "User":
            for a in Cust.objects.raw('Select * from FP_Cust where CustEmail="%s" and CustPass="%s"' % (uid, upass)):
                if a.CustEmail == uid:
                    request.session['CustId'] = uid
                    return render(request, "index.html", {'success': 'Welcome '+a.CustEmail})
            else:
                return render(request, "login.html", {'failure': 'Incorrect login details'})


def doLogout(request):
    key_session = list(request.session.keys())
    for key in key_session:
        del request.session[key]
    return render(request, 'index.html', {'success': 'Logged out successfully'})


def addcart(request, FoodId):
    sql = ' Insert into FP_Cart(CustEmail,FoodId,FoodQuant) values("%s","%d","%d")' % (
        request.session['CustId'], FoodId, 1)
    i = cursor.execute(sql)
    transaction.commit()
    return redirect('/allfood')


def delcart(request, CartId):
    cart = Cart.objects.get(CartId=CartId)
    cart.delete()
    return redirect("/allcart")


def showcart(request):
    cart = Cart.objects.raw(
        'Select CartId,FoodName,FoodPrice,FoodQuant,FoodImage from FP_Food as f inner join FP_Cart as c on f.FoodId=c.FoodId where c.CustEmail="%s"' % request.session['CustId'])
    transaction.commit()
    return render(request, "cartlist.html", {'cartlist': cart})


def updatepasswd(request):
    return render(request, 'updatepasswd.html')


def changepass(request):
    if request.method == "POST":
        aid = request.session['AdminId']
        opss = request.POST.get('OLDPass', '')
        newpss = request.POST.get('NEWPass', '')
        cnewpss = request.POST.get('CONFPass', '')
        for a in Admin.objects.raw('select * from FP_Admin where AdminId="%s" and AdminPass="%s"' % (aid, opss)):
            if a.AdminId == aid:
                sql = 'update FP_Admin set AdminPass="%s" where AdminId="%s"' % (
                    newpss, request.session['AdminId'])
                i = cursor.execute(sql)
                transaction.commit()
                session_keys = list(request.session.keys())
                for key in session_keys:
                    del request.session[key]
                return redirect("/login")
        else:
            return render(request, 'updatepasswd.html', {'failure': 'Invalid attempt.'})


def placeorder(request):
        global pay_total
        if request.method=="POST":
                form = AddFundsForm(request.POST)
                price=request.POST.getlist('FoodPrice','')
                q=request.POST.getlist('FoodQuant','')
                total=0.0
                for i in range(len(price)):
                    total=total+float(price[i])*float(q[i])
                pay_total = total
                today = datetime.datetime.now()
                sql = 'insert into FP_Order(CustEmail,OrderDate,TotalBill) values ("%s","%s","%f")' %(request.session['CustId'],today,total)
                i=cursor.execute(sql)
                transaction.commit()
                sql1= 'select * from FP_Order where CustEmail="%s" and OrderDate="%s"'%(request.session['CustId'],today)
                for o in Order.objects.raw(sql1):
                 if o.CustEmail==request.session['CustId']:
                  od=str(o.OrderId)
                  print("Going to payments")
                  return redirect('subtract_funds')
                for c in Cust.objects.raw('Select * from FP_Cust where CustEmail="%s"'%request.session['CustId']):
                 custs=c
                wallet = Wallet.objects.get(user = custs)
                print(wallet.balance)
                sql = 'delete from FP_Cart where CustEmail="%s"' %(request.session['CustId'])
                i=cursor.execute(sql)
                transaction.commit()
                
                od=Order()
        else:
            form = SubtractFundsForm()
        return redirect('subtract_funds')


def getorder(request):
    orders = Order.objects.all()
    return render(request, 'orderlist.html', {'orderlist': orders})


def updateQNT(request, s):
    print(s)
    ind = s.index('@')
    cartId = int(s[:ind])
    qt = int(s[ind+1:])
    sql = "update FP_Cart set FoodQuant='%d' where CartId='%d'" % (qt, cartId)
    i = cursor.execute(sql)
    transaction.commit()
    
def payment_interface_render(request,params = None):
    if params != None:
     return render(request,"payments.html",params)
    else:
        return render(request,"payments.html")

def initiate_payment(request,params = None):
     if request.method == "POST":
      try:
        username = request.POST.get('userId')
        password = request.POST.get('userpass')
        amount = int(request.POST.get('amount'))
        print(amount)
        sender_user = Cust.objects.get(CustEmail = username)
        rec_user = Admin.objects.get(AdminId = 'cosmix')
        sender = cust_balance.objects.get(user = sender_user)
        if (sender == None):
            cust_balance.objects.create(user= sender_user,balance = 500)
        rec = admin_balance.objects.get(user = rec_user)
        if(rec == None):
            admin_balance.objects.create(user = rec_user,balance = 0)
        if username is None:
            raise ValueError
        for a in Cust.objects.raw('Select * from FP_Cust where CustEmail="%s" and CustPass="%s"'%(username,password)):
            if a.CustEmail==username:
                sender.balance = sender.balance-int(amount)
                rec.balance = rec.balance+int(amount)
                sender.save()
                rec.save() 
        print(sender.balance)
        return render(request,'payments.html',{"balance" :  sender.balance})          
      except Exception as e:
       msg = "Transaction Failure, Please check and try again"
     return payment_interface_render(request,params)

trans_list = []

def add_funds(request):
    if request.method == 'POST':
        for c in Cust.objects.raw('Select * from FP_Cust where CustEmail="%s"'%request.session['CustId']):
         custs=c
        wallet = Wallet.objects.get(user = custs)
        amount = request.POST.get('amount')
        wallet.balance = float(wallet.balance) + float(amount)
        wallet.transactions += f'Added {amount}\n'
        wallet.save()
        return redirect('wallet')
    else:
        form = AddFundsForm()
    return render(request, 'addfunds.html', {'form' : form})

def subtract_funds(request):
    global pay_total
    adm_wallet = None
    if request.method == 'POST':
        form = SubtractFundsForm(initial={'amount': pay_total})
        for c in Cust.objects.raw('Select * from FP_Cust where CustEmail="%s"'%request.session['CustId']):
         custs=c
         wallet = Wallet.objects.get(user = custs)
        for a in Admin.objects.raw('Select * from FP_Admin where AdminId="admin"'):
         admin = a
        adm_wallet = admin_wallet.objects.get(user = admin)
        amount = request.POST.get('amount')
        if wallet.balance >= float(amount):
            #Debit at customer end
            wallet.balance = float(wallet.balance)-float(amount)
            #Credit at admin end
            adm_wallet.balance = float(adm_wallet.balance) + float(amount)
            wallet.transactions += f'Subtracted {amount}\n'
            wallet.save()
            adm_wallet.save()
            return redirect('wallet')
        else:
            return render(request, 'subtractfunds.html', {'error': 'Insufficient funds'})
    else:
        form = SubtractFundsForm(initial={'amount': pay_total})
    return render(request, 'subtractfunds.html',{'form' : form})

def append_lis(list,txt):
    list.append(txt)
    return list

def wallet(request):
     trans_list = []
     for c in Cust.objects.raw('Select * from FP_Cust where CustEmail="%s"'%request.session['CustId']):
         custs=c
     try:
      wallet = Wallet.objects.get(user= custs)
     except:
      Wallet.objects.create(user = custs,balance = 100.0)
      wallet = Wallet.objects.get(user= custs)
    #   print(trans_list)
     trans_list = wallet.transactions.split('\n')
     return render(request,'wallet.html', {'wallet': wallet,'trans':trans_list})
 
def admin_acc(request):
    print(request.session['AdminId'])
    for a in Admin.objects.raw('Select * from FP_Admin where AdminId="%s"'%(request.session['AdminId'])):
        admin = a
    try:
        adm_wallet = admin_wallet.objects.get(user = admin)
    except:
        admin_wallet.objects.create(user = admin,balance = 0.0)
        adm_wallet = admin_wallet.objects.get(user = admin)
    return render(request,'admin_wallet.html',{'adm_wallet' : adm_wallet})
