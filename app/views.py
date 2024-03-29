
from django.template import loader
from django.http import HttpResponse
from datetime import date, timedelta
from app.models import TotalStats
from django.db.models import Sum, Q
from django.db.models import F
from django.db.models.functions import TruncMonth, TruncDay, TruncYear


def get_line_data_points(data, timeline):
    for line_data_points_obj in data:
        df_data = line_data_points_obj.pop("month")
        if timeline == "day" or timeline == "30days":
            line_data_points_obj["label"] = str(df_data)
        elif timeline == "month":
            line_data_points_obj["label"] = "-".join([df_data.strftime('%Y'), df_data.strftime("%B")])
            line_data_points_obj["label"] = "-".join([df_data.strftime('%Y'), df_data.strftime("%B")])
        elif timeline == "year":
            line_data_points_obj["label"] = str(df_data.year)
        line_data_points_obj["org_val"] = df_data
    data.sort(key=lambda x: x['org_val'])
    return data


def get_line_data_points_deep(deep_data, timeline):
    data = {obj["name_of_table"]: [] for obj in deep_data}
    for line_data_points_obj in deep_data:
        df_data = line_data_points_obj.pop("month")
        if timeline == "day" or timeline == "30days":
            line_data_points_obj["label"] = str(df_data)
        elif timeline == "month":
            line_data_points_obj["label"] = "-".join([df_data.strftime('%Y'), df_data.strftime("%B")])
            line_data_points_obj["label"] = "-".join([df_data.strftime('%Y'), df_data.strftime("%B")])
        elif timeline == "year":
            line_data_points_obj["label"] = str(df_data.year)
        line_data_points_obj["org_val"] = df_data
        data[line_data_points_obj["name_of_table"]].append(line_data_points_obj)
    final_data = []
    for key in data.keys():
        data_obj = data[key]
        data_obj.sort(key=lambda x: x['org_val'])
        for obj in data_obj:
            obj.pop("org_val", None)
        final_data_obj = {"type": "area", "name": key, "showInLegend": True, "axisYType": "secondary",
                           "markerSize": 0, "legendMarkerType": "square", "dataPoints": data_obj}
        final_data.append(final_data_obj)
    return final_data


def line_data_points_qs(category, name_of_table, days, type):
     line_data_points = TotalStats.objects.filter(category=category, date_created__gte=days,
                                                  name_of_table=name_of_table)
     func = {"week": TruncDay, "30days": TruncDay, "month": TruncMonth, "year": TruncYear}
     func = func[type]
     line_data_points = list(line_data_points.annotate(month=func('date_created')).values('month')
                             .annotate(y=Sum('create_count')))
     line_data_points = get_line_data_points(line_data_points, type)
     for line_data_points_obj in line_data_points:
         line_data_points_obj.pop("org_val", None)
     return line_data_points


def get_pie_data_points(category, days):
    pie_data_points = TotalStats.objects.filter(category=category, date_created__gte=days).exclude(name_of_table__in=["Mongo Executives", "Gateway Executives"])
    pie_data_points = pie_data_points.values(indexLabel=F('name_of_table')).annotate(y=Sum('create_count'))
    pie_data_points = list(pie_data_points)
    for pie_data_point_obj in pie_data_points:
        pie_data_point_obj["legendText"] = pie_data_point_obj["indexLabel"].title()
    return pie_data_points


def get_accounts_data(days, type):
    func = {"week": TruncDay, "30days": TruncDay, "month": TruncMonth, "year": TruncYear}
    func = func[type]

    pie_data_points = get_pie_data_points("accounts", days)
    rolodex_pie_data_points = get_pie_data_points("rolodex", days)
    line_data_points = line_data_points_qs("accounts", "Accounts", days, type)
    rolodex_line_data_points = line_data_points_qs("rolodex", "App Executives", days, type)

    line_data_points_deep = TotalStats.objects.filter(category="accounts", date_created__gte=days).annotate(month=func('date_created')).values('month', 'name_of_table') \
                            .annotate(y=Sum('create_count'))

    rolodex_data_deep = TotalStats.objects.filter(
        category="rolodex", name_of_table__in=["Mongo Executives", "Gateway Executives", "App Executives"]).filter(date_created__gte=days)\
        .annotate(month=func('date_created')).values('month', 'name_of_table').annotate(y=Sum('create_count'))

    rolodex_data_filled = TotalStats.objects.exclude(name_of_table__in=["Mongo Executives", "Gateway Executives"])
    rolodex_data_filled = rolodex_data_filled.filter(category="rolodex").filter(date_created__gte=days)\
        .annotate(month=func('date_created')).values('month', 'name_of_table').annotate(y=Sum('create_count'))
    rolodex_data_filled = get_line_data_points_deep(rolodex_data_filled, type)

    rolodex_points_deep = get_line_data_points_deep(rolodex_data_deep, type)
    line_data_points_deep = get_line_data_points_deep(line_data_points_deep, type)
    return {"pie_data_points": pie_data_points, "line_data_points": line_data_points,
            "multiline_points_filled": line_data_points_deep, "rolodex_multiline_points_filled": rolodex_points_deep,
            "rolodex_line_data_points": rolodex_line_data_points, "rolodex_pie_data_points": rolodex_pie_data_points,
            "rolodex_data_filled": rolodex_data_filled}


def index(request):
    timeline = request.GET.get('timeline', 'day')

    if timeline == "30days":
        time_diff = date.today() - timedelta(days=30)
    elif timeline == 'month':
        current_dt = date.today() - timedelta(days=365)
        time_diff = date(current_dt.year, 1, 1)
    elif timeline == 'year':
        current_dt = date.today() - timedelta(days=365)
        time_diff = date(current_dt.year, 1, 1)
    else:
        time_diff = date.today() - timedelta(days=7)
    data = get_accounts_data(time_diff, timeline)
    template = loader.get_template('index_new.html')
    return HttpResponse(template.render(data))
