import json
import mysql.connector

def process_data(keyword, sort_att):
    cnx = mysql.connector.connect(user='dsci551', password='dsci551', host='127.0.0.1', database='project')
    cursor = cnx.cursor(buffered=True)

    query = "select thumbnail_link, video_title, channel_title, category_name, views, likes, comment_count, title from data_agg " \
            "where video_title like '%" + keyword + "%' or category_name like '%" + keyword + "%' or " \
            "tags like '%" + keyword + " %' order by " + sort_att
    if sort_att != "video_title":
        query += " desc;"
    cursor.execute(query)

    row_headers = [x[0] for x in cursor.description]
    rv = cursor.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data)


if __name__ == '__main__':
    print(process_data('iphone', 'views'))
