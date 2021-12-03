# 1. IMPORT CÁC THƯ VIỆN CẦN THIẾT
import pandas as pd
import os
import matplotlib.pyplot as plt

# 2. XỬ LÝ DỮ LIỆU
def xuly():
    dir = 'dataset/'
    saleLst = os.listdir(dir)  # lấy ra tên các file trong thư mục dataset

    filepath = []
    for i in range(0, len(saleLst)):
        filepath.append(dir + saleLst[i])
        # print(filepath[i])

    readFile = []
    for i in range(0, len(filepath)):
        readFile.append(pd.read_csv(filepath[i]))
        # print(readFile[i])

    # gộp tất cả các file csv vào thành một file duy nhất
    frames = pd.concat(readFile)

    df = frames
    df.to_csv('dataset/doanh_thu.csv', index=False)  # ghi file csv và bỏ cột index
    df.head().to_string()  # method to_string() để in ra full table

#4. THÁNG CÓ DOANH THU CAO NHẤT
def monthMax(df):
    values_months = df.groupby('Month').sum()['Doanh thu']  # nhóm các tháng lại và tính tổng theo doanh thu
    max_months = values_months.max()  # tháng có doanh số bán cao nhất
    for i in range(0, len(values_months)):
        if values_months[i] == max_months:
            print('Tháng có doanh thu cao nhất là tháng ' + str(i + 1) + " : " + str(max_months))
    print(values_months)
    # TRỰC QUAN HÓA DỮ LIỆU DOANH THU CỦA CÁC THÁNG TRONG NĂM
    months = range(1, 13)
    plt.title("Doanh thu các tháng trong năm")
    plt.barh(months, values_months)
    plt.yticks(months)
    plt.xlabel('Doanh thu')
    plt.ylabel('Tháng')
    plt.show()

#5. THÀNH PHỐ CÓ DOANH THU CAO NHẤT
def cityMax(df):
    df['City'] = ''
    sample_address = df['Purchase Address'].str.split(',').tolist()
    cityLst = []
    for i in range(0, len(df['Purchase Address'])):
        cityLst.append(sample_address[i][1])
    df['City'] = cityLst
    nameCity = sorted(set(df['City']))
    values_city = df.groupby('City').sum()['Doanh thu']  # nhóm các tháng lại và tính tổng doanh thu
    max_city = values_city.max()  # thành phố có doanh số bán cao nhất

    for i in range(0, len(values_city)):
        if values_city[i] == max_city:
            print("Thành phố có doanh thu cao nhất là " + str(nameCity[i]) + " : " + str(max_city))
    print(values_city)

    # TRỰC QUAN HÓA DỮ LIỆU DOANH THU CỦA CÁC THÀNH PHỐ
    city = sorted(set(df['City']))
    plt.title('Doanh thu của các thành phố')
    plt.bar(x=city, height=values_city)
    plt.xticks(city)
    plt.xticks(rotation=25)
    plt.xlabel('Thành phố')
    plt.ylabel('Doanh thu')
    plt.show()

# 6.THỜI GIAN KHÁCH HÀNG HAY ĐI MUA SẢN PHẨM NHẤT
def timeMax(df):
    df['Time to buy'] = ''
    df['Human'] = 1
    df['Time to buy'] = df['Order Date'].str[-5:-3]
    values_human = df.groupby('Time to buy').sum()['Human']
    max_human = values_human.max()
    hours = sorted(set(df['Time to buy']))
    for i in range(0, len(values_human)):
        if values_human[i] == max_human:
            print("Khoảng thời gian mà khách hàng hay đi mua nhất là: " + str(i) + " giờ")
    # print(values_human)

    # TRỰC QUAN HÓA DỮ LIỆU THỜI GIAN BÁN HÀNG CHẠY NHẤT TRONG NGÀY
    plt.plot(hours, values_human)
    plt.title('Thời gian bán chạy trong ngày')
    plt.grid()
    plt.xticks(hours)
    plt.xlabel('Giờ')
    plt.ylabel('Số lượng người mua')
    plt.show()

if __name__ == '__main__':
    xuly()
    df = pd.read_csv('dataset/doanh_thu.csv')

    #region 3. LÀM SẠCH DỮ LIỆU
    df['Month'] = ''  # thêm cột Tháng
    df['Month'] = df['Order Date'].str[0:2]  # cắt substring tháng từ cột Order Date
    # print(set(df['Month'])) # lấy ra các giá trị có trong cột Month

    # loại bỏ các giá trị nan (dòng trắng) và or (order date) trong df['Month']
    df = df.dropna(how='all')  # loại bỏ tất cả các dòng có giá trị nan
    df = df[df['Month'] != 'Or']  # loại bỏ tất cả các dòng có giá trị Or trong cột Month

    df['Doanh thu'] = ''  # thêm cột Doanh thu
    df['Quantity Ordered'] = pd.to_numeric(df['Quantity Ordered'], downcast='integer')  # convert to int
    df['Price Each'] = pd.to_numeric(df['Price Each'], downcast='float')  # convet to float
    df['Doanh thu'] = df['Quantity Ordered'] * df['Price Each']  # tính doanh thu
    moving_column = df.pop('Doanh thu')  # cắt cột Doanh thu ra khỏi data frame
    df.insert(4, 'Doanh thu', moving_column)  # chèn cột vừa cắt vào cột thứ 4 trong df
    #endregion

    monthMax(df)
    cityMax(df)
    timeMax(df)