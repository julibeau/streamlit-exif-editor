# Exercice      : 4.2
# Cours         : L1 Outils informatiques collaboratifs, DN22ET01
# Auteur        : Julian Beaubatie
# Fichier       : exif_editor.py
# Description   : Application Streamlit permettant de lire, éditer et sauvegarder
#                 les métadonnées EXIF d'une image (EXchangeable Image File Format).
# Version       : 1.0
# Date          : 18-07-2025
import streamlit as st
import pandas as pd
import numpy as np
from exif import Image
import datetime
from datetime import datetime

# on ouvre l'image en binaire pour récupérer ses métadonnées EXIF
with open('IMG_7224.JPEG', 'rb') as image_file:
    my_image = Image(image_file)

# titre de l'application
st.title('EXIF Editor')

# affiche l’image dans la page streamlit
st.image("IMG_7224.JPEG", caption=None, use_column_width=None)

# création du formulaire pour modifier les données EXIF
with st.form("exif_form"):

    # nom du constructeur de l’appareil (ex: Apple, Canon…)
    manufacturer = st.text_input('Manufacturer:', getattr(my_image, 'make', ""))

    # modèle précis de l’appareil (ex: iPhone 12, Canon EOS…)
    model = st.text_input('Model:', getattr(my_image, 'model', ""))

    # toutes les orientations possibles
    orientations = ['Top-Left', 'Top-Right', 'Bottom-Left', 'Bottom-Right', 'Left-Top', 'Right-Top', 'Left-Bottom', 'Right-Bottom']
    
    # correspondance entre les codes EXIF et leur signification
    orientation_map = {
        1: 'Top-Left',
        2: 'Top-Right',
        3: 'Bottom-Right',
        4: 'Bottom-Left',
        5: 'Left-Top',
        6: 'Right-Top',
        7: 'Left-Bottom',
        8: 'Right-Bottom'
    }
    # récupère l’orientation actuelle de la photo (par défaut top-left si absent)
    current_orientation = orientation_map.get(getattr(my_image, 'orientation', 1), orientations[0])
    # trouve la position dans la liste pour pré-remplir le menu
    orientation_default_index = orientations.index(current_orientation)
    # champ de sélection dans le formulaire
    orientation = st.selectbox('Orientation:', orientations, index=orientation_default_index)
    
    # résolution horizontale en dpi (par défaut 72)
    x_resolution = st.number_input('X-resolution:', getattr(my_image, 'x_resolution', 72))
    # résolution verticale en dpi (par défaut 72)
    y_resolution = st.number_input('Y-resolution:', getattr(my_image, 'y_resolution', 72))

    # logiciel utilisé pour traiter l’image
    software = st.text_input('Logiciel:', getattr(my_image, 'software', ""))
    
    # récupération de la date/heure d’origine (format EXIF classique)
    try:
        full_datetime = datetime.strptime(getattr(my_image, 'datetime', "2000:01:01 00:00:00"), "%Y:%m:%d %H:%M:%S")
    except ValueError:
        # si la valeur est invalide → on met une date fictive
        full_datetime = datetime(2000, 1, 1, 0, 0, 0)
    
    # deux colonnes pour séparer date et heure
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Date:", full_datetime.date())
    with col2:
        time = st.time_input("Heure:", full_datetime.time())

    # unités possibles pour la résolution
    units = ["None", "Inch", "Centimeter"]
    unit_map = {1: "None", 2: "Inch", 3: "Centimeter"}
    # récupère l’unité actuelle
    current_unit = unit_map.get(getattr(my_image, 'resolution_unit', 1), units[0])
    # index pour pré-remplir
    unit_default_index = units.index(current_unit)
    # champ de sélection de l’unité
    resolution_unit = st.selectbox('Resolution unit:', units, index=unit_default_index)

    # vitesse d’exposition -> float avec 8 décimales
    exposure_time = st.number_input("Temps d'exposition:", getattr(my_image, 'exposure_time', 0.0), format="%.f")
    
    # même logique pour datetime_original
    try:
        full_datetime_original = datetime.strptime(getattr(my_image, 'datetime_original', "2000:01:01 00:00:00"), "%Y:%m:%d %H:%M:%S")
    except ValueError:
        full_datetime_original = datetime(2000, 1, 1, 0, 0, 0)
    
    col1, col2 = st.columns(2)
    with col1:
        date_original = st.date_input("Date (originale):", full_datetime_original.date())
    with col2:
        time_original = st.time_input("Heure (originale):", full_datetime_original.time())
        
    # idem pour datetime_digitized
    try:
        full_datetime_digitized = datetime.strptime(getattr(my_image, 'datetime_digitized', "2000:01:01 00:00:00"), "%Y:%m:%d %H:%M:%S")
    except ValueError:
        full_datetime_digitized = datetime(2000, 1, 1, 0, 0, 0)
    
    col1, col2 = st.columns(2)
    with col1:    
        date_digitized = st.date_input("Date (numérisée):", full_datetime_digitized.date(), key="date_digitized")
    with col2:
        time_digitized = st.time_input("Heure (numérisée):", full_datetime_digitized.time(), key="time_digitized")

    # champs pour les offsets (décalage horaire)
    offset = st.text_input("Offset:", getattr(my_image, 'offset_time', ""))
    offset_original = st.text_input("Offset (originale):", getattr(my_image, 'offset_time_original', ""))
    offset_digitalized = st.text_input("Offset (digitilazed):", getattr(my_image, 'offset_time_digitized', ""))

    # latitude GPS au format (degrés, minutes, secondes)
    gps_lat = getattr(my_image, 'gps_latitude', (0, 0, 0))
    # référence N ou S
    gps_lat_ref = getattr(my_image, 'gps_latitude_ref', 'N')
    # longitude GPS
    gps_lon = getattr(my_image, 'gps_longitude', (0, 0, 0))
    # référence E ou W
    gps_lon_ref = getattr(my_image, 'gps_longitude_ref', 'E')

    # conversion en float (degrés décimaux, utile pour une carte)
    gps_latitude = (gps_lat[0] + gps_lat[1]/60 + gps_lat[2]/3600) * (-1 if gps_lat_ref == 'S' else 1)
    gps_longitude = (gps_lon[0] + gps_lon[1]/60 + gps_lon[2]/3600) * (-1 if gps_lon_ref == 'W' else 1)

    # ouverture de l’objectif (nombre f/)
    f_number = st.number_input('Ouverture (F-Number):', float(getattr(my_image, 'f_number', 0.0)))

    # sensibilité ISO
    iso_speed = st.text_input('ISO:', getattr(my_image, 'photographic_sensitivity', ""))

    # modes possibles du flash
    flashs = ['Auto', 'On', 'Off']
    # correspondance code/texte
    mode_map = {2: "Auto", 1: "On", 0: "Off"}
    # récupère la valeur actuelle
    current_flash = mode_map.get(getattr(getattr(my_image, 'flash', None), 'flash_mode', 1))
    # index pour pré-remplir
    flash_default_index = flashs.index(current_flash)    
    # champ de sélection du flash
    flash = st.selectbox("Flash:", flashs, index=flash_default_index)

    # bouton de validation du formulaire
    submit = st.form_submit_button('Submit the EXIF')


if submit:
    # applique toutes les valeurs modifiées dans l’objet EXIF
    my_image.make = manufacturer
    my_image.model = model
    my_image.orientation = {v: k for k, v in orientation_map.items()}[orientation]
    my_image.x_resolution = x_resolution
    my_image.y_resolution = y_resolution
    my_image.software = software
    my_image.datetime = f"{date.strftime('%Y:%m:%d')} {time.strftime('%H:%M:%S')}"
    my_image.resolution_unit = list(unit_map.keys())[list(unit_map.values()).index(resolution_unit)]
    my_image.exposure_time = exposure_time
    my_image.datetime_original = f"{date_original.strftime('%Y:%m:%d')} {time_original.strftime('%H:%M:%S')}"
    my_image.datetime_digitized = f"{date_digitized.strftime('%Y:%m:%d')} {time_digitized.strftime('%H:%M:%S')}"
    my_image.offset_time = offset
    my_image.offset_time_original = offset_original
    my_image.offset_time_digitized = offset_digitalized
    my_image.gps_latitude = gps_lat
    my_image.gps_latitude_ref = gps_lat_ref
    my_image.gps_longitude = gps_lon
    my_image.gps_longitude_ref = gps_lon_ref
    my_image.f_number = f_number
    my_image.photographic_sensitivity = iso_speed
    my_image.flash = {v: k for k, v in mode_map.items()}[flash]

    # bouton pour télécharger la nouvelle image modifiée
    st.download_button(
        label="Télécharger l'image modifiée",
        data=my_image.get_file(),
        file_name="modified_image.jpg",
        mime="image/jpeg"
    )

