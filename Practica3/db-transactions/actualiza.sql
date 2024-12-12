DO $$ 
DECLARE
    rec record;
BEGIN
    FOR rec IN 
        SELECT 
            conname AS constraint_name,
            conrelid::regclass AS table_name,
            a.attname AS column_name,
            confrelid::regclass AS foreign_table_name,
            af.attname AS foreign_column_name
        FROM 
            pg_constraint AS c
            JOIN pg_attribute AS a ON a.attnum = ANY(c.conkey)
            JOIN pg_attribute AS af ON af.attnum = ANY(c.confkey)
        WHERE 
            confdeltype = 'c'  -- Filtra solo las restricciones CASCADE
    LOOP
        -- Eliminar la restricción CASCADE
        EXECUTE 'ALTER TABLE ' || rec.table_name || ' DROP CONSTRAINT ' || rec.constraint_name;
        
        -- Volver a crear la clave foránea sin CASCADE
        EXECUTE 'ALTER TABLE ' || rec.table_name || ' ADD CONSTRAINT ' || rec.constraint_name || 
                ' FOREIGN KEY (' || rec.column_name || ') REFERENCES ' || rec.foreign_table_name || 
                ' (' || rec.foreign_column_name || ') ON DELETE NO ACTION';
    END LOOP;
END $$;
