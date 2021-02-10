-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Czas generowania: 10 Lut 2021, 14:54
-- Wersja serwera: 8.0.21
-- Wersja PHP: 7.4.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Baza danych: `g18`
--

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `accounts`
--

CREATE TABLE `accounts` (
  `idAccounts` int UNSIGNED NOT NULL,
  `number` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `dataOpened` datetime DEFAULT NULL,
  `balance` float(60,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Zrzut danych tabeli `accounts`
--

INSERT INTO `accounts` (`idAccounts`, `number`, `dataOpened`, `balance`) VALUES
(121261, '12008000001940071174870', '2021-02-06 13:58:11', 1501.00),
(121264, '12008000001940033294389', '2021-02-06 13:58:58', 0.00),
(121265, '12008000001940099570733', '2021-02-06 13:59:03', 4559.64),
(121266, '12008000001940036612348', '2021-02-06 13:59:03', 12346.11),
(121269, '12008000001940047691051', '2021-02-06 14:56:05', 0.00),
(121270, '12008000001940037270597', '2021-02-06 14:57:01', 0.00),
(121271, '12008000001940029292377', '2021-02-06 15:00:07', 7648.74),
(121276, '12008000001940062608133', '2021-02-07 13:03:27', 0.00),
(121278, '12008000001940042990169', '2021-02-07 14:28:56', 0.00),
(121295, '12008000001940099113301', '2021-02-08 14:24:24', 583.83),
(121300, '12008000001940028062057', '2021-02-08 16:18:58', 2450.01),
(121305, '12008000001940043485927', '2021-02-09 15:14:40', 0.00),
(121308, '12008000001940037142276', '2021-02-09 15:49:37', 0.00),
(121309, '12008000001940069104785', '2021-02-09 16:22:23', 0.00),
(121310, '12008000001940078928571', '2021-02-09 17:10:06', 0.00),
(121311, '12008000001940087031864', '2021-02-09 18:26:03', 0.00),
(121312, '12008000001940016864158', '2021-02-09 19:16:47', 0.00),
(121313, '12008000001940091869813', '2021-02-09 19:16:49', 0.00),
(121314, '12008000001940026594629', '2021-02-09 19:22:21', 0.00),
(121315, '12008000001940060623080', '2021-02-09 19:22:22', 0.00),
(121316, '12008000001940093491257', '2021-02-09 19:34:41', 0.00),
(121317, '12008000001940060534197', '2021-02-09 19:34:42', 0.00),
(121318, '12008000001940030517996', '2021-02-09 19:34:44', 0.00),
(121319, '12008000001940073460157', '2021-02-09 20:28:01', 0.00),
(121320, '12008000001940020893614', '2021-02-09 20:28:06', 0.00),
(121321, '12008000001940073823485', '2021-02-09 20:51:02', 0.00),
(121322, '12008000001940025693365', '2021-02-09 20:51:03', 0.00),
(121323, '12008000001940099583328', '2021-02-09 21:48:48', 0.00),
(121324, '12008000001940041254555', '2021-02-09 21:49:09', 0.00),
(121325, '12008000001940011165407', '2021-02-09 21:49:31', 0.00),
(121326, '12008000001940069055399', '2021-02-09 21:49:32', 0.00),
(121327, '12008000001940021483988', '2021-02-09 21:50:22', 0.00),
(121328, '12008000001940066588897', '2021-02-09 21:50:40', 0.00),
(121329, '12008000001940052329486', '2021-02-09 21:50:48', 0.00),
(121330, '12008000001940045944801', '2021-02-09 21:52:43', 0.00),
(121331, '12008000001940048689642', '2021-02-09 21:54:26', 0.00),
(121332, '12008000001940063606645', '2021-02-09 21:54:27', 0.00),
(121333, '12008000001940079826996', '2021-02-09 22:01:01', 0.00),
(121334, '12008000001940020001226', '2021-02-09 22:01:03', 0.00),
(121335, '12008000001940030886650', '2021-02-09 22:13:37', 0.00),
(121336, '12008000001940035845208', '2021-02-10 09:42:05', 0.00),
(121337, '12008000001940099029713', '2021-02-10 09:42:06', 0.00),
(121338, '12008000001940083126517', '2021-02-10 09:48:07', 0.00),
(121339, '12008000001940072424989', '2021-02-10 11:26:14', 0.00);

--
-- Wyzwalacze `accounts`
--
DELIMITER $$
CREATE TRIGGER `accounts_au` AFTER UPDATE ON `accounts` FOR EACH ROW BEGIN
    UPDATE owners SET idAccounts=old.idAccounts where idAccounts is NULL;
  END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `allOwners`
--

CREATE TABLE `allOwners` (
  `idAccounts` int DEFAULT NULL,
  `idCustomers` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Zrzut danych tabeli `allOwners`
--

INSERT INTO `allOwners` (`idAccounts`, `idCustomers`) VALUES
(121256, 1),
(121257, 1),
(121258, 1),
(121259, 4),
(121260, 4),
(121261, 4),
(121262, 4),
(121263, 4),
(121264, 2),
(121265, 2),
(121266, 2),
(121267, 2),
(121268, 1),
(121269, 1),
(121270, 1),
(121271, 1),
(121272, 1),
(121273, 1),
(121274, 1),
(121275, 1),
(121276, 4),
(121277, 1),
(121278, 4),
(121279, 1),
(121280, 1),
(121281, 1),
(121282, 1),
(121283, 1),
(121284, 1),
(121285, 1),
(121286, 1),
(121287, 1),
(121288, 1),
(121289, 1),
(121290, 1),
(121291, 1),
(121292, 2),
(121293, 1),
(121294, 1),
(121295, 1),
(121296, 2),
(121297, 2),
(121298, 2),
(121299, 2),
(121300, 1),
(121301, 1),
(121302, 1),
(121303, 1),
(121304, 2),
(121305, 1),
(121307, 1),
(121307, 1),
(121308, 1),
(121309, 4),
(121310, 1),
(121311, 2),
(121312, 2),
(121313, 2),
(121314, 2),
(121315, 2),
(121316, 2),
(121317, 2),
(121318, 2),
(121319, 2),
(121320, 2),
(121321, 2),
(121322, 2),
(121323, 2),
(121324, 2),
(121325, 2),
(121326, 2),
(121327, 2),
(121328, 2),
(121329, 2),
(121330, 2),
(121331, 2),
(121332, 2),
(121333, 2),
(121334, 2),
(121335, 2),
(121336, 2),
(121337, 2),
(121338, 2),
(121339, 2);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `credit_cards`
--

CREATE TABLE `credit_cards` (
  `idCreditCards` int NOT NULL,
  `maximumLimit` float UNSIGNED NOT NULL,
  `expiryDate` datetime NOT NULL,
  `idAccounts` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Zrzut danych tabeli `credit_cards`
--

INSERT INTO `credit_cards` (`idCreditCards`, `maximumLimit`, `expiryDate`, `idAccounts`) VALUES
(11, 5000, '2023-02-05 21:20:12', 2),
(12, 5000, '2023-02-06 13:19:40', 121253),
(13, 5000, '2023-02-06 13:20:53', 121253),
(14, 5000, '2023-02-06 13:23:35', 121254),
(15, 5000, '2023-02-06 13:24:31', 121254),
(16, 5000, '2023-02-06 13:26:22', 121253),
(17, 5000, '2023-02-06 13:31:05', 121254),
(18, 5000, '2023-02-06 13:32:16', 121253),
(23, 5000, '2023-02-06 13:41:57', 121257),
(28, 5000, '2023-02-06 14:44:43', 121258),
(29, 5000, '2023-02-06 14:56:52', 121269),
(30, 5000, '2023-02-06 15:00:13', 121270),
(35, 5000, '2023-02-07 13:24:44', 121277),
(48, 5000, '2023-02-07 19:15:27', 121273),
(65, 6000, '2023-02-07 19:45:57', 121279),
(67, 4000, '2023-02-07 20:31:01', 121279),
(68, 5000, '2023-02-07 22:03:11', 121286),
(78, 5000, '2023-02-09 17:30:18', 121264),
(88, 5000, '2023-02-09 18:11:39', 121264),
(89, 5000, '2023-02-09 18:26:34', 121264),
(94, 5000, '2023-02-09 18:31:38', 121264),
(98, 4000, '2023-02-09 18:56:29', 121265),
(121, 5000, '2023-02-09 23:45:25', 121265),
(123, 5000, '2023-02-09 23:52:47', 121265);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `customers`
--

CREATE TABLE `customers` (
  `idCustomers` int UNSIGNED NOT NULL,
  `firstName` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `lastName` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(9) COLLATE utf8mb4_unicode_ci NOT NULL,
  `login` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(87) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `dateBecomeCustomer` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Zrzut danych tabeli `customers`
--

INSERT INTO `customers` (`idCustomers`, `firstName`, `lastName`, `email`, `phone`, `login`, `password`, `dateBecomeCustomer`) VALUES
(1, 'Konrad', 'Trojan', 'k@k.pl', '782568123', 'trojan', '$pbkdf2-sha256$29000$FUJoba11zrn33htDiPFeKw$jmsIxm1R0BWXtWm.9h1SpVIy4DJBg6JmhlSIwmDCu3s', '2021-01-05 16:42:49'),
(2, 'Jan', 'Kowalski', 'kowalski@gmail.com', '784328663', 'kowalski', '$pbkdf2-sha256$29000$FUJoba11zrn33htDiPFeKw$jmsIxm1R0BWXtWm.9h1SpVIy4DJBg6JmhlSIwmDCu3s', '2021-01-01 14:49:10'),
(4, 'Piotr', 'Nowak', 'nowak@onet.pl', '997998999', 'nowak', '$pbkdf2-sha256$29000$FUJoba11zrn33htDiPFeKw$jmsIxm1R0BWXtWm.9h1SpVIy4DJBg6JmhlSIwmDCu3s', '2021-01-06 13:56:09');

--
-- Wyzwalacze `customers`
--
DELIMITER $$
CREATE TRIGGER `customers_BEFORE_INSERT` BEFORE INSERT ON `customers` FOR EACH ROW BEGIN
	IF NEW.`email` NOT LIKE '%_@%_.__%' THEN
		SIGNAL SQLSTATE VALUE '45000'
			SET MESSAGE_TEXT = '[table:person] - `email` column is not valid';
	END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `owners`
--

CREATE TABLE `owners` (
  `idAccounts` int UNSIGNED DEFAULT NULL,
  `idCustomers` int UNSIGNED NOT NULL
) ;

--
-- Zrzut danych tabeli `owners`
--

INSERT INTO `owners` (`idAccounts`, `idCustomers`) VALUES
(121261, 4),
(121265, 2),
(121266, 2),
(121295, 1),
(121300, 1),
(121310, 1),
(121335, 2);

--
-- Wyzwalacze `owners`
--
DELIMITER $$
CREATE TRIGGER `owners_ai` AFTER INSERT ON `owners` FOR EACH ROW BEGIN
    SET @num = CONCAT(CONVERT('120080000019400',char),CONVERT(FLOOR(RAND()*(99999999-10000000)+10000000), char));
    SET @oldNum = (select number FROM accounts WHERE number = @num);
 	IF @num = @oldNum THEN
    	SET @a=1;
    ELSE 
    INSERT INTO `accounts`(`idAccounts`, `number`, `dataOpened`, `balance`) VALUES (NULL,@num,NULL,0);
    END IF;
    END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `owners_au` AFTER UPDATE ON `owners` FOR EACH ROW UPDATE allOwners SET idAccounts=new.idAccounts where idAccounts is NULL
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `owners_bi` BEFORE INSERT ON `owners` FOR EACH ROW INSERT INTO `allOwners`(idCustomers) VALUES ( new.idCustomers)
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `transactions`
--

CREATE TABLE `transactions` (
  `idTransactions` int UNSIGNED NOT NULL,
  `date` datetime NOT NULL,
  `amountOfTransaction` float(60,2) NOT NULL,
  `idAccounts` int NOT NULL,
  `idAccountsOfRecipient` int NOT NULL,
  `old_balance` float(60,2) NOT NULL,
  `new_balance` float(60,2) NOT NULL,
  `message` tinytext CHARACTER SET utf8 COLLATE utf8_polish_ci,
  `idCreditCards` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Zrzut danych tabeli `transactions`
--

INSERT INTO `transactions` (`idTransactions`, `date`, `amountOfTransaction`, `idAccounts`, `idAccountsOfRecipient`, `old_balance`, `new_balance`, `message`, `idCreditCards`) VALUES
(7, '2021-02-06 16:42:16', 10.00, 121266, 121265, 13223.00, 13213.00, 'Przelew srodkow', NULL),
(32, '2021-02-08 11:13:42', 10.00, 121265, 121266, 11942.10, 11932.10, 'kasa', NULL),
(33, '2021-02-08 11:13:43', 10.00, 121265, 121266, 11932.10, 11922.10, 'kasa', NULL),
(34, '2021-02-08 14:31:45', 10.00, 121266, 121264, 13235.10, 13225.10, 'test', NULL),
(35, '2021-02-08 15:49:55', 10.00, 121265, 121271, 11922.10, 11912.10, '12', NULL),
(36, '2021-02-08 15:49:57', 10.00, 121265, 121271, 11912.10, 11902.10, '12', NULL),
(37, '2021-02-08 15:53:18', 10.00, 121265, 121271, 11902.10, 11892.10, '12', NULL),
(38, '2021-02-08 20:11:32', 10.00, 121264, 121265, 1441.00, 1431.00, 'test', NULL),
(39, '2021-02-08 20:40:13', 10.10, 121265, 121271, 11902.10, 11892.00, 'przelew', NULL),
(40, '2021-02-08 20:53:48', 10.00, 121265, 121271, 11892.00, 11882.00, 'ooo ooo', 98),
(41, '2021-02-08 20:56:45', 10.19, 121265, 121271, 11882.00, 11871.81, 'przelew', NULL),
(42, '2021-02-08 21:09:23', 101.00, 121265, 121266, 11871.80, 11770.80, 'przelewiki', NULL),
(43, '2021-02-08 21:12:21', 31.00, 121265, 121271, 11770.80, 11739.80, 'jestem przelewem', NULL),
(44, '2021-02-08 21:22:47', 100.00, 121265, 121271, 11739.80, 11639.80, 'jestem przelewem', NULL),
(45, '2021-02-08 21:27:58', 100.00, 121265, 121271, 11639.80, 11539.80, 'jestem przelewem', NULL),
(46, '2021-02-08 21:29:27', 1000.00, 121265, 121271, 11539.80, 10539.80, 'jestem przelewem', NULL),
(47, '2021-02-08 21:33:01', 1000.00, 121265, 121271, 10539.80, 9539.80, 'jestem przelewem', NULL),
(48, '2021-02-08 21:33:14', 1000.00, 121265, 121271, 9539.81, 8539.81, 'jestem przelewem', NULL),
(49, '2021-02-08 21:33:18', 1000.00, 121265, 121271, 8539.81, 7539.81, 'jestem przelewem', NULL),
(50, '2021-02-08 21:33:22', 100.00, 121265, 121271, 7539.81, 7439.81, 'jestem przelewem', NULL),
(51, '2021-02-08 21:36:08', 1.00, 121265, 121271, 7439.81, 7438.81, 'jestem przelewem', NULL),
(52, '2021-02-08 21:39:51', 1.00, 121265, 121271, 7438.81, 7437.81, 'jestem przelewem', NULL),
(53, '2021-02-08 21:39:52', 1.00, 121265, 121271, 7437.81, 7436.81, 'jestem przelewem', NULL),
(54, '2021-02-08 21:42:19', 1.00, 121265, 121271, 7436.81, 7435.81, 'jestem przelewem', NULL),
(55, '2021-02-08 21:42:21', 1.00, 121265, 121271, 7435.81, 7434.81, 'jestem przelewem', NULL),
(56, '2021-02-08 21:45:57', 1.00, 121265, 121271, 7434.81, 7433.81, 'jestem przelewem', NULL),
(57, '2021-02-08 21:47:20', 1.00, 121265, 121271, 7433.81, 7432.81, 'jestem przelewem', NULL),
(58, '2021-02-08 21:48:26', 100.00, 121265, 121271, 7432.81, 7332.81, 'jestem przelewem', NULL),
(59, '2021-02-08 21:49:21', 100.00, 121265, 121271, 7332.81, 7232.81, 'jestem przelewem', NULL),
(60, '2021-02-08 21:51:20', 1000.00, 121265, 121271, 7232.81, 6232.81, 'jestem przelewem', NULL),
(61, '2021-02-08 21:52:21', 1000.00, 121265, 121271, 6232.81, 5232.81, 'jestem przelewem', NULL),
(62, '2021-02-08 21:54:22', 10.10, 121265, 121271, 5232.81, 5222.71, 'przelewyyy', NULL),
(63, '2021-02-08 21:54:26', 10.10, 121265, 121271, 5222.71, 5212.61, 'przelewyyy', NULL),
(64, '2021-02-09 12:23:30', 30.13, 121265, 121271, 5212.61, 5182.48, 'Przelew na dobre życie', NULL),
(65, '2021-02-09 13:26:12', 1523.83, 121265, 121295, 5182.48, 3658.65, 'Hajsy z komunii', NULL),
(66, '2021-02-09 13:26:46', 1530.01, 121265, 121300, 3658.65, 2128.64, 'Pieniądze za las', NULL),
(67, '2021-02-09 13:27:08', 100.00, 121300, 121295, 1530.01, 1430.01, 'przelew', NULL),
(68, '2021-02-09 15:50:36', 10.00, 121295, 121266, 1623.83, 1613.83, 'test', NULL),
(69, '2021-02-09 15:56:18', 10.00, 121295, 121300, 1613.83, 1603.83, 'przelew', NULL),
(70, '2021-02-09 15:56:22', 10.00, 121295, 121300, 1603.83, 1593.83, 'przelew', NULL),
(71, '2021-02-09 15:57:13', 10.00, 121295, 121300, 1593.83, 1583.83, 'przelew', NULL),
(72, '2021-02-09 15:57:32', 1000.00, 121295, 121300, 1583.83, 583.83, 'przelew', NULL),
(73, '2021-02-09 15:58:11', 10.00, 121300, 121266, 2460.01, 2450.01, 'przelew', NULL),
(74, '2021-02-09 16:29:46', 10.00, 121261, 121309, 1501.00, 1491.00, 'przelew', NULL),
(75, '2021-02-09 16:30:58', 10.09, 121261, 121309, 1491.00, 1480.91, 'przelew test 1', NULL),
(76, '2021-02-09 16:31:29', 10.09, 121309, 121261, 20.09, 10.00, 'przelew test 2', NULL),
(77, '2021-02-09 16:32:08', 10.00, 121309, 121261, 10.00, 0.00, 'przelew test 3', NULL),
(78, '2021-02-09 18:37:04', 1000.00, 121264, 121265, 1431.00, 431.00, 'transfer', NULL),
(79, '2021-02-09 18:37:40', 431.00, 121264, 121265, 431.00, 0.00, 'przelew', NULL),
(80, '2021-02-10 11:27:11', 1000.00, 121266, 121265, 13346.11, 12346.11, 'kasa', NULL);

--
-- Indeksy dla zrzutów tabel
--

--
-- Indeksy dla tabeli `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`idAccounts`),
  ADD UNIQUE KEY `idAccounts_UQ` (`idAccounts`);

--
-- Indeksy dla tabeli `credit_cards`
--
ALTER TABLE `credit_cards`
  ADD PRIMARY KEY (`idCreditCards`),
  ADD KEY `idAccounts` (`idAccounts`);

--
-- Indeksy dla tabeli `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`idCustomers`),
  ADD UNIQUE KEY `login_UQ` (`login`),
  ADD UNIQUE KEY `email_UQ` (`email`),
  ADD UNIQUE KEY `idCustomers_UQ` (`idCustomers`);

--
-- Indeksy dla tabeli `owners`
--
ALTER TABLE `owners`
  ADD KEY `idCustomers_FK` (`idCustomers`);

--
-- Indeksy dla tabeli `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`idTransactions`),
  ADD KEY `idAccounts` (`idAccounts`),
  ADD KEY `idCreditCards` (`idCreditCards`) USING BTREE,
  ADD KEY `idAccountsOfRecipient` (`idAccountsOfRecipient`);

--
-- AUTO_INCREMENT dla zrzuconych tabel
--

--
-- AUTO_INCREMENT dla tabeli `accounts`
--
ALTER TABLE `accounts`
  MODIFY `idAccounts` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=121340;

--
-- AUTO_INCREMENT dla tabeli `credit_cards`
--
ALTER TABLE `credit_cards`
  MODIFY `idCreditCards` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=128;

--
-- AUTO_INCREMENT dla tabeli `customers`
--
ALTER TABLE `customers`
  MODIFY `idCustomers` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT dla tabeli `transactions`
--
ALTER TABLE `transactions`
  MODIFY `idTransactions` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=81;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
