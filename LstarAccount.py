
# we use solscan api to get all account,thanks solscan give me convenient

# solscan url is 'https://public-api.solscan.io/docs/#/Token/get_token_list',see this

import requests
import json


tokenAddress = 'C6qep3y7tCZUJYDXHiwuK46Gt6FsoxLi8qV1bTCRYaY1'

baseURL = 'public-api.solscan.io/'

header = {
'authority':'public-api.solscan.io',
'method': 'GET',
'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Mobile Safari/537.36'
}

def get_last_block_test():
    response =  requests.get(url='https://public-api.solscan.io/block/last?limit=10',headers = header)
    print(response.content)


def _get_account_num_by_token(address):
    url = 'https://' + baseURL + 'token/holders?tokenAddress=' + address
    response = requests.get(url=url, headers=header)

    total_address_account = json.loads(response.content.decode())['total']
    print('total_address_account is ', total_address_account)
    return total_address_account

def get_account_address_by_token(address):
    total_address_account = _get_account_num_by_token(address)
    print('please waite , it need time to waite get reponse data')
    url = 'https://' + baseURL + 'token/holders?tokenAddress=' + address + '&limit='+str(total_address_account)
    try:
        response = requests.get(url=url, headers=header)
        all_account_address = json.loads(response.content.decode())['data']
        for i in all_account_address:
            print(i)

        print('from onwer we can get SPL token balance,it include LSTAR and NFT')
    except:
        print('error network,please try again')

def get_NFT_token_list_test(ownerAddress = '5Xz9hBP75payPpxxtMNtPDyNLMq8WL5hC57MPGJVYPft' ):
    url = 'https://' + baseURL + 'account/tokens?account=' + ownerAddress

    # we will get the 'USD Coin' and 'Learning Star'
    USDC = 0
    LSTAR = 0

    try:
        response = requests.get(url=url, headers=header)
        token_list = json.loads(response.content.decode())
        print('this owner token list follow this:')
        for i in token_list:
            if i['tokenAmount']['amount'] == '1' and i['tokenAmount']['decimals'] == 0 and i['tokenAmount']['uiAmountString'] == '1' and i['tokenName'] ==''  and i['tokenIcon'] == '':
                print('NFT address is',i['tokenAddress'])
            elif i['tokenName'] == 'USD Coin':
                print('USD Coin balance is ',i['tokenAmount']['uiAmountString'])
            elif i['tokenName'] == 'Learning Star':
                print('Learning Sta balance is ', i['tokenAmount']['uiAmountString'])

    except:
        print('error network,please try again')


def get_NFT_info_test(NFTaddress = '9D16eYPYJcJv7z3251b1QLp72cZDonnW1eRA9VDep6Rz'):

    # there had issue, if we want to get NFT info the base url not work,we should use
    # https://api.solscan.io/account?address =  + 'NFT address' ,it work

    url = 'https://api.solscan.io/account?address=' + NFTaddress
    print(url)
    try:
        response = requests.get(url=url, headers=header)
        print(response)
        NFT_info = json.loads(response.content.decode())
        print('this NFT info follow this:')

        print(NFT_info['data']['tokenInfo'])
        print(NFT_info['data']['metadata']['data'])
        print(NFT_info['data']['metadata']['data']['uri'])
    except:
        print('error network,please try again')

def get_NFT_totalInfo_by_Uri_test(uri = 'https://api2.letmespeak.pro/api/1.0/metadata/8b630bc7-8e91-47f8-b969-0acaa7616587'):
    # uri info NFT all info ,it pretty important.  {"name":"#782107","symbol":"","description":"","seller_fee_basis_points":0,"image":"https://letmespeak.akamaized.net/avatars/6d074e78-35d2-4092-8012-0770fb40f425.png","external_url":"https://letmespeak.org","properties":{"files":[{"uri":"https://letmespeak.akamaized.net/avatars/6d074e78-35d2-4092-8012-0770fb40f425.png","type":"image/png"}],"category":"image","creators":[{"share":100,"address":"Fbm31wFSEkL33JT7UaYac9ZJeDjAFMfUHi4wzZEmojKy","verified":1}]},"attributes":[{"trait_type":"name","value":"Kingg"},{"trait_type":"number","value":782107},{"trait_type":"talent","value":31},{"trait_type":"activated","value":true},{"trait_type":"rarity","value":3},{"trait_type":"currency_reward","value":1},{"trait_type":"learning_speed","value":106},{"trait_type":"visa_total","value":150},{"trait_type":"visa_left","value":142},{"trait_type":"xp_level","value":10},{"trait_type":"xp","value":16490},{"trait_type":"invites_total","value":6},{"trait_type":"invites_left","value":6},{"trait_type":"skill_vocabulary","value":97},{"trait_type":"skill_pronunciation","value":68},{"trait_type":"skill_listening","value":79},{"trait_type":"skill_grammar","value":62},{"trait_type":"banned","value":false}]}


    # some data need to record,follow this:

    # trait_type  'activated'
    # trait_type  'rarity'
    # trait_type': 'currency_reward'
    # trait_type': 'learning_speed'
    # 'trait_type': 'visa_total'
    # 'trait_type': 'visa_left'
    # 'trait_type': 'invites_total'
    # 'trait_type': 'invites_left'
    # 'trait_type': 'banned'


    try:
        response = requests.get(url=uri, headers=header)
        NFT_info = json.loads(response.content.decode())
        print(NFT_info['attributes'])
        for i in NFT_info['attributes']:
            print(i)
            if i['trait_type'] == 'visa_left':
                print(i['value'])

    except:
        print('error network,please try again')


# get_account_address_by_token(tokenAddress)
# get_NFT_token_list_test()
# get_NFT_info_test()
get_NFT_totalInfo_by_Uri_test()