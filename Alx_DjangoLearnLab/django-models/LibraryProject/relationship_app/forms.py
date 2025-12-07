from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

    def clean_publication_year(self):
        year = self.cleaned_data.get('publication_year')
        if year is None or not isinstance(year, int):
            raise forms.ValidationError("Please enter a valid year.")
        return year

