from django import forms
from .models import SignUp
class SignUpForm(forms.ModelForm):
	def clean(self):
		email = self.cleaned_data.get('email')
		reg_user = SignUp.objects.filter()
		for i in reg_user:
			if (email==i.email):
				raise forms.ValidationError("Email already registered")
				break
		return self.cleaned_data
	class Meta:
	        model = SignUp
	        fields = ('email',)
