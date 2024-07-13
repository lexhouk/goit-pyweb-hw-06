SELECT s.name, d.name
FROM students s
JOIN grades g ON g.student_id = s.id
JOIN subjects d ON d.id = g.subject_id
WHERE s.id = 1
GROUP BY d.id
ORDER BY d.name;
