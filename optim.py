def getFuelPrice(e):
    return e['fuelPrice'], e['distanceOrigin']

def getDistanceOrigin(e):
    return e['distanceOrigin']

cities = [
    {
        'id': '01',
        'fuelPrice': 5.82,
        'distanceOrigin': 0
    },
    {
        'id': '02',
        'fuelPrice': 5.92,
        'distanceOrigin': 2000
    },
    {
        'id': '03',
        'fuelPrice': 5.70,
        'distanceOrigin': 2200
    },
    {
        'id': '04',
        'fuelPrice': 5.72,
        'distanceOrigin': 2350
    },
    {
        'id': '05',
        'fuelPrice': 5.84,
        'distanceOrigin': 4000
    }
]

def findNextStop(cities, currentCity, kmDisponivel, kmMinimoDisponivel, kmMinimoAbastecimento):
    #print(cities)

    #Obtem a cidade mais barata
    city = cities[0]
    print('cidade Analise: ' + str(city))

    currentDistance = currentCity['distanceOrigin']

    responseStop = {'status' : '', 'mensage' : '', 'city' : ''}

    if kmDisponivel > (city['distanceOrigin'] - currentDistance + kmMinimoDisponivel):
        print('é possivel chegar')

        if (kmDisponivel - (city['distanceOrigin'] - currentDistance) ) > kmMinimoAbastecimento:
            print('Nao necessario abastecer')  #Analisar se compensa

            #remove cidade anteriores
            auxCities = list(filter(lambda auxcity: auxcity['distanceOrigin'] > city['distanceOrigin'], cities))
            #print(cities)
            #print(auxCities)
            if len(auxCities) > 0:
                responseStop = findNextStop(auxCities, currentCity, kmDisponivel, kmMinimoDisponivel, kmMinimoAbastecimento)
            else:
                #print('NÃO TEM MAIS OPCAO')
                responseStop['status'] = '02'
                responseStop['mensage'] = 'Abastecer - NÃO TEM MAIS OPCAO'
                responseStop['city'] = city

        else:
            print('abastecer')
            responseStop['status'] = '02'
            responseStop['mensage'] = 'Abastecer'
            responseStop['city'] = city

    else:
        print('NÃO é possivel chegar')

        #remove cidade posteriores
        auxCities = list(filter(lambda auxcity: auxcity['distanceOrigin'] < city['distanceOrigin'], cities))

        if len(auxCities) > 0:
            responseStop = findNextStop(auxCities, currentCity, kmDisponivel, kmMinimoDisponivel, kmMinimoAbastecimento)
        else:
            print('NÃO TEM MAIS OPCAO')

            responseStop['status'] = '01'
            responseStop['mensage'] = 'Rota não pode ser realizada'
            responseStop['city'] = ''

    #return city
    return responseStop



def optim(cities, veiculo):

    kmMinimoDisponivel      = round( (veiculo['volumeTanque'] * 0.1) * veiculo['consumo'], 2) * 1000
    kmMinimoAbastecimento   = round( (veiculo['volumeTanque'] * 0.4) * veiculo['consumo'], 2) * 1000
    kmTotalTanque           = round( veiculo['volumeTanque'] * veiculo['consumo'], 2) * 1000

    litrosAtuais    = veiculo['volumeTanque'] * veiculo['percentualTanque']
    kmDisponivel    = round(litrosAtuais * veiculo['consumo'], 2) * 1000
    
    response = {'status' : '', 'mensage' : '', 'cities' : []}
    listStopsCities = []
    
    if kmDisponivel > (cities[-1]['distanceOrigin'] + kmMinimoDisponivel):
        response['status'] = '01'
        response['mensage'] = 'Viagem não necessita abastecimento'
    else:
        #Ordena por preço e distancia
        currentCity = cities[0]
        cities.sort(key=getFuelPrice)
        count = 0

        print('kmMinimoDisponivel: ' + str(kmMinimoDisponivel))
        print('kmMinimoAbastecimento: ' + str(kmMinimoAbastecimento))
                
        while len(cities) > 0 and count < 100:
            count = count + 1
            print('kmDisponivel: ' + str(kmDisponivel))
            print('cidade atual: ' + str(currentCity))

            nextStopCity = findNextStop(cities, currentCity, kmDisponivel, kmMinimoDisponivel, kmMinimoAbastecimento)

            print(nextStopCity)#['city']['cityName']
            
            print('AQUIIIIIIIIIII: ')
            print(nextStopCity['status'])

            if nextStopCity['status'] == '01':
                cities = []

            if nextStopCity['status'] == '02':
                auxCity = nextStopCity['city']
                

                kmRestanteTanque    = round(kmDisponivel - auxCity['distanceOrigin'], 2)
                kmAbastecer         = round(kmTotalTanque - kmRestanteTanque, 2)
                kmDisponivel        = kmTotalTanque
                currentCity         = auxCity

                #auxCity['kmAbastecido'] = round((kmAbastecer / 1000) / veiculo['consumo'], 2)
                auxCity['litroAbastecido'] = round((kmAbastecer / 1000) / veiculo['consumo'], 2)

                listStopsCities.append(auxCity)

                #km = consumo * tanque -> 200km * 1000 -> 200.000
                #tanque = (km / 1000) / consumo 

                #remove cidade anteriores
                cities = list(filter(lambda auxcity: auxcity['distanceOrigin'] > auxCity['distanceOrigin'], cities))
            
    #response['status'] = '02'
    response['cities'] = listStopsCities
    
    return response




#optim(cities, veiculo)
