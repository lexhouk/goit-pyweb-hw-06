SELECT d.name, g.name, s.name, m.value
FROM groups g
JOIN students s ON s.group_id = g.id
JOIN grades m ON m.student_id = s.id
JOIN subjects d ON d.id = m.subject_id
WHERE d.id = 1 AND g.id = 1
ORDER BY s.name;
