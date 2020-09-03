from alice_blue import *
import pandas as pd

# class login:
#     def __init__(self):
#         # Config
#         self.username = 'AB086867'
#         self.password = 'chicu244280'
#         # self.password = 'chicu@24428'
#         # self.api_secret = 'api_secret'
#         # self.twoFA ='a '
# 
#         # access_token = AliceBlue.login_and_get_access_token(username=username, password=password, twoFA=twoFA,
#         # api_secret=api_secret)
# self. access_tokan = "pRr0tpjP2ShATwrTwZxssdoFnsyTbC7VQJEisehaWkE.VoJuMcJz65HI1JRVJ38stcKcHMTBxfvQwgIYel4a5fE"
# self.access_tokan = 'GH9Hk1qjndGAY9pg7USuN62Acgx0-Dx1_LbBZQ6kJhQ.K-S0fivs1JJtqdQapDOHRPOmCaRxlGxL207Zn6yup9g'
# self.access_tokan = 'WGBbbmF8352PcXp-7TYE_Q_37LJFxn_N2RgAor82sxc.uKv2IWLwSnuvPdRdl76mrO_UJ5Ia-b4v9P_t14AoTtg'

df = pd.read_json("current.city.list.json.gz")
kd = df["id"][:5]
for i in kd:
    print(i)
