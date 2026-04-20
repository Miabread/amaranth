-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 20, 2026 at 05:04 PM
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
-- Table structure for table `comment`
--

CREATE TABLE `comment` (
  `comment_id` int(255) NOT NULL,
  `post_id` int(11) NOT NULL,
  `content` text NOT NULL,
  `author` int(255) NOT NULL,
  `date` date NOT NULL,
  `likes` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `comment`
--

INSERT INTO `comment` (`comment_id`, `post_id`, `content`, `author`, `date`, `likes`) VALUES
(1, 1, 'Normal text for test post', 3, '2026-04-20', 321),
(2, 2, '<h1>This shouldn\'t work</h1>\r\nStupid problem child.', 1, '2026-04-02', 2),
(3, 1, 'Another test comment', 2, '2026-04-09', 3),
(4, 1, 'Another another test by test_username', 3, '2026-04-17', 999),
(5, 2, 'Really long text really long text really long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long textreally long text', 1, '2026-04-01', 0);

-- --------------------------------------------------------

--
-- Table structure for table `post`
--

CREATE TABLE `post` (
  `post_id` int(11) NOT NULL,
  `title` varchar(32) NOT NULL,
  `content` text NOT NULL,
  `author` int(255) NOT NULL,
  `date` date NOT NULL,
  `likes` int(255) NOT NULL,
  `hidden` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `post`
--

INSERT INTO `post` (`post_id`, `title`, `content`, `author`, `date`, `likes`, `hidden`) VALUES
(1, 'Test post', 'Testposttestposttestpost', 1, '2026-04-07', 32, 0),
(2, 'the problem child', 'noone', 1, '2026-04-22', 3, 0),
(9, 'Test insert', 'Test', 1, '2026-04-08', 0, 0);

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
(3, 0, 'test_username', 'test@user.com', '', '2026-04-22', 'Test user displayname', 'test_username.png', 'Test user bio', 0),
(4, 0, 'test_insert_user', 'test@example.org', '$argon2id$v=19$m=65536,t=3,p=4$mCMdracRX6gRLKgb02Nd2w$wcLnmIIZo/ecFsCrJ+ELxaAgjy8eVR+q5rI7Wb9E/H8', '2026-04-16', 'test_insert_user', 'problem_child.png', '', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `comment`
--
ALTER TABLE `comment`
  ADD PRIMARY KEY (`comment_id`),
  ADD KEY `fk_comment_author_user_id` (`author`) USING BTREE,
  ADD KEY `fk_comment_post_id` (`post_id`) USING BTREE;

--
-- Indexes for table `post`
--
ALTER TABLE `post`
  ADD PRIMARY KEY (`post_id`),
  ADD KEY `fk_post_author_user_id` (`author`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `comment`
--
ALTER TABLE `comment`
  MODIFY `comment_id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `post`
--
ALTER TABLE `post`
  MODIFY `post_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `user_id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `comment`
--
ALTER TABLE `comment`
  ADD CONSTRAINT `fk_comment_author_user_id` FOREIGN KEY (`author`) REFERENCES `user` (`user_id`),
  ADD CONSTRAINT `fk_comment_post_id` FOREIGN KEY (`post_id`) REFERENCES `post` (`post_id`);

--
-- Constraints for table `post`
--
ALTER TABLE `post`
  ADD CONSTRAINT `fk_post_author_user_id` FOREIGN KEY (`author`) REFERENCES `user` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
