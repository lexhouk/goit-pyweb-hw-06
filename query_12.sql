SELECT d.name, g.name, s.name, m.value
FROM subjects d
JOIN grades m ON m.subject_id = d.id
JOIN students s ON s.id = m.student_id
JOIN groups g ON g.id = s.group_id
WHERE d.id = 1 AND g.id = 1
GROUP BY s.id
ORDER BY s.name, m.id DESC;
