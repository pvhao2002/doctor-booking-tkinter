create database if not exists `qlbv`;
use qlbv;

create table if NOT EXISTS `users`
(
    user_id   int primary key auto_increment,
    username  varchar(255) unique,
    password  varchar(255),
    role enum ('victim','doctor','admin'),
    status    enum ('active', 'inactive') default 'active'
);

create table if not exists `victim`
(
    victim_id int primary key auto_increment,
    user_id    int,
    full_name  varchar(255),
    gender     enum ('MALE','FEMALE','OTHER'),
    birthday   date,
    address    text,
    phone      varchar(20),
    age        int,
    foreign key (user_id) references users (user_id)
);

create table if not exists `doctor`
(
    doctor_id int primary key auto_increment,
    user_id   int,
    full_name varchar(255),
    specialty varchar(100),
    email     varchar(100),
    phone     varchar(20),
    foreign key (user_id) references users (user_id)
);

create table if not exists `appointment`
(
    appointment_id   int auto_increment primary key,
    victim_id       int,
    doctor_id        int,
    appointment_date datetime,
    status           enum ('pending', 'accepted' ,'completed','cancelled'),
    foreign key (victim_id) references victim (victim_id),
    foreign key (doctor_id) references doctor (doctor_id)
);

-- table dich vu
create table if not exists `services`
(
    service_id   int primary key auto_increment,
    service_name varchar(100),
    description  text,
    price        decimal(10, 2),
    status       enum ('active','inactive')
);

create table if not exists `invoice`
(
    invoice_id     int primary key auto_increment,
    appointment_id int,
    total_amount   decimal(10, 2),
    create_date    datetime,
    payment_status enum ('free','paid'),
    foreign key (appointment_id) references appointment (appointment_id)
);

create table if not exists `invoice_detail`
(
    invoice_id int,
    service_id int,
    primary key (invoice_id, service_id),
    foreign key (invoice_id) references invoice (invoice_id),
    foreign key (service_id) references services (service_id)
);

INSERT INTO users (user_id, username, password, role, status) VALUES (1, 'admin', '1234qwer', 'admin', 'active');