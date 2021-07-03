import psycopg2
conn = psycopg2.connect(dbname='titanic', user='passenger', password='mypass')
cur = conn.cursor()


cur.execute("""CREATE TABLE passengers(
    id integer,
    survived integer,
    class integer,
    name text,
    sex varchar(50),
    age varchar(50),
    sibsp integer,
    parch integer,
    ticket varchar(255),
    fare numeric NULL,
    cabin varchar(255) NULL,
    embarked varchar(50)
)
""")
with open(r'titanic.txt', 'r') as f:
    next(f)
    cur.copy_from(f, 'passengers', sep='|')
conn.commit()

#Имена погибших
def get_name_died():
    cur.execute('''SELECT name FROM passengers WHERE survived = 0''')
    rows = cur.fetchall()
    for i in rows:
        print(i)

get_name_died()

#Процент выживших женщин первого класса
def survived_womens_fclass():
    cur.execute('''SELECT COUNT(*) FROM passengers WHERE Sex = 'female' AND passengers.class = 1;
    ''')
    rows = cur.fetchone()[0]
    cur.execute('''SELECT COUNT(*) FROM passengers WHERE Sex = 'female' AND passengers.class = 1 AND survived = 1;
        ''')
    rows2 = cur.fetchone()[0]
    return rows2 * 100 / rows

print(survived_womens_fclass())

#Мужчин младше 20 лет третьего класса
def get_man_p20():
    cur.execute('''SELECT COUNT(*) FROM passengers WHERE sex = 'male' AND age < '20' AND passengers.class = 3;''')
    rows = cur.fetchone()[0]
    cur.execute('''SELECT COUNT(*) FROM passengers WHERE sex = 'male' AND age < '20' AND passengers.class = 3 AND survived = 1;''')
    rows2 = cur.fetchone()[0]
    return rows2 * 100 / rows

print(get_man_p20())

#Пассажиров второго класса старше 30 лет
def get_passenger_30y():
    cur.execute('''SELECT COUNT(*) FROM passengers WHERE age > '30' AND passengers.class = 2;''')
    rows = cur.fetchone()[0]
    cur.execute('''SELECT COUNT(*) FROM passengers WHERE age < '30' AND passengers.class = 2 AND survived = 1;''')
    rows2 = cur.fetchone()[0]
    return rows2 * 100 / rows

print(get_passenger_30y())

#Процент выживших женщин с порта Чербург
def get_woman_embarked_c():
    cur.execute('''SELECT COUNT(*) FROM passengers WHERE sex = 'female' AND passengers.class = 2 AND embarked= 'C' AND survived = 1;''')
    rows = cur.fetchone()[0]
    cur.execute('''SELECT COUNT(*) FROM passengers WHERE sex = 'female' AND passengers.class = 2 AND embarked = 'C';''')
    rows1 = cur.fetchone()[0]
    return rows * 100 / rows1

print(get_woman_embarked_c())
#Пассажиров имевших на борту братьев или сестёр
def get_sibl():
    cur.execute('''SELECT COUNT(*) FROM passengers WHERE sibsp = 1;''')
    rows = cur.fetchone()[0]
    cur.execute('''SELECT COUNT(*) FROM passengers WHERE sibsp = 1 AND survived = 0;''')
    rows1 = cur.fetchone()[0]
    return rows1 * 100 / rows

print(get_sibl())

#Средний возраст  погибших людей
def get_avg():
    cur.execute("SELECT AVG(CAST(age AS FLOAT)) FROM passengers WHERE survived = 0 and age > '0';")

    return cur.fetchall()[0][0]

print(get_avg())





#Порт с наибольшим шансом

cur.execute('''SELECT COUNT(*) FROM passengers WHERE embarked = 'C';''')
cherbourg_total = cur.fetchone()[0]
cur.execute('''SELECT COUNT(*) FROM passengers WHERE embarked = 'C' AND survived = 1;''')
cherbourg_d = cur.fetchone()[0]
cherbourg = cherbourg_d * 100 / cherbourg_total

cur.execute('''SELECT COUNT(*) FROM passengers WHERE embarked = 'Q';''')
queenstown_total = cur.fetchone()[0]
cur.execute('''SELECT COUNT(*) FROM passengers WHERE embarked = 'Q' AND survived = 1;''')
queenstown_d = cur.fetchone()[0]
queenstown = queenstown_d * 100 / queenstown_total


cur.execute('''SELECT COUNT(*) FROM passengers WHERE embarked = 'S';''')
southampton_total = cur.fetchone()[0]
cur.execute('''SELECT COUNT(*) FROM passengers WHERE embarked = 'S' AND survived = 1;''')
southampton_d = cur.fetchone()[0]
southampton = southampton_d * 100 / southampton_total

lucky_port = {
    'Cherbourg': cherbourg,'Southampton': southampton,'Queenstown': queenstown
}

lst = [cherbourg,southampton,queenstown]
lst.sort()
for key,value in lucky_port.items():
    if value == lst[len(lst)-1]:
        print(f'Luckiest port is: {key}')


cur.close()
conn.close()