#!/usr/bin/env python3

import sqlite3
import datetime

dbname = "oos.sqlite"

# period of 12 months
period = 12

output_path = "site/data.js"

# FIXME temporary colour chart
colour_chart = {
                "from": "2014-12",
                "to": "2015-11",
                # we have two 99s, one for 100 % and one for 'final value'
                "contents": [9, 19, 29, 39, 49, 59, 69, 79, 89, 99, 99],
               }


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

def generate_data(conn, project_ids, period):
    # create an array <period> in length
    # initially populated with all 0s
    data = {}

    # FIXME colour chart
    data["colour_chart"] = colour_chart

    now = datetime.datetime.now()
    year = now.year
    month = now.month

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
    output.append( '''var datasets = [\n''' )

    for project_name in sorted(data.keys()):
        project_data = data[project_name]

        dfrom = project_data["from"]
        dto = project_data["to"]
        contents = project_data["contents"]

        output.append( '''    { project: "%s", ''' %(project_name) )
        output.append( ''' date_from: "%s", ''' %(dfrom) )
        output.append( ''' date_to: "%s", ''' %(dto) )
        output.append( ''' data : [ ''' )
        for i in range(len(contents)):
            output.append( '''%d, ''' %(contents[i]) )
        output.append( '''], ''')
        output.append( '''},\n''' )

    output.append( '''];\n''' )

    with open(output_path, 'w') as file:
        file.writelines(output)

def get_project_ids(conn):
    project_ids = []
    for row in conn.execute('''select id from project'''):
        pid = row[0]
        project_ids.append(pid)

    return project_ids

if __name__ == "__main__":
    data = None
    with sqlite3.connect(dbname) as conn:
        project_ids = get_project_ids(conn)
        data = generate_data(conn, project_ids, period)
    if data is None:
        print("Error: failed to generate data")
    else:
        output_data(data, output_path)

