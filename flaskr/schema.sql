DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS menu;
DROP TABLE IF EXISTS ordered;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  address TEXT NOT NULL,
  tel INTEGER NOT NULL,
  mail TEXT,
  weight INTEGER,
  height INTEGER,
  gender TEXT,
  egg INTEGER, 
  milk INTEGER, 
  wheat INTEGER, 
  shrimp INTEGER, 
  crab INTEGER, 
  peanuts INTEGER, 
  soba INTEGER
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  -- created DATE DEFAULT (datetime('now')),
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE menu (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  menuname TEXT UNIQUE NOT NULL,
  img TEXT NOT NULL,
  eattime TEXT NOT NULL,
  type TEXT NOT NULL,
  calorie INTEGER NOT NULL,
  egg INTEGER, 
  milk INTEGER, 
  wheat INTEGER, 
  shrimp INTEGER, 
  crab INTEGER, 
  peanuts INTEGER, 
  soba INTEGER,
  details TEXT NOT NULL
);

CREATE TABLE ordered (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  menuid INTEGER NOT NULL,
  username TEXT NOT NULL,
  menuname TEXT NOT NULL,
  img TEXT NOT NULL,
  eattime TEXT NOT NULL,
  type TEXT NOT NULL,
  calorie INTEGER NOT NULL,
  details TEXT NOT NULL,
  deliverytime TEXT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (username) REFERENCES user (username)
);


-- insert into menu values(1, "納豆的食1", "health_01.png", "morning", "low", 100, "説明文1");
-- insert into menu values(2, "納豆的食2", "health_02.png", "morning", "low", 200, "説明文2");
-- insert into menu values(3, "納豆的食3", "health_03.png", "morning", "low", 300, "説明文3");
-- insert into menu values(4, "納豆的食4", "health_04.png", "lunch", "low", 400, "説明文4");
-- insert into menu values(5, "納豆的食5", "health_05.png", "lunch", "low", 500, "説明文5");
-- insert into menu values(6, "納豆的食6", "health_06.png", "lunch", "low", 600, "説明文6");
-- insert into menu values(7, "納豆的食7", "health_07.png", "dinner", "low", 700, "説明文7");
-- insert into menu values(8, "納豆的食8", "health_08.png", "dinner", "low", 800, "説明文8");
-- insert into menu values(9, "納豆的食9", "health_09.png", "dinner", "low", 900, "説明文9");
-- insert into menu values(10, "納豆的食10", "health_10.png", "morning", "high", 1000, "説明文10");
-- insert into menu values(12, "納豆的食12", "health_12.png", "morning", "high", 1200, "説明文12");
-- insert into menu values(13, "納豆的食13", "health_13.png", "morning", "high", 1300, "説明文13");
-- insert into menu values(14, "納豆的食14", "health_14.png", "lunch", "high", 1400, "説明文14");
-- insert into menu values(15, "納豆的食15", "health_15.png", "lunch", "high", 1500, "説明文15");
-- insert into menu values(16, "納豆的食16", "health_16.png", "lunch", "high", 1600, "説明文16");
-- insert into menu values(17, "納豆的食17", "health_17.png", "dinner", "high", 1700, "説明文17");
-- insert into menu values(18, "納豆的食18", "health_18.png", "dinner", "high", 1800, "説明文18");
-- insert into menu values(19, "納豆的食19", "health_19.png", "dinner", "high", 1900, "説明文19");




-- insert into menu values(1, "ネギトロ丼", "health_01.png", "morning", "low", 351, "魚の油は血液をサラサラにしてくれる効果があったり、不足しがちなミネラルを補ってくれたり、と優秀な食材です。");
-- insert into menu values(2, "マグロアボカド丼", "health_02.png", "morning", "low", 462, "魚に含まれているDHAやEPAの油は非常に身体に良く、特にマグロは高タンパク質でもあるのでとてもオススメ。マグロとアボカドの組み合わせ、美味しくて栄養価も高く、筋トレ後にうってつけですよ！");
-- insert into menu values(3, "ブロッコリーとあさりのスパゲッティ", "health_03.png", "morning", "low", 120, "ブロッコリーやあさりもタンパク質を含んでおり、筋トレ中にオススメの食材です。さらに鉄分も豊富なので貧血予防にも良い。食物繊維量が多いのでお腹の調子を整えてくれて便秘予防にもつながります。");
-- insert into menu values(4, "ささみとアボカドの照り焼き丼", "health_04.png", "lunch", "low", 517, "ささみは高タンパク質低脂質なので減量中にもオススメの食材です。ささみにアボカドを足すことでパサつきが気にならなくなり、まったりとした口当たりに。アボカドには不飽和脂肪酸のオレイン酸という、血管の若さを保つ油も多く含まれるので、おいしいだけでなく栄養価も高い組み合わせです。");
-- insert into menu values(5, "ブロッコリーグラタン", "health_05.png", "lunch", "low", 155, "ブロッコリーは筋肉を育てるに有効な成分を多く含んでいます。食物繊維やビタミン類、葉酸、鉄分やカリウム、マグネシウムなどのほか、筋肉に不可欠なタンパク質は野菜の中でみてもかなりの含有量を誇っています。");
-- insert into menu values(6, "ささみとほうれん草のナムルと炊き込みご飯", "health_06.png", "lunch", "low", 447, "ブロッコリーとほうれん草とささみは筋トレ食材にはもってこい！この2品を食べればかなりお腹いっぱいになります！");
-- insert into menu values(7, "ヤンニョムチキン風高野豆腐", "health_07.png", "dinner", "low", 221, "高野豆腐には「動脈硬化を予防する」、「お通じを改善する」効果があります。また、タンパク質がたくさんはいっているので筋トレ後には最適！");
-- insert into menu values(8, "冷凍アサリのチャーハン", "health_08.png", "dinner", "low", 335, "あさりには筋肉の収縮に必要なマグネシウムや、鉄・亜鉛などのミネラルなど、筋トレ民に必須の栄養素が豊富に含まれています。");
-- insert into menu values(9, "牛すじ丼", "health_09.png", "dinner", "low", 536, "牛すじに含まれるゼラチンは、ほぼタンパク質でできているのでアミノ酸をたくさん含んでいます！アミノ酸は筋肉を合成するのに大切なのでおすすめ！");
-- insert into menu values(10, "ふわトロスクランブルエッグ", "health_10.png", "morning", "low", 260, "ふんわりとろとろのスクランブルエッグ。火加減や卵の炒り方を工夫するだけで簡単に作れます。");
-- insert into menu values(11, "ツナチーズトースト", "health_11.png", "morning", "low", 282, "ツナマヨとチーズの間違いないコンビ。 簡単にできちゃうおかずパンレシピです。");
-- insert into menu values(12, "ハムとブロッコリーの卵焼き", "health_12.png", "morning", "low", 70, "ハムとブロッコリーをたっぷり包み込んだ卵焼きです。");
-- insert into menu values(13, "蒸し鶏", "health_13.png", "lunch", "low", 300, "炊飯器で作る蒸し鶏です。鶏むね肉を下処理してポリ袋に入れ、熱湯と一緒に炊飯器に入れるだけで作れる蒸鶏です。");
-- insert into menu values(14, "天津ラーメン", "health_14.png", "lunch", "low", 430, "天津飯風にアレンジした天津ラーメンです。最近のインスタントラーメンは麺が美味しく、麺に腰があって伸びにくいので、こんなアレンジもできます。");
-- insert into menu values(15, "豆腐チャンプルー", "health_15.png", "lunch", "low", 392, "豆腐に豚肉、鰹節、卵とバランスの良いたんぱく質配分が魅力の沖縄風炒め物です。野菜をたっぷり入れる事でビタミンやミネラルのバランスもとりやすく、アレンジも加えやすい料理です。");
-- insert into menu values(16, "ささみのごまスティック", "health_16.png", "dinner", "low", 264, "軽い食感でサクッとおいしい、ささみのごまスティックのレシピです。ごまを混ぜた衣をまぶし、フライパンで揚げ焼きにしました。");
-- insert into menu values(17, "鶏むね肉とブロッコリーのチーズ蒸し", "health_17.png", "dinner", "low", 435, "鶏むね肉とブロッコリーを使った簡単、美味しいレンジ蒸しです。筋トレ後の栄養補給にバッチリな料理です。");
-- insert into menu values(18, "鶏むね肉のしょうが焼き", "health_18.png", "dinner", "low", 357, "鶏むね肉を使ったしょうが焼きです。筋トレ、低糖質ダイエットしてる方に特におすすめ。");
-- insert into menu values(19, "納豆ご飯", "health_19.png", "morning", "high", 250, "酵素の源である納豆菌で腸内環境を整える。大豆の持つ水溶性&不溶性食物繊維が腸壁を刺激し、善玉菌を増やし便通をよくします！");
-- insert into menu values(20, "豆乳スープとフランスパン", "health_20.png", "morning", "high", 250, "大豆の持つ水溶性&不溶性食物繊維が腸壁を刺激し、善玉菌を増やして便通をよくします！フランスパンは咀嚼量が多くなる食べ物であり、満腹度をあげます！");
-- insert into menu values(21, "ヨーグルトとオートミール", "health_21.png", "morning", "high", 250, "全粉穀物であり栄養満点！ヨーグルトを添えて腸内環境を整えます！");
-- insert into menu values(22, "山かけ明太子丼", "health_22.png", "lunch", "high", 650, "山芋は少量で満腹になるため、ダイエットに最適！明太子で味も美味しく、楽しくダイエットできる");
-- insert into menu values(23, "オムライス", "health_23.png", "lunch", "high", 650, "朝食はしっかり食べて、栄養を蓄えましょう！野菜をたっぷり入れて、栄養満点に！");
-- insert into menu values(24, "サラダチキンと春雨スープと雑穀米", "health_24.png", "lunch", "high", 650, "雑穀米で栄養価満点！春雨はカロリーも低く、お腹を満たしてくれます！");
-- insert into menu values(25, "野菜たっぷりパスタ", "health_25.png", "dinner", "high", 680, "野菜をたっぷりで1日の食物繊維をとりきろう！！");
-- insert into menu values(26, "ささみときゅうりの和え物とご飯と味噌汁", "health_26.png", "dinner", "high", 680, "お味噌汁で腸内環境を整える！ささみはカロリーも低い上に、タンパク質をたくさん取れる！");
-- insert into menu values(27, "豚しゃぶとサラダとご飯", "health_27.png", "dinner", "high", 680, "豚しゃぶであっさりとタンパク質を取れる！ご飯も進むしお腹いっぱいでダイエットを楽しく乗り切ろう！");
-- insert into menu values(28, "ヨーグルトとりんご、野菜ジュース", "health_28.png", "morning", "high", 250, "ヨーグルトで腸内環境を整えて、果実で加糖と酵素を、野菜ジュースでビタミンを摂取");
-- insert into menu values(29, "ヨーグルトとパイナップル、野菜ジュース", "health_29.png", "morning", "high", 250, "ヨーグルトで腸内環境を整えて、果実で加糖と酵素を、野菜ジュースでビタミンを摂取");
-- insert into menu values(30, "ヨーグルトとバナナ、野菜ジュース", "health_30.png", "morning", "high", 250, "ヨーグルトで腸内環境を整えて、果実で加糖と酵素を、野菜ジュースでビタミンを摂取");
-- insert into menu values(31, "キノコの和風スパゲティとサラダ(レタス卵トマト)", "health_31.png", "lunch", "high", 600, "キノコは低カロリーで、パスタは低GIでダイエット向き。トマトは血糖値を下げるのにも効果が");
-- insert into menu values(32, "胸肉のソテーとブロッコリー、オニオンスープ", "health_32.png", "lunch", "high", 600, "鶏肉は低カロリーで高タンパク質。");
-- insert into menu values(33, "大根煮物(鶏肉とにんじん入り) と鯖の塩焼き、ご飯と味噌汁", "health_33.png", "lunch", "high", 660, "大根やにんじんでビタミン摂取、鶏肉でタンパク質を摂取");
-- insert into menu values(34, "つくねハンバーグ、ご飯と味噌汁、マカロニサラダ", "health_34.png", "dinner", "high", 700, "つくねハンバーグは何と200kcal程度");
-- insert into menu values(35, "サラダスパゲッティ(蒸し鳥、野菜)とジャーマンポテト", "health_35.png", "dinner", "high", 700, "ジャガイモはビタミンを多く含み、熱に強いため、ビタミン摂取を非常に効率よく行える");
-- insert into menu values(36, "水炊き(胸肉、鳥ミンチ、白菜、ネギ、豆腐、椎茸)、ポン酢を添えて", "health_36.png", "dinner", "high", 600, "水炊きはさまざまな野菜を取ることができ、豆腐でタンパク質も摂取できる。高タンパクで低カロリー、かつビタミンも取れる優れもの");




insert into menu values(1, "ネギトロ丼", "health_01.png", "morning", "low", 351, 1, 0, 0, 0, 0, 0, 0, "魚の油は血液をサラサラにしてくれる効果があったり、不足しがちなミネラルを補ってくれたり、と優秀な食材です。");
insert into menu values(2, "マグロアボカド丼", "health_02.png", "morning", "low", 462, 1, 0, 0, 0, 0, 0, 0, "魚に含まれているDHAやEPAの油は非常に身体に良く、特にマグロは高タンパク質でもあるのでとてもオススメ。マグロとアボカドの組み合わせ、美味しくて栄養価も高く、筋トレ後にうってつけですよ！");
insert into menu values(3, "ブロッコリーとあさりのスパゲッティ", "health_03.png", "morning", "low", 120, 0, 0, 1, 0, 0, 0, 0, "ブロッコリーやあさりもタンパク質を含んでおり、筋トレ中にオススメの食材です。さらに鉄分も豊富なので貧血予防にも良い。食物繊維量が多いのでお腹の調子を整えてくれて便秘予防にもつながります。");
insert into menu values(4, "ささみとアボカドの照り焼き丼", "health_04.png", "lunch", "low", 517, 1, 1, 0, 0, 0, 0, 0, "ささみは高タンパク質低脂質なので減量中にもオススメの食材です。ささみにアボカドを足すことでパサつきが気にならなくなり、まったりとした口当たりに。アボカドには不飽和脂肪酸のオレイン酸という、血管の若さを保つ油も多く含まれるので、おいしいだけでなく栄養価も高い組み合わせです。");
insert into menu values(5, "ブロッコリーグラタン", "health_05.png", "lunch", "low", 155, 1, 1, 0, 0, 0, 0, 0, "ブロッコリーは筋肉を育てるに有効な成分を多く含んでいます。食物繊維やビタミン類、葉酸、鉄分やカリウム、マグネシウムなどのほか、筋肉に不可欠なタンパク質は野菜の中でみてもかなりの含有量を誇っています。");
insert into menu values(6, "ささみとほうれん草のナムルと炊き込みご飯", "health_06.png", "lunch", "low", 447, 0, 0, 1, 0, 0, 0, 0, "ブロッコリーとほうれん草とささみは筋トレ食材にはもってこい！この2品を食べればかなりお腹いっぱいになります！");
insert into menu values(7, "ヤンニョムチキン風高野豆腐", "health_07.png", "dinner", "low", 221, 1, 0, 1, 0, 0, 0, 0, "高野豆腐には「動脈硬化を予防する」、「お通じを改善する」効果があります。また、タンパク質がたくさんはいっているので筋トレ後には最適！");
insert into menu values(8, "冷凍アサリのチャーハン", "health_08.png", "dinner", "low", 335, 1, 0, 0, 0, 0, 0, 0, "あさりには筋肉の収縮に必要なマグネシウムや、鉄・亜鉛などのミネラルなど、筋トレ民に必須の栄養素が豊富に含まれています。");
insert into menu values(9, "牛すじ丼", "health_09.png", "dinner", "low", 536, 0, 0, 1, 0, 0, 0, 0, "牛すじに含まれるゼラチンは、ほぼタンパク質でできているのでアミノ酸をたくさん含んでいます！アミノ酸は筋肉を合成するのに大切なのでおすすめ！");
insert into menu values(10, "ふわトロスクランブルエッグ", "health_10.png", "morning", "low", 260, 1, 0, 0, 0, 0, 0, 0, "ふんわりとろとろのスクランブルエッグ。火加減や卵の炒り方を工夫するだけで簡単に作れます。");
insert into menu values(11, "ツナチーズトースト", "health_11.png", "morning", "low", 282, 0, 0, 1, 0, 0, 0, 0, "ツナマヨとチーズの間違いないコンビ。 簡単にできちゃうおかずパンレシピです。");
insert into menu values(12, "ハムとブロッコリーの卵焼き", "health_12.png", "morning", "low", 70, 1, 0, 0, 0, 0, 0, 0, "ハムとブロッコリーをたっぷり包み込んだ卵焼きです。");
insert into menu values(13, "蒸し鶏", "health_13.png", "lunch", "low", 300, 0, 0, 0, 0, 0, 0, 0, "炊飯器で作る蒸し鶏です。鶏むね肉を下処理してポリ袋に入れ、熱湯と一緒に炊飯器に入れるだけで作れる蒸鶏です。");
insert into menu values(14, "天津ラーメン", "health_14.png", "lunch", "low", 430, 1, 0, 0, 0, 1, 0, 1, "天津飯風にアレンジした天津ラーメンです。最近のインスタントラーメンは麺が美味しく、麺に腰があって伸びにくいので、こんなアレンジもできます。");
insert into menu values(15, "豆腐チャンプルー", "health_15.png", "lunch", "low", 392, 1, 0, 1, 0, 0, 0, 0, "豆腐に豚肉、鰹節、卵とバランスの良いたんぱく質配分が魅力の沖縄風炒め物です。野菜をたっぷり入れる事でビタミンやミネラルのバランスもとりやすく、アレンジも加えやすい料理です。");
insert into menu values(16, "ささみのごまスティック", "health_16.png", "dinner", "low", 264, 0, 0, 1, 0, 0, 0, 0, "軽い食感でサクッとおいしい、ささみのごまスティックのレシピです。ごまを混ぜた衣をまぶし、フライパンで揚げ焼きにしました。");
insert into menu values(17, "鶏むね肉とブロッコリーのチーズ蒸し", "health_17.png", "dinner", "low", 435, 0, 0, 1, 0, 0, 0, 0, "鶏むね肉とブロッコリーを使った簡単、美味しいレンジ蒸しです。筋トレ後の栄養補給にバッチリな料理です。");
insert into menu values(18, "鶏むね肉のしょうが焼き", "health_18.png", "dinner", "low", 357, 0, 0, 1, 0, 0, 0, 0, "鶏むね肉を使ったしょうが焼きです。筋トレ、低糖質ダイエットしてる方に特におすすめ。");
insert into menu values(19, "納豆ご飯", "health_19.png", "morning", "high", 250, 0, 0, 0, 0, 0, 0, 0, "酵素の源である納豆菌で腸内環境を整える。大豆の持つ水溶性&不溶性食物繊維が腸壁を刺激し、善玉菌を増やし便通をよくします！");
insert into menu values(20, "豆乳スープとフランスパン", "health_20.png", "morning", "high", 250, 0, 1, 1, 0, 0, 0, 0, "大豆の持つ水溶性&不溶性食物繊維が腸壁を刺激し、善玉菌を増やして便通をよくします！フランスパンは咀嚼量が多くなる食べ物であり、満腹度をあげます！");
insert into menu values(21, "ヨーグルトとオートミール", "health_21.png", "morning", "high", 250, 0, 1, 1, 0, 0, 0, 0, "全粉穀物であり栄養満点！ヨーグルトを添えて腸内環境を整えます！");
insert into menu values(22, "山かけ明太子丼", "health_22.png", "lunch", "high", 650, 0, 0, 0, 0, 0, 0, 0, "山芋は少量で満腹になるため、ダイエットに最適！明太子で味も美味しく、楽しくダイエットできる");
insert into menu values(23, "オムライス", "health_23.png", "lunch", "high", 650, 1, 0, 0, 0, 0, 0, 0, "朝食はしっかり食べて、栄養を蓄えましょう！野菜をたっぷり入れて、栄養満点に！");
insert into menu values(24, "サラダチキンと春雨スープと雑穀米", "health_24.png", "lunch", "high", 650, 0, 0, 0, 0, 0, 0, 0, "雑穀米で栄養価満点！春雨はカロリーも低く、お腹を満たしてくれます！");
insert into menu values(25, "野菜たっぷりパスタ", "health_25.png", "dinner", "high", 680, 0, 0, 0, 0, 0, 0, 0, "野菜をたっぷりで1日の食物繊維をとりきろう！！");
insert into menu values(26, "ささみときゅうりの和え物とご飯と味噌汁", "health_26.png", "dinner", "high", 680, 0, 0, 0, 0, 0, 0, 0, "お味噌汁で腸内環境を整える！ささみはカロリーも低い上に、タンパク質をたくさん取れる！");
insert into menu values(27, "豚しゃぶとサラダとご飯", "health_27.png", "dinner", "high", 680, 0, 0, 0, 0, 0, 0, 0, "豚しゃぶであっさりとタンパク質を取れる！ご飯も進むしお腹いっぱいでダイエットを楽しく乗り切ろう！");
insert into menu values(28, "ヨーグルトとりんご、野菜ジュース", "health_28.png", "morning", "high", 250, 0, 1, 0, 0, 0, 0, 0, "ヨーグルトで腸内環境を整えて、果実で加糖と酵素を、野菜ジュースでビタミンを摂取");
insert into menu values(29, "ヨーグルトとパイナップル、野菜ジュース", "health_29.png", "morning", "high", 250, 0, 1, 0, 0, 0, 0, 0, "ヨーグルトで腸内環境を整えて、果実で加糖と酵素を、野菜ジュースでビタミンを摂取");
insert into menu values(30, "ヨーグルトとバナナ、野菜ジュース", "health_30.png", "morning", "high", 250, 0, 1, 0, 0, 0, 0, 0, "ヨーグルトで腸内環境を整えて、果実で加糖と酵素を、野菜ジュースでビタミンを摂取");
insert into menu values(31, "キノコの和風スパゲティとサラダ(レタス卵トマト)", "health_31.png", "lunch", "high", 600, 1, 0, 1, 0, 0, 0, 0, "キノコは低カロリーで、パスタは低GIでダイエット向き。トマトは血糖値を下げるのにも効果が");
insert into menu values(32, "胸肉のソテーとブロッコリー、オニオンスープ", "health_32.png", "lunch", "high", 600, 0, 0, 0, 0, 0, 0, 0, "鶏肉は低カロリーで高タンパク質。");
insert into menu values(33, "大根煮物(鶏肉とにんじん入り) と鯖の塩焼き、ご飯と味噌汁", "health_33.png", "lunch", "high", 660, 0, 0, 0, 0, 0, 0, 0, "大根やにんじんでビタミン摂取、鶏肉でタンパク質を摂取");
insert into menu values(34, "つくねハンバーグ、ご飯と味噌汁、マカロニサラダ", "health_34.png", "dinner", "high", 700, 0, 0, 1, 0, 0, 0, 0, "つくねハンバーグは何と200kcal程度");
insert into menu values(35, "サラダスパゲッティ(蒸し鳥、野菜)とジャーマンポテト", "health_35.png", "dinner", "high", 700, 1, 0, 1, 0, 0, 0, 0, "ジャガイモはビタミンを多く含み、熱に強いため、ビタミン摂取を非常に効率よく行える");
insert into menu values(36, "水炊き(胸肉、鳥ミンチ、白菜、ネギ、豆腐、椎茸)、ポン酢を添えて", "health_36.png", "dinner", "high", 600, 0, 0, 0, 0, 0, 0, 0, "水炊きはさまざまな野菜を取ることができ、豆腐でタンパク質も摂取できる。高タンパクで低カロリー、かつビタミンも取れる優れもの");
