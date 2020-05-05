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

create table stock_prices_info(
    id              int not null auto_increment,
    stock_name      varchar(50),
    new_buy_price   float not null,
    new_sell_price  float not null,
    modify_date     datetime,
    primary key(id)
);

insert into admin_credentials values ("admin", "idp2019");
insert into users_table(username, pass, balance) values ("Daniel", "pass1", 0);
insert into stocks_table(stock_name, buy_price, sell_price, qty) values ("Facebook", 1.5, 2.5, 1000);
insert into stocks_table(stock_name, buy_price, sell_price, qty) values ("Google", 1.2, 4.8, 1000);
insert into users_stocks values (1, 1, 5.5, 100);
insert into stock_prices_info(stock_name, new_buy_price, new_sell_price, modify_date) values ("Facebook", 0.5, 0.48, '2020-05-01 08:00:00');
insert into stock_prices_info(stock_name, new_buy_price, new_sell_price, modify_date) values ("Facebook", 0.55, 0.53, '2020-05-02 08:00:00');
insert into stock_prices_info(stock_name, new_buy_price, new_sell_price, modify_date) values ("Facebook", 0.7, 0.69, '2020-05-03 08:00:00');
insert into stock_prices_info(stock_name, new_buy_price, new_sell_price, modify_date) values ("Facebook", 0.9, 0.89, '2020-05-04 08:00:00');
insert into stock_prices_info(stock_name, new_buy_price, new_sell_price, modify_date) values ("Facebook", 1.2, 1.19, '2020-05-05 08:00:00');
insert into stock_prices_info(stock_name, new_buy_price, new_sell_price, modify_date) values ("Facebook", 1.5, 1.48, CURRENT_TIMESTAMP);
insert into stock_prices_info(stock_name, new_buy_price, new_sell_price, modify_date) values ("Google", 1, 0.97, '2020-05-01 08:00:00');
insert into stock_prices_info(stock_name, new_buy_price, new_sell_price, modify_date) values ("Google", 2, 1.98, '2020-05-02 08:00:00');
insert into stock_prices_info(stock_name, new_buy_price, new_sell_price, modify_date) values ("Google", 2.7, 2.69, '2020-05-03 08:00:00');
insert into stock_prices_info(stock_name, new_buy_price, new_sell_price, modify_date) values ("Google", 3.7, 3.69, '2020-05-04 08:00:00');
insert into stock_prices_info(stock_name, new_buy_price, new_sell_price, modify_date) values ("Google", 4.8, 4.75, '2020-05-05 08:00:00');
insert into stock_prices_info(stock_name, new_buy_price, new_sell_price, modify_date) values ("Google", 5, 4.97, CURRENT_TIMESTAMP);
