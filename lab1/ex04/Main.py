from QuanLySinhVien import QuanLySinhVien

qlsv = QuanLySinhVien()
while (1 == 1):
    print("\nCHUONG TRINH QUAN LY SINH VIEN")
    print("***************************menu******************************")
    print("***1. thêm sinh viên.                                     ***")
    print("***2. cập nhật thông tin sinh viên bởi ID                 ***")
    print("***3. xóa sinh viên bởi ID                                ***")
    print("***4. tìm kiếm sinh viên theo tên                         ***")
    print("***5. sắp xếp sinh viên theo điểm trung bình              ***")
    print("***6. sắp xếp sinh viên theo tên chuyên ngành             ***")
    print("***7. hiển thị danh sách sinh viên                        ***")
    print("***0. thoát chương trình                                  ***")
    print("*************************************************************")

    key = int(input("Nhập lựa chọn của bạn: "))
    if (key == 1):
        print("Thêm sinh viên")
        qlsv.nhapSinhVien()
        print("Thêm sinh viên thành công")
    elif (key == 2):
        if (qlsv.soLuongSinhVien() > 0):
            print("\n2. Cập nhật thông tin sinh viên")
            print("\nNhap ID sinh viên cần cập nhật: ")
            ID = int(input())
            qlsv.updateSinhVien(ID)
        else:
            print("Danh sách sinh viên rỗng")
    elif (key == 3):
        if (qlsv.soLuongSinhVien() > 0):
            print("\n3. Xóa sinh viên")
            print("\nNhap ID sinh viên cần xóa: ")
            ID = int(input())
            if (qlsv.deleteByID(ID)):
                print("\nSinh viên có ID = ", ID, " đã bị xóa.")
            else:
                print("\nSinh viên có ID = ", ID, " không tồn tại.")
        else:
            print("Danh sách sinh viên rỗng")
    elif (key == 4):
        if (qlsv.soLuongSinhVien() > 0):
            print("\n4. Tìm kiếm sinh viên theo tên")
            print("\nNhap tên sinh viên cần tìm: ")
            name = input()
            searchResult = qlsv.findByName(name)
            qlsv.showList(searchResult)
        else:
            print("Danh sách sinh viên rỗng")
    elif (key == 5):
        if (qlsv.soLuongSinhVien() > 0):
            print("\n5. Sắp xếp sinh viên theo điểm trung bình")
            qlsv.sortByDiemTB()
            qlsv.showList(qlsv.listSinhVien)
        else:
            print("Danh sách sinh viên rỗng")
    elif (key == 6):
        if (qlsv.soLuongSinhVien() > 0):
            print("\n6. sắp xếp sinh viên theo tên.")
            qlsv.sortByName()
            qlsv.showSinhVien(qlsv.getListSinhVien())
        else:
            print("Danh sách sinh viên rỗng")
    elif (key == 7):
        if (qlsv.soLuongSinhVien() > 0):
            print("\n7. Hiển thị danh sách sinh viên")
            qlsv.showSinhVien(qlsv.getListSinhVien())
        else:
            print("Danh sách sinh viên rỗng")
    elif (key == 0):
        print("Thoát chương trình")
        break
    else:
        print("Không có chức năng này.")
        print("hãy chọn chức năng trong menu")
