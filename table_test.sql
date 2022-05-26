use letscode;

#用户、管理员公用一张表
drop table if exists User;
create table User
(
   user_id int(11) primary key not null auto_increment,
   user_name varchar(50) not null,
   user_type varchar(10) not null check(user_type in ('reg','admin') ) , #用户类型
   avatar varchar(20), #用户头像的地址
   password varchar(80) not null,
   mail varchar(30) not null,
   preferrence varchar(50) not null defaule '无',
   gender varchar(6) not null check(gender in ('male','female')) default 'male',
   phone varchar(11) not null,
   black tinyint not null default 0,
   send_mail tinyint default 0,
   send_way varchar(8) default 'mail'
);


drop table if exists Game;
create table letscode.game
(
    game_id         int auto_increment
        primary key,
    game_name       varchar(50)       not null,
    game_start_time datetime          not null,
    game_end_time   datetime          null,
    duration        varchar(11)       null,
    checked         tinyint           null,
    website         varchar(100)      not null,
    game_type       varchar(20)       null,
    level_          tinyint           null,
    platform        varchar(20)       null,
    cust_reason     varchar(20)       null,
    cust_user_id    int     default 0 null,
    cust_public     tinyint default 0 null,
    check ((`game_end_time` is not null) or (`duration` is not null))
);

#帖子表
drop table if exists Post;
create table letscode.post
(
    post_id     int auto_increment
        primary key,
    user_id     int                                not null,
    headline    varchar(50)                        not null,
    create_time datetime default CURRENT_TIMESTAMP null,
    update_time datetime default CURRENT_TIMESTAMP null,
    content     mediumtext                         null,
    drafted     tinyint  default 0                 null,
    checked     tinyint  default 0                 null,
    block_type  tinyint                            not null,
    topped      tinyint  default 0                 null,
    com_count   int      default 0                 null,
    constraint post_ibfk_1
        foreign key (user_id) references letscode.user (user_id)
);


#评论表
create table letscode.comment
(
    comment_id  int auto_increment
        primary key,
    user_id     int                                not null,
    post_id     int                                not null,
    content     text                               not null,
    reply_id    int                                null,
    agree_count int      default 0                 null,
    oppo_count  int      default 0                 null,
    hidden      tinyint  default 0                 null,
    create_time datetime default CURRENT_TIMESTAMP null,
    constraint comment_ibfk_1
        foreign key (user_id) references letscode.user (user_id),
    constraint comment_ibfk_2
        foreign key (post_id) references letscode.post (post_id)
);

#订阅表
drop table if exists Subscribe;
create table letscode.subscribe
(
    subscribe_id int auto_increment
        primary key,
    user_id      int         not null,
    platform     varchar(40) not null,
    constraint subscribe_ibfk_1
        foreign key (user_id) references letscode.user (user_id)
);

#预约表
drop table if exists Reserve;
create table letscode.reserve
(
    reserve_id int auto_increment
        primary key,
    user_id    int not null,
    game_id    int not null,
    constraint reserve_ibfk_1
        foreign key (user_id) references letscode.user (user_id),
    constraint reserve_ibfk_2
        foreign key (game_id) references letscode.game (game_id)
);

#info表
create table letscode.info
(
    info_id     int(11) auto_increment
        primary key,
    user_id     int(11)     default 0                 null,
    content     varchar(100)                       null,
    headline    varchar(20)                        not null,
    create_time datetime default CURRENT_TIMESTAMP null
)

