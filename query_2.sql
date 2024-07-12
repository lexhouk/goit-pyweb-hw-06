SELECT su.name, s.name, ROUND(AVG(g.value), 1) as grade
FROM grades g
JOIN students s ON g.student_id = s.id
JOIN subjects su ON g.subject_id = su.id
WHERE su.id = 1
ORDER BY grade DESC
LIMIT 1;
