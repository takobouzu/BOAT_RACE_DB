/*
【システム】BOAT_RACE_DB2
【ファイル】mk_db.sql
【機能仕様】テーブル定義・インデックス定義 SQL
【動作環境】macOS 11.1/Raspbian OS 10.4/python 3.9.1/sqlite3 3.32.3
【来　　歴】2021.02.01 ver 1.00
*/

--選手マスタ
CREATE TABLE"m_player"(
    [player_no]		text,   --登録番号
	[player_name]	text,   --選手名
	[sex]			text,	--性別
	[height]		text,	--身長
	PRIMARY KEY("player_no")
);

--場名マスタ
CREATE TABLE"m_pool_code"(
	[pool_code]		text,	--場コード
	[pool_name]		text,	--場名
	PRIMARY KEY("pool_code")
);

--前検データ
CREATE TABLE[t_tenken](
    [yyyy]                  text,	    --開催年
	[yyyymmdd]              text,       --開催年月日
	[pool_code]             text,	    --場コード
	[title]		            text,	    --レースタイトル
	[motor_no]              text,       --モーター番号
	[rank]                  integer,    --前検タイムランク
	[player_no]             text,	    --登録番号
	[player_name]           text,       --選手名
	[class]					text,	    --級別
	[motor_double_rate]		real,	    --モーター二連率
	[boat_no]				text,       --ボート番号
	[boat_double_rate]		real,       --ボート二連率
	[time]real,
	PRIMARY KEY	([yyyy],[yyyymmdd],[pool_code],[title],[motor_no])
);


--直前情報明細
CREATE TABLE[t_info_d](
	[yyyymmdd]			text,		--開催日付
	[pool_code]			text,		--場コード
	[race_no]			text,		--レース番号
	[entry_no]			text,		--枠番
	[body_weight]		real,		--体重
	[adjusted_weight]	real,		--調整重量
	[rehearsal_time]	real,		--展示タイム
	[tilt]				real,		--チルト
	[start_course]		integer,	--スタート展示コース
	[flying]			text,		--フライング区分 F:フライングL:出遅れ
	[start_time]		real,		--スタート展示タイム
	PRIMARY KEY	([yyyymmdd],[pool_code],[race_no],[entry_no])
);

--直前情報　ヘッダ
CREATE TABLE[t_info_h](
	[yyyymmdd]			text,	--開催日付
	[pool_code]			text,	--場コード
	[race_no]			text,	--レース番号
	[temperature]		real,	--気温
	[weather]			text,	--天候
	[wind_speed]		real,	--風速
	[water_temperature]	real,	--水温
	[wave_height]		real,	--波高
	[wind]				text,	--風向
	PRIMARY KEY	([yyyymmdd],[pool_code],[race_no])
);

--交換部品
CREATE TABLE[t_info_p](
	[yyyymmdd]	text,	--開催日付
	[pool_code]	text,	--場コード
	[race_no]	text,	--レース番号
	[entry_no]	text,	--枠番
	[motor_no]	text,	--モーター番号
	[parts]		text	--部品交換区分
);

--オッズ
CREATE TABLE[t_odds](
	[yyyymmdd]		text,	--開催日付
	[pool_code]		text,	--場コード
	[race_no]		text,	--レース番号
	[ticket_type]	text,	--券種
	[focus]			text,	--組番
	[odds]			real	--オッズ
);

--出走表明細
CREATE TABLE[t_race_d](
	[yyyymmdd]		            text,	    --開催日付
	[pool_code]		            text,	    --場コード
	[race_no]		            text,	    --レース番号
	[entry_no]		            text,	    --枠番
	[pool_name]		            text,	    --場名
	[player_no]		            text,	    --登録番号
	[player_name]	            text,	    --選手名
	[class]			            text,	    --級別
	[area]			            text,	    --支部
	[player_native_place]	    text,		--出身地
	[age]					    integer,	--年齢
	[body_weight]			    real,	    --体重
	[flying_count]			    integer,    --フライング回数
	[lost_count]			    integer,    --出遅れ回数
	[st]					    real,	    --平均スタートタイミング
	[nationwide_win_rate]		real,	    --全国勝率
	[nationwide_double_rate]	real,	    --全国二連率
	[nationwide_triple_rate]	real,	    --全国三連率
	[local_win_rate]			real,	    --当地勝率
	[local_double_rate]		    real,	    --当地二連率
	[local_triple_rate]		    real,	    --当地三連率
	[motor_no]				    text,	    --モーター番号
	[motor_double_rate]		    real,	    --モーター二連率
	[motor_triple_rate]		    real,	    --モーター三連率
	[boat_no]				    text,	    --ボート番号
	[boat_double_rate]		    real,	    --ボート二連率
	[boat_triple_rate]		    real,	    --ボート三連率
	PRIMARY KEY	([yyyymmdd],[pool_code],[race_no],[entry_no])
);

--出走表ヘッダ
CREATE TABLE[t_race_h](
	[yyyymmdd]		        text,	--開催日付
	[pool_code]		        text,	--場コード
	[race_no]		        text,	--レース番号
	[pool_name]		        text,	--場名
	[scheduled_deadline]	text,	--レース締切予定時間
	[race_name]		        text,	--レース名
	[distance]		        text,	--距離
	[stabilizer]	        text,	--安定板使用区分0:未使用1:安定板使用
	[approach]		        text,	--進入固定区分0:通常1:進入固定
	PRIMARY KEY	([yyyymmdd],[pool_code],[race_no])
);

--レースタイトル
CREATE TABLE[t_race_t](
	[yyyymmdd]		text,	--開催日付
	[pool_code]		text,	--場コード
	[pool_name]		text,	--場名
	[grade]			text,	--グレード1
	[holding]		text,	--開催時間帯
	[title]			text,	--レースタイトル
	[event_date]	text,	--開催日
	[situation]		text,	--進行状況
	PRIMARY KEY	([yyyymmdd],[pool_code])
);

--レース結果明細
CREATE TABLE[t_result_d] (
	[yyyymmdd]			text,		--開催日付
	[pool_code]			text,		--場コード
	[race_no]			text,		--レース番号
	[entry_no]			text,		--枠順
	[ranking]			text,		--順位
	[race_time]			text,		--レースタイム
	[course]			integer,	--コース
	[flying]			text,		--フライング・出遅れ
	[start_time]		real,		--スタートタイム
	[decisive_facto]	text,		--決まり手
	PRIMARY KEY ([yyyymmdd],[pool_code],[race_no],[entry_no])
);

--レース結果ヘッダ
CREATE TABLE[t_result_h](
	[yyyymmdd]			text,	--開催日付
	[pool_code]			text,	--場コード
	[race_no]			text,	--レース番号
	[temperature]		real,	--気温
	[weather]			text,   --天候
	[wind_speed]		real,	--風速
	[water_temperature]	real,	--水温
	[wave_height]		real,	--波高
	[wind]				text,   --風向
	[return]			text,	--返還
	[decisive_factor]	text,   --決まり手
	[remarks]			text,	--備考
	[kiatu]				real,	--気圧
	[situdo]			real,	--湿度
	PRIMARY KEY	([yyyymmdd],[pool_code],[race_no])
);

--レース結果オッズ
CREATE TABLE[t_result_oods](
	[yyyymmdd]		text,		--開催日付
	[pool_code]		text,		--場コード
	[race_no]		text,		--レース番号
	[ticket_type]	text,		--券種
	[focus]			text,		--組番
	[dividend]		integer,	--払戻金
	[popularity]	integer		--人気
);

--当日予想用 レースタイトル
CREATE TABLE [x_race_t] (
	[yyyymmdd]      text,	    --開催日付
	[pool_code]	    text,	    --場コード
	[pool_name]     text,       --場名
	[grade]	    	text,	    --グレード 10:一般 11:女子一般 12:若手一般 20:G3 21:女子G3 22:若手G3  30:G2 31:女子G2 32:若手G2 40:G1 41:女子G1 42:若手G1 50:SG 51:女子SG 52:若手SG  
	[holding]    	text,       --開催時間帯区分 0:通常 1:モーニング 2:ナイター 3:サマータイム  
	[title]		    text,	    --レースタイトル
	[event_date]	text,	    --開催日
	[situation]	    text,	    --進行状況
	PRIMARY KEY	([yyyymmdd],[pool_code])
);

--当日予想用　出走表ヘッダ
CREATE TABLE [x_race_h] (
	[yyyymmdd]			    text,	    --開催日付
	[pool_code]			    text,	    --場コード
	[race_no]			    text,    	--レース番号
	[pool_name]				text,		--場名
	[scheduled_deadline]    text,	    --レース締切予定時間
	[race_name]			    text,	    --レース名
	[distance]			    text,       --距離
	[stabilizer]		    text,    	--安定板使用区分 0:未使用 1:安定板使用
	[approach]		    	text,   	--進入固定区分 0:通常 1:進入固定
	PRIMARY KEY	([yyyymmdd],[pool_code],[race_no])
);

--当日予想用　出走表明細
CREATE TABLE [x_race_d] (
	[yyyymmdd]			        text,	    --開催日付
	[pool_code]			        text,	    --場コード
	[race_no]			        text,    	--レース番号
	[entry_no]				    text,	    --枠番
	[pool_name]				    text,		--場名
	[player_no]				    text,	    --登録番号
	[player_name]               text,       --選手名
	[class]					    text,	    --級別
	[area]				        text,       --支部
	[player_native_place]	    text,	    --出身地
	[age]					    integer,	--年齢
	[body_weight]			    real,	    --体重
	[flying_count]			    integer,    --フライング回数
	[lost_count]				integer,    --出遅れ回数
	[st]						real,	    --平均スタートタイミング
	[nationwide_win_rate]	    real,	    --全国勝率
	[nationwide_double_rate]    real,	    --全国二連率
	[nationwide_triple_rate]	real,	    --全国三連率
	[local_win_rate]			real,	    --当地勝率
	[local_double_rate]		    real,	    --当地二連率
	[local_triple_rate]		    real,	    --当地三連率
	[motor_no]				    text,       --モーター番号
	[motor_double_rate]		    real,	    --モーター二連率
	[motor_triple_rate]		    real,	    --モーター三連率
	[boat_no]				    text,       --ボート番号
	[boat_double_rate]		    real,	    --ボート二連率
	[boat_triple_rate]		    real,	    --ボート三連率
	PRIMARY KEY	([yyyymmdd],[pool_code],[race_no],[entry_no])
);

--指数テーブル
CREATE TABLE [t_index](
    [yyyymmdd]                      TEXT,       --開催日付
    [pool_code]                     TEXT,       --場コード
    [race_no]                       TEXT,       --レース番号
    [entry_no]                      TEXT,       --枠番
    [player_no]                     TEXT,       --選手登録番号
    [motor_no]                      TEXT,       --モーター番号
    [ability]                       TEXT,       --能力
    [st]                            TEXT,       --平均ST
    [ability_count]                 TEXT,       --能力算出対象レース数
    [ability2]                      TEXT,       --直近能力
    [st2]                           TEXT,       --直近平均ST
    [ability2_count]                integer,    --直近能力算出対象
    [rate_win_motor]                real,       --モーター能力
	[motor_hensa]					real,       --モーター偏差
    [rate_win_count]                integer,    --モーター能力算出対象レース数
    [motor_count1]                  integer,    --モーター能力算出対象レース数（１コース）
    [motor_count2]                  integer,    --モーター能力算出対象レース数（２コース）
    [motor_count3]                  integer,    --モーター能力算出対象レース数（３コース）
    [motor_count4]                  integer,    --モーター能力算出対象レース数（４コース）
    [motor_count5]                  integer,    --モーター能力算出対象レース数（５コース）
    [motor_count6]                  integer,    --モーター能力算出対象レース数（６コース）
    [rate_win_motor_course1]        real,       --モーター能力（１コース）
    [rate_win_motor_course2]        real,       --モーター能力（２コース）
    [rate_win_motor_course3]        real,       --モーター能力（３コース）
    [rate_win_motor_course4]        real,       --モーター能力（４コース）
    [rate_win_motor_course5]        real,       --モーター能力（５コース）
    [rate_win_motor_course6]        real,       --モーター能力（６コース）
    [course_count_1]                integer,    --出走数（１コース）
    [ability_course_1]              real,       --能力値（１コース）
    [sinnyu_course_1]               real,       --進入偏差（１コース）
    [nige_win_count_course_1]       integer,    --逃げ切り勝ち数（１コース）
    [nige_win_rate_course_1]        real,       --逃げ切り勝ち率（１コース）
    [makuri_lost_count_course_1]    integer,    --まくられ数（１コース）
    [makuri_lost_rate_course_1]     real,       --まくられ率（１コース）
    [sashi_lost_count_course_1]     integer,    --差され数（１コース）
    [sashi_lost_rate_course_1]      real,       --差され率（１コース）
    [course_count_2]                integer,    --出走数（２コース）
    [ability_course_2]              real,       --能力値（２コース）
    [sinnyu_course_2]               real,       --進入偏差（２コース）
    [nige_lost_count_course_2]      integer,    --逃し数（２コース）
    [nige_lost_rate_course_2]       real,       --逃し率（２コース）
    [makuri_win_count_course_2]     integer,    --まくり数（２コース）
    [makuri_win_rate_course_2]      real,       --まくり率（２コース）
    [sashi_win_count_course_2]      integer,    --差し数（２コース）
    [sashi_win_rate_course_2]       real,       --差し率（２コース）
    [course_count_3]                integer,    --出走数（３コース）
    [ability_course_3]              real,       --能力値（３コース）
    [sinnyu_course_3]               real,       --進入偏差（３コース）
    [makuri_win_count_course_3]     integer,    --まくり数（３コース）
    [makuri_win_rate_course_3]      real,       --まくり率（３コース）
    [sashi_win_count_course_3]      integer,    --差し数（３コース）
    [sashi_win_rate_course_3]       real,       --差し率（３コース）
    [course_count_4]                integer,    --出走数（４コース）
    [ability_course_4]              real,       --能力値（４コース）
    [sinnyu_course_4]               real,       --進入偏差（４コース）
    [makuri_win_count_course_4]     integer,    --まくり数（４コース）
    [makuri_win_rate_course_4]      real,       --まくり率（４コース）
    [sashi_win_count_course_4]      integer,    --差し数（４コース）
    [sashi_win_rate_course_4]       real,       --差し率（４コース）
    [course_count_5]                integer,    --出走数（５コース）
    [ability_course_5]              real,       --能力値（５コース）
    [sinnyu_course_5]               real,       --進入偏差（５コース）
    [makuri_win_count_course_5]     integer,    --まくり数（５コース）
    [makuri_win_rate_course_5]      real,       --まくり率（５コース）
    [sashi_win_count_course_5]      integer,    --差し数（５コース）
    [sashi_win_rate_course_5]       real,       --差し率（５コース）
    [course_count_6]                integer,    --出走数（６コース）
    [ability_course_6]              real,       --能力値（６コース）
    [sinnyu_course_6]               real,       --進入偏差（６コース）
    [makuri_win_count_course_6]     integer,    --まくり数（６コース）
    [makuri_win_rate_course_6]      real,       --まくり率（６コース）
    [sashi_win_count_course_6]      integer,    --差し数（６コース）
    [sashi_win_rate_course_6]       real,       --差し率（６コース）
    PRIMARY KEY	([yyyymmdd],[pool_code],[race_no],[entry_no])
 );

--インデックス
CREATE INDEX t_index_index1 on t_index(player_no);
CREATE INDEX t_index_index2 on t_index(player_no,yyyymmdd,race_no);
CREATE INDEX t_race_d_index1 on t_race_d(yyyymmdd,pool_code,motor_no);
CREATE INDEX t_race_d_index2 on t_race_d(yyyymmdd,player_no);
