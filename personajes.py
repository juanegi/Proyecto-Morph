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
        "Neutral": "neutral",      # Puedes asociar 'neutral' a algún grupo si lo deseas
        "Desprecio": "desprecio"   # Por si acaso
    }

    emocion = mapeo_emociones.get(emocion_detectada, emocion_detectada).lower()

    personajes_cine = {
        "Fantasía": [
            {
                "nombre": "Willy Wonka",
                "pelicula": "Willy Wonka & the Chocolate Factory",
                "año": 1971,
                "genero_visible": "Fantasía musical",
                "emocion_asociada": "alegria"
            },
            {
                "nombre": "Atreyu",
                "pelicula": "The NeverEnding Story / La historia interminable",
                "año": 1984,
                "genero_visible": "Fantasía épica",
                "emocion_asociada": "alegria"
            },
            {
                "nombre": "Alan Parrish",
                "pelicula": "Jumanji",
                "año": 1995,
                "genero_visible": "Fantasía-aventura",
                "emocion_asociada": "alegria"
            },  # <-- ESTA COMA ES NECESARIA

            {
                "nombre": "Dorothy Gale",
                "pelicula": "The Wizard of Oz / El mago de Oz",
                "año": 1939,
                "genero_visible": "Fantasía clásica",
                "emocion_asociada": "alegria"
            },

            {
               "nombre": "Matilda Wormwood",
               "pelicula": "Matilda",
               "año": 1996,
               "genero_visible": "Fantasía infantil",
               "emocion_asociada": "alegria"
            }
        ],

        "Drama": [
            {
                "nombre": "Pink",
                "pelicula": "The Wall",
                "año": 1982,
                "genero_visible": "Drama psicológico musical",
                "emocion_asociada": "tristeza"
            },
            {
                "nombre": "Forrest Gump",
                "pelicula": "Forrest Gump",
                "año": 1994,
                "genero_visible": "Drama histórico",
                "emocion_asociada": "tristeza"
            },
            {
                "nombre": "Erik (El Fantasma)",
                "pelicula": "The Phantom of the Opera",
                "año": 1943,
                "genero_visible": "Drama romántico gótico",
                "emocion_asociada": "tristeza"
            },
            {
                "nombre": "Truman Burbank",
                "pelicula": "The Truman Show",
                "año": 1998,
                "genero_visible": "Drama satírico",
                "emocion_asociada": "tristeza"
            },
            {
                "nombre": "Harold Chasen",
                "pelicula": "Harold and Maude",
                "año": 1971,
                "genero_visible": "Drama romántico excéntrico",
                "emocion_asociada": "tristeza"
            }
        ],

        "Crimen": [
            {
                "nombre": "Travis Bickle",
                "pelicula": "Taxi Driver",
                "año": 1976,
                "genero_visible": "Crimen psicológico",
                "emocion_asociada": "asco"
            },
            {
                "nombre": "Patrick Bateman",
                "pelicula": "American Psycho",
                "año": 2000,
                "genero_visible": "Crimen psicológico",
                "emocion_asociada": "asco"
            },
            {
                "nombre": "Alex DeLarge",
                "pelicula": "A Clockwork Orange / La naranja mecánica",
                "año": 1971,
                "genero_visible": "Crimen distópico",
                "emocion_asociada": "asco"
            },
            {
                "nombre": "Tony Montana",
                "pelicula": "Scarface",
                "año": 1983,
                "genero_visible": "Crimen mafioso",
                "emocion_asociada": "asco"
            },
            {
                "nombre": "El Narrador",
                "pelicula": "Fight Club",
                "año": 1999,
                "genero_visible": "Crimen psicológico",
                "emocion_asociada": "asco"
            }
        ],

        "Aventura": [
            {
                "nombre": "Sarah Williams",
                "pelicula": "Labyrinth / Dentro del Laberinto",
                "año": 1986,
                "genero_visible": "Fantasía-aventura",
                "emocion_asociada": "sorpresa"
            },
            {
                "nombre": "Bastian Balthazar Bux",
                "pelicula": "The NeverEnding Story / La historia interminable",
                "año": 1984,
                "genero_visible": "Fantasía-aventura",
                "emocion_asociada": "sorpresa"
            },
            {
                "nombre": "Elliott",
                "pelicula": "E.T. the Extra-Terrestrial",
                "año": 1982,
                "genero_visible": "Ciencia ficción familiar",
                "emocion_asociada": "sorpresa"
            },
            {
                "nombre": "Kevin McCallister",
                "pelicula": "Home Alone / Mi pobre angelito",
                "año": 1990,
                "genero_visible": "Comedia-aventura",
                "emocion_asociada": "sorpresa"
            },
            {
                "nombre": "George McFly",
                "pelicula": "Back to the Future / Volver al futuro",
                "año": 1985,
                "genero_visible": "Ciencia ficción y aventura",
                "emocion_asociada": "sorpresa"
            }
        ],

        "Bélico": [
            {
                "nombre": "Oficial alemán",
                "pelicula": "The Bunker",
                "año": 1981,
                "genero_visible": "Bélico histórico",
                "emocion_asociada": "desprecio"
            },
            {
                "nombre": "Coronel Kurtz",
                "pelicula": "Apocalypse Now",
                "año": 1979,
                "genero_visible": "Bélico psicológico",
                "emocion_asociada": "desprecio"
            },
            {
                "nombre": "Gunnery Sgt. Hartman",
                "pelicula": "Full Metal Jacket",
                "año": 1987,
                "genero_visible": "Bélico realista",
                "emocion_asociada": "desprecio"
            },
            {
                "nombre": "Sargento Barnes",
                "pelicula": "Platoon",
                "año": 1986,
                "genero_visible": "Bélico dramático",
                "emocion_asociada": "desprecio"
            }
        ],

        "Suspenso": [
            {
                "nombre": "Mrs. Danvers",
                "pelicula": "Rebecca",
                "año": 1940,
                "genero_visible": "Suspenso psicológico",
                "emocion_asociada": "desprecio"
            }
        ],

        "Terror": [
            {
                "nombre": "Chucky",
                "pelicula": "Child's Play / Chucky: El muñeco diabólico",
                "año": 1988,
                "genero_visible": "Terror slasher",
                "emocion_asociada": "enojo"
            },
            {
                "nombre": "Freddy Krueger",
                "pelicula": "A Nightmare on Elm Street / Pesadilla en la calle Elm",
                "año": 1984,
                "genero_visible": "Terror sobrenatural",
                "emocion_asociada": "enojo"
            },
            {
                "nombre": "Regan MacNeil",
                "pelicula": "The Exorcist / El Exorcista",
                "año": 1973,
                "genero_visible": "Terror sobrenatural",
                "emocion_asociada": "enojo"
            },
            {
                "nombre": "Norman Bates",
                "pelicula": "Psycho / Psicosis",
                "año": 1960,
                "genero_visible": "Terror psicológico",
                "emocion_asociada": "enojo"
            },
            {
                "nombre": "Jack Torrance",
                "pelicula": "The Shining / El Resplandor",
                "año": 1980,
                "genero_visible": "Terror psicológico",
                "emocion_asociada": "enojo"
            },
            {
                "nombre": "Nancy Thompson",
                "pelicula": "A Nightmare on Elm Street / Pesadilla en la calle Elm",
                "año": 1984,
                "genero_visible": "Terror sobrenatural",
                "emocion_asociada": "miedo"
            },
            {
                "nombre": "Andy Barclay",
                "pelicula": "Child's Play / Chucky: El muñeco diabólico",
                "año": 1988,
                "genero_visible": "Terror slasher",
                "emocion_asociada": "miedo"
            },
            {
                "nombre": "Marion Crane",
                "pelicula": "Psycho / Psicosis",
                "año": 1960,
                "genero_visible": "Terror psicológico",
                "emocion_asociada": "miedo"
            },
            {
                "nombre": "Chris MacNeil",
                "pelicula": "The Exorcist / El Exorcista",
                "año": 1973,
                "genero_visible": "Terror psicológico",
                "emocion_asociada": "miedo"
            },
            {
                "nombre": "Danny Torrance",
                "pelicula": "The Shining / El Resplandor",
                "año": 1980,
                "genero_visible": "Terror psicológico",
                "emocion_asociada": "miedo"
            }
        ]
    }

    personajes_filtrados = []

    for genero, personajes in personajes_cine.items():
        for p in personajes:
            if p["emocion_asociada"] == emocion:
                personajes_filtrados.append(p)

    if not personajes_filtrados:
        return f"No se encontró un personaje con la emoción '{emocion_detectada}'."

    personaje = random.choice(personajes_filtrados)

    texto = (
        f"Emoción detectada: {emocion_detectada.capitalize()}\n\n"
        f"Personaje asignado: {personaje['nombre']}\n"
        f"Película: {personaje['pelicula']}\n"
        f"Año de estreno: {personaje['año']}\n"
        f"Género cinematográfico: {personaje['genero_visible']}"
    )
    return texto