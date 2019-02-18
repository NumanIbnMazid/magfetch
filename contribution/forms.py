from django import forms
from .models import DocumentCategory, Document
import re
from django.template.defaultfilters import filesizeformat
from django.conf import settings
import os


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


class DocumentUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DocumentUploadForm, self).__init__(*args, **kwargs)
        CATEGORY_QUERYSET = DocumentCategory.objects.all()
        self.fields['category'].help_text = "Select the category of your article."
        self.fields['document'].help_text = "Only .doc and .docx file format is supported and maximum file size is 2MB."
        self.fields['category'] = forms.ModelChoiceField(queryset=CATEGORY_QUERYSET, empty_label="------- SELECT -------")
        # self.fields['title'].widget.attrs.update({
        #     'placeholder': 'Ex: Poem, Novel etc.',
        #     'maxlength': 20
        # })
        # self.fields['document'].widget = forms.ClearableFileInput(attrs={'multiple': True})


    class Meta:
        model = Document
        fields = ['category', 'document']

    def clean_document(self):
        document = self.cleaned_data.get('document')
        file_extension = os.path.splitext(document.name)[1]
        allowed_types = ['.doc', '.docx']
        content_type = document.content_type.split('/')[0]
        if not file_extension in allowed_types:
            raise forms.ValidationError("Only %s file formats are supported! Current file format is %s" % (allowed_types, file_extension))
        if document.size > settings.MAX_UPLOAD_SIZE:
            raise forms.ValidationError("Please keep filesize under %s. Current filesize %s" % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(document.size)))
        return document

    
