#!/usr/bin/env python3

import sqlite3
import datetime

dbname = "oos.sqlite"

# period of 12 months
period = 12

# harcoded project id2
project_ids = [1]

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

def generate_data(dbname, project_ids, period):
    # create an array <period> in length
    # initially populated with all 0s
    data = {}

    now = datetime.datetime.now()
    year = now.year
    month = now.month

    with sqlite3.connect(dbname) as conn:
        for project_id in project_ids:
            # get project name
            row = conn.execute('''select name from project where id = ?''', (project_id,))
            row = row.fetchone()

            if row is None:
                print("Error: failed to find project with id '%d'" %(project_id))
                return []

            project_name = row[0]

            project_data = []
            for i in range(period):
                project_data.append(0)

            months = {}

            for row in conn.execute('''select month, commits_in_period from project_stats where project_id = ? order by month desc limit ?''', (project_id, period)):
                monstr = row[0]
                commits_in_period = row[1]
                months[monstr] = commits_in_period

        monstr = "%.4d-%.2d" %(year, month)
        initial_date = monstr

        for i in range(period):
            if monstr in months:
                # add from back
                project_data[-(i+1)] = months[monstr]
            monstr = prev_month(monstr)

        # note this is 'off by one'
        # this is desirable due to js data handling
        final_date = monstr

        data[project_name] = {
                            "from": final_date,
                            "to": initial_date,
                            "contents": project_data,
                             }

    return data


def output_data(data, output_path):
    output = []
    output.append( '''var dataset = [\n''' )

    for project_name in data.keys():
        project_data = data[project_name]

        dfrom = project_data["from"]
        dto = project_data["to"]
        contents = project_data["contents"]

        output.append( '''    { project: "%s", ''' %(project_name) )
        output.append( ''' data_from: "%s", ''' %(dfrom) )
        output.append( ''' data_to: "%s", ''' %(dto) )
        output.append( ''' data : [ ''' )
        for i in range(len(contents)):
            output.append( '''%d, ''' %(contents[i]) )
        output.append( '''], ''')
        output.append( '''},\n''' )

    output.append( '''];\n''' )

    with open(output_path, 'w') as file:
        file.writelines(output)

if __name__ == "__main__":

    data = generate_data(dbname, project_ids, period)
    output_data(data, output_path)

