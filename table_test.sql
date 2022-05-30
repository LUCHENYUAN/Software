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
   preferrence varchar(50) not null default '无',
   gender varchar(6) not null check(gender in ('male','female')) default 'male',
   phone varchar(11) not null,
   black tinyint not null default 0,
   send_mail tinyint default 0,
   send_way varchar(8) default 'mail'
);


drop table if exists Game;
create table Game
(
   game_id int(11) primary key not null auto_increment,
   game_name varchar(50) not null,
   game_start_time datetime not null,
   game_end_time datetime,
   duration varchar(11),
   checked tinyint default 0,
   website varchar(100) not null,
   game_type varchar(20) not null, #周赛/月赛
   level_  tinyint not null,#难易度 level是mysql保留字所以加下划线 
   platform varchar(20) ,#平台，可空
   cust_reason     varchar(20)       null,
    cust_user_id    int(11)     default 0 null,
    cust_public     tinyint default 0 null,
   
   
   check ((game_end_time is not null) or (duration is not null))
);
alter table Game  modify COLUMN checked tinyint;
alter table Game  modify COLUMN game_type varchar(20);
alter table Game  modify COLUMN level_ tinyint;

#帖子表
drop table if exists Post;
create table Post
(
post_id int(11)  primary key not null auto_increment,
user_id int(11) not null, 
headline varchar(50) not null,
create_time datetime default now(),
update_time datetime default now(),
content mediumtext ,#varchar最多256字符，存不下
drafted tinyint default 0,#是否草稿check
checked tinyint default 0,#是否已审核check
block_type tinyint not null,
topped      tinyint  default 0                 null,
com_count   int(11)      default 0                 null,

foreign key(user_id) references User(user_id)
);


#评论表
drop table if exists Comment;
create table Comment
(
comment_id int(11) primary key not null auto_increment,
user_id int(11) not null,
post_id int(11) not null,
content text not null,
reply_id int(11) default 0,#0则为原始评论，如果评论被回复，则保存评论的id
agree_count int(11) default 0,
oppo_count int(11) default 0,
hidden tinyint default 0,
create_time datetime default now(),

foreign key(user_id) references User(user_id),
foreign key(post_id) references Post(post_id)
);

#订阅表
drop table if exists Subscribe;
create table Subscribe
(
subscribe_id int(11) primary key not null auto_increment,
user_id int(11) not null,

platform varchar(40) not null,

foreign key(user_id) references User(user_id)


);

#预约表
drop table if exists Reserve;
create table Reserve
(
subscribe_id int(11) primary key not null auto_increment,
user_id int(11) not null,
game_id int(11) not null,

foreign key(user_id) references User(user_id),
foreign key(game_id) references Game(game_id)
);

create table Info
(
    info_id     int(11) auto_increment   primary key,
    user_id     int(11)      default 0,
    content     varchar(100)  ,
    headline    varchar(20)   not null,
    create_time datetime default now()
);


