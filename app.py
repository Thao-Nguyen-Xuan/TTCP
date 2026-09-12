import streamlit as st
import os
from invoice_parser import parse_invoice_pdf
from document_generator import generate_outputs

st.set_page_config(page_title="Xử lý hóa đơn MobiFone", layout="wide")

st.title("📄 Phần Mềm Xử Lý Hóa Đơn & Bảng Kê MobiFone")

uploaded_file = st.file_uploader("Tải lên file PDF hóa đơn MobiFone", type=["pdf"])

if uploaded_file is not None:
    temp_pdf_path = "temp_invoice.pdf"
    with open(temp_pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    # Phân tích dữ liệu từ PDF
    data = parse_invoice_pdf(temp_pdf_path)
    
    st.divider()
    st.subheader("🔍 Thông tin chung hóa đơn")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Số hóa đơn", value=data.get('so_hoa_don', 'N/A'))
    with col2:
        st.metric(label="Cước Từ ngày", value=data.get('tu_ngay', 'N/A'))
    with col3:
        st.metric(label="Cước Đến ngày", value=data.get('den_ngay', 'N/A'))
    with col4:
        st.metric(label="Tổng thanh toán", value=f"{data.get('tong_cong', 0):,}".replace(',', '.') + " VNĐ")
        
    st.info(f"📅 **Ngày lập hóa đơn:** {data.get('ngay_hoa_don', 'N/A')}")
    st.info(f"🏢 **Khách hàng:** {data.get('ten_khach_hang', 'N/A')}")
    st.info(f"📍 **Địa chỉ:** {data.get('dia_chi', 'N/A')}")
    st.info(f"🔢 **Mã số thuế:** {data.get('mst', 'N/A')}")
    
    # Hiển thị bảng chi tiết cước thuê bao với chiều cao cố định để chống rung giao diện
    st.subheader("📋 Bảng chi tiết cước thuê bao")
    details = data.get('chi_tiet', [])
    if details:
        table_data = []
        for item in details:
            table_data.append({
                "STT": item.get('stt'),
                "Mã KH": item.get('ma_kh'),
                "Số thuê bao": item.get('so_thue_bao'),
                "Thành tiền (VNĐ)": item.get('thanh_tien'),
                "Thuế suất": item.get('thue_suat'),
                "Tiền thuế (VNĐ)": item.get('tien_thue'),
                "Tổng cộng (VNĐ)": item.get('cong')
            })
        st.dataframe(table_data, use_container_width=True, height=400)
    else:
        st.warning("Không tìm thấy chi tiết cước thuê bao.")

    st.divider()

    if st.button("🚀 Tạo Bảng Kê Excel & Giấy Đề Nghị Word", type="primary"):
        with st.spinner("Đang tạo file..."):
            excel_path, docx_path = generate_outputs(data)
            
        st.success("✅ Đã tạo file thành công!")
        
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            if os.path.exists(excel_path):
                with open(excel_path, "rb") as f:
                    st.download_button(
                        label="📥 Tải xuống Bảng Kê (Excel)",
                        data=f,
                        file_name="BangKe_Cuoc.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    
        with col_dl2:
            if os.path.exists(docx_path):
                with open(docx_path, "rb") as f:
                    st.download_button(
                        label="📥 Tải xuống Giấy Đề Nghị (Word)",
                        data=f,
                        file_name="GiayDeNghi_ThanhToan.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )