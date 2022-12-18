# MMCA_board_crawl
남양주시립박물관 사이트 크롤링

Table Script

CREATE TABLE `board_mmca` (  
  `SEQ` int(11) NOT NULL AUTO_INCREMENT COMMENT '시퀀스',
  `TYPE` varchar(20) DEFAULT NULL COMMENT '유형',
  `CATEGORY` varchar(20) DEFAULT NULL COMMENT '카테고리',
  `TITLE` varchar(200) NOT NULL COMMENT '제목', 
  `REG_DATE` varchar(50) NOT NULL COMMENT '등록일', 
  `READ_COUNT` int(11) NOT NULL COMMENT '조회수', 
  `CONTENT` text COMMENT '내용', 
  `ATTACH_URL` varchar(2000) DEFAULT NULL COMMENT '첨부파일 URL', 
  PRIMARY KEY (`SEQ`) 
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
