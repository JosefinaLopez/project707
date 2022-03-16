CREATE table usuario(
    id_user INTEGER PRIMARY KEY,
    username VARCHAR not null, 
    password VARCHAR  not null,
    admin BOOLEAN not null
);
SELECT *FROM usuario