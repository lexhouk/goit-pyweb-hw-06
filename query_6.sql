SELECT g.name, s.name
FROM groups g
JOIN students s ON s.group_id = g.id
WHERE g.id = 1
ORDER BY s.name;
