from groq import Groq
import os
from dotenv import load_dotenv
import matplotlib.pyplot

CO2E = 0
CO2T = 0
CO2EL = 0
CO2W = 0
T = input("Enter the different vehicles used for transport ").split()
TD = {}
print("NOTE: Please enter weekly estimates")
for i in T:
    if i.upper() =="CAR":
        fuels = {"CNG":[None,0.15504,0.23722,0.17414],"LPG":[None,0.17427,0.26771,0.19599],"PETROL":[0.14308,0.17474,0.26828,0.16272],
        "DIESEL":[0.14340,0.17174,0.21007,0.17304],"HYBRID":[0.11413,0.11724,0.15650,0.12825]}
        try:
            fuel = input("Enter the fuel used ").upper()
            dist = float(input("Enter the distance travelled in km "))
            print("Select car size :-","1. Small","2. Medium","3. Large","4. Average",sep="\n")
            car_type = int(input("Enter 1/2/3/4 "))
            car = dist * fuels[fuel][car_type-1]
            CO2E +=  car
            CO2T +=  car
            TD["Car"] = car
        except KeyError:
            print("Fuel Type Not Found")
        except:
            print("An errror occured, Please try again later.")
    if i.upper() == "MOTORBIKE":
        emission = {"SMALL":  0.08319,"MEDIUM":  0.10107,"LARGE":  0.13252,"AVERAGE":  0.11367}
        try:
            dist = float(input("Enter the distance travelled in km "))
            size = input("Select motorbiker size - Small, Medium, Large, Average ").upper()
            bike = dist * emission[size]
            CO2E +=  bike
            CO2T +=  bike
            TD["Bike"] = bike
        except:
            print("An errror occured, Please try again later.")
    if i.upper() == "BUS":
        try:
            dist = float(input("Enter the distance travelled in km "))
            bus = dist * 0.10385
            CO2E += bus
            CO2T += bus
            TD["Bus"] = bus
        except:
            print("An errror occured, Please try again later.")

try:
    elec = float(input("Enter the electricity usage in kWh "))
    elect = elec * 0.17700
    CO2E += elect
    CO2EL += elect
except:
    print("An errror occured, Please try again later.")
        
try:
    wat1 = float(input("Enter your water usage in m^3  "))
    wat2 = float(input("Enter a rough estimate of water disposed in m^3 "))
    wat = wat1 *0.19130 + wat2 * 0.1708800
    CO2E += wat
    CO2W += wat
except:
    print("An errror occured, Please try again later.")

print("Your carbon footprint is", CO2E,"kg of CO2")
act = []
co2_1 = []
for veh,fp in TD.items():
    act.append(veh)
    co2_1.append(fp)
act.extend(["Electricity","Water"])
co2_1.extend([CO2EL,CO2W])
matplotlib.pyplot.bar(act,co2_1)
matplotlib.pyplot.xlabel("Daily Practices")
matplotlib.pyplot.ylabel("CO2 Footprint")
matplotlib.pyplot.show()

cat = ["Transport","Electricity","Water"]
co2_2 = [CO2T,CO2EL,CO2W]
matplotlib.pyplot.pie(co2_2, labels = cat, autopct='%0.2f%%',startangle=90 )
matplotlib.pyplot.show()

load_dotenv()
api_key = os.getenv("APIKey")
if not api_key:
    raise ValueError("API Key not found in .env file")


client = Groq(api_key=api_key)

chat = client.chat.completions.create(model="llama-3.1-8b-instant", 
messages=[{"role": "user", "content": "My carbon footprint is {} kg of CO2 for 1 week - Transport - {}; Electricity - {}, Water - {}, can you explain what it means".format(CO2E,CO2T,CO2EL,CO2W) }])
print(chat.choices[0].message.content)
    
chat = client.chat.completions.create(model="llama-3.1-8b-instant",
messages=[{"role": "user", "content": "My carbon footprint is {} for 1 week - Transport - {}; Electricity - {}, Water - {}, can you provide me with alternate practices to reduce it, I want 6 realistic alternatives to reduce it with priority fore the biggest contributor and give estimated impact only if confident".format(CO2E,CO2T,CO2EL,CO2W) }])
print(chat.choices[0].message.content)

