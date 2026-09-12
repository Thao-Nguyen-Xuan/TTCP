def doc_so_thanh_chu(so_tien):
    if so_tien == 0:
        return "Không đồng"
    
    chu_so = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
    don_vi = ["", "nghìn", "triệu", "tỷ", "nghìn tỷ", "triệu tỷ"]

    def doc_3_chu_so(baso):
        tram = int(baso // 100)
        chuc = int((baso % 100) // 10)
        don_vi_so = int(baso % 10)
        ket_qua = ""
        
        if tram == 0 and chuc == 0 and don_vi_so == 0:
            return ""
            
        ket_qua += chu_so[tram] + " trăm "
        
        if chuc == 0:
            if don_vi_so != 0 and tram != 0:
                ket_qua += "lẻ "
        elif chuc == 1:
            ket_qua += "mười "
        else:
            ket_qua += chu_so[chuc] + " mươi "
            
        if don_vi_so == 1 and chuc > 1:
            ket_qua += "mốt"
        elif don_vi_so == 5 and chuc > 0:
            ket_qua += "lăm"
        elif don_vi_so != 0:
            ket_qua += chu_so[don_vi_so]
            
        return ket_qua.strip()

    s = str(int(so_tien))
    nhom = []
    while s:
        nhom.append(s[-3:])
        s = s[:-3]
        
    i = len(nhom) - 1
    ket_qua_arr = []
    while i >= 0:
        so_nhom = int(nhom[i])
        if so_nhom > 0:
            chu = doc_3_chu_so(so_nhom)
            ket_qua_arr.append(chu)
            if don_vi[i]:
                ket_qua_arr.append(don_vi[i])
        i -= 1
        
    ket_qua = " ".join(ket_qua_arr)
    return ket_qua.capitalize() + " đồng"