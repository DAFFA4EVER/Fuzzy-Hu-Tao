# Fuzzy-Hu-Tao
![Hu Tao is our mascot 🙏](https://github.com/DAFFA4EVER/Fuzzy-Hu-Tao/blob/main/Icon_Emoji_Hu_Tao_1.png)

This is a fuzzy logic implementation in Python. If you want to try using it without doing the coding stuff. Go to this link (Fuzzy Hu Tao.exe) : https://drive.google.com/file/d/1F-1HqvsOFvaSIssCGWnRqEdVswOH7DYM/view?usp=sharing

# Disclaimer
I already leave the fuzzification and inference setting blank. Use your own brew don't do **100%** copycat 🙏

# Explanation

**(Library Import)**
* pandas = to read and output xlsx file
* warnings = not that important, it was just use to hidden any warnings
* random = to generate random value for generating random service and price value for test.xlsx
* pyi_splash = it will be used if you want to compile this code to .exe file. It is not important thou 👌

**(Fuzzification)**
![Fuzzification Legend](https://github.com/DAFFA4EVER/Fuzzy-Hu-Tao/blob/main/Teaching%20by%20Hu%20Tao.png)

**(Inference)**
* Service : Ranging from Low, Average, and High
* Price   : Ranging from Low, Average, and High
* Status  : Ranging from Rejected, Considered, and Accepted

**(Defuzzification)**
We use Sugeno method to do it
* sugeno[0] = for low
* sugeno[1] = for mid
* sugeno[2] = for high

**(Main Program)**
* mode = Yes/No
    - Yes : We try to to use a custom one data (test.xlsx)
    - No  : We use provided data from my lecturer (bengkel.xlsx)
* generate = Yes/No
    - Yes : We generate new data (test.xlsx) randomly
    - No  : We use the existing data (test.xlsx)
* flag  = True/False
    - True : Means we can read the data (either bengkel.xlsx or test.xlsx)
    - False : Means we can't read the data (either bengkel.xlsx or test.xlsx)
