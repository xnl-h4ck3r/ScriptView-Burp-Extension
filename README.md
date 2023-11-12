<center><img src="https://raw.githubusercontent.com/xnl-h4ck3r/ScriptView-Burp-Extension/main/ScriptView/images/title.png"></center>

## About - v0.1

This is a simple Burp extension that provides an additional tab called `Scripts` for any Response that has any `script` elements in the page. It will only show you the `script` tags, which is just a convenient way of only seeing all the code, which is useful when there are many scripts in a response, especially when there are a lot of inline tags and you just want to go through the code without searching through everything else.

<center><img src="https://raw.githubusercontent.com/xnl-h4ck3r/ScriptView-Burp-Extension/main/ScriptView/images/example.png"></center>

## Installation

This extension needs the external BeautifulSoup4 module to run and needs to be installed as detailed below. If you already use the Word mode in [GAP Burp Extension](https://github.com/xnl-h4ck3r/GAP-Burp-Extension) successfully, then you have already installed this and can just skip to point 5 below.

1. Visit [Jython Offical Site](https://www.jython.org/download), and download the latest stand alone JAR file, e.g. `jython-standalone-2.7.3.jar`.
2. Open Burp, go to **Extensions** -> **Extension Settings** -> **Python Environment**, set the **Location of Jython standalone JAR file** and **Folder for loading modules** to the directory where the Jython JAR file was saved.
3. On a command line, go to the directory where the jar file is and run `java -jar jython-standalone-2.7.3.jar -m ensurepip`.
4. Install `beautifulsoup4` module with Jython by running `java -jar jython-standalone-2.7.3.jar -m pip install beautifulsoup4`.
5. Go to the **Extensions** -> **Installed** and click **Add** under **Burp Extensions**.
6. Select **Extension type** of **Python** and select the **ScriptView.py** file.

<br>
Good luck and good hunting!
If you really love the tool (or any others), or they helped you find an awesome bounty, consider [BUYING ME A COFFEE!](https://ko-fi.com/xnlh4ck3r) ☕ (I could use the caffeine!)

🤘 /XNL-h4ck3r

<a href='https://ko-fi.com/B0B3CZKR5' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://storage.ko-fi.com/cdn/kofi2.png?v=3' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>
