SELECT user_login, user_group
FROM User
WHERE user_login='$login' AND user_pass='$password';