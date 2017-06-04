from django.utils.translation import ugettext_lazy as _
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard
from jet.dashboard.dashboard_modules import google_analytics


class CustomIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
       self.available_children.append(google_analytics.GoogleAnalyticsVisitorsTotals)
       self.available_children.append(google_analytics.GoogleAnalyticsVisitorsChart)
       self.available_children.append(google_analytics.GoogleAnalyticsPeriodVisitors)



from admin_tools_stats.modules import DashboardCharts, get_active_graph

# append an app list module for "Country_prefix"
self.children.append(modules.AppList(
    _('Dashboard Stats Settings'),
    models=('admin_tools_stats.*', ),
))

# Copy following code into your custom dashboard
# append following code after recent actions module or
# a link list module for "quick links"
graph_list = get_active_graph()
for i in graph_list:
    kwargs = {}
    kwargs['graph_key'] = i.graph_key
    kwargs['require_chart_jscss'] = False

    if context['request'].POST.get('select_box_' + i.graph_key):
        kwargs['select_box_' + i.graph_key] = context['request'].POST['select_box_' + i.graph_key]

    self.children.append(DashboardCharts(**kwargs))