from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()


class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
