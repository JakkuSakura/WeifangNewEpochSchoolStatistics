import os
import pandas as pd
import exam


def gen_group(group):
    filename = 'data/'+group+'.csv'
    df = pd.read_csv(filename, header=0, encoding='utf-8')
    html = """
        <html>
        <head><title>{group}成绩分析汇总</title>
        </head>
        <body>
        """.format(group=group)

    for name in df['姓名']:
        html += exam.to_html_table_and_picture(exam.tests, exam.tests_names, name)
    html += """</body></html>"""
    return html


if __name__ == '__main__':
    groups = [
        '本校初中生',
        '奖学金学生'
    ]
    for group in groups:
        with open('static/'+group+'.html', 'w') as f:
            f.write(gen_group(group))
