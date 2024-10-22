import tkinter as tk
import requests
import json
from datetime import date
import string

today = date.today().strftime("%d.%m.%Y")
todays_day = int(today[:2])

url_departure = "https://rest.api.hamburg-airport.de/v2/flights/departures"
url_arrivals = "https://rest.api.hamburg-airport.de/v2/flights/arrivals"

api_key_input = input("Insert API key: ")

headers = {
    'Cache-Control': 'no-cache',
    'Ocp-Apim-Subscription-Key': api_key_input,
}

response_arrivals = requests.get(url_arrivals, headers=headers)
response_arrivals.raise_for_status()
data_arrivals = response_arrivals.json()
pretty_data_arrivals = json.dumps(data_arrivals, indent=4)
# print(pretty_data_arrivals)

response_departures = requests.get(url_departure, headers=headers)
response_departures.raise_for_status()
data_departures = response_departures.json()
pretty_data_departure = json.dumps(data_departures, indent=4)
# print(pretty_data_departure)


def clear_entry(event):
    search_entry.delete(0, tk.END)


def search(data):
    global logo_image
    dep_arr_str = ""
    dep_origin_str = ""
    listbox.delete(0, tk.END)

    user_input = search_entry.get().lower()

    is_departure = False
    for key in data[1]:
        if key == "plannedDepartureTime":
            dep_arr_str = "Departure"
            dep_origin_str = "destination"
            logo_dep = tk.PhotoImage(file="airport_logo_departures.png")
            canvas.itemconfig(logo_image, image=logo_dep)
            canvas.image = logo_dep
            is_departure = True
            break
        else:
            dep_arr_str = "Arrival"
            dep_origin_str = "origin"
            logo_arr = tk.PhotoImage(file="airport_logo_arrivals.png")
            canvas.itemconfig(logo_image, image=logo_arr)
            canvas.image = logo_arr
            is_departure = False

    print(f"is_departure: {is_departure}")

    for index in range(len(data)):

        
        day = data[index][f"planned{dep_arr_str}Time"].split("T")[0]
        pretty_date = f"{day[8:]}.{day[5:7]}.{day[:4]}"
        print(f"{pretty_date}")
        short_date = pretty_date[:6]
        time = data[index][f"planned{dep_arr_str}Time"].split("T")[1].split("+")[0][:5]
        print(f"time: {time}")
        airline_name = data[index]["airlineName"].lower()
        print(f"airline: {airline_name}")

        if airline_name == "lufthansa (deutsche lufthansa ag)":
            airline_name = "lufthansa"
        if airline_name == "hsv airways":
            continue

        iata_code = data[index][f"{dep_origin_str}Airport3LCode"].lower()
        print(f"iata_code: {iata_code}")
        airport_name = data[index][f"{dep_origin_str}AirportLongName"].lower()
        print(f"airport_name: {airport_name}")
        cancelled = data[index]["cancelled"]
        print(f"cancelled: {cancelled}")
        terminal = data[index][f"{dep_arr_str.lower()}Terminal"]
        print(f"Terminal: {terminal}")

        flight_number = ""
        flight_number_data = data[index]["flightnumber"].replace(" ", "")

        for letter in flight_number_data:
            if letter in string.ascii_letters:
                letter = letter.lower()
            flight_number += letter

        print(f"flight_number: {flight_number}")

        if cancelled:
            cancelled = "CANCELLED"
            listbox.config(fg="red")
        else:
            cancelled = ""
            listbox.config(fg="black")

        if int(day[8:]) < todays_day:
            pass

        else:
            try:
                airline_parts = airline_name.split(" ")
                airport_parts = airport_name.split("/")
                print(f"airport_parts: {airport_parts}")

                search_criteria = [
                    iata_code,
                    airport_name,
                    airline_name,
                    flight_number,
                    pretty_date,
                    day,
                    short_date,
                    time,
                    *airline_parts,
                    airport_parts[0],
                    airport_parts[1],
                ]

                if user_input in search_criteria:

                        listbox.insert(tk.END, f"{airline_name.title()}    {flight_number_data}    "
                                               f"{airport_name.title()} ({iata_code.upper()})    {pretty_date}    "
                                               f"{time}    T: {terminal}    {cancelled}")

            except IndexError:
                search_criteria = [
                    iata_code,
                    airport_name,
                    airline_name,
                    flight_number,
                    pretty_date,
                    day,
                    short_date,
                    time,
                    ]

                if user_input in search_criteria:
                    listbox.insert(tk.END, f"{airline_name.title()}    {flight_number_data}    "
                                           f"{airport_name.title()} ({iata_code.upper()})    {pretty_date}    "
                                           f"{time}    {cancelled}    T: {terminal}")


# GUI

window = tk.Tk()
window.title("Departure Hamburg Airport")
# window.bind("<Return>", lambda event: on_enter(event))

listbox = tk.Listbox(window, highlightthickness=0, width=60, height=10, font=("calibri", 16))
listbox.grid(row=3, column=0, columnspan=6, sticky='nsew', padx=20, pady=20)

canvas = tk.Canvas(width=600, height=200, highlightthickness=0)
logo = tk.PhotoImage(file="airport_logo.png")
logo_image = canvas.create_image(300, 100, image=logo)
canvas.grid(row=0, column=0, columnspan=5, pady=20, sticky="w")

# Entries

search_entry = tk.Entry(font=("calibri", 24), width=30)
search_entry.grid(row=1, column=0, columnspan=6, padx=30, sticky="w")
search_entry.bind("<Button-1>", lambda event: clear_entry(event))
search_entry.insert(0, "Search...")

# Buttons

departure_button = tk.Button(text="Departures", command=lambda: search(data_departures), font=("calibri", 16), width=25)
departure_button.grid(row=2, column=0, pady=20, padx=20, sticky="w")

arrivals_button = tk.Button(text="Arrivals", command=lambda: search(data_arrivals), font=("calibri", 16), width=25)
arrivals_button.grid(row=2, column=2, pady=20, padx=20, sticky="w")


window.mainloop()
