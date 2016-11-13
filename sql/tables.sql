-- FB_USERS
drop table FB_USERS;
create table FB_USERS(
  UID bigserial PRIMARY KEY,
  FBID varchar UNIQUE,
  FBMID varchar UNIQUE,
  CreatedTime timestamp default NOW(),
  FBName varchar,
  RealName varchar,
  FBToken varchar,
  PushNewsFlag boolean,
  FBImgUrl varchar,
  FBMImgUrl varchar
);
create index FBID_INDEX on FB_USERS(FBID);
create index FBMID_INDEX on FB_USERS(FBMID);

-- FB_TXN
drop table FB_TXN;
create table FB_TXN(
  FBTxnID bigserial PRIMARY KEY,
  FBID varchar,
  msg varchar,
  CreatedTime timestamp not null,
  Info json
);
create index FBTXN_ID_INDEX on FB_TXN(FBID);

-- FBM_TXN
drop table FBM_TXN;
create table FBM_TXN(
  FBMTxnID bigserial PRIMARY KEY,
  FBMID varchar,
  msg varchar,
  CreatedTime timestamp not null,
  Info json
);
create index FBMTXN_ID_INDEX on FBM_TXN(FBMID);

-- FBM_NEWS_TXN
drop table FBM_NEWS_TXN;
create table FBM_NEWS_TXN(
  TXN_ID bigserial PRIMARY KEY,
  FBMID varchar,
  NEWSID varchar,
  CreatedTime timestamp not null
);
create index FBM_NEWS_TXN_ID_INDEX on FBM_NEWS_TXN(FBMID);
