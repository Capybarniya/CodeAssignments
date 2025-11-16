from django.shortcuts import render

import requests

def get_starship_data(starship_id):

    response = requests.get(f"https://swapi.dev/api/starships/{starship_id}/")

    if response.status_code == 200: return response.json()
    return None

def starship_card(request, starship_id):

    starship_data = get_starship_data(starship_id)
    
    context = {
        'starship': starship_data,
    }
    
    return render(request, 'ships/starship_card.html', context)