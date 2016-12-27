from __future__ import unicode_literals

from django.db import models

categorytypes = (('hospital', 'Hospital'),
                ('bloodbank', 'Blood Bank'),
                ('dentalclinic', 'Dental Clinic'),
                ('pathologylab', 'Pathology Lab'),
		('pathologylab2', 'Pathology Lab with Histopathology'),
                ('clinic', 'Clinic'),
                ('dispensary', 'Dispensary'),
                ('vethospital', 'Veterinary Hospital'),
		('vetclinic', 'Veterinary Clinic'),
                ('others', 'Others'))

ownershiptypes = (('government', 'Government'),
                ('semigovernment', 'Semi Government'),
                ('corporatepublic', 'Corporate Public'),
                ('corporateprivate', 'Corporate Private'),
		('partnership', 'Partnership'),
                ('individual', 'Individual Owned'),
		('others', 'Others'))
class CategoryTypes(models.Model):
	ctype = models.CharField(choices=categorytypes,max_length=64)
class OwnerShipTypes(models.Model):
	otype = models.CharField(choices=ownershiptypes,max_length=64)

class SignUp(models.Model):
	email = models.CharField(max_length=64)
	category = models.CharField(max_length=64)
	ownership = models.CharField(max_length=64)
	name = models.CharField(max_length=64)
	date = models.DateField(blank=False)
	auth_name = models.CharField(max_length=64)
	auth_desig = models.CharField(max_length=64)
	auth_mob = models.CharField(max_length=64)
	beds_icu = models.IntegerField(blank=True,null=True,default=0)
	beds_others = models.IntegerField(blank=True,null=True,default=0)
	beds_ot = models.IntegerField(blank=True,null=True,default=0)
	beds_total = models.IntegerField(blank=True,null=True,default=0)
	address = models.CharField(max_length=128)
	bio_auth1_name = models.CharField(max_length=64)
	bio_auth1_mob = models.CharField(max_length=64,default=0)
	bio_auth2_name = models.CharField(max_length=64)
	bio_auth2_mob = models.CharField(max_length=64,default=0)
	supervisor_name = models.CharField(max_length=64)
	supervisor_mob = models.CharField(max_length=64,default=0)
	supervisor_name2 = models.CharField(max_length=64)
	supervisor_mob2 = models.CharField(max_length=64,default=0)
	status = models.CharField(max_length=64)
	key = models.CharField(max_length=64,null=True)
	def __str__(self):
                return self.email


class User(models.Model):
	email = models.ForeignKey(SignUp,verbose_name="Email ID")
	username = models.CharField(max_length=64)
	password = models.CharField(max_length=64)
	def __str__(self):
                return self.username


class PrimaryAdmin(models.Model):
	username = models.CharField(max_length=64)
	password = models.CharField(max_length=64)
	def __str__(self):
                return self.username

class SecondaryAdmin(models.Model):
	username = models.CharField(max_length=64)
	password = models.CharField(max_length=64)
	def __str__(self):
                return self.username

class Waste(models.Model):
	#username = models.ForeignKey(User,verbose_name="username")
	date = models.DateField(blank=False)
	hospital_code =  models.CharField(max_length=64)
	key = models.CharField(max_length=64)
	name = models.CharField(max_length=64)
	waste1 = models.IntegerField(blank=True,null=True,default=0)	#yellow
	waste2 = models.IntegerField(blank=True,null=True,default=0)	#red 
	waste3 = models.IntegerField(blank=True,null=True,default=0)	#white
	waste4 = models.IntegerField(blank=True,null=True,default=0)	#blue
	def __str__(self):
                return (self.name+" " +str(self.date))
	

