import streamlit as st
st.image("logo.jpg.jpg")
# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Công cụ tính Lãi gửi Tiết kiệm",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Công Cụ Tính Lãi Gửi Tiết Kiệm Ngân Hàng - Nguyễn Thị Minh Ngọc")
st.write("Nhập các thông tin dưới đây để tính toán tiền lãi và tổng số tiền thu được.")

st.markdown("---")

# Tạo form nhập liệu
with st.container():
    st.subheader("📌 Nhập thông tin khoản gửi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Số tiền gửi (VND)
        amount = st.number_input(
            "Số tiền gửi (VND):",
            min_value=1_000_000,
            value=100_000_000,
            step=1_000_000,
            format="%d"
        )
        st.caption(f"👉 **{amount:,.0f} VND**")

        # Kỳ hạn gửi (Tháng)
        months = st.number_input(
            "Kỳ hạn gửi (Tháng):",
            min_value=1,
            max_value=120,
            value=12,
            step=1
        )

    with col2:
        # Lãi suất (%/năm)
        rate = st.number_input(
            "Lãi suất gửi (%/năm):",
            min_value=0.1,
            max_value=20.0,
            value=6.0,
            step=0.1,
            format="%.2f"
        )

        # Hình thức nhận lãi
        payment_type = st.selectbox(
            "Hình thức nhận lãi:",
            options=["Cuối kỳ", "Hàng tháng", "Hàng quý"]
        )

st.markdown("---")

# Xử lý tính toán
total_interest = 0.0
periodic_interest = 0.0
periodic_label = ""

# Lãi suất tháng & quý (lãi đơn theo quy chuẩn ngân hàng)
rate_per_year = rate / 100

if payment_type == "Cuối kỳ":
    # Tiền lãi = Số tiền gửi * Lãi suất/năm * (Số tháng gửi / 12)
    total_interest = amount * rate_per_year * (months / 12)
    periodic_interest = total_interest
    periodic_label = "Tiền lãi nhận cuối kỳ"

elif payment_type == "Hàng tháng":
    # Tiền lãi mỗi tháng = Số tiền gửi * Lãi suất/năm / 12
    periodic_interest = amount * rate_per_year / 12
    total_interest = periodic_interest * months
    periodic_label = "Tiền lãi nhận hàng tháng"

elif payment_type == "Hàng quý":
    # Tiền lãi mỗi quý (3 tháng) = Số tiền gửi * Lãi suất/năm / 4
    periodic_interest = amount * rate_per_year / 4
    total_interest = periodic_interest * (months / 3)
    periodic_label = "Tiền lãi nhận hàng quý"

total_amount = amount + total_interest

# Hiển thị kết quả
st.subheader("📊 Kết quả tính toán")

# 3 ô metric nổi bật
m1, m2, m3 = st.columns(3)

with m1:
    st.metric(
        label=periodic_label,
        value=f"{periodic_interest:,.0f} VND"
    )

with m2:
    st.metric(
        label="Tổng tiền lãi nhận được",
        value=f"{total_interest:,.0f} VND"
    )

with m3:
    st.metric(
        label="Tổng tiền gốc + lãi",
        value=f"{total_amount:,.0f} VND"
    )

# Bảng tóm tắt chi tiết
st.markdown("### 📋 Tóm tắt giao dịch")
st.table({
    "Thông tin": [
        "Số tiền gửi ban đầu",
        "Kỳ hạn",
        "Lãi suất niêm yết",
        "Hình thức nhận lãi",
        "Tổng lãi dự kiến",
        "Tổng tiền thu về"
    ],
    "Giá trị": [
        f"{amount:,.0f} VND",
        f"{months} tháng",
        f"{rate:.2f}% / năm",
        payment_type,
        f"{total_interest:,.0f} VND",
        f"{total_amount:,.0f} VND"
    ]
})

if payment_type == "Hàng quý" and months % 3 != 0:
    st.warning("⚠️ **Lưu ý:** Kỳ hạn gửi không chia hết cho 3 tháng. Kết quả tiền lãi quý được quy đổi theo số quý tương đương.")
