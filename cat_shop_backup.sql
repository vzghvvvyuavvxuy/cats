-- --------------------------------------------------------
-- 主机:                           127.0.0.1
-- 服务器版本:                        10.0.38-MariaDB - mariadb.org binary distribution
-- 服务器操作系统:                      Win64
-- HeidiSQL 版本:                  9.5.0.5196
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- 导出 cat shop 的数据库结构
CREATE DATABASE IF NOT EXISTS `cat shop` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin */;
USE `cat shop`;

-- 导出  表 cat shop.cart 结构
CREATE TABLE IF NOT EXISTS `cart` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `goods_id` int(11) NOT NULL,
  `count` int(11) NOT NULL DEFAULT '1',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- 正在导出表  cat shop.cart 的数据：~1 rows (大约)
/*!40000 ALTER TABLE `cart` DISABLE KEYS */;
INSERT INTO `cart` (`id`, `user_id`, `goods_id`, `count`, `create_time`) VALUES
	(2, 12, 4, 1, '2026-04-09 14:44:08');
/*!40000 ALTER TABLE `cart` ENABLE KEYS */;

-- 导出  表 cat shop.goods 结构
CREATE TABLE IF NOT EXISTS `goods` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `img_url` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- 正在导出表  cat shop.goods 的数据：~4 rows (大约)
/*!40000 ALTER TABLE `goods` DISABLE KEYS */;
INSERT INTO `goods` (`id`, `name`, `price`, `img_url`) VALUES
	(1, '逗猫棒', 4.00, './img/逗猫棒.jpg'),
	(2, '喵铮铮全价烘焙猫粮50g', 2.00, './img/喵铮铮全价烘培猫粮50g.jpg'),
	(3, '顽皮猫粮100g', 4.00, './img/顽皮猫粮100g.jpg'),
	(4, '聪颖鲜肉全价猫粮250g', 15.00, './img/聪颖鲜肉全价猫粮250g.jpg');
/*!40000 ALTER TABLE `goods` ENABLE KEYS */;

-- 导出  表 cat shop.users 结构
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE utf8mb4_bin NOT NULL,
  `password` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  `create time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- 正在导出表  cat shop.users 的数据：~12 rows (大约)
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` (`id`, `username`, `password`, `create time`) VALUES
	(1, 'testuser', '123456', '2026-04-06 21:46:25'),
	(2, '胡诗桐', '123456', '2026-04-07 19:29:02'),
	(3, '忽视它', '098765', '2026-04-07 19:35:12'),
	(4, '倪娟123', '123456', '2026-04-07 20:05:38'),
	(5, 'testuser', '123456', '2026-04-07 21:07:16'),
	(6, 'testuser', '123456', '2026-04-07 21:07:25'),
	(7, 'testuser', '123456', '2026-04-07 21:08:25'),
	(8, '原若耶', '123456', '2026-04-07 21:23:53'),
	(9, 'juauhs', '123456', '2026-04-07 21:26:16'),
	(10, 'testuser', '123456', '2026-04-09 14:34:18'),
	(11, 'testuser', '123456', '2026-04-09 14:34:33'),
	(12, '刘1+', '123456', '2026-04-09 14:42:11');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
