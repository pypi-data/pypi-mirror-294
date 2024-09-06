from netbox.plugins import PluginMenuButton, PluginMenuItem


kritencluster_buttons = [
    PluginMenuButton(
        link='plugins:kriten:kritencluster_add',
        title='Add',
        icon_class='mdi mdi-plus-thick'
    )
]

kritenrunner_buttons = [
    PluginMenuButton(
        link='plugins:kriten:kritenrunner_add',
        title='Add',
        icon_class='mdi mdi-plus-thick'
    )
]

kritentask_buttons = [
    PluginMenuButton(
        link='plugins:kriten:kritentask_add',
        title='Add',
        icon_class='mdi mdi-plus-thick'
    )
]

kritenjob_buttons = [
    PluginMenuButton(
        link='plugins:kriten:kritenjob_add',
        title='Add',
        icon_class='mdi mdi-plus-thick'
    )
]

menu_items = (
    PluginMenuItem(
        link='plugins:kriten:kritencluster_list',
        link_text='Kriten Clusters',
        buttons=kritencluster_buttons
    ),
    PluginMenuItem(
        link='plugins:kriten:kritenrunner_list',
        link_text='Kriten Runners',
        buttons=kritenrunner_buttons
    ),
    PluginMenuItem(
        link='plugins:kriten:kritentask_list',
        link_text='Kriten Tasks',
        buttons=kritentask_buttons
    ),
    PluginMenuItem(
        link='plugins:kriten:kritenjob_list',
        link_text='Kriten Jobs',
        buttons=kritenjob_buttons
    ),
)
