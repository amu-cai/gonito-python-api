CREATE TABLE IF NOT EXISTS users (
    id serial PRIMARY KEY,
    username VARCHAR (50) UNIQUE NOT NULL,
	hashed_password VARCHAR (50) NOT NULL,
	is_admin BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS challenges (
    id serial PRIMARY KEY,
    title VARCHAR (50) UNIQUE NOT NULL,
	type VARCHAR (50) NOT NULL,
	description VARCHAR (50) NOT NULL,
	main_metric VARCHAR (50) NOT NULL,
	best_score VARCHAR (50) NOT NULL,
    deadline VARCHAR (50) NOT NULL,
    award VARCHAR (50) NOT NULL,
    readme VARCHAR NOT NULL
);