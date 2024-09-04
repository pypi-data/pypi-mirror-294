import io

import streamlit as st
from streamlit_javascript import st_javascript
import qrcode


def get_st_href():
    return st_javascript("await fetch('').then(r => window.parent.location.href)")


def generate_qr_code(url: str, title: str = f"Demo Version: local, Website QR Code Expander"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=15,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    st.markdown('\n')
    st.markdown('\n')
    st.markdown('\n')
    st.markdown('\n')
    st.markdown('\n')
    st.markdown('\n')

    with st.expander(title):
        st.image(img_byte_arr, caption=url)


def set_hidden_js(js_string: str):
    st.components.v1.html(js_string, height=0, width=0)
