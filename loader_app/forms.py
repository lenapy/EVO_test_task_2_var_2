from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()

    def clean(self):
        file = self.cleaned_data['file']
        if file.size > 10000000000:
            raise forms.ValidationError("%s больше чем 10кб" % file.size)
        else:
            return file

