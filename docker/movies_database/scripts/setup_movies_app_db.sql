CREATE ROLE "movies_app_admin" WITH PASSWORD 'moviesapppassword' LOGIN;

CREATE DATABASE   movies_app_db;
\c movies_app_db


CREATE TYPE gender AS ENUM('m', 'f', 'x');
CREATE TYPE payment_type AS ENUM('credit', 'debit','checking');
CREATE TYPE billing AS ENUM('monthly', 'yearly');
CREATE TYPE account_status AS ENUM('active', 'paused','cancelled');
CREATE TYPE device_type AS ENUM('tablet', 'tv', 'computer');

CREATE TABLE IF NOT EXISTS users(
    id              SERIAL PRIMARY KEY,
    first_name      VARCHAR(50) NOT NULL ,
    last_name       VARCHAR(50) NOT null,
    birthdate       DATE NOT NULL,
    gender          GENDER DEFAULT 'x',
    city            VARCHAR(50),
    country         VARCHAR(50),
    does_account_exists bool default False


);

CREATE TABLE IF NOT EXISTS accounts(
    id              SERIAL PRIMARY KEY,
    user_id         INT NOT NULL UNIQUE,
    created_at      DATE,
    paused_date     DATE DEFAULT '1900-01-01',
    resume_date     DATE DEFAULT '1900-01-01',
    cancelled_date  DATE DEFAULT '1900-01-01',
    bill_due_date   DATE,
    payment_method  PAYMENT_TYPE,
    billing_cycle   BILLING,
    account_status  ACCOUNT_STATUS,
    device_type     DEVICE_TYPE,

    CONSTRAINT fk_users_account_key
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE

);



CREATE TABLE IF NOT EXISTS movies(
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(200) NOT NULL,
    genres      VARCHAR(400) DEFAULT 'NA',
    LANGUAGE    VARCHAR(50) DEFAULT 'ENGLISH',
    popularity  NUMERIC(11,8),
    imdb_vote_count     NUMERIC,
    imdb_vote_average   NUMERIC,
    revenue             BIGINT,
    budget              BIGINT,
    release_date        DATE,
    is_available        BOOL DEFAULT FALSE,
    runtime             INT, -- minutes
    date_added          DATE DEFAULT '1800-01-01'


);

CREATE TABLE IF NOT EXISTS movie_ratings(
    id SERIAL   PRIMARY KEY,
    user_id     INT NOT NULL,
    movie_id    INT NOT NULL,
    rating      NUMERIC(2,1) CHECK (rating >=  0.0 AND rating <= 5.0),

    CONSTRAINT fk_rating_user
        FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_rating_movie
        FOREIGN KEY (movie_id) REFERENCES movies(id)
            ON DELETE CASCADE

);



CREATE TABLE IF NOT EXISTS watched_movies(
    id SERIAL           PRIMARY KEY,
    watched_movie_id    INT NOT NULL,
    user_id             INT NOT NULL,

    CONSTRAINT fk_watched_movie
        FOREIGN KEY (watched_movie_id) REFERENCES movies(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_watched_movie_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE

);

CREATE TABLE IF NOT EXISTS production_countries(
    iso_id          VARCHAR(5) PRIMARY KEY,
    country_name    VARCHAR(50) NOT NULL
);


CREATE TABLE IF NOT EXISTS production_companies(
    id  SERIAL      PRIMARY KEY,
    company_name    VARCHAR(100),
    parent_company  VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS actors(
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(100),
    gender  GENDER DEFAULT 'x'
);

CREATE TABLE IF NOT EXISTS directors(
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(100),
    gender  GENDER DEFAULT 'x'
);

-- junctions tables

CREATE TABLE IF NOT EXISTS prod_countries_movies_junc(
    movie_id    INT NOT NULL,
    iso_id      VARCHAR(5) NOT NULL,

    CONSTRAINT fk_movie_country
        FOREIGN KEY (movie_id) REFERENCES movies(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_country_movie
        FOREIGN KEY (iso_id) REFERENCES production_countries(iso_id)
        ON DELETE CASCADE
);



CREATE TABLE IF NOT EXISTS prod_companies_movies_junc(
    movie_id INT NOT NULL,
    company_id INT NOT NULL,

    CONSTRAINT fk_movie_company
        FOREIGN KEY (movie_id) REFERENCES movies(id)
        ON DELETE CASCADE,
     CONSTRAINT fk_company_movie
        FOREIGN KEY (company_id) REFERENCES production_companies(id)
        ON DELETE CASCADE

);


CREATE TABLE IF NOT EXISTS movies_actors_junc(
    movie_id INT NOT NULL,
    actor_id INT NOT NULL,
    CONSTRAINT fk_movie_actor
        FOREIGN KEY(movie_id) REFERENCES movies(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_actor_movie
        FOREIGN KEY (actor_id) REFERENCES actors(id)
        ON DELETE CASCADE

);

CREATE TABLE IF NOT EXISTS movies_directors_junc(
    movie_id INT NOT NULL,
    director_id INT NOT NULL,
    CONSTRAINT fk_movie_director
        FOREIGN KEY(movie_id) REFERENCES movies(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_director_movie
        FOREIGN KEY (director_id) REFERENCES directors(id)
        ON DELETE CASCADE

);


COPY users FROM '/resources/users.csv' DELIMITER ',' CSV HEADER;
COPY movies FROM '/resources/movies.csv' DELIMITER ',' CSV HEADER;
COPY actors FROM '/resources/actors.csv' DELIMITER ',' CSV HEADER;
COPY directors FROM '/resources/directors.csv' DELIMITER  ',' CSV HEADER;
COPY production_countries FROM '/resources/countries.csv' DELIMITER  ',' CSV HEADER;
COPY production_companies FROM '/resources/companies.csv' delimiter ',' CSV HEADER;
COPY prod_companies_movies_junc FROM '/resources/company_movie_junc.csv' DELIMITER ',' CSV HEADER;
COPY movies_actors_junc FROM '/resources/actors_movies_junc.csv' DELIMITER ',' CSV HEADER;
COPY prod_countries_movies_junc FROM '/resources/country_movie_junc.csv' DELIMITER ',' CSV HEADER;
COPY movies_directors_junc FROM '/resources/directors_movies_junc.csv' DELIMITER ',' CSV HEADER;



CREATE OR REPLACE PROCEDURE update_account_status(
    in user_id_in int ,
    in new_account_status account_status,
    inout query_result bool = false
    )
LANGUAGE plpgsql
AS $$
    DECLARE
        today_date date := now() at time zone 'America/New_York';
        paused_date_in date := '1900-01-01';
        cancelled_date_in date := '1900-01-01';
        resume_date_in date := '1900-01-01';
        bill_due_date_in date ;
        current_account_status account_status := 'active';
        billing_cycle_type billing := 'monthly' ;
        temp_date date ;
    BEGIN
        -- Find current account status
        SELECT
            account_status into current_account_status
        FROM accounts
        WHERE user_id = user_id_in;

        -- raise exception when account status is same as requested
        -- raise exception when account is cancelled and it is requested to be paused.
        IF current_account_status = new_account_status
            THEN RAISE EXCEPTION 'Account with user_id % is already %',user_id_in, new_account_status;
        ELSIF current_account_status = 'cancelled' AND new_account_status = 'paused'
            THEN RAISE EXCEPTION  'Account is % cannot be %', current_account_status, new_account_status;
        END IF;


        IF new_account_status = 'paused' or new_account_status = 'active'
            THEN
                -- find billing cycle to assign bill_due_date accordingly
                SELECT billing_cycle
                    INTO billing_cycle_type
                FROM accounts
                WHERE user_id = user_id_in;

                -- set dates according to status
                -- temp_date is date that is used to assign bill_due_date and it different for
                -- active and paused cycles.
                IF new_account_status ='paused'
                    THEN
                    -- set dates, cancelled date shall stay to default
                    paused_date_in := to_char(today_date, 'YYYY-mm-DD');
                    resume_date_in := to_char(today_date + interval '2 months', 'YYYY-mm-DD');
                    temp_date := resume_date_in;
                ELSIF new_account_status = 'active'
                    THEN temp_date = today_date;
                END IF;

                -- set bil_due_date according to billing_cyle
                IF billing_cycle_type = 'yearly'
                    THEN bill_due_date_in := to_char(temp_date + interval  '1 year', 'YYYY-mm-DD');
                ELSIF billing_cycle_type = 'monthly'
                    THEN bill_due_date_in := to_char(temp_date + interval  '1 month', 'YYYY-mm-DD');
                END IF;

        ELSIF new_account_status = 'cancelled'
            THEN
                bill_due_date_in := '1900-01-01';
                cancelled_date_in := to_char(today_date, 'YYYY-mm-DD');
        END IF;


        UPDATE accounts
        SET paused_date = paused_date_in,
            cancelled_date = cancelled_date_in,
            resume_date = resume_date_in,
            bill_due_date = bill_due_date_in,
            account_status = new_account_status
        WHERE user_id = user_id_in;


        -- check account status and up query variable
        -- current_account_status refers to updated status
        SELECT account_status INTO current_account_status FROM accounts WHERE user_id = user_id_in;
        IF current_account_status = new_account_status
            THEN
                query_result = TRUE;
        ELSE
            Raise Exception 'Status did not updated';
        END IF;

        END;
$$;



-- keep this at the last

REVOKE CONNECT ON DATABASE movies_app_db FROM PUBLIC;
GRANT CONNECT ON DATABASE movies_app_db TO movies_app_admin;
-- following command grant privileges on new object no exiting object, use commented command to
-- gain access for existing objects.
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO movies_app_admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public to movies_app_admin;
GRANT ALL PRIVILEGES ON DATABASE movies_app_db TO movies_app_admin;