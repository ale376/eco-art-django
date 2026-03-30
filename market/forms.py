from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Profile, Review, Order

SHIPPING_LOCATION_DATA = {
    'Canada': {
        'requires_state': True,
        'states': {
            'Alberta': ['Calgary', 'Edmonton', 'Red Deer', 'Lethbridge', 'Fort McMurray', 'Airdrie', 'St. Albert', 'Grande Prairie', 'Medicine Hat'],
            'British Columbia': ['Vancouver', 'Victoria', 'Surrey', 'Burnaby', 'Kelowna', 'Richmond', 'Abbotsford', 'Coquitlam', 'Kamloops', 'Nanaimo'],
            'Manitoba': ['Winnipeg', 'Brandon', 'Steinbach', 'Thompson', 'Winkler', 'Selkirk', 'Portage la Prairie', 'Morden', 'Dauphin'],
            'New Brunswick': ['Fredericton', 'Moncton', 'Saint John', 'Miramichi', 'Edmundston', 'Bathurst', 'Dieppe', 'Campbellton'],
            'Newfoundland and Labrador': ["St. John's", 'Mount Pearl', 'Corner Brook', 'Gander', 'Labrador City', 'Grand Falls-Windsor', 'Happy Valley-Goose Bay'],
            'Northwest Territories': ['Yellowknife', 'Inuvik', 'Hay River', 'Fort Smith', 'Behchoko'],
            'Nova Scotia': ['Halifax', 'Sydney', 'Dartmouth', 'Truro', 'New Glasgow', 'Wolfville', 'Kentville', 'Yarmouth', 'Antigonish'],
            'Nunavut': ['Iqaluit', 'Rankin Inlet', 'Arviat', 'Cambridge Bay', 'Baker Lake'],
            'Ontario': ['Toronto', 'Ottawa', 'Mississauga', 'Hamilton', 'London', 'Windsor', 'Kitchener', 'Waterloo', 'Brampton', 'Vaughan', 'Markham', 'Richmond Hill', 'Burlington', 'Oakville', 'Oshawa', 'Kingston', 'Guelph', 'Thunder Bay', 'Greater Sudbury', 'Barrie', 'Peterborough', 'St. Catharines', 'Niagara Falls', 'Cambridge', 'Milton', 'Whitby', 'Ajax', 'Pickering'],
            'Prince Edward Island': ['Charlottetown', 'Summerside', 'Stratford', 'Cornwall', 'Montague'],
            'Quebec': ['Montreal', 'Quebec City', 'Laval', 'Gatineau', 'Sherbrooke', 'Longueuil', 'Trois-Rivieres', 'Saguenay', 'Drummondville'],
            'Saskatchewan': ['Saskatoon', 'Regina', 'Prince Albert', 'Moose Jaw', 'Yorkton', 'Swift Current', 'North Battleford'],
            'Yukon': ['Whitehorse', 'Dawson City', 'Watson Lake', 'Haines Junction', 'Carmacks'],
        },
    },
    'United States': {
        'requires_state': True,
        'states': {
            'California': ['Los Angeles', 'San Diego', 'San Francisco', 'San Jose', 'Sacramento'],
            'Florida': ['Miami', 'Orlando', 'Tampa', 'Jacksonville', 'St. Petersburg'],
            'Illinois': ['Chicago', 'Aurora', 'Naperville', 'Springfield', 'Rockford'],
            'New York': ['New York City', 'Buffalo', 'Rochester', 'Albany', 'Syracuse'],
            'Texas': ['Houston', 'Dallas', 'Austin', 'San Antonio', 'Fort Worth'],
            'Washington': ['Seattle', 'Spokane', 'Tacoma', 'Vancouver', 'Bellevue'],
        },
    },
    'India': {
        'requires_state': True,
        'states': {
            'Delhi': ['New Delhi', 'Dwarka', 'Rohini', 'Saket', 'Karol Bagh'],
            'Gujarat': ['Ahmedabad', 'Surat', 'Vadodara', 'Rajkot', 'Bhavnagar'],
            'Karnataka': ['Bengaluru', 'Mysuru', 'Mangaluru', 'Hubballi', 'Belagavi'],
            'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Thane'],
            'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Salem', 'Tiruchirappalli'],
        },
    },
    'Australia': {
        'requires_state': True,
        'states': {
            'New South Wales': ['Sydney', 'Newcastle', 'Wollongong', 'Central Coast', 'Albury'],
            'Queensland': ['Brisbane', 'Gold Coast', 'Cairns', 'Townsville', 'Toowoomba'],
            'Victoria': ['Melbourne', 'Geelong', 'Ballarat', 'Bendigo', 'Shepparton'],
            'Western Australia': ['Perth', 'Fremantle', 'Bunbury', 'Albany', 'Kalgoorlie'],
        },
    },
    'United Kingdom': {
        'requires_state': False,
        'cities': ['London', 'Manchester', 'Birmingham', 'Leeds', 'Glasgow'],
    },
    'France': {
        'requires_state': False,
        'cities': ['Paris', 'Lyon', 'Marseille', 'Toulouse', 'Nice'],
    },
    'Germany': {
        'requires_state': False,
        'cities': ['Berlin', 'Hamburg', 'Munich', 'Frankfurt', 'Cologne'],
    },
    'Japan': {
        'requires_state': False,
        'cities': ['Tokyo', 'Osaka', 'Yokohama', 'Nagoya', 'Sapporo'],
    },
    'Singapore': {
        'requires_state': False,
        'cities': ['Central Singapore', 'Tampines', 'Jurong East', 'Woodlands', 'Punggol'],
    },
}

COUNTRY_PLACEHOLDER = ('', 'Select country')
STATE_PLACEHOLDER = ('', 'Select state/province')
CITY_PLACEHOLDER = ('', 'Select city')
NOT_APPLICABLE_STATE = ('N/A', 'Not applicable')

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

class ProductUploadForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category', 'art_style', 'materials', 'dimensions', 'image', 'location', 'artist_statement', 'sustainability_rating']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Artwork title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your artwork...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price in USD'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'art_style': forms.Select(attrs={'class': 'form-select'}),
            'materials': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List the eco-friendly materials used (e.g., recycled paper, natural dyes, reclaimed wood)'}),
            'dimensions': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 24" x 36" or 60cm x 90cm'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your city or region'}),
            'artist_statement': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell the story behind your artwork and its environmental message...'}),
            'sustainability_rating': forms.Select(attrs={'class': 'form-select'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(
                choices=[(i, f"{i} {'★' * i}") for i in range(1, 6)],
                attrs={'class': 'form-select'}
            ),
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control', 
                    'rows': 4, 
                    'placeholder': 'Share your thoughts about this artwork...'
                }
            ),
        }

class CheckoutForm(forms.ModelForm):
    @classmethod
    def get_shipping_location_data(cls):
        return SHIPPING_LOCATION_DATA

    def _field_value(self, field_name):
        if self.is_bound:
            return (self.data.get(self.add_prefix(field_name), '') or '').strip()

        initial_value = self.initial.get(field_name)
        if initial_value not in (None, ''):
            return initial_value

        if self.instance and getattr(self.instance, 'pk', None):
            return getattr(self.instance, field_name, '')

        return ''

    def _country_choices(self):
        return [COUNTRY_PLACEHOLDER] + [(country, country) for country in SHIPPING_LOCATION_DATA]

    def _state_choices(self, country):
        country_data = SHIPPING_LOCATION_DATA.get(country)
        if not country_data:
            return [STATE_PLACEHOLDER]

        if country_data.get('requires_state'):
            return [STATE_PLACEHOLDER] + [(state, state) for state in country_data.get('states', {})]

        return [NOT_APPLICABLE_STATE]

    def _city_choices(self, country, state):
        country_data = SHIPPING_LOCATION_DATA.get(country)
        if not country_data:
            return [CITY_PLACEHOLDER]

        if country_data.get('requires_state'):
            state_cities = country_data.get('states', {}).get(state, [])
            return [CITY_PLACEHOLDER] + [(city, city) for city in state_cities]

        return [CITY_PLACEHOLDER] + [(city, city) for city in country_data.get('cities', [])]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        selected_country = self._field_value('shipping_country')
        selected_state = self._field_value('shipping_state')

        self.fields['shipping_country'].widget.choices = self._country_choices()
        self.fields['shipping_state'].widget.choices = self._state_choices(selected_country)
        self.fields['shipping_city'].widget.choices = self._city_choices(selected_country, selected_state)

        selected_country_data = SHIPPING_LOCATION_DATA.get(selected_country, {})
        if selected_country_data and not selected_country_data.get('requires_state') and not selected_state:
            self.initial['shipping_state'] = NOT_APPLICABLE_STATE[0]

    def clean_shipping_country(self):
        country = (self.cleaned_data.get('shipping_country') or '').strip()
        if country not in SHIPPING_LOCATION_DATA:
            raise forms.ValidationError('Select a valid country.')
        return country

    def clean(self):
        cleaned_data = super().clean()
        country = cleaned_data.get('shipping_country')
        state = cleaned_data.get('shipping_state')
        city = cleaned_data.get('shipping_city')

        if not country:
            return cleaned_data

        country_data = SHIPPING_LOCATION_DATA.get(country)
        if not country_data:
            return cleaned_data

        if country_data.get('requires_state'):
            valid_states = country_data.get('states', {})
            if not state:
                return cleaned_data
            if state not in valid_states:
                self.add_error('shipping_state', 'Select a valid state/province.')
                return cleaned_data

            valid_cities = valid_states.get(state, [])
            if not city:
                return cleaned_data
            if city not in valid_cities:
                self.add_error('shipping_city', 'Select a valid city for the selected state/province.')
        else:
            cleaned_data['shipping_state'] = NOT_APPLICABLE_STATE[0]
            valid_cities = country_data.get('cities', [])
            if not city:
                return cleaned_data
            if city not in valid_cities:
                self.add_error('shipping_city', 'Select a valid city for the selected country.')

        return cleaned_data

    class Meta:
        model = Order
        fields = [
            'shipping_address', 'shipping_city', 'shipping_state', 
            'shipping_zip_code', 'shipping_country', 'shipping_phone',
            'payment_method', 'notes'
        ]
        widgets = {
            'shipping_address': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Street address, apartment, suite, etc.'
            }),
            'shipping_city': forms.Select(attrs={
                'class': 'form-select checkout-location-select'
            }),
            'shipping_state': forms.Select(attrs={
                'class': 'form-select checkout-location-select'
            }),
            'shipping_zip_code': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'ZIP/Postal code'
            }),
            'shipping_country': forms.Select(attrs={
                'class': 'form-select checkout-location-select'
            }),
            'shipping_phone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Phone number'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-select'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Special instructions or notes (optional)'
            }),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'profile_picture', 'phone', 'social_link']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell us about yourself...'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your city or region'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number (optional)'}),
            'social_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Social profile link (optional)'}),
        }

# Additional forms to meet 5-member team requirements (10 forms total)

class ContactForm(forms.Form):
    """General contact form for customer inquiries"""
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email address'})
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your message'})
    )

class UserFeedbackForm(forms.Form):
    """User feedback form for website improvements"""
    FEEDBACK_TYPE_CHOICES = [
        ('bug', 'Bug Report'),
        ('feature', 'Feature Request'),
        ('improvement', 'Improvement Suggestion'),
        ('compliment', 'Compliment'),
        ('complaint', 'Complaint'),
        ('other', 'Other'),
    ]
    
    RATING_CHOICES = [
        (5, '5 - Excellent'),
        (4, '4 - Good'),
        (3, '3 - Average'),
        (2, '2 - Poor'),
        (1, '1 - Very Poor'),
    ]
    
    feedback_type = forms.ChoiceField(
        choices=FEEDBACK_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief subject line'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Tell us your feedback in detail...'})
    )
    overall_rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="How would you rate your overall experience with our platform?"
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email (optional for follow-up)'})
    )
    allow_contact = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text="Allow us to contact you about this feedback"
    )

class ShippingUpdateForm(forms.Form):
    """Form to update shipping address for existing orders"""
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Street address'})
    )
    shipping_city = forms.CharField(
        max_length=100,
        widget=forms.Select(attrs={'class': 'form-select checkout-location-select'})
    )
    shipping_state = forms.CharField(
        max_length=100,
        widget=forms.Select(attrs={'class': 'form-select checkout-location-select'})
    )
    shipping_zip_code = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ZIP/Postal code'})
    )
    shipping_country = forms.CharField(
        max_length=100,
        widget=forms.Select(attrs={'class': 'form-select checkout-location-select'})
    )

    def _field_value(self, field_name):
        if self.is_bound:
            return (self.data.get(self.add_prefix(field_name), '') or '').strip()

        initial_value = self.initial.get(field_name)
        if initial_value not in (None, ''):
            return initial_value

        return ''

    def _country_choices(self):
        return [COUNTRY_PLACEHOLDER] + [(country, country) for country in SHIPPING_LOCATION_DATA]

    def _state_choices(self, country):
        country_data = SHIPPING_LOCATION_DATA.get(country)
        if not country_data:
            return [STATE_PLACEHOLDER]

        if country_data.get('requires_state'):
            return [STATE_PLACEHOLDER] + [(state, state) for state in country_data.get('states', {})]

        return [NOT_APPLICABLE_STATE]

    def _city_choices(self, country, state):
        country_data = SHIPPING_LOCATION_DATA.get(country)
        if not country_data:
            return [CITY_PLACEHOLDER]

        if country_data.get('requires_state'):
            state_cities = country_data.get('states', {}).get(state, [])
            return [CITY_PLACEHOLDER] + [(city, city) for city in state_cities]

        return [CITY_PLACEHOLDER] + [(city, city) for city in country_data.get('cities', [])]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        selected_country = self._field_value('shipping_country')
        selected_state = self._field_value('shipping_state')

        self.fields['shipping_country'].widget.choices = self._country_choices()
        self.fields['shipping_state'].widget.choices = self._state_choices(selected_country)
        self.fields['shipping_city'].widget.choices = self._city_choices(selected_country, selected_state)

        selected_country_data = SHIPPING_LOCATION_DATA.get(selected_country, {})
        if selected_country_data and not selected_country_data.get('requires_state') and not selected_state:
            self.initial['shipping_state'] = NOT_APPLICABLE_STATE[0]

    def clean_shipping_country(self):
        country = (self.cleaned_data.get('shipping_country') or '').strip()
        if country not in SHIPPING_LOCATION_DATA:
            raise forms.ValidationError('Select a valid country.')
        return country

    def clean(self):
        cleaned_data = super().clean()
        country = cleaned_data.get('shipping_country')
        state = cleaned_data.get('shipping_state')
        city = cleaned_data.get('shipping_city')

        if not country:
            return cleaned_data

        country_data = SHIPPING_LOCATION_DATA.get(country)
        if not country_data:
            return cleaned_data

        if country_data.get('requires_state'):
            valid_states = country_data.get('states', {})
            if not state:
                return cleaned_data
            if state not in valid_states:
                self.add_error('shipping_state', 'Select a valid state/province.')
                return cleaned_data

            valid_cities = valid_states.get(state, [])
            if not city:
                return cleaned_data
            if city not in valid_cities:
                self.add_error('shipping_city', 'Select a valid city for the selected state/province.')
        else:
            cleaned_data['shipping_state'] = NOT_APPLICABLE_STATE[0]
            valid_cities = country_data.get('cities', [])
            if not city:
                return cleaned_data
            if city not in valid_cities:
                self.add_error('shipping_city', 'Select a valid city for the selected country.')

        return cleaned_data

class ArtistApplicationForm(forms.Form):
    """Form for artists to apply for verification"""
    full_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'})
    )
    artist_statement = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Tell us about your artistic journey and eco-friendly practices'})
    )
    portfolio_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Link to your portfolio'})
    )
    years_of_experience = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Years of artistic experience'})
    )
    specialization = forms.ChoiceField(
        choices=Product.CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    certifications = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List any relevant certifications or awards'})
    )

class NewsletterSubscriptionForm(forms.Form):
    """Newsletter subscription form"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'})
    )
    interests = forms.MultipleChoiceField(
        choices=Product.CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )
    frequency = forms.ChoiceField(
        choices=[
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('quarterly', 'Quarterly')
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    ) 
