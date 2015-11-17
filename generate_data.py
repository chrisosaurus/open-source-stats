#!/usr/bin/env python
import sqlite3
import datetime

dbname = "oos.sqlite"

# period of 12 months
period = 12

# FIXME harcoded project id
project_id = 1

output_path = "site/data.js"

def prev_month(monstr):
    (year, month) = monstr.split("-")
    year = int(year)
    month = int(month)

    month -= 1

    if month <= 0:
        month = 12
        year -= 1

    newmonstr = "%.4d-%.2d" %(year, month)
    return newmonstr

def generate_data(dbname, project_id, period):
    # create an array <period> in length
    # initially populated with all 0s
    data = []
    for i in range(period):
        data.append(0)

    months = {}

    with sqlite3.connect(dbname) as conn:
        for row in conn.execute('''select month, commits_in_period from project_stats where project_id = ? order by month desc limit ?''', (project_id, period)):
            monstr = row[0]
            commits_in_period = row[1]
            months[monstr] = commits_in_period

    now = datetime.datetime.now()
    year = now.year
    month = now.month

    monstr = "%.4d-%.2d" %(year, month)

    initial_date = monstr

    for i in range(period):
        if monstr in months:
            data[-i] = months[monstr]
        monstr = prev_month(monstr)

    # note this is 'off by one'
    # this is desirable due to js data handling
    final_date = monstr

    return {
            "from": final_date,
            "to": initial_date,
            "contents": data,
           }

def output_data(data, output_path):
    dfrom = data["from"]
    dto = data["to"]
    contents = data["contents"]

    output = []

    output.append( '''var dataset_from = "%s";\n''' %(dfrom) )
    output.append( '''var dataset_to = "%s";\n''' %(dto) )
    output.append( '''var dataset = [\n''' )
    for i in range(len(contents)):
        string = '''    %d''' %(contents[i])
        if i != (len(contents)-1):
            string += ","
        string += "\n"
        output.append(string)
    output.append( '''];\n''' )

    with open(output_path, 'w') as file:
        file.writelines(output)

if __name__ == "__main__":
    data = generate_data(dbname, project_id, period)
    output_data(data, output_path)

