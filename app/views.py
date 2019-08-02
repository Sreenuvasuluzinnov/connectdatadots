
from django.template import loader
from django.http import HttpResponse
from datetime import date, timedelta
from app.models import TotalStats
from django.db.models import Sum
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


def get_accounts_data(days, type):
    pie_data_points = TotalStats.objects.filter(category="accounts", date_created__gte=days)\
        .values(indexLabel=F('name_of_table')).annotate(y=Sum('create_count'))
    pie_data_points = list(pie_data_points)
    for pie_data_point_obj in pie_data_points:
        pie_data_point_obj["legendText"] = pie_data_point_obj["indexLabel"].title()

    line_data_points = TotalStats.objects.filter(category="accounts", date_created__gte=days,
                                                 name_of_table="universe_accounts")
    func = {"week": TruncDay, "30days": TruncDay, "month": TruncMonth, "year": TruncYear}
    func = func[type]
    line_data_points = list(line_data_points.annotate(month=func('date_created')).values('month') \
                            .annotate(y=Sum('create_count')))
    line_data_points = get_line_data_points(line_data_points, type)
    for line_data_points_obj in line_data_points:
        line_data_points_obj.pop("org_val", None)
    return {"pie_data_points": pie_data_points, "line_data_points": line_data_points}


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
    template = loader.get_template('index.html')
    return HttpResponse(template.render(data))
