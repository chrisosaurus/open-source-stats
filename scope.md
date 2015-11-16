scoping document
================

open source stats

maintains a list of users and projects it is tracking

initial github support only

ability for anyone to add a new GH repo via a form

collates contributions via GH username and/or email

no initial ability to login or claim accounts as yours


sections of the site
--------------------
pages:

 * front page - trending, maybe the same as global?
 * global (showing global langauge stats and global leader stats)
 * user page (showing user's commits, languages, activity, history, etc.)
 * project page (showing contributions, history, growth, activity, etc.)
 * language page (showing langauge and langauge leader stats)
 * submit new project page



architecture
-----------

d3:

 - graph generation offloaded to front-end
 - speaks to json api

python:

 - pick a web framework, serves up html/js/css
 - also hosts a json api for data

postgres db

git workers (python):

 - spin up to perform tasks such as glone, fetch, pull, gen_stats

celery

 - joq queue holding jobs for the git workers to do (jobs added via front-end and some cron system)

cron

 - inserting update tasks into celery queue (update this old repo, regen stats, ...)


fixed pool of workers, some heuristics around how often to perform work per repo
based on activity and size of repo

