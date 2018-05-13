drop database SystemData;

create database SystemData 
	DEFAULT CHARACTER 
	SET utf8 collate utf8_general_ci;
use SystemData;


create table naverUser(
	user_key varchar(50),
	serial varchar(50),
	primary key (user_key,serial)
	) ENGINE=InnoDB default character set utf8 collate utf8_general_ci;

create table mobileSystem(
	serial varchar(50),
	url varchar(50),
	primary key (serial)
	) ENGINE=InnoDB default character set utf8 collate utf8_general_ci;


select * from naverUser;
select * from mobileSystem;
insert mobileSystem value("SR0001","www.TEST.com");
insert mobileSystem value("SR0002","www.TEST.com");
insert mobileSystem value("SR0003","www.TEST.com");
select * from mobileSystem;