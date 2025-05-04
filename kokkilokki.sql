CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    image BLOB
);

CREATE TABLE Recipes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    user_id INTEGER REFERENCES Users(id),
    time_posted TEXT,
    image BLOB
);

CREATE TABLE recipe_details (
    id INTEGER PRIMARY KEY,
    preptimeh INTEGER,
    preptimem INTEGER,
    cooktimeh INTEGER,
    cooktimem INTEGER,
    ingredients TEXT,
    steps INTEGER, 
    recipe INTEGER REFERENCES Recipes(id)
);

CREATE TABLE recipe_steps (
    id INTEGER PRIMARY KEY,
    step TEXT,
    place INTEGER,
    recipe INTEGER REFERENCES Recipes(id)
);

CREATE TABLE Blogs (
    id INTEGER PRIMARY KEY,
    title TEXT,
    content TEXT,
    user_id INTEGER REFERENCES Users(id),
    time_posted TEXT
);

CREATE TABLE Comments (
    id INTEGER PRIMARY KEY,
    commenter INTEGER REFERENCES Users(id),
    post INTEGER REFERENCES Blogs(id),
    comment TEXT,
    time_posted TEXT
);

CREATE TABLE Reviews (
    id INTEGER PRIMARY KEY,
    reviewer INTEGER REFERENCES Users(id),
    post INTEGER REFERENCES Recipes(id),
    stars INTEGER,
    review TEXT,
    time_posted TEXT
);
