CREATE TABLE ExternUser (
    user_id INT NOT NULL AUTO_INCREMENT,
    user_login VARCHAR(50) NOT NULL,
    user_pass VARCHAR(50) NOT NULL,
    user_group VARCHAR(50) NOT NULL,
    PRIMARY KEY(user_id)
);