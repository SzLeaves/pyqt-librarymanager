create database BookDB;
go

use BookDB;
go

-- 更改数据库排序状态
alter database BookDB collate Chinese_PRC_CI_AS;
-- 查询数据库排序状态
select convert(varchar(50), databasepropertyex('BookDB','collation'));
go