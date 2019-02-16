from django import forms
from .models import DocumentCategory
import re


class DocumentCategoryCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DocumentCategoryCreateForm, self).__init__(*args, **kwargs)
        self.fields['title'].help_text = "Maximum 20 characters allowed"
        self.fields['title'].widget.attrs.update({
            'placeholder' : 'Ex: Poem, Novel etc.',
            'maxlength' : 20
        })

    class Meta:
        model = DocumentCategory
        fields = ['title']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title == None :
            space_identifier = re.search(r"\s", title)
            allowed_chars = re.match(r'^[A-Za-z-_]+$', title)
            length = len(title)
            if space_identifier:
                raise forms.ValidationError("Spaces are not allowed!")
            if not allowed_chars:
                raise forms.ValidationError("Only 'A-Z', 'a-z', '-', '_' are allowed!")
            if length > 20:
                raise forms.ValidationError("Maximum 20 characters allowed!")
        return title
