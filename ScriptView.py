"""
ScriptView by /XNL-h4ck3r (@xnl_h4ck3r)

Good luck and good hunting! If you really love the tool (or any others), or they helped you find an awesome bounty, consider BUYING ME A COFFEE! (https://ko-fi.com/xnlh4ck3r) (I could use the caffeine!)
"""
VERSION="0.1"

from burp import IBurpExtender, IMessageEditorTabFactory, IMessageEditorTab
from javax.swing import JPanel, JLabel, BorderFactory
from java.awt import BorderLayout, Font

ERROR_MSG = ""
try:
    import warnings
    from bs4 import BeautifulSoup, SoupStrainer
    warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
except Exception as e:
    ERROR_MSG = "This extension needs the beautifulsoup4 module which is not installed correctly.\nThe following installation instructions NEED TO BE FOLLOWED EXACTLY to be able to use this extension (as mentioned in https://github.com/xnl-h4ck3r/ScriptView-Burp-Extension#installation).\n\n1. Visit https://www.jython.org/download, and download the latest stand alone JAR file, e.g. jython-standalone-2.7.3.jar.\n2. Open Burp, go to Extensions -> Extension Settings -> Python Environment, set the Location of Jython standalone JAR file and Folder for loading modules to the directory where the Jython JAR file was saved.\n3. On a command line, go to the directory where the jar file is and run \"java -jar jython-standalone-2.7.3.jar -m ensurepip\".\n4. Install beautifulsoup4 module with Jython by running \"java -jar jython-standalone-2.7.3.jar -m pip install beautifulsoup4\".\n5. Go to the Extensions -> Installed and click Add under Burp Extensions.\n6. Select Extension type of Python and select the ScriptView.py file (this file can be placed in any directory).\n"
    
# KoFi links for buying me a coffee
URL_KOFI = "https://ko-fi.com/B0B3CZKR5"

class BurpExtender(IBurpExtender, IMessageEditorTabFactory):
    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        callbacks.setExtensionName("ScriptView")
        callbacks.registerMessageEditorTabFactory(self)
        
        # Display welcome message
        print("ScriptView - Version " + VERSION)
        print("by @xnl_h4ck3r\n")

        if ERROR_MSG != "":
            print(ERROR_MSG)
            
        print("If you ever see anything in the Errors tab, please raise an issue on Github so I can fix it!")
        print("Want to buy me a coffee?! - " + URL_KOFI + "\n")
        
    def createNewInstance(self, controller, editable):
        return ScriptsTab(self.callbacks, controller, editable)

class ScriptsTab(IMessageEditorTab):
    def __init__(self, callbacks, controller, editable):
        self.callbacks = callbacks
        self._controller = controller
        self._editable = editable
        self._txtInput = callbacks.createMessageEditor(None, editable)
        self.setup_ui()

    def setup_ui(self):
        # Set up the main panel with the "Scripts" label and text input
        self._panel = JPanel(BorderLayout())
        self._panel.add(self._txtInput.getComponent(), BorderLayout.CENTER)

        self._headersLabel = JLabel("Scripts")
        self._headersLabel.setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5))
        self._headersLabel.setFont(self._headersLabel.getFont().deriveFont(14.0).deriveFont(Font.BOLD))
        self._panel.add(self._headersLabel, BorderLayout.NORTH)

    def hasScripts(self, content):
        # Check if the content contains <script> tags
        script_strainer = SoupStrainer("script")
        soup = BeautifulSoup(content.tostring(), 'html.parser', parse_only=script_strainer)
        return len(list(soup)) > 0

    def getMessage(self):
        # Return the message from the text input
        return self._txtInput.getMessage().tostring()

    def setMessage(self, content, isRequest):
        # Set the message content in the text input
        if content and not isRequest and self.hasScripts(content):
            # Parse only the <script> tags
            script_strainer = SoupStrainer("script")
            soup = BeautifulSoup(content.tostring(), 'html.parser', parse_only=script_strainer)
            
            # Reconstruct the output while preserving formatting
            script_contents = ''
            script_count = 1
            for tag in soup:
                script_contents += '<!---- SCRIPT #{} ------------------------------------------>\n\n'.format(script_count)
                script_contents += str(tag)
                script_contents += '\n\n'
                script_count += 1

            # Set the content to show only <script> tags and their contents
            self._txtInput.setMessage(script_contents, isRequest)

            if self.callbacks and self._controller:
                # Use IRequestInfo to analyze the request and get the URL
                analyzed_request = self.callbacks.getHelpers().analyzeRequest(self._controller.getHttpService(), self._controller.getRequest())
                url = analyzed_request.getUrl().toString()

                # Remove port number if it's 80 or 443
                if analyzed_request.getUrl().getPort() == 80 or analyzed_request.getUrl().getPort() == 443:
                    # Check if it's HTTPS
                    protocol = "https" if analyzed_request.getUrl().getProtocol() == 1 else "http"
                    query_string = "?" + analyzed_request.getUrl().getQuery() if analyzed_request.getUrl().getQuery() else ""
                    url = "{}://{}{}{}".format(
                        protocol,
                        analyzed_request.getUrl().getHost(),
                        analyzed_request.getUrl().getPath(),
                        query_string
                    )

                self._headersLabel.setText("Below are the {} script(s) from request {}".format(script_count-1, url))
        else:
            # If no scripts are found, hide the tab
            self._txtInput.setMessage('', isRequest)


    def getUiComponent(self):
        return self._panel

    def getTabCaption(self):
        return "Scripts"

    def isEnabled(self, content, isRequest):
        # Enable the tab only if there are <script> tags in the response
        return not isRequest and self.hasScripts(content)

    def isModified(self):
        return self._txtInput.isMessageModified()
