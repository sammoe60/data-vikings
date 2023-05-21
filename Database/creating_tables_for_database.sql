CREATE TABLE state(
    state_ID    INT             PRIMARY KEY     IDENTITY(1,1),
    state_name  varchar(100)    NOT NULL
)

CREATE TABLE occupation_group(
    occupation_group_ID     INT             PRIMARY KEY      IDENTITY(1,1),
    occupation_group        VARCHAR(50)     NULL
)


CREATE TABLE national_poverty(
    pr_all           FLOAT  NOT NULL,
    pr_youth         FLOAT  NOT NULL,
    med_hh_income    INT    NOT NULL,
    [year]           INT    NOT NULL
)

CREATE TABLE state_poverty(
    state_ID         INT     NOT NULL,
    pr_all           FLOAT   NOT NULL,
    pr_youth         FLOAT   NOT NULL,
    med_hh_income    INT     NOT NULL,
    [year]           INT     NOT NULL,

CONSTRAINT state_id_FK
    FOREIGN KEY (state_ID)
    REFERENCES [state] (state_ID)
)

CREATE TABLE county_poverty(
    county           VARCHAR(100)    NULL,
    state_ID         INT             NOT NULL,
    pr_all           FLOAT           NULL,
    pr_youth         FLOAT           NULL,
    med_hh_income    INT             NULL,
    [year]           INT             NOT NULL,
    latitude         DECIMAL(10,6)   NULL,
    longitude        DECIMAL(10,6)   NULL,
    [population]     INT             NULL,

CONSTRAINT stateid_FK
    FOREIGN KEY (state_ID)
    REFERENCES [state] (state_ID)
)

CREATE TABLE national_employment(
    occ_title            VARCHAR(200)    NULL,
    occupation_group_ID  INT             NULL,
    tot_emp              INT             NOT NULL,
    h_mean               FLOAT           NOT NULL,
    a_mean               INT             NOT NULL,
    h_median             FLOAT           NOT NULL,
    a_median             INT             NOT NULL,
    [year]               INT             NOT NULL,

CONSTRAINT occid_fk
    FOREIGN KEY (occupation_group_ID)
    REFERENCES occupation_group (occupation_group_ID)
)

CREATE TABLE state_employment(
    state_ID             INT             NOT NULL,
    area                 INT             NOT NULL,
    occ_title            VARCHAR(200)    NOT NULL,
    occupation_group_ID  INT             NULL,
    tot_emp              INT             NOT NULL,
    jobs_1000            FLOAT           NULL,
    loc_quotient         FLOAT           NULL,
    h_mean               FLOAT           NOT NULL,
    a_mean               INT             NOT NULL,
    h_median             FLOAT           NOT NULL,
    a_median             INT             NOT NULL,
    [year]               INT             NOT NULL,

CONSTRAINT stateidfk
    FOREIGN KEY (state_ID)
    REFERENCES [state] (state_ID),

CONSTRAINT occ_id_fk
    FOREIGN KEY (occupation_group_ID)
    REFERENCES occupation_group (occupation_group_ID)
)

CREATE TABLE poverty_threshold(
    [year] INT NOT NULL,
    amount_for_one_person INT NOT NULL
)

