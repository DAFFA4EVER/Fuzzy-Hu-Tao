# (Library Import)
import pandas as pd
import warnings
import random

warnings.filterwarnings("ignore")

try:
    import pyi_splash
    pyi_splash.update_text('UI Loaded ...')
    pyi_splash.close()
except:
    pass

def read_excel(path, sheet_target):
    try:
        data = pd.read_excel(path, sheet_name=sheet_target)
        return data.to_dict('record')
    except IOError:
        print("Hu Tao could not find the file! 😟")
        return False

def output_xlsx(data_final, filename):
    df = pd.DataFrame(data_final, columns=["ID", "Service", "Price" ,"Defuzz"])
    try:
        df.to_excel(f'{filename}.xlsx')
        print(f"Hu Tao save the file as : {filename}.xlsx ✍️")
        return True
    except IOError:
        print("Hu Tao could not open file! Please close Excel! 😟")
        return False

def testing_data():
    total = 100
    price_min, price_max = (1,10)
    service_min, service_max = (1,100)

    data = []
    for i in range(0,total):
        x = {'ID': i+1, 'Service': random.randint(service_min,service_max), 'Price': random.randint(price_min,price_max), 'Defuzz': 0}
        data.append(x)

    return savefile(data, 'test')
  
def fuzz(n, data, fuzz_setting):
  choose = fuzz_setting['Method']
  final_data = []
  for i in range(0, n):
    low_fuzz = 0
    avg_fuzz = 0
    high_fuzz = 0
    # low
    if(data[i][choose] > fuzz_setting['low_top'] and data[i][choose] <= fuzz_setting['low_bot']):
      low_fuzz = abs(data[i][choose] - fuzz_setting['low_bot'])/abs(fuzz_setting['low_top']-fuzz_setting['low_bot'])
    elif(data[i][choose] <= fuzz_setting['low_top']) : low_fuzz = 1
    # avg
    if(data[i][choose] > fuzz_setting['avg_bot_left'] and data[i][choose] <= fuzz_setting['avg_top_left']):
      avg_fuzz = abs(data[i][choose] - fuzz_setting['avg_bot_left'])/abs(fuzz_setting['avg_bot_left']-fuzz_setting['avg_top_left'])
    elif(data[i][choose] > fuzz_setting['avg_top_left'] and data[i][choose] < fuzz_setting['avg_top_right']) : avg_fuzz = 1
    elif(data[i][choose] > fuzz_setting['avg_top_right'] and data[i][choose] <= fuzz_setting['avg_bot_right']) :
      avg_fuzz = abs(data[i][choose] - fuzz_setting['avg_bot_right'])/abs(fuzz_setting['avg_bot_right']-fuzz_setting['avg_top_right'])
    # low
    if(data[i][choose] > fuzz_setting['high_bot'] and data[i][choose] <= fuzz_setting['high_top']):
      high_fuzz = abs(data[i][choose] - fuzz_setting['high_bot'])/abs(fuzz_setting['high_top']-fuzz_setting['high_bot'])
    elif(data[i][choose] > fuzz_setting['high_top']) : high_fuzz = 1
    final = {'ID': data[i]['ID'], 'Low': low_fuzz, 'Average': avg_fuzz, 'High': high_fuzz}
    final_data.append(final)
  return final_data

def inference(n, fuzz_service, fuzz_price, inference_setting):
    inference_array = []
    for i in range(0,n):
        reject = []
        consider = []
        accept = []
        for j in inference_setting:
            if(j['Status'] == "Rejected"):
                take_minimum = min(fuzz_service[i][j['Service']], fuzz_price[i][j['Price']])
                reject.append(take_minimum)
            elif(j['Status'] == "Considered"):
                take_minimum = min(fuzz_service[i][j['Service']], fuzz_price[i][j['Price']])
                consider.append(take_minimum)
            elif(j['Status'] == "Accepted"):
                take_minimum = min(fuzz_service[i][j['Service']], fuzz_price[i][j['Price']])
                accept.append(take_minimum)
        result = {'ID': fuzz_service[i]['ID'], 'Rejected': max(reject), 'Considered': max(consider), 'Accepted': max(accept)}
        inference_array.append(result)
    return inference_array

def defuzz(sugeno, inference_data):
  defuzz_arr = []
  for i in inference_data:
    y = (i['Rejected'] * sugeno[0]) + (i['Considered']*sugeno[1]) + (i['Accepted']*sugeno[2]) / (i['Rejected'] + i['Considered'] + i['Accepted'] + 0.00000001)
    final = {'ID': i['ID'], 'Defuzz': y}
    defuzz_arr.append(final)
  return defuzz_arr

def bestof10(defuzz_data, read_data):
  final = sorted(defuzz_data, key=lambda i: i['Defuzz'], reverse=True)[0:10]
  for i in range(0,10):
    a = final[i]['ID']
    final[i] = {'ID': final[i]['ID'], 'Service': read_data[a-1]['Service'], 'Price': read_data[a-1]['Price'] ,'Defuzz': final[i]['Defuzz']}
  return final

def savefile(final_data, flag):
    if(flag == 'real'):
        name = input("Input the filename : ")
        sort = input("Sort by ID or Defuzz? ").upper()
        if(sort == "ID"): 
            final_data = sorted(final_data, key=lambda i: i['ID'])
        elif(sort != "DEFUZZ") : print("Sorted by Defuzz by default")
    else:
        name = 'test'

    return output_xlsx(final_data, name)

# Program Setting

# (Fuzzification)
service = {'low_top': 0, 'low_bot': 0, 'avg_top_left' : 0, 'avg_bot_left': 0, 
           'avg_top_right': 0, 'avg_bot_right': 0, 'high_top': 0, 'high_bot': 0, 'Method': 'Service'}

price = {'low_top': 0, 'low_bot': 0, 'avg_top_left' : 0, 'avg_bot_left': 0, 
           'avg_top_right': 0, 'avg_bot_right': 0, 'high_top': 0, 'high_bot': 0, 'Method': 'Price'}

# (Inference)
# Only accept : Rejected, Considered, and Accepted
inference_setting = [ 
{'Service': 'Low', 'Price': 'Low', 'Status': '?'}, {'Service': 'Low', 'Price': 'Average', 'Status': '?'}, {'Service': 'Low', 'Price': 'High', 'Status': '?'},
{'Service': 'Average', 'Price': 'Low', 'Status': '?'}, {'Service': 'Average', 'Price': 'Average', 'Status': '?'}, {'Service': 'Average', 'Price': 'High', 'Status': '?'},
{'Service': 'High', 'Price': 'Low', 'Status': '?'}, {'Service': 'High', 'Price': 'Average', 'Status': '?'}, {'Service': 'High', 'Price': 'High', 'Status': '?'}]

# (Defuzzification)
    #  low, mid, high
sugeno = [0, 0, 0]

# (Main Program)
# Main
flag = True

print("\nWelcome to Fuzzy Logic by Hu Tao 🥰\n")

input("Press enter to continue 👌 ")

print("\n-----Service Setting-----")
print(service)

print("\n-----Price Setting-----")
print(price)

print("\n-----Inference Setting-----")
for i in inference_setting:
  print(i)

print("\n-----Defuzzification Method-----")
print(f"Sugeno :\nLow = {sugeno[0]}\nMid = {sugeno[1]}\nHigh = {sugeno[2]}")

mode = input("\nDo you want Hu Tao to do debugging 🤔?(Yes/No) ").upper()

if(mode == "YES"):
  generate = input("Do you want Hu Tao to generate new data 🤔?(Yes/No) ").upper()
  if(generate == "NO"):
    print('Hu Tao trying to read test.xlsx file 📖 ')
    read_data = read_excel('test.xlsx', 'Sheet1')
    if(read_data == False):
      flag = False
  else:
    print('Hu Tao trying to generate test.xlsx file ⚒️ ')
    flag = testing_data()
    if(flag == True):  
      print('Hu Tao trying to read test.xlsx 📖 ')
      read_data = read_excel('test.xlsx', 'Sheet1')
    else: print('Hu Tao aborted the mission 😟')
else:
  mode = 'NO'
  print('Hu Tao trying to read bengkel.xlsx 📖 ')
  read_data = read_excel('bengkel.xlsx', 'Sheet1')
  if(read_data == False):
      flag = False

if(flag == True):
  length = len(read_data)

  fuzz_service = fuzz(length, read_data, service)
  fuzz_price = fuzz(length, read_data, price)

  inference_data = inference(length, fuzz_service, fuzz_price, inference_setting)

  defuzz_data = defuzz(sugeno, inference_data)

  finale = bestof10(defuzz_data, read_data)
  finale = sorted(finale, key=lambda i: i['ID'])
  print("\n-----The Result-----")
  for i in finale:
    i = {'ID': i['ID'], 'Service': i['Service'], 'Price': i['Price'],'Defuzz': i['Defuzz']}
    print(i)

  if(mode == "NO"):
    savefile(finale, 'real')

input("\nPress enter to exit 👋 ")
