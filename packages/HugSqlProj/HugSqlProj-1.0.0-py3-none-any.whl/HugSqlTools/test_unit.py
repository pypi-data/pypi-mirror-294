# encoding=utf-8

# from tag_template_engine.service_engine import service_manager as ServiceManager
# ServiceManager.start_constructor_tag_template()

import os,platform

from tag_template_engine.input_engine import input_manager as Input
from tag_template_engine.config_engine import config_manager as Config

from tag_template_constants import TagConstantsTips, TagMultipleConstantsTips

from tag_template_engine.template_engine import template_manager as TemplateManager

from tag_template_engine.utils_engine import git_utils


def resume_template_task(config_dict):
    # template_type = 1/离线标签  2/准实时标签
    template_type = 1
    tag_belong = config_dict['tag_belong']
    
    if not isinstance(tag_belong, str) or len(tag_belong) == 0 :
        raise RuntimeError('代码逻辑异常，请联系chaiyuan_dxm排查问题')
    
    __int_tag_belong = int(tag_belong)

    append_belong_path = ''
    # 标签的应用场景，0-普通筛客，1-消费宽表，2-人工电召
    # 默认全部为0-普通筛客，当优先级为高优时可用于人工电召，当放到消费目录下则用于消费宽表
    apply_scenario_value = "  - '0'\n"

    if __int_tag_belong == 1:
        template_type = 1
        append_belong_path = 'index_01_consumption'
    elif __int_tag_belong == 2:
        template_type = 1
        append_belong_path = 'index_02_xiaowei'
    elif __int_tag_belong == 3:
        template_type = 1
        append_belong_path = 'index_03_other'
    elif __int_tag_belong == 4:
        template_type = 1
        append_belong_path = 'index_04_bussiness_operation'
    elif __int_tag_belong == 5:
        template_type = 1
        append_belong_path = 'index_05_history'
    elif __int_tag_belong == 6:
        template_type = 2
        append_belong_path = 'index_06_nrt'
    elif __int_tag_belong == 7:
        template_type = 1
        append_belong_path = 'dws_loan_ccl_tag'
        apply_scenario_value = apply_scenario_value + "  - '1'\n"
    elif __int_tag_belong == 8:
        template_type = 1
        append_belong_path = 'index_08_business_self'
    elif __int_tag_belong == 9:
        template_type = 1
        append_belong_path = 'index_09_ris'
    else:
        raise RuntimeError('不支持的业务归属，请联系chaiyuan_dxm修改')

    # 处理高优标签默认可用于电召场景
    tag_priority = config_dict['tag_priority']
    if tag_priority == 'P0':
        apply_scenario_value = apply_scenario_value + "  - '2'\n"

    data_level = 'ads'

    template_config_dict = config_dict
    template_config_dict['tag_data_level'] = data_level
    template_config_dict['template_type'] = template_type
    template_config_dict['append_path'] = append_belong_path
    template_config_dict['base_path'] = '../../dw/%s/tag'%(data_level)

    processing_owner = git_utils.get_git_user_name()

    template_config_dict['processing_owner'] = processing_owner
    # template_config_dict['apply_scenario'] = apply_scenario_value

    TemplateManager.start_construct_tag_template(template_config_dict)

config_dict={'tag_name': '测试标签', 'tag_code': 'test_label2', 'tag_belong': '6', 'tag_version': '1.0.0', 'tag_entity_type': 'did', 'tag_staticize': 'false', 'tag_priority': 'P1', 'tag_dependencies': '', 'tag_dependencies_complete': 'Y', 'table': 'db.tab', 'partitions': '{DATE-1}', 'partitions_name': 'dwd_day'}
resume_template_task(config_dict)
