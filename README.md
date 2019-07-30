# gcalc

Program umożliwia wykonywanie podstawowych obliczeń geodezyjnych w sposób graficzny.

## Od czego zacząć

W wersji podstawowej program umożliwia dokonanie następujących obliczeń:

- miary ortogonalne
- przecięcie prostych

### Biblioteki

Program nie korzysta z żadnych zewntrznych bibliotek, interfejs graficzny prezentowany z wykorzystaniem tkinter.

### Pierwsze kroki

Aby rozpocząć porównywanie plików należy uruchomić program

```
python app.py
```

![Okno główne](img/main.png)

Powyżej główne okno programu

Punkty osnowy wczytujemy z pliku poprzez "Import txt" dane w pierwszej kolumnie powinny zwierać numer punktu w kolejnych jego współrzędne X i Y
Opcja "Linia Bazowa LB" z menu "Obliczenia" lub z paska narzędzi umożliwia wskazanie linii bazowej poprzez wskazanie punktu początkowego oraz końcowego. W przypadku gdy w następnym kroku chcemy wykonywać obliczenia związane z miarami ortogonalnymi linię wskazujemy raz, natomiast gdy potrzebujemy wyznaczyć przcięcie punktów wskazujemy dwie linie bazowe za każdy razem aktywując opcję "LB".

Dla miar ortogonalnych "MO" pojawi się dodatkowe okno umożliwiające podanie numeru punktu (numeracja automatycznie wzrasta, ustawiona domyślnie na 1) oraz odciętej i rzędnej do szukanego punktu.

W przypadku przecięcia prostych "PP" punkt zostanie obliczony automatycznie po wskazaniu dwóch linii bazowych.

Opcja "Raport txt" umożliwia zapisanie obliczonych punktów do pliku tekstowego w formie prostego raportu. 



## Uruchamianie testów

Testowanie z wykorzystaniem pytest, poniżej przykładowe polecenie generujące raport z testów wraz pokryciem kodu testami

```o
python -m pytest --cov-report term-missing --cov=gcalc .
```

## Wykorzystane biblioteki

* [tkinter](https://wiki.python.org/moin/TkInter) - python standard GUI



## Przyszłość

Poniżej lista rzeczy które powinny zostać dodane w najbliższym czasie

- [x] anulowanie aktualnej operacji
- [x] możliwość generowania raportów 
- [ ] konwersja prostych raportów do lepszej wizualnie postaci
- [ ] dodatkowe moduły obliczeń (wcięcia)
- [ ] czasowe wyświetlanie komunikatów na pasku status
- [ ] możliwość zmiany numeru punktu



## Autor

* **Jakub Plata** - [geokodzilla](https://github.com/geokodzilla)

## Licencja

Projekt na licencji MIT License - szczegóły w pliku [LICENSE.md](LICENSE.md) 
