CREATE TABLE IF NOT EXISTS bronze.members (
    -- member_id SERIAL PRIMARY KEY,
    transaction_id INT NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    student_id INT,
    student_email VARCHAR(255) NOT NULL,
    age INT,
    phone VARCHAR(255) NOT NULL,
    date_joined DATETIME NOT NULL,
    residency_status VARCHAR(255) NOT NULL,
    year_of_study INT,
    program_of_study VARCHAR(255) ,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);




