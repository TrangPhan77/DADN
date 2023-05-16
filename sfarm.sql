-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 20, 2023 at 08:12 AM
-- Server version: 10.4.25-MariaDB
-- PHP Version: 8.1.10
-- DROP DATABASE sfarm;
CREATE DATABASE sfarm;
USE sfarm;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sfarm`
--

-- --------------------------------------------------------

--
-- Table structure for table `area`
--

CREATE TABLE `area` (
  `A_ID` int(10) NOT NULL,
  `Name` varchar(225) NOT NULL,
  `LowestHumidity` int(10) NOT NULL,
  `AutoWaterDuration` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `area_record` (
  `A_ID` int(10) NOT NULL,
  `DateTime` datetime NOT NULL,
  `amount` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


INSERT INTO `area` (`A_ID`, `Name`, `LowestHumidity`, `AutoWaterDuration`) VALUES
(1, 'Khu Vực Cây Ăn Quả', 50, '00:20:00.000000'),
(2, 'Khu Vực Rau Củ', 25, '00:20:00.000000'),
(3, 'Khu Vực Trồng Hoa', 25, '00:20:00.000000'),
(4, 'Khu Vực Cây Kiểng', 25, '00:20:00.000000');

-- --------------------------------------------------------
--
-- Table structure for table `light_record`
--
CREATE TABLE `light_record` (
  `L_ID` int(10) NOT NULL,
  `DateTime` datetime NOT NULL,
  `data` int(10) NOT NULL,
  `A_ID` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
-- SELECT  YEAR(DateTime), MONTH(DateTime), AVG(TempData) FROM temp_record WHERE A_ID = 1 AND DateTime >= '2023-04-01 18:00' AND DateTime <= '2023-04-15 18:00' GROUP BY YEAR(DateTime), MONTH(DateTime);
--
-- Dumping data for table `light_record`
--

-- --------------------------------------------------------

--
-- Table structure for table `moist_record`
--

CREATE TABLE `moist_record` (
  `M_ID` int(10) NOT NULL,
  `DateTime` datetime NOT NULL,
  `data` int(10) NOT NULL,
  `A_ID` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `moist_record`
--

-- --------------------------------------------------------

--
-- Table structure for table `notification`
--


CREATE TABLE `notification` (
  `N_ID` int(10) NOT NULL,
  `Date` date NOT NULL,
  `Time` time(6) NOT NULL,
  `Message` varchar(255) NOT NULL,
  `A_ID` int(10) NOT NULL,
  `U_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `pumper`
--

CREATE TABLE `pumper` (
  `P_ID` int(10) NOT NULL,
  `Status` enum('Đang tắt','Đang hoạt động') NOT NULL,
  `A_ID` int(10) NOT NULL,
  `type_watering` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


INSERT INTO `pumper` (`P_ID`, `Status`, `A_ID`, `type_watering`) VALUES
(1, 'Đang tắt', 1, 0);
--
-- Dumping data for table `pumper`
--

-- --------------------------------------------------------

--
-- Table structure for table `temp_record`
--

CREATE TABLE `temp_record` (
  `T_ID` int(10) NOT NULL,
  `DateTime` datetime NOT NULL,
  `data` int(10) NOT NULL,
  `A_ID` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `temp_record`
--

CREATE TABLE `pumper_record` (
  `ID` int(10) NOT NULL,
  `DateTime` datetime NOT NULL,
  `Time` int(10) NOT NULL,
  `Type` int(10) NOT NULL,
  `A_ID` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `U_ID` int(10) NOT NULL,
  `UserName` varchar(50) NOT NULL,
  `PassWord` varchar(50) NOT NULL,
  `Name` varchar(50) DEFAULT NULL,
  `Birthday` date DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL,
  `Email` varchar(225) DEFAULT NULL,
  `Phone` varchar(11) DEFAULT NULL,
  `Image` varchar(225) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


--
-- Dumping data for table `user`
--

INSERT INTO `user` (`U_ID`, `UserName`, `PassWord`, `Name`, `Birthday`, `Address`, `Email`, `Phone`, `Image`) VALUES
(1, 'Tam', '123', NULL, NULL, NULL, NULL, NULL, NULL),
(3, 'Thanh', '123', NULL, NULL, NULL, NULL, NULL, NULL),
(7, 'Toan', '123', NULL, NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `watering_schedual`
--

CREATE TABLE `watering_schedual` (
  `SST` int(10) NOT NULL,
  `Time` int(10) NOT NULL,
  `Cycle` int(10) NOT NULL,
  `Duration` int(10) NOT NULL,
  `A_ID` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `area`
--
ALTER TABLE `area`
  ADD PRIMARY KEY (`A_ID`);

--
-- Indexes for table `light_record`
--
ALTER TABLE `light_record`
  ADD PRIMARY KEY (`L_ID`),
  ADD KEY `light1` (`A_ID`);

--
-- Indexes for table `moist_record`
--
ALTER TABLE `moist_record`
  ADD PRIMARY KEY (`M_ID`),
  ADD KEY `moist1` (`A_ID`);

--
-- Indexes for table `notification`
--
ALTER TABLE `notification`
  ADD PRIMARY KEY (`N_ID`),
  ADD KEY `Notify1` (`A_ID`),
  ADD KEY `Nodify2` (`U_ID`);

--
-- Indexes for table `pumper`
--
ALTER TABLE `pumper`
  ADD PRIMARY KEY (`P_ID`),
  ADD KEY `Pumper` (`A_ID`);

--
-- Indexes for table `temp_record`
--
ALTER TABLE `temp_record`
  ADD PRIMARY KEY (`T_ID`),
  ADD KEY `temp1` (`A_ID`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`U_ID`);

--
-- Indexes for table `watering_schedual`
--
ALTER TABLE `watering_schedual`
  ADD PRIMARY KEY (`SST`),
  ADD KEY `WS1` (`A_ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `area`
--
ALTER TABLE `area`
  MODIFY `A_ID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `light_record`
--
ALTER TABLE `light_record`
  MODIFY `L_ID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `moist_record`
--
ALTER TABLE `moist_record`
  MODIFY `M_ID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `notification`
--
ALTER TABLE `notification`
  MODIFY `N_ID` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pumper`
--
ALTER TABLE `pumper`
  MODIFY `P_ID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `temp_record`
--
ALTER TABLE `temp_record`
  MODIFY `T_ID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `U_ID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `watering_schedual`
--
ALTER TABLE `watering_schedual`
  MODIFY `SST` int(10) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `light_record`
--
ALTER TABLE `light_record`
  ADD CONSTRAINT `light1` FOREIGN KEY (`A_ID`) REFERENCES `area` (`A_ID`);

--
-- Constraints for table `moist_record`
--
ALTER TABLE `moist_record`
  ADD CONSTRAINT `moist1` FOREIGN KEY (`A_ID`) REFERENCES `area` (`A_ID`);

--
-- Constraints for table `notification`
--
ALTER TABLE `notification`
  ADD CONSTRAINT `Nodify2` FOREIGN KEY (`U_ID`) REFERENCES `user` (`U_ID`),
  ADD CONSTRAINT `Notify1` FOREIGN KEY (`A_ID`) REFERENCES `area` (`A_ID`);

--
-- Constraints for table `pumper`
--
ALTER TABLE `pumper`
  ADD CONSTRAINT `Pumper` FOREIGN KEY (`A_ID`) REFERENCES `area` (`A_ID`);

--
-- Constraints for table `temp_record`
--
ALTER TABLE `temp_record`
  ADD CONSTRAINT `temp1` FOREIGN KEY (`A_ID`) REFERENCES `area` (`A_ID`);

--
-- Constraints for table `watering_schedual`
--
ALTER TABLE `watering_schedual`
  ADD CONSTRAINT `WS1` FOREIGN KEY (`A_ID`) REFERENCES `area` (`A_ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
