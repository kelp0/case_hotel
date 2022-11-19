#Работу выполинили Лысенко Матвей 80%, Ячин Денис 45%
from random import randint

#Reading a hotel information file
a = open('fund.txt', 'r', encoding = 'utf-8')
rooms = a.readlines()
a.close()
rooms_available = []


#Setting prices for rooms
def RoomPrices(rooms):
    for element in rooms:
        price = 0
        if '\n' in element:
            element = element[0:-1]
        el = element.split(' ')
        if el[1] == 'одноместный':
            price += 2900
        elif el[1] == 'двухместный':
            price += 2300
        elif el[1] == 'полулюкс':
            price += 3200
        elif el[1] == 'люкс':
            price += 4100

        if el[3] == 'стандарт_улучшенный':
            price = price*1.2
        elif el[3] == 'апартамент':
            price = price*1.5

        element += ' ' + str(int(price))
        rooms_available.append(element)
        
RoomPrices(rooms)

dict_rooms = []


#Creating a list of dictionaries containing information about rooms
def ListOfRooms(rooms_available):
    for element in rooms_available:
        
        l = element.split()
        number = l[0]
        tip = l[1]
        places = l[2]
        quality = l[3]
        price = l[4]

        element = {'Номер':number,'Тип':tip,'Места':places,'Качество':quality,'Цена':price}
        dict_rooms.append(element)
        
ListOfRooms(rooms_available)

b = open('booking.txt', 'r', encoding='utf-8')
clients = b.readlines()
b.close()

dict_clients = []

#Creating a list of dictionaries containing information about clients
def ListOfClients(clients):
    for element in clients:
        
        if '\n' in element:
            element = element[0:-1]
            
        l = element.split()
        date_b = l[0]
        name = l[1] + ' ' + l[2] + ' ' + l[3]
        people = l[4]
        date_v = l[5]
        days = l[6]
        money = l[7]

        element = {'Бронь':date_b,'Имя':name,'Человек':people,'Въезд':date_v,'Суток':days,'Денег':money}
        dict_clients.append(element)
        
ListOfClients(clients)


class Hotel:
    '''This is a class of hotel rooms'''
    def __init__(self, tip = 'None', places = 'None', quality = 'None', price = 'None', available = 'None', availability_date = 'None'):
        '''Initializes rooms'''
        self.tip = tip
        self.places = places
        self.quality = quality
        self.price = price
        self.available = available
        self.availability_date = availability_date


#Creating class instances
items = []
for i in range(len(dict_rooms)):
    dict_rooms[i]['Номер'] = Hotel(dict_rooms[i]['Тип'], dict_rooms[i]['Места'], dict_rooms[i]['Качество'], dict_rooms[i]['Цена'], '1', dict_clients[0]['Бронь'])
    items.append(i)


#Counting the total number of rooms
free_s = 0
odnomestny_s = 0
dvuhmestny_s = 0
polulux_s = 0
lux_s = 0
rooms_s = 0
day = dict_clients[0]['Бронь']
for i in items:
    if int(dict_rooms[i]['Номер'].availability_date[0:2]) <= int(day[0:2]):
        free_s += 1
    if dict_rooms[i]['Номер'].tip == 'одноместный':
        odnomestny_s += 1
    elif dict_rooms[i]['Номер'].tip == 'двухместный':
        dvuhmestny_s += 1
    elif dict_rooms[i]['Номер'].tip == 'полулюкс':
        polulux_s += 1
    elif dict_rooms[i]['Номер'].tip == 'люкс':
        lux_s += 1
    rooms_s += 1


clients_s = 0
for i in dict_clients:
    clients_s += 1


#The main function    
day = dict_clients[0]['Бронь']
new_day = ''
total_day = 0
total_day_losses = 0
def Booking(dict_clients, total_day=0, total_day_losses = 0, day = dict_clients[0]['Бронь'], new_day = ''):
    for element in dict_clients:
                
        #Checking numbers available
        fit_numbers_av = []
        for i in items:
            if int(dict_rooms[i]['Номер'].availability_date[0:2]) <= int(element['Въезд'][0:2]):
                fit_numbers_av.append(i)
                

        #Checking numbers which have enough places
        fit_numbers_pl = []
        fit_numbers_pl_2 = []
        for i in fit_numbers_av:
            if dict_rooms[i]['Номер'].places == element['Человек']:
                fit_numbers_pl.append(i)
        if len(fit_numbers_pl) == 0:
            for i in fit_numbers_av:
                if dict_rooms[i]['Номер'].places > element['Человек']:
                    fit_numbers_pl_2.append(i)
                    

        #Getting the best room that fits client's budget
        max_price = 0
        max_room = -1
        min_price = 100000000000
        if len(fit_numbers_pl) != 0:
            for i in fit_numbers_pl:
                if int(dict_rooms[i]['Номер'].price) > int(max_price) and int(dict_rooms[i]['Номер'].price) <= int(element['Денег']):
                    max_price = int(dict_rooms[i]['Номер'].price)
                    max_room = i
            overall = max_price
        elif len(fit_numbers_pl) == 0:
            for i in fit_numbers_pl_2:
                if 0.7*int(dict_rooms[i]['Номер'].price) < int(min_price) and int(dict_rooms[i]['Номер'].price) <= int(element['Денег']):
                    min_price = 0.7*int(dict_rooms[i]['Номер'].price)
                    max_room = i
            overall = min_price


        #Installing a meal package for a customer
        if max_room != -1:
            money_left = int(element['Денег']) - int(dict_rooms[max_room]['Номер'].price)
            if money_left >= 1000:
                food = 'Полупансион'
                price = 1000
            elif 280 <= money_left < 1000:
                food = 'Завтрак'
                price = 280
            elif money_left < 280:
                food = 'Без питания'
                price = 0

                
        #Receiving refusal or consent of the client with a chance of 25 and 75%, respectively
        agree = randint(1,4)
        if agree != 4:
            condition = 'Клиент согласен. Номер забронирован.'
        elif agree == 4:
            condition = 'Клиент отказался от варианта.'


        #Making the room unavailable for the time client lives there and counting day revenue and losses
        if max_room != -1 and agree != 4:
            
            if int(element['Въезд'][0:2]) + int(element['Суток']) > 9:
                date_quit = str(int(element['Въезд'][0:2]) + int(element['Суток']))+element['Въезд'][2:]
            elif int(element['Въезд'][0:2]) + int(element['Суток']) < 10:
                date_quit = '0' + str(int(element['Въезд'][0:2]) + int(element['Суток']))+element['Въезд'][2:]

            dict_rooms[max_room]['Номер'].availability_date = date_quit

            total_for_person = price + overall
            total_day += total_for_person
            total_day_losses += int(element['Денег']) - total_for_person
        elif max_room != -1 and agree == 4:
            total_for_person = price + int(dict_rooms[max_room]['Номер'].price)
            total_day_losses += total_for_person


        #Allowance for a discount for a room with a larger capacity than necessary
        if max_price == 0 and min_price != 0:
            total_day_losses += 0.3*int(dict_rooms[max_room]['Номер'].price)


        #Displaying customer information
        if max_room != -1:
            print('--------------------------------------------------------------------------------------')
            print()
            print('Поступила заявка на бронирование:')
            print(element['Бронь'], element['Имя'], element['Человек'], element['Въезд'], element['Суток'], element['Денег'])
            print()
            print('Найден:')
            print()
            print('Номер: ',(max_room+1))
            print('Количество мест: ',dict_rooms[max_room]['Номер'].places)
            print('Степень комфортности: ',dict_rooms[max_room]['Номер'].quality)
            print('Вместительность номера: ',dict_rooms[max_room]['Номер'].places, ' чел.')
            print('Фактически: ', element['Человек'], ' чел.')
            print('Питание: ', food)
            print('Стоимость: ',total_for_person,' руб./сутки')
            print()
            print(condition)
        elif max_room == -1:
            print('--------------------------------------------------------------------------------------')
            print()
            print('Поступила заявка на бронирование:')
            print(element['Бронь'], element['Имя'], element['Человек'], element['Въезд'], element['Суток'], element['Денег'])
            print()
            print('Предложений по данному запросу нет. В бронировании отказано.')



        #Output statistics for the day
        new_day = element['Бронь']
        if new_day != day or element == dict_clients[clients_s-1]:
            free = 0
            busy = 0
            dvuhmestny = 0
            odnomestny = 0
            polulux = 0
            lux = 0
            for i in items:
                if int(dict_rooms[i]['Номер'].availability_date[0:2]) <= int(day[0:2]):
                    free += 1
                    if dict_rooms[i]['Номер'].tip == 'одноместный':
                        odnomestny += 1
                    elif dict_rooms[i]['Номер'].tip == 'двухместный':
                        dvuhmestny += 1
                    elif dict_rooms[i]['Номер'].tip == 'полулюкс':
                        polulux += 1
                    elif dict_rooms[i]['Номер'].tip == 'люкс':
                        lux += 1
            print('=====================================================================================================================')
            print('Итог за ',day)
            print()
            print('Количество занятых номеров: ', rooms_s - free)
            print()
            print('Количество свободных номеров: ', free)
            print()
            print('Занятость по категориям:')
            print()
            print('Одноместных: ', odnomestny_s - odnomestny, ' из ', odnomestny_s)
            print()
            print('Двухместных: ', dvuhmestny_s - dvuhmestny, ' из ', dvuhmestny_s)
            print()
            print('Полулюкс: ', polulux_s - polulux, ' из ', polulux_s)
            print()
            print('Люкс: ', lux_s - lux, ' из ', lux_s)
            print()
            print('Процент загруженности гостиницы: ', round(100-free/rooms_s*100, 2),'%')
            print()
            print('Доход за день: ', total_day)
            print()
            print('Упущенный доход: ',total_day_losses)
            day = new_day
            total_day = 0
            total_day_losses = 0
            
            

Booking(dict_clients)
