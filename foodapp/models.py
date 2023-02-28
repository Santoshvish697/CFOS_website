from django.db import models

# Create your models here.

class Food(models.Model):
	FoodId    = models.AutoField(primary_key=True)
	FoodName  = models.CharField(max_length=30)
	FoodCat   = models.CharField(max_length=30)
	FoodPrice = models.FloatField(max_length=15)
	FoodImage = models.ImageField(upload_to='media',default='')
	class Meta:
		db_table = "FP_Food"
		
class Cust(models.Model):
	CustId    = models.AutoField(primary_key=True)
	CustFName  = models.CharField(max_length=30)
	CustLName  = models.CharField(max_length=30)
	CustCont  = models.CharField(max_length=10)
	CustEmail = models.CharField(max_length=50)
	CustPass  = models.CharField(max_length=60)
	Address  = models.CharField(max_length=150,default='')
	class Meta:
		db_table = "FP_Cust"
		
class Admin(models.Model):
	AdminId   = models.CharField(primary_key=True,max_length=20)
	AdminPass = models.CharField(max_length=60)
	class Meta:
		db_table = "FP_Admin"
		
class Cart(models.Model):
	CartId    = models.AutoField(primary_key=True)
	CustEmail = models.CharField(max_length=50)
	FoodId    = models.CharField(max_length=50)
	FoodQuant = models.CharField(max_length=10)
	class Meta:
		db_table = "FP_Cart"
		
class Order(models.Model):
	OrderId   = models.AutoField(primary_key=True)
	CustEmail = models.CharField(max_length=30)
	OrderDate = models.CharField(max_length=40)
	TotalBill = models.FloatField(max_length=50)
	class Meta:
		db_table = "FP_Order"

class transact_money(models.Model):
	transact_ID = models.AutoField(primary_key=True)
	made_by = models.ForeignKey(Cust,related_name='transactions',on_delete=models.CASCADE)
	made_on = models.DateTimeField(auto_now_add=True)
	amount = models.IntegerField()
	orders = models.ForeignKey(Order,related_name="order_id",on_delete=models.CASCADE,default = 0)
	checksum = models.CharField(max_length=100, null=True, blank=True)
	def save(self, *args, **kwargs):
		if self.order_id is None and self.made_on and self.id:
			self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
		return super().save(*args, **kwargs)



class cust_balance(models.Model):
    wallet_ID = models.AutoField(primary_key=True)
    user = models.ForeignKey(Cust,on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    
    
class admin_balance(models.Model):
    wallet_ID = models.AutoField(primary_key=True)
    user = models.ForeignKey(Admin,on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    
    
class Wallet(models.Model):
    user = models.ForeignKey(Cust, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    transactions = models.TextField(default='', blank=True)
    
class admin_wallet(models.Model):
    user = models.ForeignKey(Admin,on_delete = models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)