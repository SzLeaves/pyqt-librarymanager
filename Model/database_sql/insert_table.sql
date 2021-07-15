use BookDB
go

-- reader_info
insert into reader_info (id, name, gender, department, telephone, status) values (N'B00001', N'张宇', N'男', N'理学院', N'8233023',0);
insert into reader_info (id, name, gender, department, telephone, status) values (N'B00002', N'刘虹', N'女', N'信息学院', N'3422455',0);
insert into reader_info (id, name, gender, department, telephone, status) values (N'B00003', N'陈瑗', N'女', N'艺术学院', N'2467755',0);
insert into reader_info (id, name, gender, department, telephone, status) values (N'B00006', N'李源', N'男', N'土木建筑学院', N'2344455',0);
insert into reader_info (id, name, gender, department, telephone, status) values (N'B00009', N'吴明', N'男', N'航空学院', N'2288766',0);
insert into reader_info (id, name, gender, department, telephone, status) values (N'B00011', N'李星', N'女', N'航空学院', N'3345782',0);
insert into reader_info (id, name, gender, department, telephone, status) values (N'B00023', N'陈盛', N'女', N'信息学院', N'2316543',0);
insert into reader_info (id, name, gender, department, telephone, status) values (N'J00001', N'黄蓓', N'女', N'材料科学学院', N'1298765',0);
insert into reader_info (id, name, gender, department, telephone, status) values (N'J00002', N'李怡', N'女', N'信息学院', N'2341567',0);
go

-- book_info
insert into book_info (id, name, author, press, price) values (N'10150001', N'C++程序设计', N'李海', N'北京邮电大学出版社', 38);
insert into book_info (id, name, author, press, price) values (N'10150002', N'VB.NET应用实践', N'陈思民', N'中国铁道出版社', 38);
insert into book_info (id, name, author, press, price) values (N'10150003', N'JAVA程序设计', N'黄钰', N'北京邮电大学出版社', 38);
insert into book_info (id, name, author, press, price) values (N'10160001', N'数据库技术与应用', N'刘卫国', N'清华大学出版社', 36);
insert into book_info (id, name, author, press, price) values (N'10160002', N'SQL SERVER原理及应用', N'盛立', N'中南大学出版社', 39);
insert into book_info (id, name, author, press, price) values (N'10160003', N'ORACLE数据库技术', N'李达', N'中国水利水电出版社', 30);
go

-- borrow_info
insert into borrow_info (reader_id, book_id, borrow_date, return_date) values (N'B00001', N'10150001', N'2014-07-01', N'2014-08-30');
insert into borrow_info (reader_id, book_id, borrow_date, return_date) values (N'B00001', N'10150002', N'2014-07-01', N'2014-08-30');
insert into borrow_info (reader_id, book_id, borrow_date, return_date) values (N'B00002', N'10150002', N'2014-06-08', N'2014-08-07');
insert into borrow_info (reader_id, book_id, borrow_date, return_date) values (N'B00002', N'10160001', N'2014-06-03', N'2014-08-02');
insert into borrow_info (reader_id, book_id, borrow_date, return_date) values (N'B00006', N'10160003', N'2014-07-01', N'2014-08-30');
insert into borrow_info (reader_id, book_id, borrow_date, return_date) values (N'J00001', N'10160001', N'2014-06-09', N'2014-08-08');
go

-- system_info
insert into system_info (id, name, password) values ('0000', 'admin', 'admin')
