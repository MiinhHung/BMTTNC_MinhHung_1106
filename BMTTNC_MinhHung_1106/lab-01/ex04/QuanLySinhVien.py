from SinhVien import SINHVIEN

class QuanLySinhVien:
    listSINHVIEN = []

    def generateID(self):
        maxID = 1
        if (self.soLuongSinhVien() > 0):
            # Sửa lỗi: Sử dụng listSINHVIEN thay vì listSinhVien
            maxID = self.listSINHVIEN[0]._id
            for sv in self.listSINHVIEN:
                if (maxID < sv._id):
                    maxID = sv._id
            maxID = maxID + 1
        return maxID

    def soLuongSinhVien(self):
        return self.listSINHVIEN.__len__()

    def nhapSinhVien(self):
        svId = self.generateID()
        name = input("Nhap ten sinh vien: ")
        sex = input("Nhap gioi tinh sinh vien: ")
        major = input("Nhap chuyen nganh cua sinh vien: ") # Giữ nguyên là chuỗi
        diemTB = float(input("Nhap diem cua sinh vien: "))
        sv = SINHVIEN(svId, name, sex, major, diemTB)
        self.xepLoaiHocLuc(sv) # Sửa lỗi: exploitHocLuc thành xepLoaiHocLuc
        self.listSINHVIEN.append(sv)

    def updateSinhVien(self, ID):
        sv:SINHVIEN = self.findByID(ID)
        if (sv != None):
            name = input("Nhap ten sinh vien: ")
            sex = input("Nhap gioi tinh sinh vien: ")
            major = input("Nhap chuyen nganh cua sinh vien: ") # Giữ nguyên là chuỗi
            diemTB = float(input("Nhap diem cua sinh vien: "))
            sv._name = name
            sv._sex = sex
            sv._major = major
            sv._diemTB = diemTB
            self.xepLoaiHocLuc(sv) # Sửa lỗi: exploitHocLuc thành xepLoaiHocLuc
        else: # Sửa lỗi thụt lề của else
            print("Sinh vien co ID = {} khong ton tai.".format(ID))

    def sortByID(self):
        # Sửa lỗi: Sử dụng listSINHVIEN thay vì listSinhVien
        self.listSINHVIEN.sort(key=lambda x: x._id, reverse=False)

    def sortByName(self):
        # Sửa lỗi: Sử dụng listSINHVIEN thay vì listSinhVien
        self.listSINHVIEN.sort(key=lambda x: x._name, reverse=False)

    def sortByDiemTB(self):
        # Sửa lỗi: Sử dụng listSINHVIEN thay vì listSinhVien
        self.listSINHVIEN.sort(key=lambda x: x._diemTB, reverse=False)

    def findByID(self, ID):
        searchResult = None
        if (self.soLuongSinhVien() > 0):
            # Sửa lỗi: Sử dụng listSINHVIEN thay vì listSinhVien
            for sv in self.listSINHVIEN:
                if (sv._id == ID):
                    searchResult = sv
                    return searchResult
        return searchResult # Thêm return searchResult ở đây để xử lý trường hợp không tìm thấy

    def findByName(self, keyword):
        listSV = []
        if (self.soLuongSinhVien() > 0):
            # Sửa lỗi: Sử dụng listSINHVIEN thay vì listSinhVien
            for sv in self.listSINHVIEN:
                if (keyword.upper() in sv._name.upper()):
                    listSV.append(sv)
        return listSV

    def deleteByID(self, ID):
        isDeleted = False
        sv = self.findByID(ID)
        if (sv != None):
            # Sửa lỗi: Sử dụng listSINHVIEN thay vì listSinhVien
            self.listSINHVIEN.remove(sv)
            isDeleted = True
        return isDeleted

    def xepLoaiHocLuc(self, sv:SINHVIEN): # Sửa lỗi: SinhVien thành SINHVIEN
        if (sv._diemTB >= 8):
            sv._hocLuc = "Gioi"
        elif (sv._diemTB >= 6.5):
            sv._hocLuc = "Kha"
        elif (sv._diemTB >= 5): # Sửa lỗi thụt lề
            sv._hocLuc = "Trung binh"
        else: # Sửa lỗi thụt lề
            sv._hocLuc = "Yeu"

    def showSinhVien(self, listSV):
        print("{:<8} {:<18} {:<8} {:<8} {:<8} {:<8}".format("ID", "Name", "Sex", "Major", "Diem TB", "Hoc Luc"))
        if (listSV.__len__() > 0):
            for sv in listSV:
                print("{:<8} {:<18} {:<8} {:<8} {:<8} {:<8}".format(sv._id, sv._name, sv._sex, sv._major, sv._diemTB, sv._hocLuc))

        print("\n")

    def getListSinhVien(self):
        return self.listSINHVIEN # Sửa lỗi: Sử dụng listSINHVIEN thay vì listSinhVien