## AppleRain  _by Mateusz Kisiel_

### Opis projektu:
Projekt składa się z prostej gry na której została wytrenowana sztuczna inteligencja, z użyciem algorytmu PPO z biblioteki stable-baselines3.
Gra polega na łapaniu spadających jabłek sterując postacią w lewo/prawo.

Jedyne informacje jakie otrzymuje sieć neuronowa to pozycja gracza oraz pozycje jabłek, na podstawie tego zwraca jedną z 3 możliwości ruch w lewo/prawo lub pozostanie w miejscu. Trening został odpalony na noc tworząc model po 8 milionach iteracji z średnim wynikiem powyżej 40 zebranych jabłek. 
Możemy się zmierzyć z AI - po odpaleniu pierwsze gramy my, a następnie w tej samej konfiguracji jabłek AI, kto zbierze więcej jabłek wygrywa.


### Instalacja:
Najprościej jest używając managera paczek Anaconda:
```
conda create -n <environment-name> --file req.txt
```
Jeżeli nie masz karty graficznej nvidia ze wsparciem cuda, zainstaluj tensorflow oddzielnie

### Przykład gry AI:

https://user-images.githubusercontent.com/25119453/211150127-b5435e51-c114-42dd-bf6c-28e36db9bfa1.mp4
