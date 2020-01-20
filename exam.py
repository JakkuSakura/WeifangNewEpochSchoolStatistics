#!/bin/python3
# coding: utf-8
import pandas as pd


def read_test(filename):
    test = pd.read_csv(filename, header=0, encoding='utf-8', index_col=0)
    return test


def get_selected(row):
    selected = []
    labels = row.keys().values
    for label in labels:
        if '排名' not in label and not pd.isna(row[label]):
            selected.append(label)
    return selected


def to_html_table(exams, order, stu):
    for e in exams.values():
        try:
            selected = get_selected(e.loc[stu])
            break
        except:
            pass
    else:
        return ''

    exam_table = '<table border="1"><tr><th>考试</th>' + \
        ''.join(['<th>%s</th><th>%s排名</th>' % (x, x)
                 for x in selected]) + '</tr>'
    for name in order:
        exam = exams[name]
        exam_table += '<tr><th>' + name + '</th>'
        for subj in selected:
            try:
                if not pd.isna(exam.loc[stu, subj]):
                    exam_table += "<td>" + str(exam.loc[stu, subj]) + "</td><td>" + str(exam.loc[stu, subj+'排名']) + "</td>"
                    continue
            except:
                pass
            exam_table += "<td><td>"
            # why there's single <td></td> but still works?
        exam_table += '</tr>'
    exam_table += '</table>'
    return exam_table

def to_html_table_and_picture(exams, order, stu):
    exam_table = to_html_table(exams, order, stu)
    with open('table_and_picture.html', "r") as expl:
        text = expl.read().format(name=stu, table=exam_table)
    return text


def to_html(exams, order, stu):
    exam_table = to_html_table(exams, order, stu)
    with open('student_example.html', "r") as expl:
        text = expl.read().format(name=stu, table=exam_table)
    return text


def calc_extra(test):
    subjects = list(test.columns.values)
    test['总分'] = test.apply(lambda x: sum([float(x[y])
                                           for y in subjects if not pd.isna(x[y])]), axis=1)
    subjects.append('总分')
    for subj in subjects:
        test[subj+'排名'] = 0
        test[subj+'排名'] = test[subj].rank(method='min', ascending=False)
    new_labels = []
    for subj in subjects:
        new_labels.append(subj)
        new_labels.append(subj+'排名')
    return test[new_labels]


tests_names = [
    '2019年10月新高考联盟高三质检',
    '高三期中考试',
    '山东省高考模拟成绩',
    '高三期末考试'
]
tests = {}
for test_name in tests_names:
    test = read_test('data/'+test_name+'.csv')
    test = calc_extra(test)
    # print(test_name)
    # print(test.head(5))
    tests[test_name] = test

if __name__ == '__main__':
    print(to_html(tests, tests_names, "邱江坤"))
