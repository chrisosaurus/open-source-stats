
pragma foreign_keys=on;

create table user (
    id      integer primary key autoincrement not null ,
    email   text                              not null
);

create table project (
    id              integer primary key autoincrement not null ,
    repo_url        text                              not null ,
    name            text                                       ,
    checkout        text                                       ,
    branch          text                                       default "master",
    -- time this project was added
    added           datetime                          not null default CURRENT_TIMESTAMP,
    -- time this project was updated (git fetch / clone)
    last_updated    datetime                                   default null,
    -- time this project's stats were last generated
    last_gen        datetime                                   default null,
    -- hash after last fetch
    last_hash       text                                       default null
);

create table project_stats (
    id           integer primary key autoincrement not null ,
    project_id   integer                           not null references project(id) ,
    generated    datetime                          not null ,
    -- month with year reference in iso format: "2015-11"
    month        text                              not null,
    -- the hash of origin/<branch> when we generated this entry
    hash         text                              not null ,
    -- the hash for the previous entry
    parent_hash  text                                     default "",
    -- count of commits to this project up to and including this has
    -- so this includes the count for parent_hash and parent_hash's parent_hash and so on
    total_commits integer                     not null,
    -- count of commits only in this period (so excluding parent hash's count)
    commits_in_period integer                 not null
);

create table project_user_stats (
    id           integer primary key autoincrement not null ,
    project_id   integer                           not null references project(id) ,
    user_id      integer                           not null references user(id) ,
    generated    datetime                          not null ,
    -- month with year reference in iso format: "2015-11"
    month        text                              not null,
    -- the hash of origin/<branch> when we generated this entry
    hash         text                              not null ,
    -- the hash for the previous entry
    parent_hash  text                                     default "",
    -- count of commits to this project up to and including this has
    -- so this includes the count for parent_hash and parent_hash's parent_hash and so on
    total_commits integer                     not null,
    -- count of commits only in this period (so excluding parent hash's count)
    commits_in_period integer                 not null
);

insert into project (repo_url) values ("https://github.com/CausalityLtd/ponyc.git");
insert into project (repo_url) values ("https://github.com/rust-lang/rust.git");
insert into project (repo_url) values ("https://github.com/golang/go.git");

