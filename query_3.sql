SELECT d.name, g.name, ROUND(AVG(m.value), 1)
FROM groups g
JOIN students s ON g.id = s.group_id
JOIN grades m ON s.id = m.student_id
JOIN subjects d ON d.id = m.subject_id
WHERE d.id = 1
GROUP BY g.id;
