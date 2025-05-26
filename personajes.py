import random

def mostrar_info_personaje(emocion_detectada):
    # Mapeo de emociones del modelo a las emociones de los personajes
    mapeo_emociones = {
        "Enojo": "enojo",
        "Disgusto": "asco",
        "Miedo": "miedo",
        "Feliz": "alegria",
        "Triste": "tristeza",
        "Sorpresa": "sorpresa",
        "Neutral": "neutral",
    }

    emocion = mapeo_emociones.get(emocion_detectada, emocion_detectada).lower()

    personajes_cine = {
        "Fantasía": [
            {
                "nombre": "Willy Wonka",
                "pelicula": "Willy Wonka & the Chocolate Factory",
                "año": 1971,
                "genero_visible": "Fantasía musical",
                "emocion_asociada": "alegria",
                "imagen": "personajes_img/willy_wonka.png"
            },
            {
                "nombre": "Atreyu",
                "pelicula": "The NeverEnding Story / La historia interminable",
                "año": 1984,
                "genero_visible": "Fantasía épica",
                "emocion_asociada": "alegria",
                "imagen": "personajes_img/atreyu.jpg"
            },
            {
                "nombre": "Alan Parrish",
                "pelicula": "Jumanji",
                "año": 1995,
                "genero_visible": "Fantasía-aventura",
                "emocion_asociada": "alegria",
                "imagen": "personajes_img/alan_parrish.jpg"
            },
            {
                "nombre": "Dorothy Gale",
                "pelicula": "The Wizard of Oz / El mago de Oz",
                "año": 1939,
                "genero_visible": "Fantasía clásica",
                "emocion_asociada": "alegria",
                "imagen": "personajes_img/dorothy_gale.jpg"
            },
            {
               "nombre": "Matilda Wormwood",
               "pelicula": "Matilda",
               "año": 1996,
               "genero_visible": "Fantasía infantil",
               "emocion_asociada": "alegria",
               "imagen": "personajes_img/matilda.jpg"
            }
        ],
        "Drama": [
            {
                "nombre": "Pink",
                "pelicula": "The Wall",
                "año": 1982,
                "genero_visible": "Drama psicológico musical",
                "emocion_asociada": "tristeza",
                "imagen": "personajes_img/pink.jpg"
            },
            {
                "nombre": "Forrest Gump",
                "pelicula": "Forrest Gump",
                "año": 1994,
                "genero_visible": "Drama histórico",
                "emocion_asociada": "tristeza",
                "imagen": "personajes_img/forrest.png"
            },
            {
                "nombre": "Erik (El Fantasma)",
                "pelicula": "The Phantom of the Opera",
                "año": 1943,
                "genero_visible": "Drama romántico gótico",
                "emocion_asociada": "tristeza",
                "imagen": "personajes_img/erik.jpg"
            },
            {
                "nombre": "Truman Burbank",
                "pelicula": "The Truman Show",
                "año": 1998,
                "genero_visible": "Drama satírico",
                "emocion_asociada": "tristeza",
                "imagen": "personajes_img/truman.jpg"
            },
            {
                "nombre": "Harold Chasen",
                "pelicula": "Harold and Maude",
                "año": 1971,
                "genero_visible": "Drama romántico excéntrico",
                "emocion_asociada": "tristeza",
                "imagen": "personajes_img/harold.jpg"
            }
        ],
        "Crimen": [
            {
                "nombre": "Travis Bickle",
                "pelicula": "Taxi Driver",
                "año": 1976,
                "genero_visible": "Crimen psicológico",
                "emocion_asociada": "asco",
                "imagen": "personajes_img/travis.jpg"
            },
            {
                "nombre": "Patrick Bateman",
                "pelicula": "American Psycho",
                "año": 2000,
                "genero_visible": "Crimen psicológico",
                "emocion_asociada": "asco",
                "imagen": "personajes_img/patrick.png"
            },
            {
                "nombre": "Alex DeLarge",
                "pelicula": "A Clockwork Orange / La naranja mecánica",
                "año": 1971,
                "genero_visible": "Crimen distópico",
                "emocion_asociada": "asco",
                "imagen": "personajes_img/alex.jpg"
            },
            {
                "nombre": "Tony Montana",
                "pelicula": "Scarface",
                "año": 1983,
                "genero_visible": "Crimen mafioso",
                "emocion_asociada": "asco",
                "imagen": "personajes_img/tony.jpg"
            },
            {
                "nombre": "El Narrador",
                "pelicula": "Fight Club",
                "año": 1999,
                "genero_visible": "Crimen psicológico",
                "emocion_asociada": "asco",
                "imagen": "personajes_img/narrador.jpg"
            }
        ],
        "Aventura": [
            {
                "nombre": "Sarah Williams",
                "pelicula": "Labyrinth / Dentro del Laberinto",
                "año": 1986,
                "genero_visible": "Fantasía-aventura",
                "emocion_asociada": "sorpresa",
                "imagen": "personajes_img/sarah.jpg"
            },
            {
                "nombre": "Bastian Balthazar Bux",
                "pelicula": "The NeverEnding Story / La historia interminable",
                "año": 1984,
                "genero_visible": "Fantasía-aventura",
                "emocion_asociada": "sorpresa",
                "imagen": "personajes_img/bastian.jpg"
            },
            {
                "nombre": "Elliott",
                "pelicula": "E.T. the Extra-Terrestrial",
                "año": 1982,
                "genero_visible": "Ciencia ficción familiar",
                "emocion_asociada": "sorpresa",
                "imagen": "personajes_img/elliott.png"
            },
            {
                "nombre": "Kevin McCallister",
                "pelicula": "Home Alone / Mi pobre angelito",
                "año": 1990,
                "genero_visible": "Comedia-aventura",
                "emocion_asociada": "sorpresa",
                "imagen": "personajes_img/kevin.png"
            },
            {
                "nombre": "George McFly",
                "pelicula": "Back to the Future / Volver al futuro",
                "año": 1985,
                "genero_visible": "Ciencia ficción y aventura",
                "emocion_asociada": "sorpresa",
                "imagen": "personajes_img/george.png"
            }
        ],
        "Multigénero": [
           {
                "nombre": "Wednesday Addams",
                "pelicula": "The Addams Family",
                "año": 1991,
                "genero_visible": "Comedia oscura",
                "emocion_asociada": "neutral",
                "imagen": "personajes_img/wednesday.jpg"
           },
           {
                "nombre": "Clarice Starling",
                "pelicula": "The Silence of the Lambs",
                "año": 1991,
                "genero_visible": "Suspenso psicológico",
                "emocion_asociada": "neutral",
                "imagen": "personajes_img/clarice.jpg"
           },
           {
                "nombre": "Léon",
                "pelicula": "Léon: The Professional",
                "año": 1994,
                "genero_visible": "Drama de acción",
                "emocion_asociada": "neutral",
                "imagen": "personajes_img/leon.jpg"
           },
           {
                "nombre": "Vincent Vega",
                "pelicula": "Pulp Fiction",
                "año": 1994,
                "genero_visible": "Crimen / Comedia negra",
                "emocion_asociada": "neutral",
                "imagen": "personajes_img/vincent.jpg"
           },
           {
                "nombre": "Mia Wallace",
                "pelicula": "Pulp Fiction",
                "año": 1994,
                "genero_visible": "Crimen / Comedia negra",
                "emocion_asociada": "neutral",
                "imagen": "personajes_img/mia.jpg"
          }
       ],
        "Terror": [
            {
                "nombre": "Chucky",
                "pelicula": "Child's Play / Chucky: El muñeco diabólico",
                "año": 1988,
                "genero_visible": "Terror slasher",
                "emocion_asociada": "enojo",
                "imagen": "personajes_img/chucky.jpg"
            },
            {
                "nombre": "Christiane Génessier",
                "pelicula": "Les Yeux sans visage / Los ojos sin rostro",
                "año": 1960,
                "genero_visible": "Terror y drama",
                "emocion_asociada": "enojo",
                "imagen": "personajes_img/eyes.jpg"
            },
            {
                "nombre": "Regan MacNeil",
                "pelicula": "The Exorcist / El Exorcista",
                "año": 1973,
                "genero_visible": "Terror sobrenatural",
                "emocion_asociada": "enojo",
                "imagen": "personajes_img/regan.jpg"
            },
            {
                "nombre": "Norman Bates",
                "pelicula": "Psycho / Psicosis",
                "año": 1960,
                "genero_visible": "Terror psicológico",
                "emocion_asociada": "enojo",
                "imagen": "personajes_img/norman.png"
            },
            {
                "nombre": "Jack Torrance",
                "pelicula": "The Shining / El Resplandor",
                "año": 1980,
                "genero_visible": "Terror psicológico",
                "emocion_asociada": "enojo",
                "imagen": "personajes_img/jack.jpg"
            },
            {
                "nombre": "Nancy Thompson",
                "pelicula": "A Nightmare on Elm Street / Pesadilla en la calle Elm",
                "año": 1984,
                "genero_visible": "Terror sobrenatural",
                "emocion_asociada": "miedo",
                "imagen": "personajes_img/nancy.jpg"
            },
            {
                "nombre": "Andy Barclay",
                "pelicula": "Child's Play / Chucky: El muñeco diabólico",
                "año": 1988,
                "genero_visible": "Terror slasher",
                "emocion_asociada": "miedo",
                "imagen": "personajes_img/andy.png"
            },
            {
                "nombre": "Marion Crane",
                "pelicula": "Psycho / Psicosis",
                "año": 1960,
                "genero_visible": "Terror psicológico",
                "emocion_asociada": "miedo",
                "imagen": "personajes_img/marion.png"
            },
            {
                "nombre": "Chris MacNeil",
                "pelicula": "The Exorcist / El Exorcista",
                "año": 1973,
                "genero_visible": "Terror psicológico",
                "emocion_asociada": "miedo",
                "imagen": "personajes_img/chris.jpg"
            },
            {
                "nombre": "Danny Torrance",
                "pelicula": "The Shining / El Resplandor",
                "año": 1980,
                "genero_visible": "Terror psicológico",
                "emocion_asociada": "miedo",
                "imagen": "personajes_img/danny.jpg"
            }
        ]
    }

    personajes_filtrados = []

    for genero, personajes in personajes_cine.items():
        for p in personajes:
            if p["emocion_asociada"] == emocion:
                personajes_filtrados.append(p)

    if not personajes_filtrados:
        return None, f"No se encontró un personaje con la emoción '{emocion_detectada}'."

    personaje = random.choice(personajes_filtrados)

    texto = (
        #f"Emoción detectada: {emocion_detectada.capitalize()}\n\n"
        f"Personaje asignado: {personaje['nombre']}\n"
        f"Película: {personaje['pelicula']}\n"
        f"Año de estreno: {personaje['año']}\n"
        f"Género cinematográfico: {personaje['genero_visible']}"
    )
    return personaje["imagen"], texto
