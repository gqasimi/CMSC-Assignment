

SELECT Permissions.permission_name AS PermissionName
FROM Permissions
LEFT JOIN Role_Permissions ON Permissions.permission_id = Role_Permissions.permission_id
WHERE Role_Permissions.role_id IS NULL;