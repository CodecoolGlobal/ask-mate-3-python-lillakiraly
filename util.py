from datetime import datetime
from time import mktime


def increase_page_view_num(question_id):
    data = data_handler.read_csv(reverse=False)
    for row in data:
        if int(row['id']) == int(question_id):
            row['view_number'] = int(row['view_number']) + 1
    data_handler.write_questions_to_csv(data)


def convert_date(datas=None, time_data=None):
    # for question in datas:
    #     for key in question:
    #         if key == sorted_by:
    #             question[key] = int(question[key])
    # return sorted(datas, key=operator.itemgetter(sorted_by), reverse=(order == 'desc'))
    if time_data is not None:
        position_of_last_dot = str(time_data).rfind(".")
        return int(mktime(datetime.strptime(str(time_data)[:position_of_last_dot], '%Y-%m-%d %H:%M:%S').timetuple()))

    for data in datas:
        for key in data:
            if key == 'submission_time':
                data[key] = datetime.utcfromtimestamp(int(data[key])).strftime('%Y-%m-%d %H:%M:%S')
    return datas


def generate_id(data):
    ids = [int(item['id']) for item in data]
    if not ids:
        return 1
    return max(ids) + 1


def vote(id: int, csvdata: str, voting_direction: str, switch=True):
    all_data = data_handler.read_csv(csv_database=csvdata, reverse=False)
    for row in all_data:
        if int(row['id']) == int(id):
            row['id'] = id
            if voting_direction == 'up':
                row['vote_number'] = int(row['vote_number']) + 1
            else:
                row['vote_number'] = int(row['vote_number']) - 1
    data_handler.write_questions_to_csv(export=all_data, switch=switch)


if __name__ == '__main__':
    print(convert_date(datetime.now(), to_timestamp=True))
    print(convert_date(1655151674, to_timestamp=False))
    print(generate_id(data=data_handler.read_csv()))
