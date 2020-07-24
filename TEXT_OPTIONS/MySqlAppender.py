import pymysql.cursors
import os


def DBworker(dirr, folder):
    # Establishing connection
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='',
                                 db='textcorpus',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)

    print('\n\n' + dirr)
    for x in os.listdir(dirr):
        if x != '__pycache__' and x != '.idea' and x != '.git' and os.path.isdir(dirr + '\\' + x):
            print(x)

    # Choosing action
    print('\nSelect action:\n'
          '1. Table Generation\n'
          '2. Fill DB\n'
          '3. Exit')
    chh = int(input())

    if chh == 1:
        with connection.cursor() as cursor:
            sql = '''CREATE TABLE `%(dir)s` (
                  `ID` int NOT NULL AUTO_INCREMENT,
                  `Title` varchar(500) NOT NULL,
                  `Text` LongText NOT NULL,
                  `Lemmas` varchar(150) DEFAULT NULL,
                  `Segments` varchar(250) DEFAULT NULL,
                  `Genre` varchar(100) NOT NULL,
                  `Keywords` varchar(100) DEFAULT NULL,
                  `Subject` varchar(100) NOT NULL,
                  `URL` varchar(500) NOT NULL, PRIMARY KEY (ID)
                );''' % {'dir': folder}

            cursor.execute(sql)
            print('Action successful!\n')

        connection.close()
        DBworker(dirr, folder)

    elif chh == 2:
        for cat in os.listdir(dirr):
            if cat != '__pycache__' and cat != '.idea' and cat != '.git' and os.path.isdir(dirr + '\\' + cat):
                print('\n\t' + cat)
                for file in os.listdir(dirr + '\\' + cat):
                    if file.endswith('.txt'):
                        with open(dirr + '\\' + cat + '\\' + file, 'r', encoding='utf-8') as text:

                            url = ''
                            for url_file in os.listdir(dirr + '\\' + cat):
                                if url_file.endswith('.url') and url_file.startswith(file[:-4]):
                                    with open(dirr + '\\' + cat + '\\' + url_file, 'r') as uf:
                                        url = uf.read()
                                        break

                            textt = text.read()
                            print(file[:-4])
                            print(textt)
                            print(url)

                            with connection.cursor() as cursor:
                                try:
                                    sql = '''INSERT INTO %(dir)s (Title, Text, Genre, Subject, URL) 
                                            VALUES ('%(file)s', '%(text)s', '%(cat)s', '%(cat)s', '%(url)s');''' \
                                          % {'dir': folder, 'file': file[:-4], 'text': textt, 'cat': cat, 'url': url}
                                    cursor.execute(sql)

                                    # sql = '''UPDATE %(dir)s
                                    #         SET Text = '%(text)s' WHERE Title = '%(file)s\'''' \
                                    #       % {'dir': folder, 'file': file[:-4], 'text': textt}
                                    # cursor.execute(sql)
                                    connection.commit()
                                except pymysql.err.ProgrammingError:
                                    print('TEXT ERROR')

        connection.close()
        print('Action successful!\n')
        DBworker(dirr, folder)

    elif chh == 3:  # Exit
        connection.close()


def main():
    # Getting path
    directory = 'D:\\Documents\\MyCodes\\MyPy\\ParsePjt\\'
    print('Exact the path:', end='  ')
    folderr = input(directory)
    directory += folderr

    if os.path.exists(directory):
        DBworker(directory, folderr)

    else:
        print('No such path', directory)
        main()


main()
