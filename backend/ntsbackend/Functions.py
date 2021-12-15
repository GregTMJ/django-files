import datetime
import json

import pyodbc
from pyodbc import Error


class GetData:

    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

    def getInfo(self):
        try:
            established_connection = pyodbc.connect(
                "Driver={ODBC driver 17 for SQL server};"
                + "Server=tcp:192.100.1.93;"
                + "Database=ReportsDataBase;"
                + "UID=ReportsUser;"
                + "PWD=qwsxzaq;"
            )

            filename = 'static/example.json'

            cursor = established_connection.cursor()

            # В данном запросе мы получаем все доступные цеха для ремонта НКТ
            cursor.execute("SELECT t1.id, t1.Name , t2.Name, count(init.id) 'Количество ремонтных труб'"
                           "FROM [ReportsDataBase].[dbo].[ntsssdb_WorkStationTube] init "
                           f"left join [ReportsDataBase].[dbo].ntsssdb_TechUnit as t1 on t1.Id = init.TechUnitRef "
                           "left join [ReportsDataBase].dbo.ntsssdb_TechUnit as t2 on t2.Id = t1.RefToTopUnit "
                           " group by t1.Name, init.TechUnitRef, t2.Name,  t1.id "
                           "order by init.TechUnitRef")

            dict_of_techOp: dict[any] = {}
            list_of_techOp: list[any] = []

            for element in cursor:
                if element[1] == "Участок НК №1" or element[1] == "Участок НК №2" or element[1] == "Участок НК":
                    dict_of_techOp = {
                        'id': element[0],
                        'Название установки': element[1],
                        'Наименование цеха': element[2],
                        'Общее количество Обработанных труб': 0,
                        'Количество годных': 0,
                        'Количество брака': 0,
                        'Количество неопределённых': 0
                    }
                    list_of_techOp.append(dict_of_techOp)
                    dict_of_techOp = {}
                else:
                    dict_of_techOp = {
                        'id': element[0],
                        'Название установки': element[1],
                        'Наименование цеха': element[2],
                        'Общее количество Обработанных труб': 0,
                    }
                    list_of_techOp.append(dict_of_techOp)
                    dict_of_techOp = {}

            cursor.execute("SELECT t1.id, t1.Name , t2.Name, count(init.id) 'Количество ремонтных труб'"
                           "FROM [ReportsDataBase].[dbo].[ntsssdb_WorkStationTube] init "
                           f"left join [ReportsDataBase].[dbo].ntsssdb_TechUnit as t1 on t1.Id = init.TechUnitRef "
                           "left join [ReportsDataBase].dbo.ntsssdb_TechUnit as t2 on t2.Id = t1.RefToTopUnit "
                           " group by t1.Name, init.TechUnitRef, t2.Name,  t1.id "
                           "order by init.TechUnitRef")

            dict_of_Fact: dict[any] = {}
            list_of_fact: list[any] = []

            for element in cursor:
                dict_of_Fact[element[2]] = {}

                for n in list_of_techOp:
                    if element[2] == n['Наименование цеха']:
                        list_of_fact.append(n)

                dict_of_Fact[element[2]] = list_of_fact
                list_of_fact = []

            # with open(filename, mode='w', encoding='utf-8') as text:
            #     json.dump(dict_of_Fact, text, ensure_ascii=False)

            y = 1

            start_date = datetime.date(day=self.day, month=self.month, year=self.year)
            print(start_date)

            closure_date = start_date + datetime.timedelta(days=1)
            print(closure_date)

            # for i in range(1, y + 1):
            #     # Далее мы просто добавляем разницу в один н день для получения правильного запроса
            #     end_date = start_date + datetime.timedelta(days=i)
            #     close_date = start_date + datetime.timedelta(days=i - 1)

            # Данный формат необходим для запроса из БД
            startD = start_date.strftime("%Y/%d/%m")
            EndD = closure_date.strftime("%Y/%d/%m")
            date_used = start_date.strftime("%d/%m/%Y")

            cursor.execute(f"SELECT  t2.Name, t1.ID, count(init.Id) as 'Количество обработанных труб' "
                           "FROM [ReportsDataBase].[dbo].[ntsssdb_WorkStationTube] init "
                           "left join [ReportsDataBase].[dbo].ntsssdb_TechUnit as t1 on t1.Id = init.TechUnitRef "
                           "left join [ReportsDataBase].dbo.ntsssdb_TechUnit as t2 on t2.Id = t1.RefToTopUnit "
                           f"where init.AttachTime between '{startD}' and '{EndD}' "
                           "group by t1.ID, t2.Name order by t1.Id ")

            dict_of_data = {
                date_used: [dict_of_Fact]
            }

            for element in cursor:
                for key, value in dict_of_Fact.items():
                    if element[0] == key:
                        for lst in value:
                            if element[1] == lst["id"]:
                                lst["Общее количество Обработанных труб"] = element[2]

            cursor.execute(f"SELECT  t2.Name, t1.ID, count(init.Id) as 'Количество обработанных труб' "
                           "FROM [ReportsDataBase].[dbo].[ntsssdb_WorkStationTube] init "
                           "left join [ReportsDataBase].[dbo].ntsssdb_TechUnit as t1 on t1.Id = init.TechUnitRef "
                           "left join [ReportsDataBase].dbo.ntsssdb_TechUnit as t2 on t2.Id = t1.RefToTopUnit "
                           f"where init.AttachTime between '{startD}' and '{EndD}' and init.Result = 0 "
                           "group by t1.ID, t2.Name order by t1.Id ")

            for element in cursor:
                for key, value in dict_of_Fact.items():
                    if element[0] == key:
                        for lst in value:
                            if element[1] == lst["id"]:
                                lst["Количество неопределённых"] = element[2]

            cursor.execute(f"SELECT  t2.Name, t1.ID, count(init.Id) as 'Количество обработанных труб' "
                           "FROM [ReportsDataBase].[dbo].[ntsssdb_WorkStationTube] init "
                           "left join [ReportsDataBase].[dbo].ntsssdb_TechUnit as t1 on t1.Id = init.TechUnitRef "
                           "left join [ReportsDataBase].dbo.ntsssdb_TechUnit as t2 on t2.Id = t1.RefToTopUnit "
                           f"where init.AttachTime between '{startD}' and '{EndD}' and init.Result = 1 "
                           "group by t1.ID, t2.Name order by t1.Id ")

            for element in cursor:
                for key, value in dict_of_Fact.items():
                    if element[0] == key:
                        for lst in value:
                            if element[1] == lst["id"]:
                                lst["Количество годных"] = element[2]

            cursor.execute(f"SELECT  t2.Name, t1.ID, count(init.Id) as 'Количество обработанных труб' "
                           "FROM [ReportsDataBase].[dbo].[ntsssdb_WorkStationTube] init "
                           "left join [ReportsDataBase].[dbo].ntsssdb_TechUnit as t1 on t1.Id = init.TechUnitRef "
                           "left join [ReportsDataBase].dbo.ntsssdb_TechUnit as t2 on t2.Id = t1.RefToTopUnit "
                           f"where init.AttachTime between '{startD}' and '{EndD}' and init.Result = 2 "
                           "group by t1.ID, t2.Name order by t1.Id ")

            for element in cursor:
                for key, value in dict_of_Fact.items():
                    if element[0] == key:
                        for lst in value:
                            if element[1] == lst["id"]:
                                lst["Количество брака"] = element[2]

            dict_of_results = [dict_of_data]

            with open(filename, mode='w', encoding='utf-8') as text:
                json.dump(dict_of_results, text, ensure_ascii=False)

        except Error as e:
            print(e)

    def __del__(self):
        print("data deleted")


# x = GetData(25, 5, 2021)
# x.getInfo()
