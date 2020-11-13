import xml.dom.minidom as minidom
import classList

class XuiCanvas:
    def __init__(self):
        self.childElements= {}
        
    def load(self, fileName):
        file = minidom.parse(fileName)
        canvas = file.getElementsByTagName("XuiCanvas")
        canvas = canvas[0]
        for node in canvas.childNodes:
            self.buildSubElements(node)
        print("Finished loading XuiCanvas")

    def save(self, fileName):
        doc = minidom.Document()
        root = doc.createElement("XuiCanvas")
        root.setAttribute("Version", "000c")
        doc.appendChild(root)
        data = self.makeXML(root, doc)
        file = open(fileName, 'w+')
        root.writexml(file)
        file.close()

    def makeXML(self,tempRoot, doc):
        for key, value in self.childElements.items():
            tempChild = doc.createElement(value.elementName)
            tempRoot.appendChild(tempChild)
            data = value.makeXML(tempChild, doc)
        return tempRoot

    def tree(self):
        strTree = ""
        depth = "\t"
        for key, value in self.childElements.items():
            if isinstance(value, element):
                strTree = strTree + depth + str(value.__class__) + ": " + key + "\n"
                strTree = strTree + value.tree(depth)
            else:
                strTree = strTree + depth + key + ": " + str(value)+ "\n"
        return strTree

    def buildSubElements(self, node):
        child = classList[node.nodeName]()
        child.load(node, self)

    def changeProperty(self, name, newValue):
        #returns 0 on success, 1 if the property doesnt exist and 2 if the node has no properties element
        #some elements, such as keyframes have properties that are not contained within a property element
        #this function will not work for them, as the first step is to check for a properties element
        if self.childElements["Properties"]:
            if self.childElements["Properties"].childElements[name]:
                self.childElements["Properties"].childElements[name] = newValue
                return 0
            else:
                return 1
        else:
            return 2
        
class element:

    def load(self, data, parent):
        for node in data.childNodes:
            self.buildSubElements(node)
        parent.childElements[self.childElements["Properties"].childElements["Id"]] = self

    def makeXML(self,tempRoot, doc):
        for key, value in self.childElements.items():
            if isinstance(value, element):
                tempParent = doc.createElement(value.elementName)
                #tempRoot.appendChild(tempParent)
                data = value.makeXML(tempParent, doc)
                tempRoot.appendChild(tempParent)
            else:
                tempParent = doc.createElement(key)
                tempRoot.appendChild(tempParent)
                if value:
                    tempChild = doc.createTextNode(value)
                else:
                    tempChild = doc.createTextNode("")
                tempParent.appendChild(tempChild)
            
        return tempRoot

    def tree(self, depth):
        strTree = ""
        depth = depth + "\t"
        for key, value in self.childElements.items():
            if isinstance(value, element):
                strTree = strTree + depth + str(value.__class__) + ": " + key + "\n"
                strTree = strTree + value.tree(depth)
            else:
                strTree = strTree + depth + key + ": " + str(value) + "\n"
        return strTree

    def buildSubElements(self, node):
        child = classList[node.nodeName]()
        child.load(node, self)

    def changeProperty(self, name, newValue):
        #returns 0 on success, 1 if the property doesnt exist and 2 if the node has no properties element
        #some elements, such as keyframes have properties that are not contained within a property element
        #this function will not work for them, as the first step is to check for a properties element
        if self.childElements["Properties"]:
            if self.childElements["Properties"].childElements[name]:
                self.childElements["Properties"].childElements[name] = newValue
                return 0
            else:
                return 1
        else:
            return 2
        
class Properties(element):
    def __init__(self):
        self.childElements = {}
        self.elementName = "Properties"
        self.draw = False
        
    def load(self, propNode, parent):
        for node in propNode.childNodes:
            self.childElements[node.nodeName] = getNodeValue(node)
        parent.childElements["Properties"] = self

class XuiScene(element):
    def __init__(self):
        self.childElements = {}
        self.elementName = "XuiScene"
        self.draw = False
        
class AdvGroup(element):
    def __init__(self):
        self.childElements = {}
        self.elementName = "AdvGroup"
        self.draw = False
        
class UIStackPanel(element):
    def __init__(self):
        self.childElements = {}  
        self.elementName = "UIStackPanel"
        self.draw = False
        
class XuiGroup(element):
    def __init__(self):
        self.childElements = {}  
        self.elementName = "XuiGroup"
        self.draw = False
        
class AdvButton(element):
    def __init__(self):
        self.childElements = {}  
        self.elementName = "AdvButton"
        self.draw = False
class MyText(element):
    def __init__(self):
        self.childElements = {}  
        self.elementName = "MyText"
        self.draw = False
        
class MyImage(element):
    def __init__(self):
        self.childElements = {}  
        self.elementName = "MyImage"
        self.draw = False
        
class UIMaskedText(element):
    def __init__(self):
        self.childElements = {}  
        self.elementName = "UIMaskedText"
        self.draw = False
        
class UIMaskedImage(element):
    def __init__(self):
        self.childElements = {}  
        self.elementName = "UIMaskedImage"
        self.draw = False
        
class Timelines(element):
    def __init__(self):
        self.childElements = {}
        self.elementName = "Timelines"
        self.draw = False
        
    def load(self, timelineNode, parent):
        for node in timelineNode.childNodes:
            self.buildSubElements(node)        
        parent.childElements["Timelines"] = self

class Timeline(element):
    def __init__(self):
        self.childElements = {}
        self.elementName = "Timeline"
        self.ePropCount = 0
        self.draw = False
        
    def load(self, timelineNode, parent):
        for node in timelineNode.childNodes:
            if node.nodeName == "KeyFrame":
                self.buildSubElements(node)
            elif node.nodeName == "Id":
                self.childElements["Id"] = getNodeValue(node)
            elif node.nodeName == "TimelineProp":
                self.childElements["TimelineProp" + str(self.ePropCount)] = getNodeValue(node)
                self.ePropCount += 1
            else: print("Unexpected node " + node.nodeName + " found")
        parent.childElements[self.childElements["Id"]] = self

    def makeXML(self,tempRoot, doc):
        for key, value in self.childElements.items():
            if isinstance(value, element):
                tempParent = doc.createElement(value.elementName)
                data = value.makeXML(tempParent, doc)
                tempRoot.appendChild(tempParent)
            else:
                if key[:-1] == "TimelineProp":
                    key = "TimelineProp"
                tempParent = doc.createElement(key)
                tempRoot.appendChild(tempParent)
                if value:
                    tempChild = doc.createTextNode(value)
                else:
                    tempChild = doc.createTextNode("")
                tempParent.appendChild(tempChild)
            
        return tempRoot
            
class KeyFrame(element):
    def __init__(self):
        self.childElements = {}
        self.elementName = "KeyFrame"
        self.ePropCount = 0
        self.draw = False
        
    def load(self, frameNode, parent):
        for node in frameNode.childNodes:
            if node.nodeName == "Prop":
                self.childElements["Prop" + str(self.ePropCount)] = getNodeValue(node)
                self.ePropCount += 1
            else: self.childElements[node.nodeName] = getNodeValue(node)
        parent.childElements[self.childElements["Time"]] = self

    def makeXML(self,tempRoot, doc):
        for key, value in self.childElements.items():
            if isinstance(value, element):
                tempParent = doc.createElement(value.elementName)
                data = value.makeXML(tempParent, doc)
                tempRoot.appendChild(tempParent)
            else:
                if key[:-1] == "Prop":
                    key = "Prop"
                tempParent = doc.createElement(key)
                tempRoot.appendChild(tempParent)
                if value:
                    tempChild = doc.createTextNode(value)
                else:
                    tempChild = doc.createTextNode("")
                tempParent.appendChild(tempChild)
            
        return tempRoot

class NamedFrames(element):
    def __init__(self):
        self.childElements = {}
        self.elementName = "NamedFrames"
        self.draw = False
        
    def load(self, frameNode, parent):
        for node in frameNode.childNodes:
            self.buildSubElements(node)
        parent.childElements["NamedFrames"] = self

class NamedFrame(element):
    def __init__(self):
        self.childElements = {}
        self.elementName = "NamedFrame"
        self.draw = False
        
    def load(self, frameNode, parent):
        self.childElements = makeProperties(frameNode)
        parent.childElements[self.childElements["Name"]] = self
                               
class IUIProgressText(element):
    def __init__(self):
        self.childElements = {}
        self.elementName = "IUIProgressText"
        self.draw = False
        
class UIWrapPanel(element):
    def __init__(self):
        self.childElements = {}
        self.elementName = "UIWrapPanel"
        self.draw = False
        
class UITextWithGameActions(element):
    def __init__(self):
        self.childElements = {}
        self.elementName = "UITextWithGameActions"
        self.draw = False
        
class IUIAARectangle(element):
    def __init__(self):
        self.childElements = {}
        self.elementName = "IUIAARectangle"
        self.draw = False
        
class IUISoundEmitter(element):
    def __init__(self):
        self.childElements = {}
        self.elementName = "IUISoundEmitter"
        self.draw = False
        
def makeProperties(propNode):
        properties = {}
        for value in propNode.childNodes:
            properties[value.nodeName] = getNodeValue(value)
        return properties
    
def getNodeValue(node):
    if node.childNodes.length > 0:
        return node.childNodes[0].nodeValue
    else: return None

classList = classList.cList("xuiLoader")     

