CREATE TABLE InternUser (
    user_id INT NOT NULL AUTO_INCREMENT,
    user_login VARCHAR(50) NOT NULL,
    user_pass VARCHAR(50) NOT NULL,
    user_group VARCHAR(50) NOT NULL,
    user_name VARCHAR(50) NOT NULL,
    user_contact VARCHAR(50) NOT NULL,
    user_post VARCHAR(50) NOT NULL,
    PRIMARY KEY(user_id)
);