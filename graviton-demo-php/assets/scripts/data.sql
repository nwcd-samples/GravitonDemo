CREATE TABLE `customer` (
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `gender` enum('male','female') NOT NULL,
  `status` enum('active','pending','deleted','') NOT NULL DEFAULT 'pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


INSERT INTO customer VALUES ('Gates', 'Bill', 'b@shopxx.com', 'male', 'pending');
INSERT INTO customer VALUES ('Ram', 'Singh', 'ram@shopxx.com', 'male', 'pending');
INSERT INTO customer VALUES ('Lakshman', 'Shama', 'lak@shopxx.com', 'male', 'pending');
INSERT INTO customer VALUES ('Priya', 'Mathur', 'pri@shopxx.com', 'male', 'pending');
INSERT INTO customer VALUES ('Ram', 'Agarwal', 'ram2@shopxx.com', 'male', 'pending');
INSERT INTO customer VALUES ('Sidharth', 'Goyal', 'sid@shopxx.com', 'male', 'pending');
