# ChatGPT-Desktop-UI
Usas tu API key y puedes usar GTP: 3.5-turbo y su versión 16k, y la preview de GPT-4-turbo.

Tan solo debes cambiar abajo del todo de ChatGPT_Desktop_UI.py donde pone YOUR_API_KEY_HERE poner la tuya y luego compilar con:
```
pyinstaller --noconsole --onefile --hidden-import=openai main.py
```

Pero primero debes tener:
```
pip install openai==0.28
pip install PySimpleGui
```
