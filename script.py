import pandas as pd
import flask
header_list = ['geonameid', "name", "asciiname",
               "alternatenames", "latitude", "longitude",
               "feature_class", "feature_code", "country_code",
               "cc2", "admin1_code", "admin2_code",
               "admin3_code", "admin4_code", "population",
               "elevation", "dem", "timezone",
               "modification_date"]  # Create list with names of columns(Создаю лист с именами колонок)

all_city = pd.read_csv("http://download.geonames.org/export/dump/RU.zip",compression='zip', sep="\t", names=header_list,
                       low_memory=False)  # save RU.txt as DataFrame(Создаю датафрейм с данными из RU.txt)
all_city = all_city.query("feature_class=='P'")  # choose only cities(Оставляю города)
all_city["alternatenames"] = all_city["alternatenames"].fillna(" ")
# rename all "NaN" in column "alternatenames" to " "(все значения NaN в колонке alternatenames заменяем на " ")
app = flask.Flask(__name__)


@app.route('/')  # create home page
def Hello():
    result = '<html><body><div align="center"><form action="/City" method="POST">'
    result += '<p>1method. geonameid<input name="geonameid" type="text" value=""/></p>'  # 1 method
    result += '<input type="submit" value="1"/>'
    result += '</form>'
    result += '<div align="center"><form action="/Book" method="POST">'  # 2 method
    result += '<p>2method. Page<input name="Page" type="text" value=""/></p>'
    result += '<p> Count<input name="Count" type="text" value=""/></p>'
    result += '<input type="submit" value="2"/>'
    result += '</form>'
    result += '<div align="center"><form action="/Twocity" method="POST">'  # 3 method
    result += '<p>3method. First city<input name="First" type="text" value=""/></p>'
    result += '<p> Second city<input name="Second" type="text" value=""/></p>'
    result += '<input type="submit" value="3"/>'
    result += '</form>'
    result += '<div align="center"><form action="/Help" method="POST">'  # 4 method
    result += '<p>4method. Beginning<input name="temp" type="text" value=""/></p>'
    result += '<p> name or altname<input name="Name" type="text" value=""/></p>'
    result += '<input type="submit" value="HELP"/>'
    result += '</form>'
    result += '</form></div></body></html>'  # create simple HTML template
    return result


@app.route('/City', methods=['POST'])
# 1st method
def City():
    try:  # check data format(Проверка что формат данных верен)
        City = all_city.iloc[all_city.geonameid.values == int(flask.request.form['geonameid'])]
        # search geonameid in all_city(Нахожу нужный элемент)
        if City.empty:  # check if City is empty or not(Проверяю нашeлся ли такой id)
            return "Try another id"
        else:
            return City.to_html(justify="left",
                                index_names=False)  # print City in HTML format(печатаю в html формате найденый город)
    except:
        return "Please check you data"


@app.route('/Book', methods=['POST'])
# 2nd method
def Book():
    try:  # check data format(Проверка что формат данных верен)
        page = int(flask.request.form['Page'])
        # processing request of page(обработка запроса введённой страницы)
        count = int(flask.request.form['Count'])
        # processing request of count(обработка запроса введённого числа городов)
        if count <= 0 or page <= 0:
            return "Count and page can't be Zero or negative number"
        else:
            number_of_pages = all_city.shape[0] // count
            # calculating number of pages in the book (нахождение кол-ва страниц в книге)
            if all_city.shape[0] % count != 0:
                number_of_pages = number_of_pages + 1
            if page > number_of_pages:
                return "Page doesn't exist"
            else:
                if page == number_of_pages:
                    return all_city.iloc[(page - 1) * count:].to_html(justify="left",
                                                                      index_names=False)
                    # return last page from the book(отправляем последнюю страницу)
                else:
                    return all_city.iloc[(page - 1) * count: (page) * count].to_html(justify="left",
                                                                                     index_names=False)
                    # return requested page from the book(отправляем нужную страницу)
    except:
        return "Please check you data"


@app.route('/Twocity', methods=['POST'])
# 3hd method
def Twocity():
    First_city = "^" + flask.request.form['First'] + "," + "|" + "^" + flask.request.form['First'] + "$" + "|"
    First_city += "," + flask.request.form['First'] + "$" + "|" + "," + flask.request.form['First'] + ","
    # create Regex for the 1st city (Создаю регулярное выражение)
    Second_city = "^" + flask.request.form['Second'] + "," + "|" + "^" + flask.request.form['Second'] + "$" + "|"
    Second_city += "," + flask.request.form['Second'] + "$" + "|" + "," + flask.request.form['Second'] + ","
    # Regex for the 2nd city
    First_city = all_city[all_city["alternatenames"].str.contains(First_city,
                                                                  regex=True)]
    # find all cities which have alternatenames=First_city(Нахожу все города которые имеют alternatenames=First_city )
    Second_city = all_city[all_city["alternatenames"].str.contains(Second_city, regex=True)]
    if Second_city.empty or First_city.empty:  # if empty or not(Проверяю нашлись ли такие города)
        return "Please check you data"
    else:
        Second_city = Second_city.sort_values(by=["population", "geonameid"], ascending=[False,
                                                                                         True])
        # Sort by population and geonameid(сортирую по убыванию популяции и далее по индексам)
        First_city = First_city.sort_values(by=["population", "geonameid"], ascending=[False, True])
        Result = pd.concat([First_city.iloc[[0]], Second_city.iloc[[0]]])
        # choose first element from First_city and Seond_city(Выбираю первый город из обоих Дата фреймов)

        if Result["latitude"].iloc[0] > Result["latitude"].iloc[1]:
            # find which city is north ( нахожу какой из городов севернее)
            North = Result["name"].iloc[0]
        else:
            North = Result["name"].iloc[1]
        if Result["timezone"].iloc[0] == Result["timezone"].iloc[1]:
            # check if the same timezone(Одинаковые ли временные зоны)
            return Result.to_html() + "Northen city : " + North + ". Same timezone "
        else:
            TimeZone = {'Europe/Moscow': 3, 'Europe/Astrakhan': 4, 'Asia/Yekaterinburg': 5, 'Asia/Aqtobe': 5,
                        'Europe/Riga': 3, 'Europe/Samara': 4, 'Europe/Volgograd': 4, 'Europe/Saratov': 4,
                        'Europe/Kirov': 3, 'Europe/Ulyanovsk': 4, 'Europe/Kaliningrad': 2, 'Europe/Kiev': 3,
                        'Europe/Helsinki': 3, '0': 0, 'Europe/Vilnius': 3, 'Asia/Irkutsk': 8, 'Europe/Minsk': 3,
                        'Asia/Krasnoyarsk': 7, 'Europe/Simferopol': 3, 'Asia/Tbilisi': 4, 'Europe/Zaporozhye': 3,
                        'Europe/Oslo': 2, 'Asia/Baku': 4, 'Asia/Novosibirsk': 7, 'Asia/Barnaul': 7,
                        'Asia/Novokuznetsk': 7, 'Asia/Omsk': 6, 'Asia/Tomsk': 7, 'Asia/Ulaanbaatar': 8,
                        'Asia/Qyzylorda': 5, 'Asia/Hovd': 7, 'Asia/Chita': 9, 'Asia/Yakutsk': 9,
                        'Asia/Vladivostok': 10, 'Asia/Sakhalin': 11, 'Asia/Shanghai': 8, 'Asia/Anadyr': 12,
                        'Asia/Magadan': 11, 'Asia/Khandyga': 9, 'Asia/Kamchatka': 12, 'Asia/Tokyo': 9,
                        'Asia/Srednekolymsk': 11, 'Asia/Ust-Nera': 10, 'Asia/Ashgabat': 5, 'Europe/Paris': 2,
                        'Europe/Tallinn': 3, 'Europe/Warsaw': 2, 'Asia/Tashkent': 5, 'Asia/Karachi': 5}
            # create dictionary for all Timezones using (all_city["timezone"].unique() and Geoname).
            # (Создал словарь со всевозможными timezones в all_city)
            TimeDiff = abs(TimeZone[Result["timezone"].iloc[0]] - TimeZone[
                Result["timezone"].iloc[1]])  # calculating the time difference(считаю разницу во времени)
            return Result.to_html() + "Northern city : " + North + \
                   ". Different timezones. Time difference : " + str(TimeDiff)


@app.route('/Help', methods=['POST'])
# 4th method
def Help():
    name = flask.request.form['Name']  # processing request of page(обработка запроса введённой страницы)
    if name == "alternatenames":  # searching in alternatenames(если поиск задан по alternatenames)

        Template = "," + flask.request.form['temp'] + "|" + "^" + flask.request.form['temp']
        # create regex(создаем регулярное выражение)
        Help = all_city[all_city["alternatenames"].str.contains(Template,
                                                                regex=True)]
        # find all cities which alternatenames begin with template(находим города, имена которых начинаются с template)
        Help = Help.sort_values(by="population", ascending=False)  # Sort by population (сортирую по убыванию популяции)
        if len(Help) > 0:
            return Help[["geonameid",
                         "alternatenames"]].to_html()
            # return HTML table with columns(geonameid,alternatenames).(вывожу таблицу с колонками (geonameid,alternatenames))
        else:
            return "Not found alternatenames such as " + flask.request.form['temp']
    elif name == "name":  # searching in alternatenames(если поиск задан по alternatenames)
        Template = "^" + flask.request.form['temp']  # look at the previous method(Аналогично предыдушему)
        Help = all_city[all_city["name"].str.contains(Template, regex=True)]
        Help = Help.sort_values(by="population", ascending=False)
        if len(Help) > 0:
            return Help[['geonameid',"name"]].to_html()
        else:
            return "Not found the name such as " + flask.request.form['temp']
    else:
        return "Please check you data"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
