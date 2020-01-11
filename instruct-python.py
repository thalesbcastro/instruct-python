import requests
import csv
import sys


def gravar_no_csv(email, website, hemisferio, username):
    fieldnames = ['email', 'website', 'hemisferio', 'username']

    try:
        # Se não levantar a exceção, é porque ainda não foi criado, sendo necesário criar o cabeçalho
        with open('jsonplaceholder.csv') as f:
            # Caso o arquivo já tenha sido criado, gravar com o mode='a'
            print('-----\nAdicionando dados novos ao arquivo-----')
            fieldnames = ['email', 'website', 'hemisferio', 'username']
            with open('jsonplaceholder.csv', mode='a', newline='', encoding='utf-8') as f:
                wa = csv.DictWriter(f, fieldnames=fieldnames)
                wa.writerow({'email': email, 'website': website, 'hemisferio': hemisferio, 'username': username})

    except FileNotFoundError:
        # Caso o arquivo ainda não foi aberto/criado, cria-se um com o cabeçalho e a primeira linha
        print('\n-----O arquivo .csv foi criado.-----')
        fieldnames = ['email', 'website', 'hemisferio', 'username']
        with open('jsonplaceholder.csv', mode='w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerow({'email': email, 'website': website, 'hemisferio': hemisferio, 'username': username})


def hemisferio(lat):
    lat = float(lat)
    if lat == 0:
        return 'Linha do Equador'
    elif lat > 0:
        return 'Norte'
    else:
        return 'Sul'


def func_request(username):
    print('-----Usando o Request para consultar-----\n')
    url = 'https://jsonplaceholder.typicode.com/users'

    try:
        reponse = requests.get(url)
        reponse.raise_for_status()
        jsonResponse = reponse.json()

        for x in jsonResponse:
            if x['username'] == username:
                print('e-mail:', x['email'])
                print('website:', x['website'])
                hm = hemisferio(x['address']['geo']['lat'])
                print('hemisfério (norte ou sul):', hemisferio(x['address']['geo']['lat']))
                gravar_no_csv(x['email'], x['website'], hm, x['username'])

    except requests.exceptions.HTTPError as ErroHttp:
        print("Erro HTTP: ", ErroHttp)
    except requests.exceptions.ConnectionError as ErroConect:
        print("Erro de conexão: ", ErroConect)
    except requests.exceptions.RequestException as OutroErro:
        print("Algum outro erro: ", OutroErro)


if __name__ == '__main__':

    username = sys.argv[1]
    try:
        # Quando da primeira vez, não vai existir o arquivo, uma exeção será levantada, e a funcção func_request deve
        # ser chamada Se existir o arquivo, deve procurar primeiro nele. Caso encontre, imprime o que se quer e dar
        # sai do programa Caso contrário, chama a função func_request para pegar lá no Link

        with open('jsonplaceholder.csv') as f:
            readed = csv.reader(f)
            for x in readed:
                if x[-1] == username:
                    print("---------Usuário em cache--------\n")
                    print('e-mail:', x[0])
                    print('website:', x[1])
                    print('Hemisfério:', (x[2]))
                    sys.exit()
            func_request(username)
    except FileNotFoundError:
        func_request(username)
