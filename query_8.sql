SELECT t.name, s.name, ROUND(AVG(g.value), 1)
FROM teachers t
JOIN subjects s ON s.teacher_id = t.id
JOIN grades g ON g.subject_id = s.id
WHERE t.id = 5
GROUP BY s.id
ORDER BY s.name;
