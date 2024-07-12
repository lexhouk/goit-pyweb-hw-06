SELECT s.name, ROUND(AVG(g.value), 1) as grade
FROM grades g
JOIN students s ON g.student_id = s.id
GROUP BY g.student_id
ORDER BY grade DESC
LIMIT 5;
