from django import forms
from .models import DocumentCategory, Document, Image
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
        self.fields['document'].help_text = "Only .doc and .docx file format is supported and maximum file size is 2.5MB."
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
        if not document == None:
            file_extension = os.path.splitext(document.name)[1]
            allowed_types = settings.DOCUMENT_TYPES
            content_type = document.content_type.split('/')[0]
            file_name_length = len(os.path.splitext(document.name)[0])
            if file_name_length > 100:
                raise forms.ValidationError("File name is too long!!! Please rename the file and then try to upload again.")
            if not file_extension in allowed_types:
                if file_extension in settings.IMAGE_TYPES:
                    url = "<a href='/contribution/image/upload/'>here</a>"
                    raise forms.ValidationError(
                        "Seems you want to upload image file! Please click %s to upload image." % url)
                raise forms.ValidationError("Only %s file formats are supported! Current file format is %s" % (allowed_types, file_extension))
            if document.size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError("Please keep filesize under %s. Current filesize %s" % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(document.size)))
            return document
        return None


class ImageUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ImageUploadForm, self).__init__(*args, **kwargs)
        self.fields['title'].help_text = "Tiny description about the image"
        self.fields['title'].label = "Subject"
        self.fields['image'].help_text = "Only image file is supported and maximum file size is 2.5MB."
        self.fields['title'].widget.attrs.update({
            'placeholder': 'Enter Image Subject',
            'maxlength': 20
        })

    class Meta:
        model = Image
        fields = ['title', 'image']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title == None:
            space_identifier = re.search(r"\s", title)
            allowed_chars = re.match(r'^[A-Za-z0-9-_ ]+$', title)
            length = len(title)
            if not allowed_chars:
                raise forms.ValidationError(
                    "Only Alpha Numeric values, -, _ and spaces are allowed!")
            if length > 20:
                raise forms.ValidationError("Maximum 20 characters allowed!")
        return title

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image == None:
            file_extension = os.path.splitext(image.name)[1]
            allowed_types = settings.IMAGE_TYPES
            content_type = image.content_type.split('/')[0]
            file_name_length = len(os.path.splitext(document.name)[0])
            if file_name_length > 100:
                raise forms.ValidationError(
                    "File name is too long!!! Please rename the file and then try to upload again.")
            if not file_extension in allowed_types:
                if file_extension in settings.DOCUMENT_TYPES:
                    url = "<a href='/contribution/document/upload/'>here</a>"
                    raise forms.ValidationError(
                        "Seems you want to upload word document! Please click %s to upload document." % url)
                raise forms.ValidationError("Only %s file formats are supported! Current file format is %s" % (
                    allowed_types, file_extension))
            if image.size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError("Please keep filesize under %s. Current filesize %s" % (
                    filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(image.size)))
            return image
        return None


    
