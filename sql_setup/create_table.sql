create table stocks_table(
    id              int not null auto_increment,
    stock_name      varchar(50),
    buy_price       float not null,
    sell_price      float not null,
    qty             int not null,
    primary key(id)
);

create table users_table(
    id              int not null auto_increment,
    username        varchar(60),
    pass            varchar(60),
    balance         float,
    primary key(id)
);

create table users_stocks(
    user_id        int not null,
    stock_id       int not null,
    price          float not null,
    qty            int not null,
    foreign key(user_id) REFERENCES users_table(id) on delete cascade,
    foreign key(stock_id) REFERENCES stocks_table(id) on delete cascade,
    primary key(user_id, stock_id)
);

create table admin_credentials(
    username        varchar(60),
    pass            varchar(60)
);

insert into admin_credentials values ("admin", "idp2019");
insert into users_table(username, pass, balance) values ("Daniel", "pass1", 0);
insert into stocks_table(stock_name, buy_price, sell_price, qty) values ("Facebook", 1.5, 2.5, 1000);
insert into stocks_table(stock_name, buy_price, sell_price, qty) values ("Google", 1.2, 4.8, 1000);
insert into users_stocks values (1, 1, 5.5, 100);
