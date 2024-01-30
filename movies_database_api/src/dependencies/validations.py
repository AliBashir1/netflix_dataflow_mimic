from fastapi.exceptions import HTTPException


def validate_country_name(country: str) -> str:
    country = country.lower().title()
    countries = ['Argentina', 'Australia', 'Austria', 'Bangladesh',
                 'Bolivia', 'Brazil', 'Canada', 'Chile', 'Ecuador',
                 'Egypt', 'France', 'Germany', 'Greece', 'Hungary',
                 'India', 'Indonesia', 'Ireland', 'Israel', 'Italy',
                 'Japan', 'Kuwait', 'Lebanon', 'Malaysia', 'Mexico',
                 'Morocco', 'Netherlands', 'New zealand', 'Nigeria',
                 'Oman', 'Pakistan', 'Panama', 'Paraguay', 'Peru',
                 'Poland', 'Portugal', 'Puerto rico', 'Russia',
                 'Saudi arabia', 'South africa', 'South korea',
                 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'United Arab Emirates',
                 'United Kingdom', 'United States', 'Uruguay', 'Venezuela', 'Zimbabwe']

    if country not in countries:
        raise HTTPException(status_code=404, detail="Country not found")
    return country

def validate_genre(genre:str) -> str:
    genre = genre.lower()
    available_genre = ['animation', 'comedy', 'family', 'adventure', 'fantasy', 'romance', 'drama', 'action', 'crime',
                       'thriller', 'horror', 'history', 'science fiction', 'mystery', 'war', 'foreign', 'music',
                       'documentary', 'western', 'tv movie']
    if genre not in available_genre:
        raise HTTPException(status=404, detail="Genre not found")
    return genre
