import streamlit as st
import os
from scraper import *


def main():
    st.title("Web Scraper")

    url = st.text_input("Enter the URL of the website you want to scrape")
    prompt = st.text_area("Enter the prompt for the AI")

    if st.button("Scrape"):
        result = gptv_crawl(url, prompt)
        st.write(result)


if __name__ == "__main__":
    main()
