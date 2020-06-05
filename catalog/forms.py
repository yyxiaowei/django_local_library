from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import datetime

from .models import BookInstance

# 自定义表单组件
class RenewBookForm(forms.Form):
    due_back = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        # 获取页面表单due_back的值
        data = self.cleaned_data['due_back']
        
        #Check date is not in past. 
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        #Check date is in range librarian allowed to change (+4 weeks).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data

# 使用ModelForm定义表单组件
class RenewBookModelForm(forms.ModelForm):
    # clear_field_name 对某个字段进行验证
    def clean_due_back(self):
        # 获取页面表单due_back的值
        data = self.cleaned_data['due_back']
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
        return data
    
    class Meta:
        model = BookInstance
        # fields = '__all__' # 添加所有字段
        fields = ['due_back']
        # exclude = ['id'] # 排除显示某个字段
        labels = { 'due_back': _('Renewal date'), }
        help_texts = { 'due_back': _('Enter a date between now and 4 weeks (default 3).'), } 
        