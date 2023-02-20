from django.forms import ModelForm, TextInput
from .models import City

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name' : TextInput(attrs={'class' : 'option-btn', 'id' : 'add-btn', 'name' : 'watchlist', 'type' : 'submit', 'value' : 'Add to Watchlist'})}

    def __init__(self, *args, **kwargs):
        super(CityForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = ""

    def set_city(self, city_name):
        data = self.data.copy()
        print(data)
        data['name'] = city_name
        self.data = data