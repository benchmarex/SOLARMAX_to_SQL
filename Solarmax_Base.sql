-- phpMyAdmin SQL Dump
-- version 5.0.4deb2+deb11u1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Czas generowania: 30 Mar 2023, 22:19
-- Wersja serwera: 10.5.15-MariaDB-0+deb11u1
-- Wersja PHP: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Baza danych: `Solarmax_Base`
--

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `Solarmax`
--

CREATE TABLE `Solarmax` (
  `Id` double NOT NULL,
  `date` datetime DEFAULT NULL,
  `Energy` float DEFAULT NULL COMMENT 'kWh',
  `Power_AC` float DEFAULT NULL COMMENT 'W',
  `Inverter_Temperature` float DEFAULT NULL COMMENT '°C',
  `Voltage_AC1` float DEFAULT NULL COMMENT 'V',
  `Voltage_AC2` float DEFAULT NULL COMMENT 'V',
  `Voltage_AC3` float DEFAULT NULL COMMENT 'V',
  `Current_AC1` float DEFAULT NULL COMMENT 'A',
  `Current_AC2` float DEFAULT NULL COMMENT 'A',
  `Current_AC3` float DEFAULT NULL COMMENT 'A',
  `Power_DC1` float DEFAULT NULL COMMENT 'W',
  `Power_DC2` float DEFAULT NULL COMMENT 'W',
  `Voltage_DC1` float DEFAULT NULL COMMENT 'V',
  `Voltage_DC2` float DEFAULT NULL COMMENT 'V',
  `Current_DC1` float DEFAULT NULL COMMENT 'A',
  `Current_DC2` float DEFAULT NULL COMMENT 'A',
  `Time_Stamp` datetime NOT NULL DEFAULT current_timestamp(),
  `Ac_freq` float DEFAULT NULL COMMENT 'Hz',
  `Module_temperature` float DEFAULT NULL COMMENT '°C',
  `Insulation_imp_cath_gnd` float DEFAULT NULL COMMENT 'kΩ',
  `Insulation_imp_PV1` float DEFAULT NULL COMMENT 'kΩ',
  `Insulation_imp_PV2` float DEFAULT NULL COMMENT 'kΩ',
  `AC_reactive_power` float DEFAULT NULL COMMENT 'VAR',
  `AC_Today_Generation_Time` int(4) DEFAULT NULL COMMENT 'minutes'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indeksy dla zrzutów tabel
--

--
-- Indeksy dla tabeli `Solarmax`
--
ALTER TABLE `Solarmax`
  ADD PRIMARY KEY (`Id`);

--
-- AUTO_INCREMENT dla zrzuconych tabel
--

--
-- AUTO_INCREMENT dla tabeli `Solarmax`
--
ALTER TABLE `Solarmax`
  MODIFY `Id` double NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
