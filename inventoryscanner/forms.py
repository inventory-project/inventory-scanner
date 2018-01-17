from django import forms

STATUS_CHOICES = (
    (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"), (6, "6"), (7, "7"), (8, "8"), (9, "9"), 
    (10, "10"), (11, "11"), (12, "12"), (13, "13"), (14, "14"), (15, "15"), (16, "16"), (17, "17"), (18, "18"), (19, "19"),
    (20, "20"), (21, "21"), (22, "22"), (23, "23"), (24, "24"), (25, "25"), (26, "26"), (27, "27"), (28, "28"), (29, "29"),
    (30, "30"), (31, "31"), (32, "32"), (33, "33"), (34, "34"), (35, "35"), (36, "36"), (37, "37"), (38, "38"), (39, "39"),
    (40, "40"), (41, "41"), (42, "42"), (43, "43"), (44, "44"), (45, "45"), (46, "46"), (47, "47"), (48, "48"), (49, "49"),
    (50, "50"), (51, "51"), (52, "52")
)

SERVICE_CHOICES = (
    ("p1", "P1"),
    ("p2", "P2"),
)

class SelectWeeksForm(forms.Form):
    weeks = forms.ChoiceField(choices = STATUS_CHOICES, initial=52)

class DemandForm(forms.Form):
    quantity = forms.CharField(required=True, initial=0, widget=forms.TextInput(attrs={'class':'form-quantity' , 'autocomplete':'off', 'pattern':'[0-9]+', 'title':'Enter numbers Only '}))
    active = forms.CharField(initial=True, widget=forms.HiddenInput(attrs={'class':'form-active'}))
    #quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'number-input'}), required=True)

class ParameterForm(forms.Form):
    l_avg = forms.CharField(required=True, initial=0, widget=forms.TextInput(attrs={'class':'form-parameters' , 'autocomplete':'off', 'pattern':'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?', 'title':'Enter numbers only '}))
    l_std = forms.CharField(required=True, initial=0, widget=forms.TextInput(attrs={'class':'form-parameters' , 'autocomplete':'off', 'pattern':'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?', 'title':'Enter numbers only, decimals are denoted as 0.7'}))
    order_quantity = forms.CharField(required=True, initial=0, widget=forms.TextInput(attrs={'class':'form-parameters' , 'autocomplete':'off', 'pattern':'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?', 'title':'Enter numbers only, decimals are denoted as 0.7'}))
    service = forms.CharField(required=True, initial=0, widget=forms.TextInput(attrs={'class':'form-parameters' , 'autocomplete':'off', 'pattern':'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?', 'title':'Enter numbers only, decimals are denoted as 0.7'}))
    service_measure = forms.ChoiceField(choices = SERVICE_CHOICES, initial='P1')
    costprice = forms.CharField(required=True, initial=0, widget=forms.TextInput(attrs={'class':'form-parameters' , 'autocomplete':'off', 'pattern':'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?', 'title':'Enter numbers only, decimals are denoted as 0.7'}))
    current_reorderpoint = forms.CharField(required=True, initial=0, widget=forms.TextInput(attrs={'class':'form-parameters' , 'autocomplete':'off', 'pattern':'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?', 'title':'Enter numbers only, decimals are denoted as 0.7'}))