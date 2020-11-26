mkdir -p ~/.streamlit/

echo "\

[general]\n\

email = \"zdv88@rambler.ru\"\n\

" > ~/.streamlit/credentials.toml

echo "\

[server]\n\

headless = true\n\

enableCORS=false\n\

port = $PORT\n\

" > ~/.streamlit/config.toml