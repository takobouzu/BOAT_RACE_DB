/*
【システム】BOAT_RACE_DB2
【ファイル】mk_m_cyakuten.sql
【機能仕様】着点マスタ定義
【動作環境】macOS 11.1/Raspbian OS 10.4/python 3.9.1/sqlite3 3.32.3
【来　　歴】2021.03.01 ver 1.00
*/
--着点マスタ
CREATE TABLE "m_cyakuten"(
	[race_name_kubun]	text,	--レース区分　優勝戦 or 優勝戦以外
	[grade]				text,	--グレード
	[ranking]			text,	--順位
	[cyakuten]			integer,	--着点
	PRIMARY KEY([race_name_kubun],[grade],[ranking])
);
