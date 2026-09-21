-- AI 点餐助手项目用到的表：food（菜品）、notice（公告）、user（用户）
-- 导入方式: mysql -uroot -p menu_system < sql/food.sql
-- （需要先建好 menu_system 库：CREATE DATABASE menu_system DEFAULT CHARSET utf8mb4;）
-- 注意：user 表只建结构不含数据，注册功能可自行注册新账号

SET NAMES utf8mb4;
DROP TABLE IF EXISTS food;
CREATE TABLE `food` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `image` varchar(200) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `description` text,
  `status` int DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
DROP TABLE IF EXISTS notice;
CREATE TABLE `notice` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `content` text,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
DROP TABLE IF EXISTS user;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `role` int DEFAULT '2',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO food (id, name, image, price, description, status) VALUES (5, '白切鸡', 'image/白切鸡.jpg', 28.8, '肉类', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (6, '煲仔饭', 'image/煲仔饭.jpg', 16.0, '主食', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (7, '干锅虾', 'image/干锅虾.jpg', 29.9, '海鲜类', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (8, '菠萝咕噜肉', 'image/菠萝咕噜肉.jpg', 28.8, '肉类', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (9, '宫保鸡丁', 'image/宫保鸡丁.jpg', 28.0, '肉类', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (10, '蒜蓉空心菜', 'image/蒜蓉空心菜.jpg', 12.8, '蔬菜类', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (11, '番茄炒蛋', 'image/番茄炒蛋.jpg', 16.6, '蔬菜类', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (12, '辣椒炒肉', 'image/辣椒炒肉.jpg', 28.0, '肉类', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (13, '清蒸鱼', 'image/清蒸鱼.jpg', 38.8, '海鲜类', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (14, '双皮奶', 'image/双皮奶.jpg', 10.8, '甜食', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (15, '云吞面', 'image/云吞面.jpg', 15.0, '主食', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (16, '排骨', 'image/排骨.jpg', 35.0, '肉类', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (17, '麻婆豆腐', 'image/麻婆豆腐.jpg', 23.8, '肉类', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (18, '橙汁', 'image/橙汁.jpg', 4.0, '饮料|果汁', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (19, '红牛', 'image/红牛.jpg', 5.0, '饮料', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (20, '养乐多', 'image/养乐多.jpg', 3.0, '牛奶|饮料', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (21, '矿泉水', 'image/矿泉水.jpg', 2.0, '饮料|水', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (22, '冰香草拿铁', 'image/冰香草拿铁.jpg', 6.0, '饮料|咖啡', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (23, '焦糖玛奇朵', 'image/焦糖玛奇朵.jpg', 6.0, '饮料|咖啡', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (24, '树莓石榴汁', 'image/树莓石榴汁.jpg', 6.0, '饮料|果汁', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (25, '水溶C', 'image/水溶C.jpg', 5.0, '饮料', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (26, '西瓜汁', 'image/西瓜汁.jpg', 5.0, '饮料|果汁', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (27, '西柚血橙气泡饮料', 'image/西柚血橙气泡饮料.jpg', 6.0, '饮料|汽水', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (28, '榛果巧克力牛奶', 'image/榛果巧克力牛奶.jpg', 7.0, '牛奶|饮料', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (29, '草莓奥利奥蛋糕', 'image/草莓奥利奥蛋糕.jpg', 15.0, '蛋糕|甜点', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (30, '草莓车厘子千层', 'image/草莓车厘子千层.jpg', 16.0, '蛋糕|甜点|千层', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (31, '草莓舒芙蕾', 'image/草莓舒芙蕾.jpg', 18.0, '舒芙蕾|蛋糕|甜点', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (32, '车厘子草莓抹茶味蛋糕', 'image/车厘子草莓抹茶味蛋糕.jpg', 18.0, '蛋糕|甜点', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (33, '法棍', 'image/法棍.jpg', 10.0, '面包|甜点', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (34, '开心果千层', 'image/开心果千层.jpg', 16.0, '蛋糕|甜点|千层', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (35, '蓝莓千层', 'image/蓝莓千层.jpg', 16.0, '蛋糕|甜点|千层', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (36, '芒果千层', 'image/芒果千层.jpg', 16.0, '蛋糕|千层|甜点', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (37, '抹茶蛋糕', 'image/抹茶蛋糕.jpg', 15.0, '蛋糕|甜点', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (38, '抹茶曲奇', 'image/抹茶曲奇.jpg', 6.0, '曲奇|甜点|饼干', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (39, '抹茶吐司', 'image/抹茶吐司.jpg', 20.0, '面包|甜点|吐司', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (40, '巧克力蛋糕', 'image/巧克力蛋糕.jpg', 20.0, '蛋糕|甜点', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (41, '树莓冰淇淋', 'image/树莓冰淇淋.jpg', 16.0, '冰淇淋', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (42, '菠萝', 'image/菠萝.jpg', 8.0, '水果', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (43, '草莓', 'image/草莓.jpg', 13.8, '水果\r\n', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (44, '哈密瓜', 'image/哈密瓜.jpg', 15.0, '水果', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (45, '红芭乐', 'image/红芭乐.jpg', 5.0, '水果', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (46, '蓝莓', 'image/蓝莓.jpg', 9.9, '水果', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (47, '榴莲', 'image/榴莲.jpg', 188.0, '水果', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (48, '芒果', 'image/芒果.jpg', 8.0, '水果', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (49, '猕猴桃', 'image/猕猴桃.jpg', 10.0, '水果', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (50, '牛油果', 'image/牛油果.jpg', 13.8, '水果', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (51, '柠檬', 'image/柠檬.jpg', 3.0, '水果', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (52, '水蜜桃', 'image/水蜜桃.jpg', 6.0, '水果', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (53, '西瓜', 'image/西瓜.jpg', 20.0, '水果', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (54, '苹果', 'image/苹果.jpg', 6.0, '水果', 1);
INSERT INTO food (id, name, image, price, description, status) VALUES (55, '水果盘', 'image/水果盘.jpg', 26.0, '水果', 1);

INSERT INTO notice (title, content) VALUES ('今日份上新', '白切鸡');
INSERT INTO notice (title, content) VALUES ('NOTICE', 'Now，everything is OK!');
INSERT INTO notice (title, content) VALUES ('emmmm', 'today.....');
INSERT INTO notice (title, content) VALUES ('吐槽', 'i do not like meat');
INSERT INTO notice (title, content) VALUES ('提问', '双皮奶好吃吗？？');
INSERT INTO notice (title, content) VALUES ('你今天想吃什么', '........');
