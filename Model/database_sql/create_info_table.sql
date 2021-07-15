use BookDB
go

create table reader_info
(
    id         char(6)     not null primary key,
    name       nvarchar(8) not null,
    gender     char(2)     not null,
    department nvarchar(50),
    telephone  nvarchar(11),
    status     tinyint
)
go

create table book_info
(
    id     char(8)      not null primary key,
    name   nvarchar(50) not null,
    author nvarchar(8)  not null,
    press  nvarchar(50),
    price  real
)
go

create table borrow_info
(
    reader_id   char(6) not null,
    book_id     char(8) not null,
    borrow_date date,
    return_date date,
    status      tinyint,
    constraint PK_borrow_info primary key (reader_id, book_id),
    constraint FK_reader_id foreign key (reader_id) references reader_info (id),
    constraint FK_book_id foreign key (book_id) references book_info (id)
)
go

create table system_info
(
    id       char(4)     not null primary key,
    name     nvarchar(8) not null,
    password char(8)     not null
)
go