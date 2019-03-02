from django import forms
from .models import ContributionCategory, Contribution
import re
from django.template.defaultfilters import filesizeformat
from django.conf import settings
import os



class ContributionCategoryCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContributionCategoryCreateForm, self).__init__(*args, **kwargs)
        self.fields['category_for'].help_text = "Select if the category is for images or documents."
        self.fields['title'].help_text = "Maximum 23 characters allowed"
        self.fields['title'].widget.attrs.update({
            'placeholder': 'Ex: Poem, Novel, Potrait, Landscape etc.',
            'maxlength': 23
        })

    class Meta:
        model = ContributionCategory
        fields = ['category_for', 'title']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title == None:
            
            allowed_chars = re.match(r'^[A-Za-z-_ ]+$', title)
            length = len(title)
            # space_identifier = re.search(r"\s", title)
            # if space_identifier:
            #     raise forms.ValidationError("Spaces are not allowed!")
            if not allowed_chars:
                raise forms.ValidationError(
                    "Only 'A-Z', 'a-z', '-', '_' and spaces are allowed!")
            if length > 23:
                raise forms.ValidationError("Maximum 23 characters allowed!")
        return title


class ContributionUploadForm(forms.ModelForm):
    DOC_CATEGORY_QUERYSET = ContributionCategory.objects.filter(
        category_for=0)
    IMG_CATEGORY_QUERYSET = ContributionCategory.objects.filter(
        category_for=1)
    doc_category = forms.ModelChoiceField(
        queryset=DOC_CATEGORY_QUERYSET, label="Document Category", required=False, empty_label="------- SELECT -------")
    img_category = forms.ModelChoiceField(
        queryset=IMG_CATEGORY_QUERYSET, label="Image Category", required=False, empty_label="------- SELECT -------")
    def __init__(self, *args, **kwargs):
        super(ContributionUploadForm, self).__init__(*args, **kwargs)
        self.fields['title'].help_text = "Enter the subject of contribution."
        self.fields['title'].widget.attrs.update({
            'placeholder': 'Enter contribution title',
            'maxlength': 30
        })
        self.fields['file'].widget.attrs.update({
            'id': 'file-upload',
            'onchange': "categoryFunction()"
        })
        self.fields['file'].help_text = "Only .doc, .docx, .jpg, .jpeg, .png and .svg file format is supported and maximum file size is 2.5MB."
        self.fields['category'].widget = forms.HiddenInput()
        self.fields['category'].required = False
        self.fields['doc_category'].widget.attrs.update({
            'id': 'doc-category',
        })
        self.fields['img_category'].widget.attrs.update({
            'id': 'img-category',
        })


    class Meta:
        model = Contribution
        fields = ['title', 'file', 'category']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title == None:
            allowed_chars = re.match(r'^[A-Za-z0-9-_ ]+$', title)
            length = len(title)
            if not allowed_chars:
                raise forms.ValidationError(
                    "Only Alpha Numeric values, -, _ and spaces are allowed!")
            if length > 30:
                raise forms.ValidationError("Maximum 30 characters allowed!")
        return title

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file == None:
            file_extension = os.path.splitext(file.name)[1]
            allowed_types = settings.FILE_TYPES
            content_type = file.content_type.split('/')[0]
            # file_name_length = len(os.path.splitext(file.name)[0])
            # if file_name_length > 100:
            #     raise forms.ValidationError("File name is too long!!! Please rename the file and then try to upload again.")
            if not file_extension in allowed_types:
                raise forms.ValidationError("Only %s file formats are supported! Current file format is %s" % (
                    allowed_types, file_extension))
            if file.size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError("Please keep filesize under %s. Current filesize %s" % (
                    filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(file.size)))
            return file
        return None
