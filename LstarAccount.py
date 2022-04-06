
# we use solscan api to get all account,thanks solscan give me convenient
# solscan url is 'https://public-api.solscan.io/docs/#/Token/get_token_list',see this
# for any NFT and user data I use mysql to restore. So before you use this,make sure you mysql server has run.

import requests
import json
import pymysql
import time
import asyncio
import aiohttp


# base url
tokenAddress = 'C6qep3y7tCZUJYDXHiwuK46Gt6FsoxLi8qV1bTCRYaY1'

baseURL = 'public-api.solscan.io/'

header = {
'authority':'public-api.solscan.io',
'method': 'GET',
'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Mobile Safari/537.36'
}

conn = pymysql.connect(host='127.0.0.1', user='root', password='1416615127dj', database='letmespeak')
# cursor=pymysql.cursors.DictCursor,是为了将数据作为一个字典返回
cursor = conn.cursor()

errorNFTADDRESS = []
erroruserAccount = []

global errorNFTADDRESSCount
global erroruserAccountCount

errorNFTADDRESSCount=0
erroruserAccountCount=0

def mysql_insert_test(useraccount = 'C6qep3y7tCZUJYDXHiwuK46Gt6FsoxLi8qV1bTCRYaY1',usdc=100,lstar=1312.1,nftaddress='DDDsbU5q717qG4pop8dpNvtso5P1UvhQpiWCtQMBhDzm'):
    conn = pymysql.connect(host='127.0.0.1', user='root', password='1416615127dj', database='letmespeak')
    # cursor=pymysql.cursors.DictCursor,是为了将数据作为一个字典返回
    cursor = conn.cursor()
    sql = "insert into Userdata(useraccount,usdc,lstar,nftaddress) values('%s','%s','%s','%s')"  % \
          (useraccount, usdc, lstar, nftaddress)
    print(sql)
    rows = cursor.execute(sql)
    print(rows)

    result = cursor.fetchall()
    print(result)
    # 这里一定要提交

    conn.commit()
    cursor.close()
    conn.close()

def mysql_get_oneline(num):
    # sql  = "select * from Owner"
    # row_count = cursor.execute(sql)
    result = cursor.fetchall()
    return result(num)

def get_last_block_test():
    response =  requests.get(url='https://public-api.solscan.io/block/last?limit=10',headers = header)
    print(response.content)

def _get_account_num_by_token(address):
    '''

    :param address:
    :return:
    '''
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
            get_NFT_token_list_by_owner(i['owner'])
            #print(i['owner'])

        print('from onwer we can get SPL token balance,it include LSTAR and NFT')
    except:
        print('error network,please try again')

def get_NFT_token_list_by_owner_test(ownerAddress = '5Xz9hBP75payPpxxtMNtPDyNLMq8WL5hC57MPGJVYPft' ):
    url = 'https://' + baseURL + 'account/tokens?account=' + ownerAddress

    # we will get the 'USD Coin' and 'Learning Star'
    USDC = 0
    LSTAR = 0

    try:
        response = requests.get(url=url, headers=header)
        token_list = json.loads(response.content.decode())
        print('this owner token list follow this:')
        for i in token_list:
            # print(i)
            if i['tokenAmount']['amount'] == '1' and i['tokenAmount']['decimals'] == 0 and i['tokenAmount']['uiAmountString'] == '1' and i['tokenName'] ==''  and i['tokenIcon'] == '':
                print('NFT address is',i['tokenAddress'])
            elif i['tokenName'] == 'USD Coin':
                print('USD Coin balance is ',i['tokenAmount']['uiAmountString'])
            elif i['tokenName'] == 'Learning Star':
                print('Learning Sta balance is ', i['tokenAmount']['uiAmountString'])

    except:
        print('error network,please try again')

def get_NFT_token_list_by_owner(ownerAddress):
    url = 'https://' + baseURL + 'account/tokens?account=' + ownerAddress

    # we will get the 'USD Coin' and 'Learning Star'
    USDC = 0
    LSTAR = 0
    nft = ''

    try:
        response = requests.get(url=url, headers=header)
        token_list = json.loads(response.content.decode())
        print('this owner token list follow this:')

        #first to get usdc and lstar
        for i in token_list:
            if i['tokenName'] == 'USD Coin':
                USDC = i['tokenAmount']['uiAmountString']
                #print('USD Coin balance is ',USDC)
            if i['tokenName'] == 'Learning Star':
                LSTAR =i['tokenAmount']['uiAmountString']

        # second get the NFT address
        for i in token_list:
            # print(i)
            #time.sleep(1)
            if i['tokenAmount']['amount'] == '1' and i['tokenAmount']['decimals'] == 0 and i['tokenAmount']['uiAmountString'] == '1' and i['tokenName'] ==''  and i['tokenIcon'] == '':
                nft =i['tokenAddress']
                #print('NFT address is',nft)

                try:
                    print('try to get uri and NFT info ')
                    url  = get_NFT_uri(nft)
                    (name, number, talent, activated, rarity, currency_reward,
                     learning_speed, visa_total, visa_left, xp_level, invites_total, invites_left, banned) = get_NFT_totalInfo_by_Uri(url)

                except:
                    print('uri or NFT info error')
                    continue
            else:
                continue
            # storage to mysql database
            # print(name, number, talent, activated, rarity, currency_reward,
            #       learning_speed, visa_total, visa_left, xp_level, invites_total, invites_left, banned)

            try:
                sql_insert = "insert into Userdata(useraccount,usdc,lstar,nftaddress,nftname,nftnumber,talent,activated ,rarity ,currency_reward ,learning_speed ,visa_total,visa_left ,xp_level ,invites_total ,invites_left , banned) values('%s',%s,%s,'%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % \
                      (ownerAddress, USDC, LSTAR, nft,name,number,talent,activated ,rarity ,currency_reward ,learning_speed ,visa_total,visa_left ,xp_level ,invites_total ,invites_left , banned)
                print(sql_insert)
                cursor.execute(sql_insert)
                conn.commit()
                print('插入成功',ownerAddress, USDC, LSTAR, nft,name,number,talent,activated ,rarity ,currency_reward ,learning_speed ,visa_total,visa_left ,xp_level ,invites_total ,invites_left , banned)
            except:
                sql_nft = "insert into ErrorNFT(nftaddress) values(%s)" % \
                            (nft)
                cursor.execute(sql_nft)
                conn.commit()
                errorNFTADDRESS.append(i['tokenAddress'])
                print('get item error',i['tokenAddress'])


    except:

        try:
            sql_owner = "insert into ErrorOwner(nftaddress) values(%s)" % \
                  ( ownerAddress )
            cursor.execute(sql_owner)
            conn.commit()
        except:
            print('owner 添加失败')
        print('error network,please try again-- ',ownerAddress,' -- had to list, Already have  ')

def get_NFT_uri_test(NFTaddress = '9D16eYPYJcJv7z3251b1QLp72cZDonnW1eRA9VDep6Rz'):

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

def get_NFT_uri(NFTaddress):

    # there had issue, if we want to get NFT info the base url not work,we should use
    # https://api.solscan.io/account?address =  + 'NFT address' ,it work

    url = 'https://api.solscan.io/account?address=' + NFTaddress
    # print(url)
    try:
        response = requests.get(url=url, headers=header)
        # print(response)
        NFT_info = json.loads(response.content.decode())
        # print('this NFT info follow this:')
        #
        # print(NFT_info['data']['tokenInfo'])
        # print(NFT_info['data']['metadata']['data'])
        # print(NFT_info['data']['metadata']['data']['uri'])
    except:
        errorNFTADDRESS.append(NFTaddress)
        print('GET Uri error')
        return
    return NFT_info['data']['metadata']['data']['uri']

def get_NFT_totalInfo_by_Uri(uri):
    # uri info NFT all info ,it pretty important.  {"name":"#782107","symbol":"","description":"","seller_fee_basis_points":0,"image":"https://letmespeak.akamaized.net/avatars/6d074e78-35d2-4092-8012-0770fb40f425.png","external_url":"https://letmespeak.org","properties":{"files":[{"uri":"https://letmespeak.akamaized.net/avatars/6d074e78-35d2-4092-8012-0770fb40f425.png","type":"image/png"}],"category":"image","creators":[{"share":100,"address":"Fbm31wFSEkL33JT7UaYac9ZJeDjAFMfUHi4wzZEmojKy","verified":1}]},"attributes":[{"trait_type":"name","value":"Kingg"},{"trait_type":"number","value":782107},{"trait_type":"talent","value":31},{"trait_type":"activated","value":true},{"trait_type":"rarity","value":3},{"trait_type":"currency_reward","value":1},{"trait_type":"learning_speed","value":106},{"trait_type":"visa_total","value":150},{"trait_type":"visa_left","value":142},{"trait_type":"xp_level","value":10},{"trait_type":"xp","value":16490},{"trait_type":"invites_total","value":6},{"trait_type":"invites_left","value":6},{"trait_type":"skill_vocabulary","value":97},{"trait_type":"skill_pronunciation","value":68},{"trait_type":"skill_listening","value":79},{"trait_type":"skill_grammar","value":62},{"trait_type":"banned","value":false}]}


    # some data need to record,follow this:

    name = ''
    number = 0
    talent = 0
    activated = None
    rarity = 0
    currency_reward = 0
    learning_speed = 0
    visa_total = 0
    visa_left = 0
    xp_level = 0
    invites_total = 0
    invites_left = 0
    banned = None

    try:
        response = requests.get(url=uri, headers=header)
        NFT_info = json.loads(response.content.decode())
        # print(NFT_info['attributes'])
        for i in NFT_info['attributes']:
            # print(i)
            if i['trait_type'] == 'name':
                name = i['value']
                # print(i['value'])
            elif i['trait_type'] == 'number':
                number = i['value']
                # print(i['value'])
            elif i['trait_type'] == 'talent':
                talent = i['value']
                # print(i['value'])
            elif i['trait_type'] == 'activated':
                activated = i['value']
                # print(i['value'])
            elif i['trait_type'] == 'rarity':
                rarity = i['value']
                # print(i['value'])
            elif i['trait_type'] == 'currency_reward':
                currency_reward = i['value']
                # print(i['value'])
            elif i['trait_type'] == 'learning_speed':
                learning_speed = i['value']
                # print(i['value'])
            elif i['trait_type'] == 'visa_total':
                visa_total = i['value']
                # print(i['value'])
            elif i['trait_type'] == 'visa_left':
                visa_left = i['value']
                # print(i['value'])
            elif i['trait_type'] == 'xp_level':
                xp_level = i['value']
                # print(i['value'])
            elif i['trait_type'] == 'invites_total':
                invites_total = i['value']
                # print(i['value'])
            elif i['trait_type'] == 'invites_left':
                invites_left = i['value']
                # print(i['value'])
            elif i['trait_type'] == 'banned':
                banned = i['value']
                # print(i['value'])

        return [name,number,talent,activated ,rarity ,currency_reward ,learning_speed ,visa_total,visa_left ,xp_level ,invites_total ,invites_left , banned]
    except:
        errorNFTADDRESS.append(uri)
        print('get nft info error')
        return 'error'

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
            # if i['trait_type'] == 'visa_left':
            #     print(i['value'])

    except:
        print('error network,please try again')

def get_mysql_inser_different_boo_int_char_test(banned=True, nftaddress='D16eYPYJcJv72z3251b1QLp72cZDonnW1eRA9VDep6Rz', lstar=111):
    conn = pymysql.connect(host='127.0.0.1', user='root', password='1416615127dj', database='letmespeak')
    # cursor=pymysql.cursors.DictCursor,是为了将数据作为一个字典返回
    cursor = conn.cursor()

    #make sure your sql values is right ,in python connect to mysql, we must make sure type is same.
    sql = "insert into Test(lstar,nftaddress,banned) values(%s,'%s',%s)" % \
          (lstar,nftaddress,banned)
    print(sql)
    rows = cursor.execute(sql)
    conn.commit()

def get_account_address_by_token_restored_msyql(address):
    total_address_account = _get_account_num_by_token(address)
    time.sleep(1)
    print('please waite , it need time to waite get reponse data')
    url = 'https://' + baseURL + 'token/holders?tokenAddress=' + address + '&limit='+str(total_address_account)

    response = requests.get(url=url, headers=header)
    all_account_address = json.loads(response.content.decode())['data']
    # print(all_account_address)
    for i in all_account_address:
        # get_NFT_token_list_by_owner(i['owner'])
        print(i['owner'])
        sql = "insert into Owner(owneraddress,status) values('%s',%d)" % \
              (i['owner'], 0)
        print(sql)
        cursor.execute(sql)
        conn.commit()
        print('成功插入', i['owner'])

    print('from onwer we can get SPL token balance,it include LSTAR and NFT')
    print('finnish')

async def get_NFT_token_address_by_mysql():
    sql = "select * from Owner"
    row_count = cursor.execute(sql)
    result = cursor.fetchall()

    for k in range(len(result)-1,0,-10):
        print(' 第 k 轮 --  ',k)

        task_list = []

        for i in range(0,10):
            task = asyncio.create_task(get_nft_address(result[k-i][0]))
            task_list.append(task)
        done, pending = await asyncio.wait(task_list, timeout=None)
            # 得到执行结果
        if done == 'owneraddress error':
            continue

        for done_task in done:
             # print(f"{time.time()} 得到执行结果 {done_task.result()}")
             try:
                token_list = json.loads(done_task.result()[0])
                owneraddress=done_task.result()[1]
             except:
                 continue
             USDC = 0
             LSTAR = 0
             for i in token_list:
                 if i['tokenName'] == 'USD Coin':
                     USDC = i['tokenAmount']['uiAmountString']
                     # print('USD Coin balance is ',USDC)
                 if i['tokenName'] == 'Learning Star':
                     LSTAR = i['tokenAmount']['uiAmountString']

             for i in token_list:
                # print(i)
                nft = ''
                if i['tokenAmount']['amount'] == '1' and i['tokenAmount']['decimals'] == 0 and i['tokenAmount']['uiAmountString'] == '1' and i['tokenName'] ==''  and i['tokenIcon'] == '':
                    print('NFT address is',i['tokenAddress'])
                    nft = i['tokenAddress']
                    try:
                        sql = "insert into NFTcontract(owneraddress,nftaddress,status,lstar,usdc) values('%s','%s',%d,%s,%s)" % \
                              (owneraddress, nft, 0,LSTAR,USDC)
                        cursor.execute(sql)
                        conn.commit()
                    except:
                        print('插入错误')
        time.sleep(10)

async def get_nft_address(ownerAddress):
    '''
    this is async fuction for get nft addres.
    :param owneraddress:
    :return:
    '''
    url = 'https://' + baseURL + 'account/tokens?account=' + ownerAddress
    # we will get the 'USD Coin' and 'Learning Star'
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url=url, headers=header, timeout=15) as response:
                #print(await response.text()),
                return await response.text(),ownerAddress
        except:
            return ('owneraddress error')



async def get_nft_uri_by_mysql():
    sql = "select * from NFTcontract"
    row_count = cursor.execute(sql)
    result = cursor.fetchall()

    for k in range(len(result)-1,0,-10):
        print(' 第 k 轮 --  ',k)

        task_list = []

        for i in range(0,10):
            task = asyncio.create_task(get_nft_uri_async(result[k-i][1]))
            task_list.append(task)
        done, pending = await asyncio.wait(task_list, timeout=None)
            # 得到执行结果
        print(done)
        if done == 'owneraddress error':
            continue

        for done_task in done:
             # print(f"{time.time()} 得到执行结果 {done_task.result()}")
             try:
                token_list = json.loads(done_task.result()[0])
                nftaddress=done_task.result()[1]
                uri = token_list['data']['metadata']['data']['uri']
                print('uri is',uri)
                print('nfraddress',nftaddress)

                try:
                    sql = "insert into NFTUri(nftaddress,uri,status) values('%s','%s',%d)" % \
                          (nftaddress,uri,0)
                    cursor.execute(sql)
                    conn.commit()
                except:
                    print('插入错误')

             except:
                 continue

        time.sleep(10)

async def get_nft_uri_async(NFTaddress):
    url = 'https://api.solscan.io/account?address=' + NFTaddress
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url=url, headers=header, timeout=15) as response:
                # print(await response.text()),
                return await response.text(), NFTaddress
        except:
            return ('owneraddress error')



async def test():
    url = "https://www.cnblogs.com/yoyoketang/"
    task_list = []
    for i in range(10):
        task = asyncio.create_task(get_nft_address(url))
        task_list.append(task)
    done, pending = await asyncio.wait(task_list, timeout=None)
    # 得到执行结果
    for done_task in done:
        print(f"{time.time()} 得到执行结果 {done_task.result()}")



#  -- 异步  -- 获取  nft address
# start_time = time.time()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(get_NFT_token_address_by_mysql())
# print("总耗时: ", time.time()-start_time)

#  -- 异步  -- 获取  nft url
start_time = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(get_nft_uri_by_mysql())
print("总耗时: ", time.time()-start_time)

#  --  run
# get_account_address_by_token(tokenAddress)
# get_account_address_by_token_restored_msyql(tokenAddress)
# mysql_get_oneline()
# get_NFT_token_address_by_mysql()

#  --   test
# get_mysql_inser_different_boo_int_char_test()
# get_NFT_token_list_by_owner_test()
# get_NFT_uri_test()
# get_NFT_totalInfo_by_Uri_test()
# mysql_insert_test()