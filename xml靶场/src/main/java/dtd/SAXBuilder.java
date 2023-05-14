package dtd;

import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.JDOMException;

import java.io.File;
import java.io.IOException;

public class SAXBuilder {
    public static void main(String[] args) {
        try {
            String xmlFile = "Data.xml";
            org.jdom2.input.SAXBuilder saxBuilder = new org.jdom2.input.SAXBuilder();
            saxBuilder.setFeature("http://xml.org/sax/features/external-general-entities", true);
            saxBuilder.setFeature("http://xml.org/sax/features/external-parameter-entities", true);
            Document document = saxBuilder.build(new File(xmlFile));

            Element root = document.getRootElement();
            Element id = root.getChild("content");
            System.out.println("id: " + id.getTextTrim());
        } catch (JDOMException | IOException e) {
            System.out.println(e);
        }
    }
}