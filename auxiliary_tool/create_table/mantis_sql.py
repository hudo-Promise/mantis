create_mantis_db_sql = """CREATE DATABASE IF NOT EXISTS mantis_db DEFAULT CHARSET utf8mb4;"""

create_mantis_board_sql = """
    create table if not exists `board`
(
    `id`                    int auto_increment comment '主键' primary key,
    `board_id`              varchar(40)  not null comment '唯一标识',
    `user_id`               int          not null comment '所属用户id',
    `username`              varchar(64)  not null comment '所属用户姓名',
    `name`                  varchar(64)  not null comment '看板名称',
    `description`           varchar(128) not null comment '看板描述',
    `cluster`               int   not null comment '集群  43/44/45',
    `status`                int          not null comment '状态  0 进行中  1 已完成',
    `visibility_level`      int default 0 not null comment '能见度  0 private 1 public',
    `create_time`           datetime     not null comment '创建时间',
    `delete_flag`           int          not null comment '0 未删除 1 删除'
) ENGINE = InnoDB CHARACTER SET = utf8mb4;
"""

create_mantis_board_location_sql = """
        create table if not exists `board_location`
(
    `id`              int auto_increment comment '主键' primary key,
    `board_id`        varchar(40)  not null comment '看板id',
    `location_id`     int          not null comment '位置id',
    `type`            varchar(64)  not null comment '数据类型',
    `length`          varchar(128) not null comment '长',
    `width`           varchar(8)   not null comment '宽',
    `data_id`         int          not null comment '里程碑/卡片'
) ENGINE = InnoDB CHARACTER SET = utf8mb4;
"""

create_mantis_milestone_sql = """
    create table if not exists `milestone`
(
    `id`                             int auto_increment comment '主键' primary key,
    `milestone_name`                 varchar(64) not null default('untitled') comment '里程碑名称',
    `cluster`                        json not null comment '集群',
    `board_id`                       varchar(40) not null comment '所属看板',
    `category`                       json not null comment '测试类别 Spec/Validation',
    `available_platform`             json not null comment '平台',
    `available_carline`              json not null comment '生产线',
    `available_market`               json not null comment '市场',
    `available_variant`              json not null comment '规格',
    `available_language`             json not null comment '语言',
    `available_environment`          json not null comment '环境',
    `available_logic`                json not null comment '逻辑与或',
    `milestone_line`                 json not null comment '时间线配置',
    `milestone_group`                json not null comment '组配置',
    `start_date`                     varchar(16) null comment '开始时间',
    `end_date`                       varchar(16) null comment '结束时间',
    `start_year`                     varchar(8)  null comment '时间 -- 年',
    `end_year`                       varchar(8)  null comment '时间 -- 年',
    `start_week`                     varchar(2) not null comment '开始时间 -- 周',
    `end_week`                       varchar(3) not null comment '结束时间 -- 周',
    `create_time`                    datetime    not null comment '创建时间',
    `delete_flag`                    int         not null comment '0 未删除 1 删除'
) ENGINE = InnoDB CHARACTER SET = utf8mb4;
"""

create_mantis_milestone_group_sql = """
    create table if not exists `milestone_group`
(
    `id`                        int auto_increment comment '主键' primary key,
    `milestone_id`              int not null comment '所属里程碑',
    `milestone_group_result`    json not null comment '组配置',
    `uuid`                      varchar(40)  not null comment '0 未删除 1 删除',
    `update_time`               datetime    not null comment '创建时间'
) ENGINE = InnoDB CHARACTER SET = utf8mb4;
"""

create_mantis_card_sql = """
    create table if not exists `card`
(
    `id`                    int auto_increment comment '主键' primary key,
    `board_id`              varchar(40) not null comment '看板id',
    `name`                  varchar(64) not null comment '名称',
    `cluster`               json        not null comment '集群',
    `category`              json        null comment '测试类别',
    `available_carline`     json        null comment '产品线',
    `test_carline`          json        null comment '测试平台',
    `available_market`      json        null comment '市场',
    `available_language`    json        null comment '语言',
    `available_variant`     json        null comment '规格',
    `test_variant`          json        null comment '测试环境',
    `available_environment` json        null comment '环境',
    `available_platform`    json        null comment '平台',
    `level`                 json        null comment '等级',
    `card_groups`           json        null comment '功能',
    `test_market`           json        null comment '测试语言',
    `available_logic`       json        null,
    `test_platform`         json        null comment '测试平台',
    `test_language`         json        null comment '测试语言',
    `test_environment`      json        null comment '测试环境',
    `bar_type`              varchar(8)  null comment '卡片类型 fuli/function'
) ENGINE = InnoDB CHARACTER SET = utf8mb4;
"""

create_mantis_card_group_sql = """
    create table if not exists `card_group`
(
    `id`                        int auto_increment comment '主键' primary key,
    `card_id`                   int not null comment '所属卡片',
    `card_group_result`         json not null comment '组配置',
    `uuid`                      varchar(40)  not null comment '0 未删除 1 删除',
    `update_time`               datetime    not null comment '创建时间'
) ENGINE = InnoDB CHARACTER SET = utf8mb4;
"""

create_mantis_group_sql = """
    create table if not exists `group`
(
    id         int auto_increment comment '主键' primary key,
    group_name varchar(64) not null comment '组名'
) ENGINE = InnoDB CHARACTER SET = utf8mb4;
"""

create_mantis_functions_sql = """
    create table if not exists `functions`
(
    `id`         int auto_increment comment '主键' primary key,
    `test_group` int         not null comment '测试组',
    `function`   varchar(64) not null comment '功能'
) ENGINE = InnoDB CHARACTER SET = utf8mb4;
"""

create_mantis_sub_functions_sql = """
    create table if not exists `sub_functions`
(
    `id`           int auto_increment comment '主键' primary key,
    `test_group`   int         not null comment '测试组',
    `function`     int         not null comment '功能',
    `sub_function` varchar(64) not null comment '子功能'
) ENGINE = InnoDB CHARACTER SET = utf8mb4;
"""

create_mantis_fuLi_group_sql = """
    create table if not exists `mantis_fuLi_group`
(
    `id`                   int auto_increment comment '主键' primary key,
    `fuLi_group_name`      varchar(64) not null comment 'fuLi组'
) ENGINE = InnoDB CHARACTER SET = utf8mb4;
"""

create_mantis_fuLi_sql = """
    create table if not exists `mantis_fuLi`
(
    `id`                int auto_increment comment '主键' primary key,
    `fuLi_id`           varchar(16) not null comment 'fuLi ID',
    `fuLi_desc`         varchar(512) not null comment 'fuLi 描述',
    `fuLi_group_id`     int null comment 'fuLi group ID',
    `delete_flag`       int not null default 1 comment '删除标志 1 正常 2 删除'
) ENGINE = InnoDB CHARACTER SET = utf8mb4;
"""

create_mantis_case_field_sql = """
    create table if not exists `mantis_case_field`
(
    `id`                   int auto_increment comment '主键' primary key,
    `case_field`           varchar(64) null comment '字段名',
    `case_field_mapping`   json null comment '值名',
    `comment`              varchar(512) null comment '描述'
) ENGINE = InnoDB CHARACTER SET = utf8mb4;
"""

create_mantis_mapping_rule_sql = """
    create table if not exists `mantis_mapping_rule`
(
    `id`               int auto_increment comment '主键' primary key,
    `cluster_id`       int null comment 'cluster 配置',
    `mapping_name`     varchar(64) null comment 'mapping 名称',
    `mapping_rule`     json null comment 'mapping 配置',
    `create_time`      datetime null comment '创建时间',
    `update_time`      datetime null comment '更新时间'
) ENGINE = InnoDB CHARACTER SET = utf8mb4;
"""

create_mantis_test_case_sql = """
    create table if not exists `test_case`
(
    `id`                        int auto_increment comment '主键' primary key,
    `category`                  int  null comment '测试类别 Spec/Validation',
    `function`                  int          not null comment '功能',
    `sub_function`              int          not null comment '子功能',
    `fuLi_id`                   int  not null comment 'fuLi ID',
    `level`                     int   null comment '测试用例等级 -- 有测试结果不可为空 F4/F6/F8',
    `cluster`                   int   not null comment '集群  43/44/45',
    `available_platform`        json  null comment '平台 -- 有测试结果不可为空 PPC/PPE/All',
    `available_carline`         json  null comment '车系',
    `available_variant`         json  null comment '车辆规格',
    `available_market`          json  null comment '市场 CN/TW/HK/MC/JP/KR',
    `available_language`        json  null comment '语言 TCN/SCN/TW/EN/JP/KR',
    `available_environment`     json  null comment '环境  car/all',
    `title`                     text  not null comment '标题、描述',
    `precondition`              text  not null comment '前置条件',
    `action`                    text  not null comment '测试步骤',
    `expectation`               text  not null comment '测试期望结果',
    `reference_spec`            text         null comment '参考标准',
    `create_time`               datetime     not null comment '创建时间',
    `upgrade_time`              datetime     null comment '更新时间',
    `delete_flag`               int          not null comment '0 未删除 1 删除'
) ENGINE = InnoDB CHARACTER SET = utf8mb4;
"""

create_mantis_case_result_sql = """
    create table if not exists `case_result`
(
    id               int auto_increment comment '主键' primary key,
    m_id             int          null comment 'case id',
    test_sw          varchar(32)  null comment '软件版本 -- 有测试结果不可为空',
    sw_num           int          null,
    test_result      int          null comment '结果 pass fail tb empty n/a null',
    test_platform    int          null comment '平台 -- PPC/PPE/All',
    test_carline     int          null comment '车系  -- 有测试结果不可为空',
    test_variant     int          null comment '车辆规格 -- 有测试结果不可为空',
    test_market      int          null comment '市场  -- 有测试结果不可为空',
    test_language    int          null comment '语言 -- TCN/SCN/TW/EN/JP/KR',
    test_environment int          null comment '环境 -- car/all',
    tb_type          int          null comment '用例停滞原因',
    issue_descr      varchar(512) null,
    comments         text         null comment '备注',
    extra_1          varchar(16)  null comment '补充数据1',
    extra_2          varchar(16)  null comment '补充数据2',
    extra_3          varchar(16)  null comment '补充数据3',
    create_time      datetime     not null comment '创建时间',
    upgrade_time     datetime     null comment '更新时间'
) ENGINE = InnoDB CHARACTER SET = utf8mb4;
"""

create_mantis_sw_map_sql = """
    create table if not exists `sw_map`
(
    `id`                int auto_increment comment '主键' primary key,
    `sw_alpha`          varchar(8) null comment '软件版本',
    `sw_num`            int null comment '软件版本',
    `create_time`       datetime not null comment '创建时间',
    `update_time`       datetime null comment '更新时间',
    `delete_flag`       int not null comment '0 未删除 1 删除'
) ENGINE = InnoDB CHARACTER SET = utf8mb4;
"""

create_mantis_share_record_sql = """
    create table if not exists `mantis_share_record`
(
    `id`                int auto_increment comment '主键' primary key,
    `unique_id`         varchar(40) not null comment '唯一标识',
    `sender`            int  not null comment '发送人',
    `share_type`        int  not null comment '分享类型',
    `receiver`          json  null comment '接收人',
    `status`            varchar(32)  null comment '状态 1 未读 2 已读',
    `content`           json  null comment '内容',
    `config`            json  null comment '配置',
    `create_time`       datetime  null comment '创建时间',
    `update_time`       datetime null comment '更新时间',
    `delete_flag`       int         null comment '0 未删除 1 删除'
) ENGINE = InnoDB CHARACTER SET = utf8mb4;
"""

create_mantis_plan_sql = """
    create table if not exists `mantis_plan`
(
    `id`                int auto_increment comment '主键' primary key,
    `unique_id`         varchar(40) not null comment '唯一标识',
    `name`              varchar(128) not null comment '计划名称',
    `description`       text null comment '计划描述',
    `creator`           varchar(64) null comment '创建人',
    `project`           json null comment '项目类型',
    `function`          json not null comment '功能',
    `sub_function`      json not null comment '子功能',
    `cluster`           int not null comment '集群  43/44/45',
    `market`            json not null comment '市场 CN/TW/HK/MC/JP/KR',
    `language`          json not null comment '语言 TCN/SCN/TW/EN/JP/KR',
    `level`             json null comment '测试用例等级 -- 有测试结果不可为空 F4/F6/F8',
    `platform`          json null comment '项目平台',
    `carline`           json null comment '车型',
    `case_list`         json null comment 'case id list',
    `create_time`       datetime null comment '创建时间',
    `update_time`       datetime null comment '更新时间',
    `delete_flag`       int null comment '0 未删除 1 删除'
) ENGINE = InnoDB CHARACTER SET = utf8mb4;
"""

create_mantis_operate_record_sql = """
    create table if not exists `mantis_operate_record`
(
    `id`              int auto_increment comment '主键' primary key,
    `operator`        int          null comment '操作人',
    `operator_name`   varchar(64)  null comment '操作人姓名',
    `operate_url`     varchar(128) null comment '访问路径',
    `operate_content` json         null comment '操作内容',
    `operate_time`    datetime     null comment '操作时间'
) ENGINE = InnoDB CHARACTER SET = utf8mb4;
"""


create_mantis_filter_record_sql = """
    create table if not exists `mantis_filter_record`
(
    `id`                    int auto_increment comment '主键' primary key,
    `filter_name`           varchar(32) null comment '创建人',
    `filter_desc`           varchar(256) null comment '集群 id',
    `creator`               int null comment '创建人',
    `mapping_rule_id`       int null comment 'mapping rule id',
    `filter_config`         json null comment '筛选配置',
    `visibility_level`      int null comment '能见度  0 private 1 public',
    `create_time`           datetime null comment '创建时间',
    `update_time`           datetime null comment '更新时间'
) ENGINE = InnoDB CHARACTER SET = utf8mb4;
"""


create_mantis_test_milestone_sql = """
    create table if not exists `mantis_test_milestone`
(
    `id`                int auto_increment comment '主键' primary key,
    `name`              varchar(64) null comment 'test milestone name',
    `description`       text null comment '描述',
    `project`           int null comment '项目',
    `cluster`           int null comment '集群',
    `status`            int null comment '状态',
    `start_date`        varchar(16) null comment '开始日期',
    `due_date`          varchar(16) null comment '截至日期',
    `create_time`       datetime null comment '创建时间',
    `update_time`       datetime null comment '更新时间'
) ENGINE = InnoDB CHARACTER SET = utf8mb4;
"""


create_mantis_test_cycle_sql = """
    create table if not exists `mantis_test_cycle`
(
    `id`                    int auto_increment comment '主键' primary key,
    `name`                  varchar(64) null comment 'test cycle name',
    `test_group`            int null comment '测试组',
    `linked_milestone`      int null comment '所属 test milestone',
    `project`               int null comment '项目',
    `cluster`               int null comment '集群',
    `market`                json null comment '市场',
    `start_date`            varchar(16) null comment '开始日期',
    `due_date`              varchar(16) null comment '截至日期',
    `actual_finish_date`    varchar(16) null comment '实际完成日期',
    `description`           text null comment '描述',
    `filter_id`             int null comment 'filter config',
    `test_scenario`         int null comment '类型 1 test case 2 free test',
    `free_test_item`        json null comment '测试人员记录',
    `status`                int null comment '状态',
    `create_time`           datetime null comment '创建时间',
    `update_time`           datetime null comment '更新时间'
) ENGINE = InnoDB CHARACTER SET = utf8mb4;
"""
