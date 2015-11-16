Database scheme ideas
=====================

all dates are stored and processed in UTC,
conversion to user timezone takes place at display level.

currently we need to track:

 * projects
 * users
 * commits per user per project (over time)
 * commits per user (over time)
 * commits per project (over time)
 * contributors per project (over time)
 * source code stats - lines of code, comments, blanks (over time)

we will have to make sure to be able to correctly deal with history rewriting,
so everything should be tied to a git hash

we also need to make sure to avoid reprocessing, so git hashes and datetimes
should be used heavily to reuse results from previous calculations


Schema
------

    project:
        git repo url : string
        added : datetime with tz
        last generated : datetime with tz
        last_HEAD : string (git hash)
        important : integer (used for heuristic to decide when to recheck)

    project_stats:
        link to project - need to pick project primary key
        time : datetime with tz
        hash : string (git hash)
        commit_count : integer

    project_source_stats:
        link to project - need to pick project primary key
        time : datetime with tz
        hash : string (git hash)
        lines of code : integer
        lines of comments : integer
        blank lines : integer

    user:
        unique id goes here

    user_stats:
        link to user - need to pick user primary key
        time : datetime with tz
        hash : string (git hash)
        commit_count : integer

    project_user_stats:
        link to project - need to pick project primary key
        link to user - need to pick user primary key
        time : datetime with tz
        hash : string (git hash)
        commit_count : integer


