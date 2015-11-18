#!/usr/bin/env python3

import sqlite3
import os
import pygit2
import datetime

repo_dir = "repos"
dbname = "oos.sqlite"

def timestamp_to_monstr(timestamp):
    date = datetime.date.fromtimestamp(timestamp)
    year = date.year
    month = date.month
    monstr = "%.4d-%.2d" %(year, month)
    return monstr

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

# update a project's git checkout
def update_project(conn, project_id, repo_url, name, checkout, branch, last_updated, last_hash):
    path = os.path.join(repo_dir, checkout)
    repo = None

    if os.path.exists(path):
        print("fetching to '%s'" %(path))
        # if project exists, then fetch it
        #update_cmd = "GIT_DIR=%s git fetch" %(path)
        #subprocess.call(update_cmd, shell=True)
        repo = pygit2.Repository(path)
        repo.remotes["origin"].fetch()

    else:
        print("cloning to '%s'" %(checkout))
        # if project doesn't exist, then we clone it
        #clone_cmd = "git clone --no-checkout --bare %s %s" %(repo_url, path)
        #subprocess.call(clone_cmd, shell=True)
        repo = pygit2.clone_repository(url=repo_url, path=path, bare=True, checkout_branch=None)

    # get current hash
    commit = repo.revparse_single("origin/%s" %(branch))
    hash = str(commit.oid)

    # save hash to db along with last_updated
    conn.execute("UPDATE project set last_updated=CURRENT_TIMESTAMP, last_hash=? where id=?", (hash, project_id))

# calculate project and project user stats
def get_project_stats(conn, repo, project_id):
    # seen is a set holding all the commits we already have stats for
    # seen is a map of previously seen hash => previous data
    seen = {}
    for row in conn.execute('''SELECT hash, total_commits, commits_in_period, month from project_stats where project_id=?''', (project_id,)):
        hash = row[0]
        total_commits = row[1]
        commits_in_period = row[2]
        monstr = row[3]

        seen[hash] = {
                "total" :     total_commits,
                "in period" : commits_in_peroid,
                "monstr" :    monstr
                     }

    master = repo.revparse_single("origin/master")
    # we want to generate stats
    # by walking the tree until we hit a commit we have seen before
    walker = repo.walk(master.oid, pygit2.GIT_SORT_TOPOLOGICAL)

    # stats [monstr] = {
    #        "hash": ,
    #        "parent_hash": ,
    #        "commits_in_period" : ,
    #        "total_commits": ,
    #        "commits_in_period_per_user": ,
    # }
    stats = {}

    # our current hash
    master_hash = str(master.oid)
    # tracking our final hash
    final_hash = ""
    for commit in walker:
        commit_hash = str(commit.oid)
        author_name = commit.author.name
        author_email = commit.author.email
        commit_time = commit.commit_time
        commit_message = commit.message

        monstr = timestamp_to_monstr(commit_time)

        if monstr not in stats:
            stats[monstr] = {
                "hash": commit_hash, # we want a month's hash to be the 'first' hash we see for that month
                "parent_hash": "",
                "commits_in_period" : 0,
                "total_commits": 0,
                "commits_in_period_per_user": {},
                            }

        month = stats[monstr]

        # stop when we find somewhere we have been before
        if commit_hash in seen:
            month["final_hash"] = commit_hash
            month["commits_in_period"] += seen[commit_hash]["commits_in_period"]
            # FIXME this total commit logic doesn't work
            # as for 99.99% of the time there is nothing immediately below us
            month["total_commits"] = month["commits_in_period"] + seen[commit_hash]["total_commits"]
            break;

        # otherwise we add this to our current data set
        month["commits_in_period"] += 1

        # count user commits on this project
        if not author_email in month["commits_in_period_per_user"]:
            month["commits_in_period_per_user"][author_email] = 0
        month["commits_in_period_per_user"][author_email] += 1
        # NOTE: commits per user do NOT include previous information
        # this is taken care of later

    # once we have finished collecting all data we now want to go through and set the previous_hash values
    # we also want to make sure that the 'total commits' is correctly set
    parent_hash = None
    total_commits = 0
    for monstr in sorted(stats.keys()):
        month = stats[monstr]

        if parent_hash is None:
            prev_monstr = prev_month(monstr)
            row = conn.execute('''select hash, total_commits from project_stats where project_id=? and month=?''', (project_id, prev_monstr));
            row = row.fetchone()
            if row is not None:
                # find hash
                parent_hash = row[0]

                # set total commits
                total_commits = row[1]
            else:
                parent_hash = ""


        total_commits += month["commits_in_period"]
        month["total_commits"] = total_commits
        month["parent_hash"] = parent_hash
        parent_hash = month["hash"]

    return stats

def project_month_exists(conn, project_id, monstr):
    row = conn.execute('''select * from project_stats where project_id=? and month=?''', (project_id, monstr))
    row = row.fetchone()
    if row is None:
        return False

    return True

def record_project_stats(conn, project_id, stats):
    # newest hash
    newest_hash = sorted(list(stats.keys()))[-1]

    # record that we have generated stats
    conn.execute("UPDATE project set last_gen=CURRENT_TIMESTAMP, last_hash=? where id=?", (project_id, newest_hash))

    for monstr in stats:
        month = stats[monstr]
        hash = month["hash"]
        parent_hash = month["parent_hash"]
        commits_in_period = month["commits_in_period"]
        total_commits = month["total_commits"]
        #commits_in_period_per_user = month["commits_in_period_per_user"]

        if project_month_exists(conn, project_id, monstr):
            # update
            conn.execute('''update project_stats set (generated,         hash, parent_hash, total_commits, commits_in_period)
                                              values (CURRENT_TIMESTAMP, ?,    ?,           ?,             ?                ) where project_id = ? and month = ?''',
                                                     (                   hash, parent_hash, total_commits, commits_in_period, project_id, monstr))
        else:
            # insert
            conn.execute('''insert into project_stats (generated,         project_id, month,  hash, parent_hash, total_commits, commits_in_period)
                                               values (CURRENT_TIMESTAMP, ?,          ?,      ?,    ?,           ?,             ?                )''',
                                                      (                   project_id, monstr, hash, parent_hash, total_commits, commits_in_period))
        pass

def record_project_user_stats(conn, project_id, stats):
    pass

    hash = stats["hash"]
    parent_hash = stats["parent_hash"]
    commits_in_period_per_user = stats["commits_in_period_per_user"]

    total_commits_per_user = {}

    # make sure current commits per user includes every user we know of for this project
    for row in conn.execute('''select user_id, total_commits from project_user_stats where hash=? and project_id=?''', (parent_hash, project_id)):
        user_id = row[0]
        commit_count = row[1]

        row = conn.execute('''select email from user where id=?''', (user_id,))
        row = row.fetchone()
        if row is None:
            raise Exception("Error: record_project_user_stats failed to find user from id '%s'" %(user_id))

        email = row[0]

        commits_in_period = 0
        if email in commits_in_period_per_user:
            commits_in_period = commits_in_period_per_user[email]

        total_commits_per_user[email] = commits_in_peiod + commit_count

    # record project user stats
    for author_email in commits_in_period_per_user:
        row = conn.execute('''select id from user where email=?''', (author_email,))
        row = row.fetchone()
        if row is None:
            conn.execute('''insert into user (email) values(?)''', (author_email,))
            row = conn.execute('''select id from user where email=?''', (author_email,))
            row = row.fetchone()

        if row is None:
            raise Exception("Error: record_project_user_stats failed to create new user for email '%s'" %(author_email))

        commits_in_period = commits_in_period_per_user[author_email]
        total_commits = 0
        if author_email in total_commits_per_user:
            total_commits = total_commits_per_user[author_email]
        else:
            total_commits = commits_in_period
        user_id = int(row[0])

        conn.execute('''insert into project_user_stats (project_id, user_id, generated,         hash,  parent_hash,   total_commits, commits_in_period)
                                                values (?,          ?,       CURRENT_TIMESTAMP, ?,     ?,             ?,                  ?)''',
                                                       (project_id, user_id,                    hash,  parent_hash,   total_commits, commits_in_period))

# generate statistics for a project
def gen_project_stats(conn, project_id, repo_url, name, checkout, branch, last_updated, last_hash):
    path = os.path.join(repo_dir, checkout)
    repo = None

    if os.path.exists(path):
        repo = pygit2.Repository(path)
    else:
        print("Error: gen_project_state could not find repository '%s'" %(path))
        raise Exception("Error: gen_project_state could not find repository '%s'" %(path))

    #{hash, parent_hash, total_commits, commits_per_user}
    stats = get_project_stats(conn=conn, repo=repo, project_id=project_id)
    record_project_stats(conn=conn, project_id=project_id, stats=stats)
    #record_project_user_stats(conn=conn, project_id=project_id, stats=stats)

# update all projects we know of
def update_projects(dnbame):
    if not os.path.exists(repo_dir):
        os.mkdir(repo_dir)

    with sqlite3.connect(dbname) as conn:
        # go through projects
        for row in conn.execute('''SELECT
                                        id,
                                        repo_url,
                                        name,
                                        checkout,
                                        branch,
                                        last_updated,
                                        last_hash
                                   FROM
                                        project'''):
            project_id     = row[0]
            repo_url       = row[1]
            name           = row[2]
            checkout       = row[3]
            branch         = row[4]
            last_updated   = row[5]
            last_hash      = row[6]

            # if
            if branch is None:
                branch = "master"
                # save this branch to db
                conn.execute("UPDATE project set branch=? where id=?", (branch, project_id))

            # if name is not set, then generate
            if name is None:
                name = repo_url
                name = name.split("/")
                name = name[-1]
                name = name.replace(".git", "")
                # save this name to db
                conn.execute("UPDATE project set name=? where id=?", (name, project_id))
                print("name is '%s'" %(name))

            # if checkout is not set, then generate
            if checkout is None:
                checkout = repo_url
                checkout = checkout.replace("http://", "")
                checkout = checkout.replace("https://", "")
                checkout = checkout.replace("/", "_")
                # save this name to db
                conn.execute("UPDATE project set checkout=? where id=?", (checkout, project_id))
                print("checkout is '%s'" %(checkout))

            update_project(conn=conn, project_id=project_id, repo_url=repo_url, name=name, checkout=checkout, branch=branch, last_updated=last_updated, last_hash=last_hash)
            gen_project_stats(conn=conn, project_id=project_id, repo_url=repo_url, name=name, checkout=checkout, branch=branch, last_updated=last_updated, last_hash=last_hash)


if __name__ == "__main__":
    update_projects(dbname)

