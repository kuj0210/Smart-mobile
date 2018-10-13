drop database SystemData;

create database SystemData 
	DEFAULT CHARACTER 
	SET utf8 collate utf8_general_ci;
use SystemData;


create table naverUser(
	user_key varchar(50),
	serial varchar(50),
  email varchar(100),
  location varchar(30),
	primary key (user_key,serial)
	) ENGINE=InnoDB default character set utf8 collate utf8_general_ci;

create table mobileSystem(
	serial varchar(50),
	primary key (serial)
	) ENGINE=InnoDB default character set utf8 collate utf8_general_ci;

create table request(
	serial varchar(50),
	requestor varchar(50),
	request varchar(50),
	FOREIGN KEY (serial) REFERENCES mobileSystem (serial)
	) ENGINE=InnoDB default character set utf8 collate utf8_general_ci;

create table TempID(
  user_key varchar(50),
	ID varchar(50),
	primary key (user_key, ID)
	) ENGINE=InnoDB default character set utf8 collate utf8_general_ci;


select * from naverUser;
select * from mobileSystem;
insert mobileSystem value("SR0001");
insert mobileSystem value("SR0002");
insert mobileSystem value("SR0003");


delete from naverUser ;
delete from TempID ;
delete from request ;

select * from naverUser;
select * from TempID;
select * from request;









