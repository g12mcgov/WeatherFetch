CREATE TABLE `members` (
  `memberID` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(60) NOT NULL,
  `EmailAddress` varchar(255) NOT NULL,
  `Time` time NOT NULL,
  `Timezone` varchar(255) NOT NULL,
  `Zipcode` char(5) NOT NULL,
  `active` varchar(255) NOT NULL,
  `resetToken` varchar(255) DEFAULT NULL,
  `resetComplete` varchar(3) DEFAULT 'No',
  PRIMARY KEY (`memberID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
