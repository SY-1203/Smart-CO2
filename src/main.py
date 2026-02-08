from groq import Groq
import os
import matplotlib.pyplot as m
import streamlit as s

s.title("SmartCO2 - Carbon Footprint Calculator")

if s.button("Reset"):
    s.session_state.clear()
    s.rerun()

CO2E = 0
CO2T = 0
CO2EL = 0
CO2W = 0

s.write("NOTE: Please enter weekly estimates")

T = s.multiselect("Choose vehicles used for transport: ", ["CAR","MOTORBIKE","BUS"])
TD = {}

for i in T:
    if i.upper() =="CAR":
        s.subheader("Car Details")
        fuels = {"CNG":[None,0.15504,0.23722,0.17414],"LPG":[None,0.17427,0.26771,0.19599],"PETROL":[0.14308,0.17474,0.26828,0.16272],
        "DIESEL":[0.14340,0.17174,0.21007,0.17304],"HYBRID":[0.11413,0.11724,0.15650,0.12825]}
        try:
            fuel =s.selectbox("Select the fuel used for your car: ",["CNG","LPG","PETROL","DIESEL","HYBRID"])
            dist = s.number_input("Enter the car distance travelled (km):",min_value = 0.0 )
            size =s.selectbox("What is your car size: ",["Small","Medium","Large","Average"])
            sizel = ["Small","Medium","Large","Average"]
            sizenum = sizel.index(size)
            car = dist * fuels[fuel][sizenum]
            CO2E +=  car
            CO2T +=  car
            TD["Car"] = car
        except:
            s.warning("An errror occured, Please check the data entered")

    if i.upper() == "MOTORBIKE":
        s.subheader("Bike Details")
        emission = {"Small":  0.08319,"Medium":  0.10107,"Large":  0.13252,"Average":  0.11367}
        try:
            dist = s.number_input("Enter the bike distance travelled (km):",min_value = 0.0 )
            size =s.selectbox("What is your bike size: ",["Small","Medium","Large","Average"])
            bike = dist * emission[size]
            CO2E +=  bike
            CO2T +=  bike
            TD["Bike"] = bike
        except:
            s.warning("An errror occured, Please check the data entered")
            
    if i.upper() == "BUS":
        s.subheader("Bus Details")
        try:
            dist = s.number_input("Enter the bus distance travelled (km):",min_value = 0.0 )
            bus = dist * 0.10385
            CO2E += bus
            CO2T += bus
            TD["Bus"] = bus
        except:
            s.warning("An errror occured, Please check the data entered")
            

try:
    s.subheader("Electricity  Details")
    elec = s.number_input("Enter the electricity usage (kWh):",min_value = 0.0 )
    if elec > 0.0:
        elect = elec * 0.17700
        CO2E += elect
        CO2EL += elect
except:
    s.warning("An errror occured, Please check the data entered")
        
try:
    s.subheader("Water Details")
    wat1 = s.number_input("Enter the water usage (m^3):",min_value = 0.0 )
    wat2 = s.number_input(" Enter a rough estimate of water disposed (m^3):", min_value = 0.0)
    if wat1>0 and wat2>0:
        wat1 = float(wat1)
        wat2 = float(wat2)
        wat = wat1 *0.19130 + wat2 * 0.1708800
        CO2E += wat
        CO2W += wat
    elif wat1>0:
        wat1 = float(wat1)
        wat = wat1 *0.19130 
        CO2E += wat
        CO2W += wat
    elif wat2>0:
        wat2 = float(wat2)
        wat = wat2 * 0.1708800
        CO2E += wat
        CO2W += wat
except:
    s.warning("An errror occured, Please check the data entered")

if s.button("Show Carbon Footprint"):
    s.write("Your carbon footprint is", CO2E,"kg of CO2")
    act = list(TD.keys())
    co2_1 = list(TD.values())
    if CO2EL != 0:
        act.append("Electricity")
        co2_1.append(CO2EL)
    if CO2W != 0:
        act.append("Water")
        co2_1.append(CO2W)
    if len(co2_1)>0:
        fig, x = m.subplots()

        x.bar(act,co2_1)
        x.set_xlabel("Daily Practices")
        x.set_ylabel("CO2 Footprint")
        s.pyplot(fig)
    else:
        s.write("No data to display in bar graph")

    cat = []
    co2_2 = []
    if CO2T != 0:
        cat.append("Transport")
        co2_2.append(CO2T)
    if CO2EL != 0:
        cat.append("Electricity")
        co2_2.append(CO2EL)
    if CO2W != 0:
        cat.append("Water")
        co2_2.append(CO2W)
    if len(co2_2)>0:
        fig, x = m.subplots()
        x.pie(co2_2, labels = cat, autopct='%0.2f%%',startangle=90 )
        s.pyplot(fig)
    else:
        s.write("No data to display in pie chart")

if s.button("Get AI Explanation and Alternatives"):
    try:
        api_key = s.secrets["APIKey"]
    except:
        s.error("API Key is missing")
    
    try:
        client = Groq(api_key=api_key)

        chat = client.chat.completions.create(model="llama-3.1-8b-instant", 
        messages=[{"role": "user", "content": "My carbon footprint is {} kg of CO2 for 1 week - Transport - {}; Electricity - {}, Water - {}, can you explain what it means, also provide me with alternate practices to reduce it, I want 6 realistic alternatives to reduce it with priority for the biggest contributor and Give qualitative impact only: High/Medium/Low".format(CO2E,CO2T,CO2EL,CO2W) }])
        s.subheader("AI Response")
        s.write(chat.choices[0].message.content)

    except:
        s.error("AI functionality is not available right now, Please try again later")

