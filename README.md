<!-- Komentář k souboru Python -->
<p><strong>Soubor Python:</strong> Tento soubor je určen pro export výsledků voleb ze stránek Českého statistického úřadu za danou oblast pod daným odkazem/webovou stránkou. Spouští se ve virtuálním prostředí a vyžaduje splnění požadavků definovaných v souboru <code>requirements.txt</code>.</p>
<p><strong>Argumenty při spuštění:</strong> Při spuštění se v terminálu zadávají 2 argumenty:</p>
<ol>
  <li><span style="color: blue;">Webová stránka</span> - tato webová stránká je procházena a z každého pododkazu, který splňuje definovaná kritéria, jsou exportovány do výsledného souboru volební výsledky se identifikátorem obce a čísla obce.</li>
  <li><span style="color: green;">Jméno výsledného souboru</span> - název souboru, do kterého budou uloženy výsledky ve formátu CSV.</li>
</ol>
<p><strong>Příklad zadání:</strong></p>
<pre><code>python project_3.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "output.csv"</code></pre>
<p><strong>Výsledný soubor:</strong> V tomto případě bude výsledný soubor uložen pod názvem <code>output.csv</code>.</p>
<p><u>Důležité:</u> Nezapomeňte nainstalovat všechny potřebné knihovny a balíčky uvedené v souboru <code>requirements.txt</code> před spuštěním skriptu, tedy:</p>
<ul>
  <li><i>beautifulsoup4==4.12.2</i></li>
  <li><i>black==23.3.0</i></li>
  <li><i>certifi==2022.12.7</i></li>
  <li><i>charset-normalizer==3.1.0</i></li>
  <li><i>click==8.1.3</i></li>
  <li><i>colorama==0.4.6</i></li>
  <li><i>idna==3.4</i></li>
  <li><i>lxml==4.9.2</i></li>
  <li><i>mypy-extensions==1.0.0</i></li>
  <li><i>packaging</i></li>
</ul>
</br>
<p><strong>Příklad výstupu (CSV soubor):</strong></p>
<table border="1" cellspacing="0" cellpadding="5" style="border-collapse:collapse;">
    <thead>
        <tr>
            <th>Obec</th>
            <th>Číslo obce</th>
            <th>Voliči v seznamu</th>
            <th>Vydané obálky</th>
            <th>Platné hlasy</th>
            <th>Občanská demokratická strana</th>
            <!-- další sloupce -->
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Alojzov</td>
            <td>506761</td>
            <td>205</td>
            <td>145</td>
            <td>144</td>
            <td>29</td>
            <!-- další buňky -->
        </tr>
        <tr>
            <td>Bedihošť</td>
            <td>589268</td>
            <td>834</td>
            <td>527</td>
            <td>524</td>
            <td>51</td>
            <!-- další buňky -->
        </tr>
        <!-- další řádky -->
    </tbody>
</table>
<p><u><i>Pozn:</u> Příklad pouze jedné polické strany ve dvou obcích sledovaného regionu, ostatní strany jsou v dalších sloupcích exportu napravo. </i>
