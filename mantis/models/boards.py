from mantis.models import mantis_db


class Board(mantis_db.Model):
    __tablename__ = 'board'
    id = mantis_db.Column(mantis_db.Integer, primary_key=True, comment='主键')
    board_id = mantis_db.Column(mantis_db.String(40), nullable=False, comment='唯一标识')
    user_id = mantis_db.Column(mantis_db.Integer, nullable=False, comment='所属用户id')
    username = mantis_db.Column(mantis_db.String(64), nullable=True, comment='所属用户姓名')
    name = mantis_db.Column(mantis_db.String(64), nullable=False, comment='看板名称')
    description = mantis_db.Column(mantis_db.String(128), nullable=False, comment='看板描述')
    cluster = mantis_db.Column(mantis_db.Integer, nullable=False, comment='集群  43/44/45')
    status = mantis_db.Column(mantis_db.Integer, nullable=False, comment='状态  0 进行中  1 已完成')
    visibility_level = mantis_db.Column(mantis_db.Integer, nullable=False, comment='能见度  0 private 1 public')
    create_time = mantis_db.Column(mantis_db.DateTime, nullable=False, comment='创建时间')
    delete_flag = mantis_db.Column(mantis_db.Integer, nullable=False, comment='0 未删除 1 删除')


class MileStone(mantis_db.Model):
    __tablename__ = 'milestone'
    id = mantis_db.Column(mantis_db.Integer, primary_key=True, comment='主键')
    milestone_name = mantis_db.Column(mantis_db.String(64), nullable=False, comment='所属看板')
    cluster = mantis_db.Column(mantis_db.JSON, nullable=False, comment='集群')
    board_id = mantis_db.Column(mantis_db.String(40), nullable=False, comment='所属看板')
    category = mantis_db.Column(mantis_db.JSON, nullable=False, comment='测试类别 Spec/Validation')
    available_market = mantis_db.Column(mantis_db.JSON, nullable=False, comment='市场')
    available_platform = mantis_db.Column(mantis_db.JSON, nullable=False, comment='平台')
    available_carline = mantis_db.Column(mantis_db.JSON, nullable=False, comment='生产线')
    available_variant = mantis_db.Column(mantis_db.JSON, nullable=False, comment='规格')
    available_environment = mantis_db.Column(mantis_db.JSON, nullable=False, comment='环境')
    available_language = mantis_db.Column(mantis_db.JSON, nullable=False, comment='语言')
    available_logic = mantis_db.Column(mantis_db.JSON, nullable=False, comment='逻辑与或')
    milestone_line = mantis_db.Column(mantis_db.JSON, nullable=False, comment='时间线配置')
    milestone_group = mantis_db.Column(mantis_db.JSON, nullable=False, comment='组配置')
    start_date = mantis_db.Column(mantis_db.String(16), nullable=True, comment='开始日期')
    end_date = mantis_db.Column(mantis_db.String(16), nullable=True, comment='结束时间')
    start_year = mantis_db.Column(mantis_db.String(8), nullable=True, comment='时间 -- 年')
    end_year = mantis_db.Column(mantis_db.String(8), nullable=True, comment='时间 -- 年')
    start_week = mantis_db.Column(mantis_db.String(2), nullable=True, comment='时间 -- 周')
    end_week = mantis_db.Column(mantis_db.String(2), nullable=True, comment='时间 -- 周')
    create_time = mantis_db.Column(mantis_db.DateTime, nullable=False, comment='创建时间')
    delete_flag = mantis_db.Column(mantis_db.Integer, nullable=False, comment='0 未删除 1 删除')


class MileStoneGroup(mantis_db.Model):
    __tablename__ = 'milestone_group'
    id = mantis_db.Column(mantis_db.Integer, primary_key=True, comment='主键')
    milestone_id = mantis_db.Column(mantis_db.Integer, nullable=False, comment='看板id')
    milestone_group_result = mantis_db.Column(mantis_db.JSON, nullable=False, comment='组数据')
    uuid = mantis_db.Column(mantis_db.String(40), nullable=False, comment='更新凭证')
    update_time = mantis_db.Column(mantis_db.DateTime, nullable=False, comment='更新时间')


class Card(mantis_db.Model):
    __tablename__ = 'card'
    id = mantis_db.Column(mantis_db.Integer, primary_key=True, comment='主键')
    board_id = mantis_db.Column(mantis_db.String(40), nullable=False, comment='看板id')
    name = mantis_db.Column(mantis_db.String(64), nullable=False, comment='名称')
    bar_type = mantis_db.Column(mantis_db.String(8), nullable=False, comment='卡片类型 fuli/function')
    cluster = mantis_db.Column(mantis_db.JSON, nullable=False, comment='集群')
    category = mantis_db.Column(mantis_db.JSON, nullable=True, comment='测试类别')
    available_market = mantis_db.Column(mantis_db.JSON, nullable=False, comment='市场')
    test_market = mantis_db.Column(mantis_db.JSON, nullable=False, comment='测试市场')
    available_platform = mantis_db.Column(mantis_db.JSON, nullable=False, comment='平台')
    test_platform = mantis_db.Column(mantis_db.JSON, nullable=False, comment='测试平台')
    available_carline = mantis_db.Column(mantis_db.JSON, nullable=False, comment='生产线')
    test_carline = mantis_db.Column(mantis_db.JSON, nullable=False, comment='测试生产线')
    available_variant = mantis_db.Column(mantis_db.JSON, nullable=False, comment='规格')
    test_variant = mantis_db.Column(mantis_db.JSON, nullable=False, comment='测试规格')
    available_environment = mantis_db.Column(mantis_db.JSON, nullable=False, comment='环境')
    test_environment = mantis_db.Column(mantis_db.JSON, nullable=False, comment='测试环境')
    available_language = mantis_db.Column(mantis_db.JSON, nullable=False, comment='语言')
    test_language = mantis_db.Column(mantis_db.JSON, nullable=False, comment='测试语言')
    level = mantis_db.Column(mantis_db.JSON, nullable=True, comment='等级')
    card_groups = mantis_db.Column(mantis_db.JSON, nullable=True, comment='功能')
    available_logic = mantis_db.Column(mantis_db.JSON, nullable=False, comment='逻辑与或')


class CardGroup(mantis_db.Model):
    __tablename__ = 'card_group'
    id = mantis_db.Column(mantis_db.Integer, primary_key=True, comment='主键')
    card_id = mantis_db.Column(mantis_db.Integer, nullable=False, comment='看板id')
    card_group_result = mantis_db.Column(mantis_db.JSON, nullable=False, comment='组数据')
    uuid = mantis_db.Column(mantis_db.String(40), nullable=False, comment='更新凭证')
    update_time = mantis_db.Column(mantis_db.DateTime, nullable=False, comment='更新时间')


class BoardLocation(mantis_db.Model):
    __tablename__ = 'board_location'
    id = mantis_db.Column(mantis_db.Integer, primary_key=True, comment='主键')
    board_id = mantis_db.Column(mantis_db.String(40), nullable=False, comment='看板id')
    location_id = mantis_db.Column(mantis_db.Integer, nullable=False, comment='位置id')
    type = mantis_db.Column(mantis_db.String(10), nullable=False, comment='数据类型')
    length = mantis_db.Column(mantis_db.Integer, nullable=False, comment='长')
    width = mantis_db.Column(mantis_db.Integer, nullable=False, comment='宽')
    data_id = mantis_db.Column(mantis_db.Integer, nullable=False, comment='里程碑/卡片')
