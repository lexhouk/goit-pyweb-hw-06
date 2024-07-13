SELECT t.name, s.name, d.name
FROM teachers t
JOIN subjects d ON d.teacher_id = t.id
JOIN grades g ON g.subject_id = d.id
JOIN students s ON s.id = g.student_id
WHERE t.id = 5 AND s.id = 2
GROUP BY d.id
ORDER BY d.name;
