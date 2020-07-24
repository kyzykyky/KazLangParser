import xlwt



def file_write(Cat, file):
    print('file')
    # corpus = webtext()
    style = xlwt.easyxf("align: horiz left; align: vert top; align: wrap yes;")
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(Cat)
    ws.write(0, 0, "title", style)
    ws.write(0, 1, "text", style)
    ws.write(0, 2, "lemmas", style)
    ws.write(0, 3, "segments", style)
    ws.write(0, 4, "genre", style)
    ws.write(0, 5, "keywords", style)
    ws.write(0, 6, "subject", style)
    ws.write(0, 7, "url", style)
    i = 1
    ws.col(0).width = 10000
    ws.col(1).width = 10000
    ws.col(7).width = 10000
    for ob in corpus:
        ws.write(i, 0, ob["title"], style)
        ws.write(i, 1, ob["text"], style)
        ws.write(i, 2, "", style)
        ws.write(i, 3, "", style)
        ws.write(i, 4, "Maqala", style)
        ws.write(i, 5, "", style)
        ws.write(i, 6, "", style)
        ws.write(i, 7, ob["url"], style)
        i += 1
    wb.save(file + ".xls")

    print('file end')