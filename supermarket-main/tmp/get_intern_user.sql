SELECT user_login, user_group
FROM InternUser
WHERE user_login='$login' AND user_pass='$password';