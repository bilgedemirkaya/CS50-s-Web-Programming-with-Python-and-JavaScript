from django import forms

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Let us know your opinion','rows':5}))


class BidForm(forms.Form):
    bid = forms.IntegerField()