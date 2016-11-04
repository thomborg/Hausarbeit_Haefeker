import glob


def import_textfiles():
    """
     Funktion welche alle Datein mit '.txt' einliest und als Liste zurückgibt
    :return: textfiles TYPE=LIST:
    """
    # Findet alle Dateien mit der Endung 'txt' im aktuellen Verzeichnis
    textfiles = glob.glob('*.txt')
    # Ignorieren falsches Textfile (Wegen Zusatzaufgabe nötig)
    if "stopwords.txt" in textfiles:
        textfiles.remove("stopwords.txt")
    return textfiles


def normalize(string):
    """
     Zerlegt den Eingabstring in einzele Wörter (anhand von whitespaces) und
     ersetzt alle Zahlen durch '<N>' und Großbuchstaben zu lowercase
    :param string:
    :return dic TYPE=DICTONARY:
    """
    # Entfernen der Satzzeichen
    string = string.replace('.', '')
    string = string.replace(',', '')
    string = string.replace(':', '')
    string = string.replace('_', '')
    string = string.replace('"', '')
    # Enfernen der Sonderzeichen
    string = string.strip('\t\n\r')
    words = string.split()
    # dictonary für alle Wörter im Text
    dic = {}
    # for-Schleife zum eintragen Aller Wörter ins Dicornary
    for word in words:
        # Einfache Normalisierung
        word = word.lower()
        # Zahlen mit '<N>' ersetzen
        if word[0].isdigit():
            word = "<N>"
        if len(word) == 0:
            continue
        # Unbekanntes Wort eintragen
        if word not in dic:
            dic[word] = 0
        # Zähler für bekanntes Wort eintragen
        dic[word] += 1
    return dic


def nr_words(dic):
    """
     Gibt die Summe der Werte im Dictonary zurück.
     Mit Duplikaten!
    :param dic:
    :return nr_words TYPE=INTEGER:
    """
    return sum(dic.values())


def nr_words_uniq(dic):
    """
     Gibt die Anzahl der Eintrgäge im Dictonary zurück.
     Ohne Duplicate!
    :param dic:
    :return nr_words_unique TYPE=INTEGER:
    """
    return len(dic)


def avg_words_len(dic):
    """
     Sucht die durchschnittliche Länge von Wörtern im Dictonary
    :param dic:
    :return avg_words_len TYPE=INTEGER:
    """
    word_length = 0
    for word in dic.keys():
        # Summiert die Wortlänge und ggf. die Worthäufigkeit auf
        word_length += len(word) * dic[word]
    # Berechnet den Durchschnitt aus Wortlängen und Anzahl von Wörtern gerundet
    return round(word_length / nr_words(dic))


def nr_numbers(dic):
    """
     Gibt den Zähler für den '<N>'-Eintrag aus dem Diconary zurück
    :param dic:
    :return nr_numbers TYPE=INTEGER:
    """
    return dic['<N>']


def common_words(dic):
    """
     Gibt die drei Häufigsten Wörter als sortierte Liste zurück
    :param dic:
    :return commen_words TYPE=LIST:
    """
    # Nach häufigkeit sortierte Repräsentation des Diconaries
    sorted_dic = sorted(dic, key=dic.get, reverse=True)
    # Liste zum Speichern der häufigsten Wörter
    common = ["", "", ""]
    # Speichert die drei größten Werte in der Liste
    for i in range(3):
        common[i] = sorted_dic[i]
    return common


def text_analisis():
    """
     Ausführen der Textanlyse und rückgabe der Ergebnisse auf der Konsole im CSV Format
    :param:
    :return csv_vektor TYPE=STRING:
    """
    # Einlesen der Textfiles
    textfiles = import_textfiles()

    # CSV-Header für Tabellen überschriften
    print("file;nr_words;nr_words_uniq;avg_word_len;nr_numbers;word_1;word_2;word_3")
    # Iterien über die einzelnen Textfiles
    for textfile in textfiles:
        # Einlesen des Textdokuments
        file = open(textfile, 'r')
        text = file.read()

        # Normalisiern des Ursprungstext und speichern unter Arbeitsvariable
        work = normalize(text)

        # Estellen des CSV Strings
        csv_vektor = textfile + ";"  # Name des Textdokuments
        csv_vektor += str(nr_words(work)) + ";"  # Anzahl Wörter
        csv_vektor += str(nr_words_uniq(work)) + ";"  # Anzahl einzigartigen Wörter
        csv_vektor += str(avg_words_len(work)) + ";"  # Duchschnittliche Wortlänge
        csv_vektor += str(nr_numbers(work)) + ";"  # Anzahl von Zahlen
        for word in common_words(work):
            csv_vektor += word + ";"
        # Entfernen des letzten Semikolos für CSV konfomität
        csv_vektor = csv_vektor[:-1]

        # Ausgabe auf der Konsole
        print(csv_vektor)


def text_analisis_without_stopwords():
    """
     Ausführen der Textanalyse ohne Stopwords und anschließende Ausgabe auf der Konsole im CSV-Format
    :return:
    """
    # Einlesen der Textfiles
    textfiles = import_textfiles()

    # Einlesne des Stopwordsfiles
    stopwordsfile = open("stopwords.txt", 'r')
    stopwords = stopwordsfile.read()
    stopwords = normalize(stopwords)

    # CSV-Header für Tabellen überschriften
    print("file;s_nr_words;s_nr_words_uniq;s_avg_word_len;s_nr_numbers;s_word_1;s_word_2;s_word_3")

    # Iterien über die einzelnen Textfiles
    for textfile in textfiles:
        # Einlesen des Textdokuments
        file = open(textfile, 'r')
        text = file.read()

        # Normalisiern des Ursprungstext und speichern unter Arbeitsvariable
        work = normalize(text)

        # Entfernen der Stopwords aus dem Diconary
        for stopword in stopwords.keys():
            del work[stopword]

        # Erstellen des CSV Strings
        csv_vektor = textfile + ";"
        csv_vektor += str(nr_words(work)) + ";"
        csv_vektor += str(nr_words_uniq(work)) + ";"
        csv_vektor += str(avg_words_len(work)) + ";"
        csv_vektor += str(nr_numbers(work)) + ";"
        for word in common_words(work):
            csv_vektor += word + ";"
        # Entfernen des letzten Semikolos für CSV konfomität
        csv_vektor = csv_vektor[:-1]

        # Ausgabe auf der Konsole
        print(csv_vektor)


############ MAIN ##############
# Normale Textanalyse
text_analisis()
print()
# Textanalyse mit entferen der Stopwords
text_analisis_without_stopwords()
