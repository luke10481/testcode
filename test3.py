import datetime
import re


def parse_date(date_str):
    match = re.match(r'(\d+)年(\d+)月(\d+)日', date_str)
    if match:
        return int(match.group(1)), int(match.group(2)), int(match.group(3))
    return None

def get_progress_list(today_date, plan_list):
    #current_year = today_date.year
    progress_list = []
    for i , plan in enumerate(plan_list):
        date_part, name_part = plan.split('\n')
        start_str, end_str = date_part.split('-')
        start_str = start_str.strip()
        end_str = end_str.strip()
        start_year, start_month, start_day = parse_date(start_str)
        end_year, end_month, end_day = parse_date(end_str)
        start_date = datetime.date(start_year, start_month, start_day)
        end_date = datetime.date(end_year, end_month, end_day)
        if i ==1:
            pass
        if today_date < start_date:
            status = '未开始'
            progress = 0
        elif today_date > end_date:
            status = '已完成'
            progress = 100
        else:
            status = '进行中'
            if today_date < start_date:
                progress = 0
            elif today_date > end_date:
                progress = 100
            else:
                total_days = (end_date - start_date).days + 1
                passed_days = (today_date - start_date).days + 1
                progress = int((passed_days / total_days) * 100)
        progress_list.append([status,progress])
    return progress_list

if __name__ == "__main__":

    today_date = datetime.date.today()
    today_date = datetime.date(2026, 1, 11)
    plan_list = ['2025年12月8日 - 2026年1月10日\n第一轮测试(3个工作日)',
                 '2026年1月11日 - 2026年1月19日\n第一轮测试(7个工作日)',
                 '2026年1月20日 - 2026年1月26日\n第一轮测试(7个工作日)']
    p=get_progress_list(today_date, plan_list)
    print(p)