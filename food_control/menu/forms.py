import django.forms

import menu.models


class BreakfastMenuForm(django.forms.ModelForm):
    class Meta:
        model = menu.models.BreakfastMenu
        fields = ["drink1", "drink2", "dish1", "dish2"]
        widgets = {
            "drink1": django.forms.Select(attrs={"class": "form-select"}),
            "drink2": django.forms.Select(attrs={"class": "form-select"}),
            "dish1": django.forms.Select(attrs={"class": "form-select"}),
            "dish2": django.forms.Select(attrs={"class": "form-select"}),
        }


class LunchMenuForm(django.forms.ModelForm):
    class Meta:
        model = menu.models.LunchMenu
        fields = [
            "drink1",
            "drink2",
            "soup1",
            "soup2",
            "main",
            "salad1",
            "salad2",
        ]
        widgets = {
            field: django.forms.Select(attrs={"class": "form-select"})
            for field in [
                "drink1",
                "drink2",
                "soup1",
                "soup2",
                "main",
                "salad1",
                "salad2",
            ]
        }
