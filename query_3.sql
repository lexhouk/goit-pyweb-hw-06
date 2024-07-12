SELECT su.name, g.name, ROUND(AVG(m.value), 1)
FROM groups g
JOIN students s ON g.id = s.group_id
JOIN grades m ON s.id = m.student_id
JOIN subjects su ON su.id = m.subject_id
WHERE su.id = 1
GROUP BY g.id;
