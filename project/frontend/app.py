import streamlit as st

from frontend.api_client import ApiUnavailableError, ProductApi

st.set_page_config(page_title="건강한하루", page_icon="🌱", layout="wide")
st.title("건강한하루")
st.caption("상품 목록을 살펴보고 제품 정보를 확인하세요.")

page = st.number_input("페이지", min_value=1, value=1, step=1)
try:
    result = ProductApi().list_products(limit=20, offset=(page - 1) * 20)
except ApiUnavailableError as exc:
    st.error(str(exc))
    st.stop()

st.write(f"전체 {result['total']}개 상품")
if not result["items"]:
    st.info("표시할 상품이 없습니다. 이전 페이지를 선택하세요.")

for product in result["items"]:
    with st.expander(f"{product['name']} · {product['category']}"):
        st.text(f"업체: {product['manufacturer']}")
        st.text(f"주요 원료: {product['ingredient_keyword']}")
        st.write("**기능성 정보**")
        st.text(product["functionality"])
        st.write("**섭취 방법**")
        st.text(product["intake_method"])
        st.write("**주의사항**")
        st.text(product["precautions"] or "원본 데이터에 주의사항이 없습니다.")
        st.caption(f"출처: {product['data_source']}")
        url = product.get("source_url")
        if url and url.startswith("https://"):
            st.link_button("원문 보기", url)
