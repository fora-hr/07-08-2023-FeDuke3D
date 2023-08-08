import time
import json


def sort_key(elem):
    return elem.get('result')


def read_results():
    res = {}
    with open('results_RUN.txt') as file:
        content = file.read().replace('\ufeff', '').split('\n')
    if content:
        for i in content:
            if len(i) == 0:
                continue
            words = i.split()
            number = int(words[0])
            status = words[1]
            msec = 1e-6 * int(words[2].split(',')[1])
            timestamp = time.mktime(time.strptime(words[2],
                                                  '%H:%M:%S,%f')) + msec
            if number not in res:
                res[number] = {}
            if status == 'start':
                res[number]['start'] = timestamp
            elif status == 'finish':
                res[number]['finish'] = timestamp
                if 'start' in res[number]:
                    res[number]['time'] = res[number]['finish'] \
                                          - res[number]['start']
    return res


def read_contestants():
    with open('competitors2.json') as file:
        res = json.loads(file.read().replace('\ufeff', ''))
    return res


def print_table(data):
    place = 1
    for i in data:
        print(f"{place}\t{i['number']}\t{i['name']}\t{i['surname']}\t{round(i['result'], 2)}")
        place += 1


if __name__ == '__main__':
    results = read_results()
    contestants = read_contestants()

    compiled_list = [{'number': i, 'name': contestants.get(str(i))['Name'],
                      'surname': contestants.get(str(i))['Surname'],
                      'result': results[i]['time']} for i in results]
    compiled_list.sort(key=sort_key)

    print_table(compiled_list)
