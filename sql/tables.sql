drop table FB_USERS;
create table FB_USERS(
  UID bigserial,
  FBID varchar,
  FBMID varchar,
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