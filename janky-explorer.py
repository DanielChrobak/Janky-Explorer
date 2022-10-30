from threading import Thread
import pyperclip
import requests
from datetime import datetime
from datetime import date
import customtkinter as CTk
import tkinter as tk
from threading import Thread
from dataclasses import dataclass
from PIL import Image, ImageTk
from time import sleep

header = {"User-Agent":"NotABot/1.0.0"}

disabled_button = ""

api_url = "https://api.helium.io/v1"
hotspots_url = "/hotspots"
roles_url = "/roles"
witnesses_url = "/witnesses"
cursors_url = "?cursor="
name_url = "/name"
transactions_url = "/transactions"

def do_requests(ext1="", ext2="", ext3="", ext4="", ext5="", ext6=""):
    while True:
        response = requests.get(f"{api_url}{ext1}{ext2}{ext3}{ext4}{ext5}{ext6}", headers=header, timeout=999)
        print(f"{api_url}{ext1}{ext2}{ext3}{ext4}{ext5}{ext6}")
        if response.status_code in (429, 502, 503):
            print("Too Many Requests")
            sleep(2)
        if response.status_code == 200:
            return response.json()
        if response.status_code == 404:
            print("Page Not Found")

def copy_to_clipboard(thingy):
    pyperclip.copy(thingy)


today = date.today()
Date = today.strftime

Witness_Time_List = []
Beacons_Time_List = []
Rewards_Time_List = []
Receipts_List = []
Beacons_List = []
Witness_List = []
Rewards_List = []
Witness_Height_List = []
Rewards_Height_List = []
Beacons_Height_List = []
activity_part_list = []
beacon_labels = []
witness_labels = []
reward_labels = []
witnesses = []
w_beacon_labels = []

for index in range(15):
    activity_part_list.append(index)

hotspots = {}

witness_y = 310
reward_y = 310
beacon_y = 310

w_y = 250

activity_buttons_placed = False
witness_displayed = False
beacons_displayed = False
rewards_displayed = False
w_is_loading = False
extra_data_canvas_placed = False
w_is_loaded = False
general_data_labels_loaded = False

r_is_loaded = False
r_is_loading = False

b_is_loading = False
b_is_loaded = False

GUI = CTk.CTk()

GUI.geometry('1080x880')
GUI.title("Janky Explorer")

GUI.minsize(1080, 880)
GUI.maxsize(1080, 880)

frame = CTk.CTkFrame(master=GUI, width=1080, height=880, fg_color="#10182c")
frame.place(x=0, y=0)

search_box = CTk.CTkEntry(master=frame, width=205, height=40, placeholder_text="Enter Hot-Spot-Name", fg_color="white")
search_box.configure(font=('Alias'), text_color="black", justify=tk.CENTER)
search_box.place(x=765, y=10)

def search_hotspot():
    global Witness
    global Hotspot
    def get_general_hs_data():
        global hs_activity_data, hs_id, hs_city, hs_state, hs_country, hs_listening_addrs, hs_name, hs_wallet_addrs
        hs_name = search_box.get().replace(" ", "-").lower()
        loading_general_data_label = CTk.CTkLabel(master=frame, text_color="#98A1A6", width=100, height=30, text="Getting General Hotspot Data", fg_color=None)
        loading_general_data_label.place(x=900, y=850)
        generic_hs_data = do_requests(hotspots_url, name_url, "/", hs_name)
        loading_general_data_label.destroy()
        hs_listening_addrs = generic_hs_data['data'][0]['status']['listen_addrs'][0].split("/")[2]
        hs_wallet_addrs = generic_hs_data['data'][0]['owner']
        hs_country = generic_hs_data['data'][0]['geocode']['short_country']
        hs_state = generic_hs_data['data'][0]['geocode']['long_state']
        hs_city = generic_hs_data['data'][0]['geocode']['long_city']
        hs_id = generic_hs_data['data'][0]['address']
        role_data = do_requests(hotspots_url, "/", hs_id, roles_url)
        cursor_id = role_data['cursor']
        roles_page_data = do_requests(hotspots_url, "/", hs_id, roles_url, cursors_url, cursor_id)
        hs_activity_data = roles_page_data['data']
        hs_name = hs_name.replace("-", " ").title()
        load_general_data_labels()
        load_activity_data()
        create_activity_buttons()

    def load_general_data_labels():
        global general_data_frame
        global hotspot_name_label
        global general_data_labels_loaded
        global hotspot_location_label
        global hotspot_data_label
        if general_data_labels_loaded == False:
            general_data_frame = CTk.CTkFrame(width=525, height=100, fg_color="#080c1c")
            general_data_frame.place(x=70, y=50)
            hotspot_name_label = CTk.CTkLabel(width=400, height=20, fg_color="#080c1c")
            hotspot_name_label.configure(font=('Alias', 16), text=f"{hs_name}", anchor="center")
            hotspot_name_label.place(x=135, y=60)
            hotspot_data_label = CTk.CTkFrame(width=525, height=60, fg_color="white")
            hotspot_data_label.place(x=70, y=90)
            hotspot_location_label = CTk.CTkLabel(width=500, height=20, bg_color="#080c1c")
            hotspot_location_label.configure(text=f"Hotspot Location : {hs_city}, {hs_state}, {hs_country}\nWallet Address : {hs_wallet_addrs}\nHotspot ID : {hs_id}", anchor="center", text_color="black", bg_color="white")
            hotspot_location_label.place(x=80, y=95)
            general_data_labels_loaded = True


    def load_activity_data():
        global Receipts_List, Beacons_List, Witness_List, Rewards_List
        global Witness_Height_List, Beacons_Height_List, Rewards_Height_List
        global Witness_Time_List, Beacons_Time_List, Rewards_Time_List

        for Activity in hs_activity_data:
            if Activity['type'] == "poc_receipts_v2":
                Receipts_List.append(Activity)
            if Activity['type'] == "rewards_v2":
                Rewards_List.append(Activity)

        for Receipt in Receipts_List:
            if Receipt['role'] == "challengee":
                Beacons_List.append(Receipt)
            if Receipt['role'] == "witness":
                Witness_List.append(Receipt)

        for Witness in Witness_List:
            Witness_Height_List.append(Witness['height'])
            Witness_Time_List.append(str(datetime.fromtimestamp(Witness['time'])))

        for Beacon in Beacons_List:
            Beacons_Height_List.append(Beacon['height'])
            Beacons_Time_List.append(str(datetime.fromtimestamp(Beacon['time'])))

        for Reward in Rewards_List:
            Rewards_Height_List.append(Witness['height'])
            Rewards_Time_List.append(str(datetime.fromtimestamp(Reward['time'])))

    def create_activity_buttons():
        global beacons_button, witness_button, rewards_button
        global general_data_label
        global activity_buttons_placed

        general_data_label = CTk.CTkLabel(master=frame, width=500, height=200, text="Recent Hotspot Activity")
        general_data_label.configure(font=('Alias', 24), fg_color=None)
        general_data_label.place(x=80, y=100)

        witness_button = CTk.CTkButton(text="Witnesses", width=100, height=20, command=show_witnesses, fg_color="#fcc945", text_color="black")
        witness_button.place(x=120, y=250)
        beacons_button = CTk.CTkButton(text="Beacons", width=100, height=20, command=show_beacons, fg_color="#484cfc", text_color="black")
        beacons_button.place(x=280, y=250)
        rewards_button = CTk.CTkButton(text="Rewards", width=100, height=20, command=show_rewards, fg_color="#b47cf4", text_color="black")
        rewards_button.place(x=430, y=250)

        activity_buttons_placed = True

    def show_witnesses():
        global witness_displayed, witness_labels, witness_y
        check_for_activity_labels()
        for index in range(len(Witness_List)):
            if index <= 14:
                witness_part = activity_part_list[index]
                witness_label = CTk.CTkButton(master=frame, text_color="black", text=f"Witnessed on block {Witness_Height_List[index]} at {Witness_Time_List[index]}", width=315, height=10, command=lambda m=(witness_part) : which_witness(m), fg_color="#fff9a9")
                witness_labels.append(witness_label)
                witness_label.place(x=173, y=witness_y)
                witness_y = witness_y + 30
        witness_displayed = True

    def show_beacons():
        global beacon_y, beacon_labels, beacons_displayed
        check_for_activity_labels()
        for index in range(len(Beacons_List)):
            if index <= 14:
                beacon_part = activity_part_list[index]
                beacon_label = CTk.CTkButton(master=frame, text_color="black", text=f"Beaconed on block {Beacons_Height_List[index]} at {Beacons_Time_List[index]}", width=315, height=10, command=lambda m=(beacon_part) : which_beacon(m), fg_color="#4466c5")
                beacon_labels.append(beacon_label)
                beacon_label.place(x=173, y=beacon_y)
                beacon_y = beacon_y + 30
        beacons_displayed = True

    def show_rewards():
        global reward_y, reward_labels, rewards_displayed
        check_for_activity_labels()
        for index in range(len(Rewards_List)):
            if index <= 14:
                reward_part = activity_part_list[index]
                reward_label = CTk.CTkButton(master=frame, text_color="black", text=f"Rewarded on block {Rewards_Height_List[index]} at {Rewards_Time_List[index]}", width=315, height=10, command=lambda m=(reward_part) : which_reward(m), fg_color="#ccacf4")
                reward_labels.append(reward_label)
                reward_label.place(x=173, y=reward_y)
                reward_y = reward_y + 30
        rewards_displayed = True

    def check_for_activity_labels():
        global witness_y, witness_labels, witness_displayed
        global beacon_y, beacon_labels, beacons_displayed
        global reward_y, reward_labels, rewards_displayed
        if witness_displayed == True:
            for witness_label in witness_labels:
                witness_label.destroy()
            witness_labels = []
            witness_y = 310
            witness_displayed = False
        if beacons_displayed == True:
            for beacon_label in beacon_labels:
                beacon_label.destroy()
            beacon_labels = []
            beacon_y = 310
            beacons_displayed = False
        if rewards_displayed == True:
            for reward_label in reward_labels:
                reward_label.destroy()
            reward_labels = []
            reward_y = 310
            rewards_displayed = False

    def which_witness(witness_pressed):
        check_if_wbr_is_loaded()
        def get_witness_data():
            global extra_data_canvas, extra_data_canvas_placed
            global w_beacon_labels, w_is_loaded, w_y, w_is_loading, w_beaconer_label
            w_is_loading = True
            hash = Witness_List[witness_pressed]['hash']
            transaction_data = do_requests(transactions_url, "/", hash)
            transaction_beaconer_gateway = transaction_data['data']['path'][0]['receipt']['gateway']
            transaction_witnesses = transaction_data['data']['path'][0]['witnesses']
            for witness in transaction_witnesses:
                if witness['is_valid'] == True:
                    witness_object = Witness(gateway=witness['gateway'], rssi=witness['signal'], snr=round(witness['snr'], 1), validity="Is Valid")
                    witnesses.append(witness_object)
                else:
                    witness_object = Witness(gateway=witness['gateway'], rssi=witness['signal'], snr=round(witness['snr'], 1), validity=f"Is Invalid : {witness['invalid_reason']}")
                    witnesses.append(witness_object)
            loading_data_label = CTk.CTkLabel(master=frame, text_color="#98A1A6", text="Loading witness data, please be patient...", fg_color=None, height=30)
            loading_data_label.place(x=830, y=850)
            beaconing_hotspot_data = do_requests(hotspots_url, "/", transaction_beaconer_gateway)
            loading_data_label.destroy()
            loading_data_label = CTk.CTkLabel(master=frame, text_color="#98A1A6", text=f"Loading Beaconer", width=50, height=30, fg_color=None)
            loading_data_label.place(x=900, y=850)
            beaconing_hotspot_name = beaconing_hotspot_data['data']['name'].replace("-", " ")
            for (number, witness) in enumerate(witnesses):
                owner_data = do_requests(hotspots_url, "/", witness.gateway)
                name = owner_data['data']['name'].replace("-", " ")
                hotspots[witness.gateway] = Hotspot(id=witness.gateway, name=name)
                loading_data_label.configure(text=f"{number + 1} out of {len(witnesses)} witnesses loaded")
            extra_data_canvas = CTk.CTkFrame(master=frame, width=350, height=650, fg_color="#575b5f")
            extra_data_canvas.place(x=650, y=170)
            extra_data_canvas_placed = True
            w_beaconer_label = CTk.CTkLabel(master=frame, text=f"{beaconing_hotspot_name.title()}", width=330, height=60, fg_color="#575b5f")
            w_beaconer_label.configure(font=('Alias', 16))
            w_beaconer_label.place(x=660, y=180)
            w_beacon_surround_label = CTk.CTkLabel()
            for witness in witnesses:
                hotspot_name = hotspots[witness.gateway].name
                w_beacon_label = CTk.CTkLabel(master=frame, text=f"{hotspot_name.title()}\n{witness.validity} | SNR = {witness.snr} | RSSI : {witness.rssi}", width=330, height=30, fg_color="#575b5f")
                w_beacon_labels.append(w_beacon_label)
                w_beacon_label.place(x=660, y=w_y)
                w_y = w_y + 40
            loading_data_label.destroy()
            witness_labels[witness_pressed].configure(state="disabled")
            w_is_loaded = True
            w_is_loading = False
        if w_is_loading == False:
            Thread(target=get_witness_data).start()

    def check_if_wbr_is_loaded():
        global w_is_loaded, w_y, w_beacon_labels
        global extra_data_canvas_placed, extra_data_canvas
        global witnessed_beacon_id_names, witnessed_beacon_id_validity, witnesses, witnessed_beacon_id_list
        if w_is_loading == False and r_is_loading == False:
            if w_is_loaded == True:
                w_beaconer_label.destroy()
                for label in w_beacon_labels:
                    label.destroy()
                extra_data_canvas.destroy()
                w_beacon_labels = []
                w_y = 250
                witnessed_beacon_id_validity = []
                witnesses = []
                witnessed_beacon_id_list = []
                witnessed_beacon_id_names = []
                w_is_loaded = False 
                for witness in witness_labels:
                    witness.configure(state="enabled")
        if w_is_loading == True or r_is_loading == True or b_is_loading == True:
            print("Please wait for your data to load.")

    def which_beacon(beacon_pressed):
        check_if_wbr_is_loaded()

    def which_reward(reward_pressed):
        check_if_wbr_is_loaded()

    def check_for_labels():
        global activity_buttons_placed
        global witness_displayed, witness_labels, witness_y
        global general_data_labels_loaded
        if activity_buttons_placed == True:
            general_data_label.destroy()
            witness_button.destroy()
            beacons_button.destroy()
            rewards_button.destroy()
            activity_buttons_placed = False
        if witness_displayed == True:
            for witness_label in witness_labels:
                witness_label.destroy()
                witness_labels = []
                witness_y = 310
                witness_displayed = False
        if general_data_labels_loaded == True:
            general_data_frame.destroy()
            hotspot_name_label.destroy()
            hotspot_location_label.destroy()
            general_data_labels_loaded = False



    @dataclass
    class Witness:
        gateway: str
        snr: float
        rssi: float
        validity: bool

    @dataclass
    class Hotspot:
        id: str
        name: str

    if w_is_loading == False and r_is_loading == False:
        check_for_labels()
        Thread(target=get_general_hs_data).start()

search_img = ImageTk.PhotoImage(Image.open("searchicon.png").resize((20, 20), Image.ANTIALIAS))

search_button = CTk.CTkButton(master=frame, width=80, height=35, image=search_img, text="", command=search_hotspot, bg_color="#10182c", fg_color="#10182c")
search_button.place(x=985, y=12.5)

GUI.mainloop()
