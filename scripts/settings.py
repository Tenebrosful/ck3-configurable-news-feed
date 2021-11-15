import itertools

newline = '\n'

class Subject:
    def __init__(self, name, *, icon):
        self.name = name
        self.icon = icon

    def __str__(self):
        return self.name

class Type:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

subjects = [
    Subject('self', icon = """    
        newsfeed_subject_icon_template = {
            texture = "gfx/interface/icons/flat_icons/window_me.dds"
        }
    """),
    Subject('spouse', icon = """
        newsfeed_subject_icon_template = {
            texture = "gfx/interface/icons/faith_doctrine_groups/doctrine_marriage_type.dds"
        }
    """),
    Subject('close_dynastic_family', icon = """
        newsfeed_subject_icon_template = {
            texture = "gfx/interface/icons/portraits/relation.dds"
            framesize = { 40 40 }
            frame = 5
        }
    """),
    Subject('extended_dynastic_family', icon = """
        newsfeed_subject_icon_template = {
            texture = "gfx/interface/icons/portraits/relation.dds"
            framesize = { 40 40 }
            frame = 5
            position = { 10 0 }
            size = { 20 20 }
        }
        newsfeed_subject_icon_template = {
            texture = "gfx/interface/icons/portraits/relation.dds"
            framesize = { 40 40 }
            frame = 5
            position = { 0 10 }
            size = { 20 20 }
        }
    """),
    Subject('dynasty', icon = """
        newsfeed_subject_icon_template = {
            texture = "gfx/interface/icons/flat_icons/dynasty.dds"
        }
    """),
    Subject('liege', icon = """
        newsfeed_subject_icon_template = {
            texture = "gfx/interface/icons/flat_icons/mapmode_kingdom.dds"
            position = { 0 7 }
        }
        newsfeed_subject_icon_template = {
            texture = "gfx/interface/icons/symbols/icon_arrow_up.dds"
            size = { 15 15 }
            position = { 8 0 }
        }    
    """),
    Subject('direct_vassal', icon = """
        newsfeed_subject_icon_template = {
            texture = "gfx/interface/icons/flat_icons/mapmode_kingdom.dds"
            position = { 0 -5 }
        }
        newsfeed_subject_icon_template = {
            texture = "gfx/interface/icons/symbols/icon_arrow_green_down.dds"
            size = { 15 15 }
            position = { 8 15 }
        }
    """),
    Subject('courtier', icon = """
        newsfeed_subject_icon_template = {
            texture = "gfx/interface/icons/flat_icons/multiplayer.dds"
        }
    """),
    Subject('pinned_character', icon = """
        newsfeed_subject_icon_template = {
            texture = "gfx/interface/icons/flat_icons/pin.dds"
        }
    """),
]

types = [
    Type('marriage'),
    Type('pregnancy'),
    Type('birth'),
    Type('death'),
    Type('offensive_war'),
    Type('defensive_war'),
    Type('titles'),
    Type('faith'),
    Type('culture'),
]

combos = list(itertools.product(subjects, types))

def lines(items):
    return newline.join(items)

def gui_template():
    return f"""
        types NewsFeed {{
            type newsfeed_settings_columns = hbox {{
                vbox = {{
                    margin_right = 8

                    newsfeed_column_spacer = {{}}
                    {lines(label_row(type) for type in types)}
                }}

                {lines(subject_column(subject) for subject in subjects)}
            }}
        }}
    """

def label_row(type):
    return f"""
        hbox = {{
            margin_right = 8
            layoutpolicy_horizontal = expanding

            text_single = {{
                layoutpolicy_horizontal = expanding
                align = right|nobaseline
                text = newsfeed_type_{type}_label
                default_format = "#high"
                margin_right = 8
            }}

            newsfeed_select_all_checkbox = {{
                checked = "[GetScriptedGui('newsfeed_select_all_state_type_{type}').IsValid( GuiScope.SetRoot(GetPlayer.MakeScope).End )]"
                onclick = "[GetScriptedGui('newsfeed_select_all_toggle_type_{type}').Execute( GuiScope.SetRoot(GetPlayer.MakeScope).End )]"
                tooltip = "[GetScriptedGui('newsfeed_select_all_for_type_tooltip').BuildTooltip( GuiScope.AddScope( 'newsfeed_type', MakeScopeFlag('{type}') ).End )]"
                using = tooltip_ne
            }}
        }}
    """

def subject_column(subject):
    return f"""
        flowcontainer = {{
            direction = vertical

            flowcontainer = {{
                widget = {{
                    size = {{ 30 30 }}
                    {subject.icon}
                    tooltip = newsfeed_subject_{subject}_label
                    using = tooltip_ne
                }}
                margin_bottom = 8
            }}

            flowcontainer = {{
                newsfeed_select_all_checkbox = {{
                    checked = "[GetScriptedGui('newsfeed_select_all_state_subject_{subject}').IsValid( GuiScope.SetRoot(GetPlayer.MakeScope).End )]"
                    onclick = "[GetScriptedGui('newsfeed_select_all_toggle_subject_{subject}').Execute( GuiScope.SetRoot(GetPlayer.MakeScope).End )]"
                    tooltip = "[GetScriptedGui('newsfeed_select_all_for_subject_tooltip').BuildTooltip( GuiScope.AddScope( 'newsfeed_subject', MakeScopeFlag('{subject}') ).End )]"
                    using = tooltip_ne
                }}
                margin_bottom = 16
            }}
            
            {lines(setting_checkbox(subject, type) for type in types)}
        }}
    """

def setting_checkbox(subject, type):
    return f"""
        flowcontainer = {{
            margin_right = 8
            button_checkbox = {{
                checked = "[GetScriptedGui('newsfeed_setting_state_subject_{subject}_type_{type}').IsValid( GuiScope.SetRoot(GetPlayer.MakeScope).End )]"
                onclick = "[GetScriptedGui('newsfeed_setting_toggle_subject_{subject}_type_{type}').Execute( GuiScope.SetRoot(GetPlayer.MakeScope).End )]"
                tooltip = "[GetScriptedGui('newsfeed_setting_tooltip').BuildTooltip( GuiScope.AddScope( 'newsfeed_subject', MakeScopeFlag('{subject}') ).AddScope( 'newsfeed_type', MakeScopeFlag('{type}') ).End )]"
                using = tooltip_ne
            }}
        }}
    """

def is_setting_enabled(subject, type):
    return f"""
        newsfeed_is_setting_enabled = {{
            SUBJECT = {subject}
            TYPE = {type}
        }}
    """

def disable_setting(subject, type):
    return f"""
        newsfeed_disable_setting = {{
            SUBJECT = {subject}
            TYPE = {type}
        }}
    """

def clear_setting(subject, type):
    return f"""
        newsfeed_clear_setting = {{
            SUBJECT = {subject}
            TYPE = {type}
        }}
    """

def enable_setting(subject, type):
    return f"""
        newsfeed_enable_setting = {{
            SUBJECT = {subject}
            TYPE = {type}
        }}
    """

def toggle_setting(subject, type):
    return f"""
        newsfeed_toggle_setting = {{
            SUBJECT = {subject}
            TYPE = {type}
        }}
    """

def copy_setting(subject, type):
    return f"""
        newsfeed_copy_setting = {{
            SUBJECT = {subject}
            TYPE = {type}
        }}
    """

def select_all_triggers():
    return f"""
        newsfeed_selected_all_for_subject = {{
            {lines(is_setting_enabled('$SUBJECT$', type) for type in types)}
        }}
        newsfeed_selected_all_for_type = {{
            {lines(is_setting_enabled(subject, '$TYPE$') for subject in subjects)}
        }}
    """

def select_all_effects():
    return f"""
        newsfeed_select_all_for_subject = {{
            {lines(enable_setting('$SUBJECT$', type) for type in types)}
        }}
        newsfeed_select_all_for_type = {{
            {lines(enable_setting(subject, '$TYPE$') for subject in subjects)}
        }}
        newsfeed_deselect_all_for_subject = {{
            {lines(disable_setting('$SUBJECT$', type) for type in types)}
        }}
        newsfeed_deselect_all_for_type = {{
            {lines(disable_setting(subject, '$TYPE$') for subject in subjects)}
        }}
    """

def toggle_gui(subject, type):
    return f"""
        newsfeed_setting_toggle_subject_{subject}_type_{type} = {{
            scope = character

            effect = {{
                custom_tooltip = newsfeed_setting_tooltip

                newsfeed_toggle_setting = {{
                    SUBJECT = {subject}
                    TYPE = {type}
                }}
            }}
        }}

        newsfeed_setting_state_subject_{subject}_type_{type} = {{
            scope = character

            is_valid = {{
                newsfeed_is_setting_enabled = {{
                    SUBJECT = {subject}
                    TYPE = {type}
                }}
            }}
        }}
    """

def select_all_for_subject_gui(subject):
    return f"""
    newsfeed_select_all_state_subject_{subject} = {{
        scope = character

        is_valid = {{
            newsfeed_selected_all_for_subject = {{
                SUBJECT = {subject}
            }}
        }}
    }}

    newsfeed_select_all_toggle_subject_{subject} = {{
        scope = character

        effect = {{
            newsfeed_toggle_select_all_for_subject = {{
                SUBJECT = {subject}
            }}
        }}
    }}
    """

def select_all_for_type_gui(type):
    return f"""
        newsfeed_select_all_state_type_{type} = {{
            scope = character

            is_valid = {{
                newsfeed_selected_all_for_type = {{
                    TYPE = {type}
                }}
            }}
        }}

        newsfeed_select_all_toggle_type_{type} = {{
            scope = character

            effect = {{
                newsfeed_toggle_select_all_for_type = {{
                    TYPE = {type}
                }}
            }}
        }}
    """

def interest_trigger(type):
    return f"""
        newsfeed_is_interested_in_{type} = {{
            newsfeed_is_interested_in = {{
                PERSON = $PERSON$
                TYPE = {type}
            }}
        }}
    """

def is_interested_in_trigger():
    return f"""
        newsfeed_is_interested_in = {{
            OR = {{
                {lines(is_interested_in_as_subject(subject) for subject in subjects)}
            }}
        }}
    """

def is_interested_in_as_subject(subject):
    return f"""
		newsfeed_is_interested_in_as_subject = {{
			PERSON = $PERSON$
			SUBJECT = {subject}
			TYPE = $TYPE$
		}}
    """

def clear_all_settings_effect():
    return f"""
        newsfeed_clear_all_settings = {{
            {lines(clear_setting(subject, type) for subject, type in combos)}
        }}
    """

def copy_all_settings_effect():
    return f"""
        newsfeed_copy_all_settings = {{
            {lines(copy_setting(subject, type) for subject, type in combos)}
        }}
    """

def copy_setting(subject, type):
    return f"""
        newsfeed_copy_setting = {{
            TARGET = $TARGET$
            SUBJECT = {subject}
            TYPE = {type}
        }}
    """

def migrate_all_settings_effect():
    return f"""
        newsfeed_migrate_all_settings_from_old_style = {{
            {lines(migrate_setting(subject, type) for subject, type in combos)}
        }}
    """

def migrate_setting(subject, type):
    return f"""
        newsfeed_migrate_setting_from_old_style = {{
            SUBJECT = {subject}
            TYPE = {type}
        }}
    """

def all_effects():
    return f"""
        {select_all_effects()}
        {clear_all_settings_effect()}
        {copy_all_settings_effect()}
        {migrate_all_settings_effect()}
    """

def all_triggers():
    return f"""
        {select_all_triggers()}
        {is_interested_in_trigger()}
        {lines(interest_trigger(type) for type in types)}
    """

def all_scripted_guis():
    return f"""
        {lines(toggle_gui(subject, type) for subject, type in combos)}
        {lines(select_all_for_subject_gui(subject) for subject in subjects)}
        {lines(select_all_for_type_gui(type) for type in types)}
    """

def format_code(code):
    import re

    lines = [re.sub(r'^\s+|\s+$', '', line) for line in code.splitlines() if not re.match(r'^\s*$', line)]
    result = ''
    indent = 0
    for line in lines:
        if line.endswith('}'):
            indent += line.count('{') - line.count('}')
        result += '\t' * indent + line + '\n'
        if line.endswith('{'):
            indent += line.count('{') - line.count('}')
    return result

def write_code(code, filename):
    with open(filename, 'w', encoding = 'utf-8-sig') as file:
        file.write(format_code(code))

def generate_settings():
    write_code(all_effects(), './common/scripted_effects/newsfeed_generated.txt')
    write_code(all_triggers(), './common/scripted_triggers/newsfeed_generated.txt')
    write_code(all_scripted_guis(), './common/scripted_guis/newsfeed_generated.txt')
    write_code(gui_template(), './gui/newsfeed_generated.gui')
