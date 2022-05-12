# (Library Import)
import pandas as pd
import warnings
import random

warnings.filterwarnings("ignore")


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
  
def fuzz(n, data, fuzz_setting):
  choose = fuzz_setting['Method']
  final_data = []
  for i in range(0, n):
    low_fuzz = 0
    avg_fuzz = 0
    high_fuzz = 0
    # low
    if(data[i][choose] > fuzz_setting['low_top'] and data[i][choose] <= fuzz_setting['low_bot']):

    elif(data[i][choose] <= fuzz_setting['low_top']) : low_fuzz = 1
    # avg
    if(data[i][choose] > fuzz_setting['avg_bot_left'] and data[i][choose] <= fuzz_setting['avg_top_left']):

    elif(data[i][choose] > fuzz_setting['avg_top_left'] and data[i][choose] < fuzz_setting['avg_top_right']) : 
    elif(data[i][choose] > fuzz_setting['avg_top_right'] and data[i][choose] <= fuzz_setting['avg_bot_right']) :

    # low
    if(data[i][choose] > fuzz_setting['high_bot'] and data[i][choose] <= fuzz_setting['high_top']):

    elif(data[i][choose] > fuzz_setting['high_top']) : high_fuzz = 1


  return final_data

def inference(n, fuzz_service, fuzz_price, inference_setting):
    inference_array = []
    for i in range(0,n):
        reject = []
        consider = []
        accept = []
        for j in inference_setting:
            if(j['Status'] == "Rejected"):


            elif(j['Status'] == "Considered"):


            elif(j['Status'] == "Accepted"):


    return inference_array

def defuzz(sugeno, inference_data):
  defuzz_arr = []
  for i in inference_data:

    final = {'ID': i['ID'], 'Defuzz': y}
    defuzz_arr.append(final)
  return defuzz_arr

def bestof10(defuzz_data, read_data):
  final = sorted(defuzz_data, key=lambda i: i['Defuzz'], reverse=True)[0:10]
  for i in range(0,10):
    a = final[i]['ID']

  return final

def savefile(final_data, flag):
    if(flag == 'real'):
        name = input("Input the filename : ")
        sort = input("Sort by ID or Defuzz? ").upper()
        final_data = sorted(final_data, key=lambda i: i['Defuzz'])
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
