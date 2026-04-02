-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 02, 2026 at 08:29 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `amaranth`
--

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `user_id` int(255) NOT NULL,
  `type` int(3) NOT NULL,
  `username` varchar(32) NOT NULL,
  `email` varchar(128) NOT NULL,
  `password` varchar(128) NOT NULL,
  `date` date NOT NULL,
  `display_name` varchar(128) NOT NULL,
  `profile_picture` varchar(48) NOT NULL,
  `bio` text NOT NULL,
  `private` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `type`, `username`, `email`, `password`, `date`, `display_name`, `profile_picture`, `bio`, `private`) VALUES
(1, 0, 'problem_child', '', '', '2026-03-11', 'problemchild problemchild problemchild problemchild', 'problem_child.png', 'problemchild problemchild problemchild problemchildproblemchild problemchild problemchild problemchildproblemchild problemchild problemchild problemchildproblemchild problemchild problemchild problemchildproblemchild problemchild problemchild problemchildproblemchild problemchild problemchild problemchildproblemchild problemchild problemchild problemchildproblemchild problemchild problemchild problemchild', 0),
(2, 1, 'missing_bio', '', '', '2026-04-08', 'missing bio', '', '', 0),
(3, 0, 'test_username', 'test@user.com', '', '2026-04-22', 'Test user displayname', 'test_username.png', 'Test user bio', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `user_id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
