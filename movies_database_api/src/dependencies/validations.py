from fastapi.exceptions import HTTPException


def validate_country_name(country: str) -> str:
    country = country.lower().title()
    countries = ['Argentina', 'Australia', 'Austria',
                 'Bangladesh', 'Bolivia', 'Brazil',
                 'Canada', 'Chile', 'Ecuador',
                 'Egypt', 'France', 'Germany',
                 'Greece', 'Hungary', 'India',
                 'Indonesia', 'Ireland', 'Israel',
                 'Italy', 'Japan', 'Kuwait',
                 'Lebanon', 'Malaysia', 'Mexico',
                 'Morocco', 'Netherlands', 'New Zealand',
                 'Nigeria', 'Oman', 'Pakistan',
                 'Panama', 'Paraguay', 'Peru',
                 'Poland', 'Portugal', 'Puerto Rico',
                 'Russia', 'Saudi Arabia', 'South Africa',
                 'South Korea', 'Spain', 'Sweden',
                 'Switzerland', 'Turkey', 'United Arab Emirates',
                 'United Kingdom', 'United States', 'Uruguay',
                 'Venezuela', 'Zimbabwe']

    if country not in countries:
        raise HTTPException(status_code=404, detail="Country not found")
    return country


def validate_genre(genre: str) -> str:
    genre = genre.lower()
    available_genre = [
        'animation', 'comedy', 'family',
        'adventure', 'fantasy', 'romance',
        'drama', 'action', 'crime',
         'thriller', 'horror', 'history',
        'science fiction', 'mystery',
        'war', 'foreign', 'music',
        'documentary', 'western', 'tv movie'
    ]
    if genre not in available_genre:
        raise HTTPException(status=404, detail="Genre not found")
    return genre


def validate_language(language: str) -> str:
    language = language.lower().title()
    available_languages = [
                           'Georgian', 'Tamil', 'Slovak',
                           'Tibetan', 'Uzbek', 'Dutch',
                           'Tajik', 'Javanese', 'Samoan',
                           'Spanish', 'Arabic', 'Pashto',
                           'Kurdish', 'French', 'Bangla',
                           'Ukrainian', 'Thai', 'Kannada',
                           'Bambara', 'Kazakh', 'Czech',
                           'Punjabi', 'Amharic', 'Korean',
                           'Polish', 'Russian', 'Latvian',
                           'Malay', 'Persian', 'Croatian',
                           'Chinese', 'Mongolian', 'Esperanto',
                           'Norwegian', 'Indonesian', 'Malayalam',
                           'Latin', 'Norwegian Bokmål', 'Kyrgyz',
                           'Serbo-Croatian', 'Wolof', 'Nauru',
                           'English', 'Danish', 'Bulgarian',
                           'Greek', 'Aymara', 'Luxembourgish',
                           'Turkish', 'Urdu', 'Tagalog',
                           'Albanian', 'Bosnian', 'Japanese',
                           'Slovenian', 'Maltese', 'Armenian',
                           'Galician', 'Hebrew', 'Western Frisian',
                           'Hungarian', 'Telugu', 'Basque',
                           'Abkhazian', 'Catalan', 'Icelandic',
                           'Marathi', 'Afrikaans', 'German',
                           'Italian', 'Swedish', 'Kinyarwanda',
                           'Finnish', 'Vietnamese', 'Sinhala',
                           'Portuguese', 'Hindi', 'Lithuanian',
                           'Romanian', 'Zulu', 'Quechua',
                           'Inuktitut', 'Serbian', 'Lao', 'Welsh',
                           'Nepali', 'Estonian', 'Macedonian'
                           ]
    print(language)
    if language not in available_languages:
        raise HTTPException(status_code=404, detail="Language not found")
    return language
