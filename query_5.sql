SELECT t.name, s.name
FROM teachers t
JOIN subjects s ON s.teacher_id = t.id
WHERE t.id = 5;
