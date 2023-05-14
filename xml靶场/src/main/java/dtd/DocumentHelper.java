package dtd;

import org.dom4j.Document;
import org.dom4j.DocumentException;
import org.dom4j.Element;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;


public class DocumentHelper {
    public static void main(String[] args) {
        try {
            String xmlFile = "Data.xml";
            String xmlContent = new String(Files.readAllBytes(Paths.get(xmlFile)));

            // Intentionally make the DocumentHelper vulnerable to XXE
            System.setProperty("org.xml.sax.driver", "org.apache.xerces.parsers.SAXParser");
            Document document = org.dom4j.DocumentHelper.parseText(xmlContent);

            Element dataElement = document.getRootElement();
            Element contentElement = dataElement.element("content");

            if (contentElement != null) {
                String content = contentElement.getTextTrim();
                System.out.println("Extracted content: \n" + content);
            }
        } catch (IOException | DocumentException e) {
            System.out.println(e);
        }
    }
}