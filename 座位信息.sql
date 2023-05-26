create database information;
use information;
create table select_information(
    my_account varchar(20) comment '账号',
    my_movie varchar(30) comment '电影名',
    my_line varchar(5) comment '行数',
    my_row varchar(5) comment '列数'
)comment '选座信息';

ALTER TABLE select_information CHANGE my_account 账号 varchar(10) ;
ALTER TABLE select_information CHANGE my_movie 电影 varchar(20);
ALTER TABLE select_information CHANGE my_line 行 varchar(5);
ALTER TABLE select_information CHANGE my_row 列 varchar(5);

select *from select_information;