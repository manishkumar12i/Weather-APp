import requests
from django.shortcuts import render
from datetime import datetime

def home(request):
    # Get city from POST data or use default
    city = request.POST.get('city', '').strip()
    if not city:
        city = "Delhi"
    api_key = 'use own api'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    PARAMS = {'units': 'metric'}
    
    try:
        # Make the API request
        response = requests.get(url, params=PARAMS)
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()

            # Extract necessary information from the JSON response
            description = data['weather'][0]['description']
            icon = data['weather'][0]['icon']
            temp = data['main']['temp']
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            # Format current date
            day = datetime.today().strftime('%A, %d %B %Y')  # Day of the week, day, month, year

            # Return the rendered template with data
            return render(request, 'index.html', {
                'description': description,
                'icon': icon,
                'temp': temp,
                'day': day,
                'city': city,
                'wind_speed': wind_speed,
                'humidity': humidity
            })
        else:
            # Handle invalid city or API errors
            error_message = "City not found or API error. Please try again."
            not_found = "Enter any city."
            return render(request, 'index.html', {'error_message': error_message,'not_found':not_found})

    except requests.exceptions.RequestException as e:
        # Handle network-related errors
        error_message = f"Error occurred while fetching weather data: {str(e)}"
        return render(request, 'index.html', {'error_message': error_message})
