import csv
import sqlite3

con = sqlite3.connect("friends.db")  # change to 'sqlite:///your_filename.db'
cur = con.cursor()
cur.executescript("""
create table friends (
	id INT,
	name VARCHAR(50),
	last_name VARCHAR(50),
	company VARCHAR(50),
	phone_number VARCHAR(50),
	email VARCHAR(50)
);
insert into friends (id, name, last_name, company, phone_number, email) values (1, 'Pru', 'Stempe', 'Twitterbridge', '1643663270', 'pstempe0@theglobeandmail.com');
insert into friends (id, name, last_name, company, phone_number, email) values (2, 'Tracie', 'Steeples', 'Buzzbean', '8192391826', 'tsteeples1@accuweather.com');
insert into friends (id, name, last_name, company, phone_number, email) values (3, 'Broderick', 'Dishman', 'Agivu', '3906912833', 'bdishman2@phoca.cz');
insert into friends (id, name, last_name, company, phone_number, email) values (4, 'Peadar', 'Stichall', 'Zazio', '9921764871', 'pstichall3@furl.net');
insert into friends (id, name, last_name, company, phone_number, email) values (5, 'Daron', 'Harber', 'Skipstorm', '1434731702', 'dharber4@dedecms.com');
insert into friends (id, name, last_name, company, phone_number, email) values (6, 'Anatollo', 'Pease', 'LiveZ', '8145821523', 'apease5@tripod.com');
insert into friends (id, name, last_name, company, phone_number, email) values (7, 'Ferdinand', 'Simonazzi', 'Yoveo', '8119736602', 'fsimonazzi6@blinklist.com');
insert into friends (id, name, last_name, company, phone_number, email) values (8, 'Ollie', 'Bergeon', 'Divanoodle', '7214810506', 'obergeon7@purevolume.com');
insert into friends (id, name, last_name, company, phone_number, email) values (9, 'Hube', 'Gurry', 'Dabshots', '2803131564', 'hgurry8@netscape.com');
insert into friends (id, name, last_name, company, phone_number, email) values (10, 'Bay', 'Gurrado', 'InnoZ', '2197470793', 'bgurrado9@i2i.jp');
insert into friends (id, name, last_name, company, phone_number, email) values (11, 'Dicky', 'Isakson', 'Skalith', '7846800765', 'disaksona@gov.uk');
insert into friends (id, name, last_name, company, phone_number, email) values (12, 'Fancie', 'Mance', 'Thoughtstorm', '1281373744', 'fmanceb@foxnews.com');
insert into friends (id, name, last_name, company, phone_number, email) values (13, 'Shea', 'Bolesma', 'Dynabox', '7451922815', 'sbolesmac@usatoday.com');
insert into friends (id, name, last_name, company, phone_number, email) values (14, 'Pattin', 'Feben', 'Gabvine', '8725231608', 'pfebend@mit.edu');
insert into friends (id, name, last_name, company, phone_number, email) values (15, 'Rabbi', 'Benford', 'Meevee', '3816145818', 'rbenforde@cbc.ca');
insert into friends (id, name, last_name, company, phone_number, email) values (16, 'Beckie', 'Egerton', 'Kwinu', '3496290763', 'begertonf@craigslist.org');
insert into friends (id, name, last_name, company, phone_number, email) values (17, 'Ruy', 'Mufford', 'Skajo', '4586922810', 'rmuffordg@archive.org');
insert into friends (id, name, last_name, company, phone_number, email) values (18, 'Urbano', 'Bofield', 'Avaveo', '4855955649', 'ubofieldh@hexun.com');
insert into friends (id, name, last_name, company, phone_number, email) values (19, 'Rica', 'McGarrity', 'Photospace', '2192379655', 'rmcgarrityi@macromedia.com');
insert into friends (id, name, last_name, company, phone_number, email) values (20, 'Cherye', 'Yanson', 'Gabspot', '2441801124', 'cyansonj@google.pl');
insert into friends (id, name, last_name, company, phone_number, email) values (21, 'Beilul', 'Paull', 'Topdrive', '4706127260', 'bpaullk@kickstarter.com');
insert into friends (id, name, last_name, company, phone_number, email) values (22, 'Amara', 'Faichney', 'InnoZ', '8615863768', 'afaichneyl@php.net');
""")
con.commit()
con.close()
