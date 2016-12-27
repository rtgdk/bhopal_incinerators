from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest, JsonResponse
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
#addddddd
from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
#import django_excel as excel
from datetime import datetime,date,timedelta
from django.core.mail import send_mail,send_mass_mail
from django.views.decorators.cache import cache_control
#mail
#from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.core.mail import send_mail
#excel
import xlsxwriter

from .models import SignUp,User,PrimaryAdmin,SecondaryAdmin,Waste
def index(request):
	context_dict={}
	b=SignUp.objects.filter()
	context_dict['b'] = b 
	if request.method == 'POST':
		if 'primaryadmin' in request.session:
			try:
				name = request.POST['name']
				a= SignUp.objects.get(key=name)
				Waste.objects.create( date = datetime.now().strftime("%Y-%m-%d") , hospital_code = a.id , key = a.key ,name = a.name, waste1 = request.POST['bag_1'] , waste2 = request.POST['bag_2'] ,waste3 = request.POST['bag_3'],waste4 = request.POST['bag_4'] ) 
			except: 
				return HttpResponse("error")
			return render(request, 'app/index.html',context_dict)
		elif 'secondaryadmin' in request.session:
			try:
				name = request.POST['name']
				a= SignUp.objects.get(key=name)
				Waste.objects.create( date = datetime.now().strftime("%Y-%m-%d") , hospital_code = a.id , key = a.key ,name = a.name, waste1 = request.POST['bag_1'] , waste2 = request.POST['bag_2'] ,waste3 = request.POST['bag_3'],waste4 = request.POST['bag_4'] ) 
			except: 
				return HttpResponse("error")
			return render(request, 'app/index.html',context_dict)
	else:
		if 'user' in request.session:
			try:
				w=Waste.objects.filter(username=request.session['user'])
				context_dict['waste']=w
			except:
				pass
			return render(request, 'app/index.html',context_dict)
		elif 'primaryadmin' in request.session:
			try:
				pending_user = SignUp.objects.filter(status="pending")
				context_dict['pending_user']=pending_user
				approved_user = SignUp.objects.filter(status="approved")
				context_dict['approved_user']=approved_user
			except: 
				pass
			return render(request, 'app/index.html',context_dict)
		elif 'secondaryadmin' in request.session:
			pending_user = SignUp.objects.filter(status="pending")
			context_dict['pending_user']=pending_user
			return render(request, 'app/index.html',context_dict)
	return render(request, 'app/index.html')

def contact(request):
	return render(request, 'app/contact.html')

def about(request):
	return render(request, 'app/about.html')

def services(request):
	return render(request, 'app/services.html')

def our_technology(request):
	return render(request, 'app/our_technology.html')

def signup(request):
	context_dict = {}
	reg_user=SignUp.objects.filter()
	context_dict['reg_user']= reg_user
	if request.method == 'POST':
		email = request.POST['email']
		for i in reg_user :
			if (i.email==email):
				context_dict["done"]=2
				return render(request, 'app/signup.html',context_dict)
		category = request.POST['category']
		if category == "Other":
			category = request.POST['specify_cat']
		ownership = request.POST['ownership']
		if ownership == "Other":
			ownership = request.POST['specify_own']
		name = request.POST['establishment_name']
		for i in reg_user :
			if (i.name==name):
				context_dict["done"]=3
				return render(request, 'app/signup.html',context_dict)
		date = request.POST.get('demo')
		auth_name = request.POST['auth_name']
		auth_desig = request.POST['auth_designation']
		auth_mob = request.POST['auth_contact']
		beds_icu = request.POST['beds_icu']
		beds_others = request.POST['beds_other']
		beds_ot = request.POST['beds_ot']
		if (beds_icu == "" ):
			beds_icu=0
		if (beds_others == "" ):
			beds_others=0
		if (beds_ot == "" ):
			beds_ot=0
		beds_total = int(beds_others)+int(beds_ot)+int(beds_icu)
		address = request.POST['address']
		bio_auth1_name = request.POST['bio_auth_name1']
		bio_auth1_mob = request.POST['bio_auth_mob1']
		bio_auth2_name = request.POST['bio_auth_name2']
		bio_auth2_mob = request.POST['bio_auth_mob2']
		supervisor_name = request.POST['sup_name1']
		supervisor_mob = request.POST['sup_mob1']
		supervisor_name2 = request.POST['sup_name1']
		supervisor_mob2 = request.POST['sup_mob2']
		#return HttpResponse(supervisor_mob)
		status="pending"
		a=SignUp.objects.create(email=email,category=category,ownership=ownership,name=name,date=date,auth_name=auth_name,auth_desig=auth_desig,
					auth_mob=auth_mob,beds_icu=beds_icu,beds_others=beds_others,beds_ot=beds_ot,beds_total=beds_total,
					address=address,bio_auth1_name=bio_auth1_name,bio_auth2_name=bio_auth2_name, 						bio_auth1_mob=bio_auth1_mob,
					bio_auth2_mob=bio_auth2_mob,supervisor_name=supervisor_name,supervisor_name2=supervisor_name2,
					supervisor_mob=supervisor_mob,
					supervisor_mob2=supervisor_mob2,status=status)
		a.key = str(a.id)+"-"+str(a.name)
		a.save()
		#return HttpResponse(a.key)
		#return HttpResponse("Done")
		context_dict["done"]=1
		html_content = "<body><p> Fill the attachments and submit them to Bhopal Incinerators. </body>"
	   	email1 = EmailMessage("Bhopal Incinerators", html_content, "ssms7907@gmail.com", [email])
	   	email1.content_subtype = "html"
	   
	   	fd = open('Affidavit for New Client.doc', 'r')
	   	email1.attach('Affidavit for New Client.doc', fd.read())
	   	fd2 = open('Agreement.doc', 'r')
	   	email1.attach('Agreement.doc', fd2.read())
	   	res = email1.send()
		return render(request, 'app/signup.html',context_dict)
	else :
		context_dict["done"]=0
		return render(request, 'app/signup.html',context_dict)

def admin_login(request):
	context_dict={}
	if request.method == 'POST':
		username=request.POST['username']
		password=request.POST['password']
		try:
			user = PrimaryAdmin.objects.get(username=username)
			if password == user.password:
				request.session['primaryadmin']=user.username
				return HttpResponseRedirect("/app/")
			else :
				context_dict["notlogin"]="Invalid Credentials"
				return render(request, 'app/admin_login.html',context_dict)
		except:
			try :
				user = SecondaryAdmin.objects.get(username=username)
				if password == user.password:
					request.session['secondaryadmin']=user.username
					return HttpResponseRedirect("/app/")
				else :
					context_dict["notlogin"]="Invalid Credentials"
					return render(request, 'app/admin_login.html',context_dict)
			except :
				context_dict["notlogin"]="Invalid Credentials"
				return render(request, 'app/admin_login.html',context_dict)
	else :

		return render(request, 'app/admin_login.html')

def user_login(request):
	context_dict={}
	if request.method == 'POST':
		username=request.POST['username']
		password=request.POST['password']
		try:
			user = User.objects.get(username=username)	
			request.session['user']=user.username
			if password == user.password:
				return HttpResponseRedirect("/app/update/")
		except:
			context_dict["notlogin"]="Invalid Credentials"
			return render(request, 'app/user_login.html',context_dict)
			return HttpResponseRedirect("/app/user_login/")
	else :

		return render(request, 'app/user_login.html')


def logout(request):
    	if 'user' in request.session:
        	request.session.flush()
        	return HttpResponseRedirect("/app/user_login/")
   	elif 'primaryadmin' in request.session:
		request.session.flush()
		return HttpResponseRedirect("/app/admin_login/")
	elif 'secondaryadmin' in request.session:
		request.session.flush()
		return HttpResponseRedirect("/app/admin_login/")
    	request.session.flush()
    	return HttpResponseRedirect("/")


def user_page(request,user_id):
	context_dict={}
	if 'primaryadmin' in request.session or 'secondaryadmin' in request.session:
		try:
			signup=SignUp.objects.get(id=user_id)
			context_dict['signup']=signup
			
			
			if request.method == 'POST':
				a=request.POST.get('username')
				b=request.POST.get('password')
				if (User.objects.filter(username=a).count()>0) :
					error="User Name already Exist"
					context_dict["error"]=error
				else:
					User.objects.create(username=a,password=b,email=signup)
					signup.status="approved"
					signup.save()
					try :
						user1=User.objects.get(email=signup)
						context_dict['user1']=user1
					except :
						pass
			else :
				
				try :
					user1=User.objects.get(email=signup)
					context_dict['user1']=user1
				except :
					pass
			
			return render(request, 'app/user_page.html',context_dict)
		except :
			return HttpResponseRedirect("/app/")

	else :
		return HttpResponseRedirect("/")




def update(request):  #i denotes whether submit button clicked or not, s denotes 1 for single day and 0 for multiple day
	context_dict={}
	
	if request.method == 'POST':
		if 'form1' in request.POST:
			name= request.POST['name1']
			if name=="":
				date= request.POST['demo1_1']
				waste = Waste.objects.filter(date=date)
				context_dict['date']=date
				i=1
				s=1
				context_dict['i']=i
				context_dict['s']=s
				context_dict['waste']=waste
				total={}
				a1=0
				a2=0
				a3=0
				a4=0
				b=[]
				for k in waste :
					a1=a1+k.waste1
					a2=a2+k.waste2
					a3=a3+k.waste3
					a4=a4+k.waste4
					b.append([str(k.date),str(k.name),str(k.waste1),str(k.waste2),str(k.waste3),str(k.waste4)]) #excel
				print(b)	
				total['a1']=a1
				total['a2']=a2
				total['a3']=a3
				total['a4']=a4
				context_dict['total']=total
				#excel
				workbook = xlsxwriter.Workbook('app/media/'+'All'+'_'+date+'_list.xlsx')
				context_dict['link']='All'+'_'+date+'_list.xlsx'
				worksheet = workbook.add_worksheet()
				worksheet.set_column('A:A', 15)
				worksheet.set_column('B:B', 25)
				worksheet.set_column('C:C', 15)
				worksheet.set_column('D:D', 15)
				worksheet.set_column('E:E', 15)
				worksheet.set_column('F:F', 15)
				bold = workbook.add_format({'bold': 1})
				worksheet.write('A1', 'Date', bold)
				worksheet.write('B1', 'Name', bold)
				worksheet.write('C1', 'Yellow Bag', bold)
				worksheet.write('D1', 'Red Bag', bold)
				worksheet.write('E1', 'White Bag', bold)
				worksheet.write('F1', 'Blue Bag', bold)
				row = 1
				col = 0
				for i in b:
					worksheet.write_string  (row, col,i[0] )
					worksheet.write_string(row, col + 1, i[1] )
					worksheet.write_string  (row, col + 2,i[2] )
					worksheet.write_string  (row, col+3,i[3] )
					worksheet.write_string(row, col + 4, i[4] )
					worksheet.write_string  (row, col + 5,i[5] )
					row += 1
				workbook.close()
				return render(request, 'app/update.html',context_dict)
			date= request.POST['demo1_1']
			waste = Waste.objects.filter(key=name,date=date)
			i=1
			s=1
			context_dict['i']=i
			context_dict['s']=s
			context_dict['waste']=waste
			context_dict['date']=date
			total={}
			a1=0
			a2=0
			a3=0
			a4=0
			b=[]
			for k in waste :
				a1=a1+k.waste1
				a2=a2+k.waste2
				a3=a3+k.waste3
				a4=a4+k.waste4
				b.append([str(k.date),str(k.name),str(k.waste1),str(k.waste2),str(k.waste3),str(k.waste4)]) #excel
			print(b)
			total['a1']=a1
			total['a2']=a2
			total['a3']=a3
			total['a4']=a4
			context_dict['total']=total
			#excel
			workbook = xlsxwriter.Workbook('app/media/'+name+'_'+date+'_list.xlsx')
			context_dict['link']= name+'_'+date+'_list.xlsx'
			worksheet = workbook.add_worksheet()
			worksheet.set_column('A:A', 15)
			worksheet.set_column('B:B', 25)
			worksheet.set_column('C:C', 15)
			worksheet.set_column('D:D', 15)
			worksheet.set_column('E:E', 15)
			worksheet.set_column('F:F', 15)
			bold = workbook.add_format({'bold': 1})
			worksheet.write('A1', 'Date', bold)
			worksheet.write('B1', 'Name', bold)
			worksheet.write('C1', 'Yellow Bag', bold)
			worksheet.write('D1', 'Red Bag', bold)
			worksheet.write('E1', 'White Bag', bold)
			worksheet.write('F1', 'Blue Bag', bold)
			row = 1
			col = 0
			for i in b:
				worksheet.write_string  (row, col,i[0] )
				worksheet.write_string(row, col + 1, i[1] )
				worksheet.write_string  (row, col + 2,i[2] )
				worksheet.write_string  (row, col+3,i[3] )
				worksheet.write_string(row, col + 4, i[4] )
				worksheet.write_string  (row, col + 5,i[5] )
				row += 1
			workbook.close()
			return render(request, 'app/update.html',context_dict)
		if 'form2' in request.POST:
			total={}
			name= request.POST['name2']
			if name=="":
				from_date= request.POST['demo1_2']
				to_date= request.POST['demo2_2']
				context_dict['fdate']=from_date
				context_dict['tdate']=to_date
				waste = Waste.objects.filter(date__range=[from_date, to_date])
				i=1
				s=0
				context_dict['i']=i
				context_dict['s']=s
				context_dict['waste']=waste
				a1=0
				a2=0
				a3=0
				a4=0
				b=[]
				for k in waste :
					a1=a1+k.waste1
					a2=a2+k.waste2
					a3=a3+k.waste3
					a4=a4+k.waste4
					b.append([str(k.date),str(k.name),str(k.waste1),str(k.waste2),str(k.waste3),str(k.waste4)])
				print(b)
				total['a1']=a1
				total['a2']=a2
				total['a3']=a3
				total['a4']=a4
				context_dict['total']=total
				#excel
				workbook = xlsxwriter.Workbook('app/media/'+'All'+'_'+from_date+'to'+to_date+'_list.xlsx')
				context_dict['link']= 'All'+'_'+from_date+'to'+to_date+'_list.xlsx'
				worksheet = workbook.add_worksheet()
				worksheet.set_column('A:A', 15)
				worksheet.set_column('B:B', 25)
				worksheet.set_column('C:C', 15)
				worksheet.set_column('D:D', 15)
				worksheet.set_column('E:E', 15)
				worksheet.set_column('F:F', 15)
				bold = workbook.add_format({'bold': 1})
				worksheet.write('A1', 'Date', bold)
				worksheet.write('B1', 'Name', bold)
				worksheet.write('C1', 'Yellow Bag', bold)
				worksheet.write('D1', 'Red Bag', bold)
				worksheet.write('E1', 'White Bag', bold)
				worksheet.write('F1', 'Blue Bag', bold)
				row = 1
				col = 0
				for i in b:
					worksheet.write_string  (row, col,i[0] )
					worksheet.write_string(row, col + 1, i[1] )
					worksheet.write_string  (row, col + 2,i[2] )
					worksheet.write_string  (row, col+3,i[3] )
					worksheet.write_string(row, col + 4, i[4] )
					worksheet.write_string  (row, col + 5,i[5] )
					row += 1
				workbook.close()
				return render(request, 'app/update.html',context_dict)
			from_date= request.POST['demo1_2']
			to_date= request.POST['demo2_2']
			waste = Waste.objects.filter(key=name,date__range=[from_date, to_date])
			i=1
			s=0
			context_dict['i']=i
			context_dict['s']=s
			context_dict['fdate']=from_date
			context_dict['tdate']=to_date
			context_dict['waste']=waste
			a1=0
			a2=0
			a3=0
			a4=0
			b=[]
			for k in waste :
				a1=a1+k.waste1
				a2=a2+k.waste2
				a3=a3+k.waste3
				a4=a4+k.waste4
				b.append([str(k.date),str(k.name),str(k.waste1),str(k.waste2),str(k.waste3),str(k.waste4)])
			print(b)
			total['a1']=a1
			total['a2']=a2
			total['a3']=a3
			total['a4']=a4
			context_dict['total']=total
			#excel
			workbook = xlsxwriter.Workbook('app/media/'+name+'_'+from_date+'to'+to_date+'_list.xlsx')
			context_dict['link']= name+'_'+from_date+'to'+to_date+'_list.xlsx'
			worksheet = workbook.add_worksheet()
			worksheet.set_column('A:A', 15)
			worksheet.set_column('B:B', 25)
			worksheet.set_column('C:C', 15)
			worksheet.set_column('D:D', 15)
			worksheet.set_column('E:E', 15)
			worksheet.set_column('F:F', 15)
			bold = workbook.add_format({'bold': 1})
			worksheet.write('A1', 'Date', bold)
			worksheet.write('B1', 'Name', bold)
			worksheet.write('C1', 'Yellow Bag', bold)
			worksheet.write('D1', 'Red Bag', bold)
			worksheet.write('E1', 'White Bag', bold)
			worksheet.write('F1', 'Blue Bag', bold)
			row = 1
			col = 0
			for i in b:
				worksheet.write_string  (row, col,i[0] )
				worksheet.write_string(row, col + 1, i[1] )
				worksheet.write_string  (row, col + 2,i[2] )
				worksheet.write_string  (row, col+3,i[3] )
				worksheet.write_string(row, col + 4, i[4] )
				worksheet.write_string  (row, col + 5,i[5] )
				row += 1
			workbook.close()
			return render(request, 'app/update.html',context_dict)
					
		
		if 'form3' in request.POST:
			date=request.POST['date']
			name=request.POST['name']
			waste1=request.POST['bag_1']
			waste2=request.POST['bag_2']
			waste3=request.POST['bag_3']
			waste4=request.POST['bag_4']
			a = Waste.objects.get(date=date,name=name)
			a.waste1=waste1
			a.waste2=waste2
			a.waste3=waste3
			a.waste4=waste4
			a.save()
			return render(request, 'app/update.html',context_dict)
		if 'form4' in request.POST:
			username=request.session['user']
			a=User.objects.get(username=username)
			c=SignUp.objects.get(email=a.email)
			date= request.POST['demo1_1']
			waste = Waste.objects.filter(name=c.name,date=date)
			i=1
			s=1
			context_dict['i']=i
			context_dict['s']=s
			context_dict['waste']=waste
			total={}
			a1=0
			a2=0
			a3=0
			a4=0
			b=[]
			for k in waste :
				a1=a1+k.waste1
				a2=a2+k.waste2
				a3=a3+k.waste3
				a4=a4+k.waste4
				b.append([str(k.date),str(k.name),str(k.waste1),str(k.waste2),str(k.waste3),str(k.waste4)])
			print(b)
			total['a1']=a1
			total['a2']=a2
			total['a3']=a3
			total['a4']=a4
			context_dict['total']=total
			#excel
			workbook = xlsxwriter.Workbook('app/media/'+c.name+'_'+date+'_list.xlsx')
			context_dict['link']= c.name+'_'+date+'_list.xlsx'
			worksheet = workbook.add_worksheet()
			worksheet.set_column('A:A', 15)
			worksheet.set_column('B:B', 25)
			worksheet.set_column('C:C', 15)
			worksheet.set_column('D:D', 15)
			worksheet.set_column('E:E', 15)
			worksheet.set_column('F:F', 15)
			bold = workbook.add_format({'bold': 1})
			worksheet.write('A1', 'Date', bold)
			worksheet.write('B1', 'Name', bold)
			worksheet.write('C1', 'Yellow Bag', bold)
			worksheet.write('D1', 'Red Bag', bold)
			worksheet.write('E1', 'White Bag', bold)
			worksheet.write('F1', 'Blue Bag', bold)
			row = 1
			col = 0
			for i in b:
				worksheet.write_string  (row, col,i[0] )
				worksheet.write_string(row, col + 1, i[1] )
				worksheet.write_string  (row, col + 2,i[2] )
				worksheet.write_string  (row, col+3,i[3] )
				worksheet.write_string(row, col + 4, i[4] )
				worksheet.write_string  (row, col + 5,i[5] )
				row += 1
			workbook.close()
			return render(request, 'app/update.html',context_dict)
		if 'form5' in request.POST:
			total={}
			username=request.session['user']
			a=User.objects.get(username=username)
			c=SignUp.objects.get(email=a.email)
			from_date= request.POST['demo1_2']
			to_date= request.POST['demo2_2']
			waste = Waste.objects.filter(name=c.name,date__range=[from_date, to_date])
			i=1
			s=0
			context_dict['i']=i
			context_dict['s']=s
			context_dict['waste']=waste
			a1=0
			a2=0
			a3=0
			a4=0
			b=[]
			for k in waste :
				a1=a1+k.waste1
				a2=a2+k.waste2
				a3=a3+k.waste3
				a4=a4+k.waste4
				b.append([str(k.date),str(k.name),str(k.waste1),str(k.waste2),str(k.waste3),str(k.waste4)])
			print(b)
			total['a1']=a1
			total['a2']=a2
			total['a3']=a3
			total['a4']=a4
			context_dict['total']=total
			#excel
			workbook = xlsxwriter.Workbook('app/media/'+c.name+'_'+from_date+'to'+to_date+'_list.xlsx')
			context_dict['link']= c.name+'_'+from_date+'to'+to_date+'_list.xlsx'
			worksheet = workbook.add_worksheet()
			worksheet.set_column('A:A', 15)
			worksheet.set_column('B:B', 25)
			worksheet.set_column('C:C', 15)
			worksheet.set_column('D:D', 15)
			worksheet.set_column('E:E', 15)
			worksheet.set_column('F:F', 15)
			bold = workbook.add_format({'bold': 1})
			worksheet.write('A1', 'Date', bold)
			worksheet.write('B1', 'Name', bold)
			worksheet.write('C1', 'Yellow Bag', bold)
			worksheet.write('D1', 'Red Bag', bold)
			worksheet.write('E1', 'White Bag', bold)
			worksheet.write('F1', 'Blue Bag', bold)
			row = 1
			col = 0
			for i in b:
				worksheet.write_string  (row, col,i[0] )
				worksheet.write_string(row, col + 1, i[1] )
				worksheet.write_string  (row, col + 2,i[2] )
				worksheet.write_string  (row, col+3,i[3] )
				worksheet.write_string(row, col + 4, i[4] )
				worksheet.write_string  (row, col + 5,i[5] )
				row += 1
			workbook.close()
			return render(request, 'app/update.html',context_dict)
	else :
		i=0
		context_dict['i']=i
		return render(request, 'app/update.html',context_dict)
	
	
def complain(request):
	subject = request.session['user']+" : "+request.POST['subject']
	body= request.POST['complain']
	send_mail(subject,body,'ssms7907@gmail.com',['rohit.lodhartg@gmail.com'],fail_silently=False,)
	return render(request, 'app/complain.html')

	
	
	
	"""
import json
from django.utils.translation import ugettext_lazy as _

def email_validate(request):
    error = ''
    success = False
    return HttpResponse("heer")
    if request.method == 'POST':
        email = request.POST.get('email', None)
        if not email:
            error = _('Please enter email')
        elif SignUp.objects.filter(email=email).exists():
            error = _('This email is already registered')
        else:
            success = True

    ajax_vars = {'success': success, 'error': error}
    return HttpResponse(json.dumps(ajax_vars),
                    mimetype='application/javascript')"""
                    
                    
                    
import json
def autocompleteModel(request):
    if 'term' in request.GET:
        tags = SignUp.objects.filter(status="approved",key__icontains=request.GET['term']).values_list('key',flat=True)[:10]
        
        return HttpResponse( json.dumps( [ tag for tag in tags ] ) )
    return HttpResponse()


"""
def autocompleteModel2(request):
    if 'term' in request.GET:
        tags = SignUp.objects.filter(status="approved",id__istartswith=request.GET['term']).values_list('id', flat=True).distinct()[:10]
        return HttpResponse( json.dumps( [ tag for tag in tags ] ) )
    return HttpResponse()"""
    
    
 

