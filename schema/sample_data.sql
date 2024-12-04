

SELECT Users.username AS Username, Roles.role_name AS RoleName
FROM Users
JOIN User_Roles ON Users.user_id = User_Roles.user_id
JOIN Roles ON User_Roles.role_id = Roles.role_id;