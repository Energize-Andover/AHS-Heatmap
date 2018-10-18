import datetime
import time
from bacnet_gateway_requests import *
from PyPDF2 import PdfFileReader
from FileHelpers import *

pdf_path = None
svg_path = None
png_path = None
coords_df = None
media_box = None
svg_width = None
svg_height = None
HOSTNAME = None
PORT = None
DATA_PATH = None
data = None

BLUE_VALUE = (60, 600)
GREEN_VALUE = (70, 800)
RED_VALUE = (80, 1000)

GRADIENTS = generate_gradients(BLUE_VALUE, GREEN_VALUE, RED_VALUE)


def init(hostname, port, data_path):
    global svg_width, svg_height, media_box, pdf_path, svg_path, png_path, coords_df, HOSTNAME, PORT, DATA_PATH

    pdf_path = os.path.join('static', 'pdf', 'Andover HS level 3.pdf')
    svg_path = os.path.join('static', 'svg', 'Andover HS level 3.svg')
    png_path = os.path.join('static', 'png', 'Andover HS level 3.png')

    coords_df = get_text_and_coordinates(pdf_path)

    svg_to_pdf(svg_path, pdf_path)

    # Gets PDF size in pts (1pt = 1/72 in) [0, 0, width, height]
    media_box = PdfFileReader(open(pdf_path, 'rb')).getPage(0).mediaBox

    svg_to_png(svg_path, png_path, 72)

    HOSTNAME = hostname
    PORT = port

    DATA_PATH = data_path if data_path != 'AHS' else os.path.join('data', 'csv', 'ahs_air.csv')

    return 'Ok!'


def get_air_value_df(hostname, port, selected_room):
    df_dictionary = {
        'Date / Time': [],
        'Room': [],
        'Temperature': [],
        'Temperature Units': [],
        'CO2 Level': [],
        'CO2 Units': []
    }

    # Read spreadsheet into a DataFrame.
    # Each row contains the following:
    #   - Location
    #   - Instance ID of CO2 sensor
    #   - Instance ID of temperature sensor
    df = pd.read_csv(DATA_PATH, na_filter=False, comment='#')

    chosen_room = df['Label'] == selected_room
    filtered_room = df[chosen_room]

    for row_index, row in filtered_room.iterrows():
        # Retrieve data
        temp_value, temp_units = get_value_and_units(row['Facility'], row['Temperature'], hostname,
                                                     port)
        co2_value, co2_units = get_value_and_units(row['Facility'], row['CO2'], hostname, port)

        # Prepare to print
        temp_value = round(int(temp_value)) if temp_value else ''
        temp_units = temp_units.replace('deg ', '°') if temp_units else ''
        co2_value = round(int(co2_value)) if co2_value else ''
        co2_units = co2_units if co2_units else ''

        # Update dictionary
        df_dictionary['Date / Time'].append(datetime.datetime.now().strftime("%m/%d/%Y %H:%M"))
        df_dictionary['Room'].append(row['Label'])
        df_dictionary['Temperature'].append(temp_value)
        df_dictionary['Temperature Units'].append(temp_units)
        df_dictionary['CO2 Level'].append(co2_value)
        df_dictionary['CO2 Units'].append(co2_units)

        break

    return pd.DataFrame.from_dict(df_dictionary)


def get_all_room_data(selected_rooms, floor):
    room_data = None

    for row_index, row in selected_rooms.iterrows():
        if row['Label'] in coords_df['text'].unique() or row['Label'] in [str(floor) + text for text in
                                                                          coords_df['text'].unique()]:
            if room_data is None:
                room_data = get_air_value_df(HOSTNAME, PORT, row['Label'])
            else:
                room_data = room_data.append(get_air_value_df(HOSTNAME, PORT, row['Label']), ignore_index=True)

    return room_data


def update_with_data(temp_data):
    global data
    data = temp_data

    return 'Ok!' if data is not None else 'Error!'


def get_color_index_from_measure(measure, c02):
    if measure <= BLUE_VALUE[c02]:
        return 0
    elif measure >= RED_VALUE[c02]:
        return len(GRADIENTS[c02]) - 1
    else:
        return (RED_VALUE[c02] - BLUE_VALUE[c02]) - (RED_VALUE[c02] - measure)


def fill_chosen_room(room, measure, units):
    while DATA_PATH is None:
        time.sleep(1)
        continue

    selected_row = coords_df.loc[coords_df['text'] == str(room)]

    if not selected_row.empty:
        x = int(round(selected_row['x0']))
        y = int(round(selected_row['y0']))

        color = GRADIENTS[0][get_color_index_from_measure(measure, 0)].rgb
        color = list(tuple([int(round(255 * x)) for x in color]))
        color.append(200)
        color = tuple(color)

        flood_fill(png_path, (x, y), color)

        return True

    return False
