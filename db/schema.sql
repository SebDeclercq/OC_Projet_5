CREATE TABLE Products (
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    nutrition_grade TEXT NOT NULL, -- ENUM ?
    url TEXT NOT NULL
);
CREATE TABLE Stores (
    id INTEGER AUTO_INCREMENT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL
);
CREATE TABLE is_sold_in (
    product_id INTEGER REFERENCES Products(id),
    store_id INTEGER REFERENCES Stores(id),
    PRIMARY KEY (product_id, store_id)
);
CREATE TABLE Categories (
    id INTEGER AUTO_INCREMENT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL
);
CREATE TABLE has_category (
    product_id INTEGER REFERENCES Products(id),
    category_id INTEGER REFERENCES Categories(id),
    PRIMARY KEY(product_id, category_id)
);
